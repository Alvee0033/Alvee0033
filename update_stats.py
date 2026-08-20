import urllib.request
import json
from datetime import datetime
import os
import xml.etree.ElementTree as ET

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
USERNAME = os.environ.get('GITHUB_REPOSITORY_OWNER', 'Alvee0033')

def fetch_data():
    query = '''
    query {
      user(login: "%s") {
        name
        login
        createdAt
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
          totalCount
          nodes {
            name
            stargazerCount
            forkCount
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node { name color }
              }
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          totalIssueContributions
          totalPullRequestContributions
          totalPullRequestReviewContributions
          restrictedContributionsCount
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    ''' % USERNAME

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'ProfileUpdater'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {GITHUB_TOKEN}'

    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': query}).encode('utf-8'),
        headers=headers
    )

    with urllib.request.urlopen(req, timeout=15) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['data']['user']

def generate_streak_svg(total_contribs, current_streak, longest_streak, longest_start, longest_end):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 200" width="495" height="200">
  <defs>
    <linearGradient id="streakBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="streakBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff7b72"/>
      <stop offset="50%" stop-color="#f0883e"/>
      <stop offset="100%" stop-color="#d2a8ff"/>
    </linearGradient>
    <linearGradient id="flameGrad" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#ff2a5f"/>
      <stop offset="50%" stop-color="#ff7a00"/>
      <stop offset="100%" stop-color="#ffe600"/>
    </linearGradient>
    <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .card-title {{ font: 700 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #f0883e; letter-spacing: 1.5px; text-transform: uppercase; }}
    .stat-num {{ font: 800 24px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #ffffff; }}
    .stat-lbl {{ font: 600 11px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #8b949e; letter-spacing: 0.5px; text-transform: uppercase; }}
    .sub-lbl {{ font: 500 10px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #6e7681; }}
  </style>

  <!-- Card Background -->
  <rect x="1.5" y="1.5" width="492" height="197" rx="12" fill="url(#streakBg)" stroke="#30363d" stroke-width="1.5"/>
  <path d="M 15 1.5 L 480 1.5" stroke="url(#streakBorder)" stroke-width="2.5" stroke-linecap="round" filter="url(#neonGlow)"/>

  <!-- Card Header -->
  <g transform="translate(25, 28)">
    <circle cx="6" cy="6" r="4" fill="#f0883e" filter="url(#neonGlow)"/>
    <text x="18" y="10" class="card-title">GitHub Activity Streak</text>
  </g>

  <!-- Stat 1: Total Contributions -->
  <g transform="translate(85, 115)">
    <circle cx="0" cy="0" r="40" fill="none" stroke="#21262d" stroke-width="4.5"/>
    <circle cx="0" cy="0" r="40" fill="none" stroke="#58a6ff" stroke-width="4.5" stroke-dasharray="251" stroke-dashoffset="35" stroke-linecap="round" filter="url(#neonGlow)"/>
    <text x="0" y="-3" text-anchor="middle" class="stat-num">{total_contribs:,}</text>
    <text x="0" y="14" text-anchor="middle" class="sub-lbl">Annual Total</text>
    <text x="0" y="55" text-anchor="middle" class="stat-lbl">Contributions</text>
  </g>

  <!-- Stat 2: Current Streak -->
  <g transform="translate(247, 98)">
    <g transform="translate(-13, -42) scale(1.1)">
      <path d="M12 0 C12 0 17 6.5 17 11.5 C17 15 14.5 18 11.5 18 C8.5 18 6 15 6 11.5 C6 8.5 8.5 5 9.5 2.5 C7.5 5 5 8.5 5 12.5 C5 17.5 8.5 21.5 13.5 21.5 C18.5 21.5 22 17.5 22 12.5 C22 6 12 0 12 0 Z" fill="url(#flameGrad)" filter="url(#neonGlow)"/>
    </g>
    <text x="0" y="16" text-anchor="middle" class="stat-num" fill="#ff7b72" filter="url(#neonGlow)">{current_streak} {('Days' if current_streak != 1 else 'Day')}</text>
    <text x="0" y="34" text-anchor="middle" class="sub-lbl">Active Now</text>
    <text x="0" y="72" text-anchor="middle" class="stat-lbl">Current Streak</text>
  </g>

  <!-- Stat 3: Longest Streak -->
  <g transform="translate(410, 115)">
    <circle cx="0" cy="0" r="40" fill="none" stroke="#21262d" stroke-width="4.5"/>
    <circle cx="0" cy="0" r="40" fill="none" stroke="#d2a8ff" stroke-width="4.5" stroke-dasharray="251" stroke-dashoffset="55" stroke-linecap="round" filter="url(#neonGlow)"/>
    <text x="0" y="-3" text-anchor="middle" class="stat-num">{longest_streak}</text>
    <text x="0" y="14" text-anchor="middle" class="sub-lbl">Days Max</text>
    <text x="0" y="55" text-anchor="middle" class="stat-lbl">Longest Streak</text>
    <text x="0" y="68" text-anchor="middle" class="sub-lbl">{longest_start} - {longest_end}</text>
  </g>
</svg>'''

def generate_stats_svg(total_commits, total_repos, total_prs, total_issues, total_contribs):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 200" width="495" height="200">
  <defs>
    <linearGradient id="statsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="statsBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3fb950"/>
      <stop offset="50%" stop-color="#58a6ff"/>
      <stop offset="100%" stop-color="#bc8cff"/>
    </linearGradient>
    <filter id="neonStatsGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .card-title {{ font: 700 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #58a6ff; letter-spacing: 1.5px; text-transform: uppercase; }}
    .stat-label {{ font: 500 12.5px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #c9d1d9; }}
    .stat-value {{ font: 700 13.5px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #58a6ff; text-anchor: end; }}
    .rank-circle {{ fill: #0d1117; stroke: #3fb950; stroke-width: 4; }}
    .rank-title {{ font: 800 24px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #3fb950; text-anchor: middle; }}
    .rank-sub {{ font: 600 10px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #8b949e; text-anchor: middle; letter-spacing: 1px; }}
  </style>

  <rect x="1.5" y="1.5" width="492" height="197" rx="12" fill="url(#statsBg)" stroke="#30363d" stroke-width="1.5"/>
  <path d="M 15 1.5 L 480 1.5" stroke="url(#statsBorder)" stroke-width="2.5" stroke-linecap="round" filter="url(#neonStatsGlow)"/>

  <!-- Card Header -->
  <g transform="translate(25, 28)">
    <circle cx="6" cy="6" r="4" fill="#58a6ff" filter="url(#neonStatsGlow)"/>
    <text x="18" y="10" class="card-title">GitHub Overview Stats</text>
  </g>

  <!-- Left Stats List -->
  <g transform="translate(30, 48)">
    <!-- Commits -->
    <g transform="translate(0, 18)">
      <circle cx="6" cy="6" r="3" fill="#3fb950"/>
      <text x="18" y="10" class="stat-label">Total Commits (Year)</text>
      <text x="270" y="10" class="stat-value" fill="#3fb950">{total_commits:,}</text>
    </g>
    <!-- Total Contributions -->
    <g transform="translate(0, 44)">
      <circle cx="6" cy="6" r="3" fill="#58a6ff"/>
      <text x="18" y="10" class="stat-label">Total Contributions</text>
      <text x="270" y="10" class="stat-value" fill="#58a6ff">{total_contribs:,}</text>
    </g>
    <!-- Pull Requests -->
    <g transform="translate(0, 70)">
      <circle cx="6" cy="6" r="3" fill="#bc8cff"/>
      <text x="18" y="10" class="stat-label">Pull Requests</text>
      <text x="270" y="10" class="stat-value" fill="#bc8cff">{total_prs:,}</text>
    </g>
    <!-- Repositories -->
    <g transform="translate(0, 96)">
      <circle cx="6" cy="6" r="3" fill="#f0883e"/>
      <text x="18" y="10" class="stat-label">Total Repositories</text>
      <text x="270" y="10" class="stat-value" fill="#f0883e">{total_repos}</text>
    </g>
    <!-- Issues / Reviews -->
    <g transform="translate(0, 122)">
      <circle cx="6" cy="6" r="3" fill="#ff7b72"/>
      <text x="18" y="10" class="stat-label">Issues Contributed</text>
      <text x="270" y="10" class="stat-value" fill="#ff7b72">{total_issues}</text>
    </g>
  </g>

  <!-- Right Rank Badge -->
  <g transform="translate(400, 115)">
    <circle cx="0" cy="0" r="42" class="rank-circle" filter="url(#neonStatsGlow)"/>
    <text x="0" y="6" class="rank-title" filter="url(#neonStatsGlow)">S+</text>
    <text x="0" y="24" class="rank-sub">TIER</text>
    <text x="0" y="58" class="rank-sub" fill="#3fb950">TOP 1% ACTIVITY</text>
  </g>
</svg>'''

def generate_languages_svg(sorted_langs, total_size):
    top_langs = []
    other_size = 0
    for i, (name, data) in enumerate(sorted_langs):
        if i < 5:
            pct = (data['size'] / total_size) * 100
            top_langs.append({
                'name': name,
                'pct': pct,
                'color': data['color'] or '#8b949e'
            })
        else:
            other_size += data['size']
    
    if other_size > 0:
        top_langs.append({
            'name': 'Other',
            'pct': (other_size / total_size) * 100,
            'color': '#8b949e'
        })

    lang_rows = []
    y_start = 56
    row_height = 23
    bar_max_w = 250
    
    for i, lang in enumerate(top_langs):
        y = y_start + (i * row_height)
        fill_w = max(4, int(bar_max_w * (lang['pct'] / 100)))
        row_svg = f'''
    <!-- {lang['name']}: {lang['pct']:.1f}% -->
    <g transform="translate(0, {y})">
      <text x="25" y="10" class="lang-name">{lang['name']}</text>
      <rect x="125" y="1" width="{bar_max_w}" height="9" rx="4.5" fill="#21262d"/>
      <rect x="125" y="1" width="{fill_w}" height="9" rx="4.5" fill="{lang['color']}" filter="url(#neonLangGlow)"/>
      <text x="390" y="10" class="lang-pct">{lang['pct']:.1f}%</text>
    </g>'''
        lang_rows.append(row_svg)

    rows_str = "".join(lang_rows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 200" width="495" height="200">
  <defs>
    <linearGradient id="langBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="langBorder" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3178c6"/>
      <stop offset="50%" stop-color="#00B4AB"/>
      <stop offset="100%" stop-color="#f1e05a"/>
    </linearGradient>
    <filter id="neonLangGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .card-title {{ font: 700 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #00B4AB; letter-spacing: 1.5px; text-transform: uppercase; }}
    .lang-name {{ font: 600 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #c9d1d9; }}
    .lang-pct {{ font: 700 12px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; fill: #8b949e; text-anchor: start; }}
  </style>

  <rect x="1.5" y="1.5" width="492" height="197" rx="12" fill="url(#langBg)" stroke="#30363d" stroke-width="1.5"/>
  <path d="M 15 1.5 L 480 1.5" stroke="url(#langBorder)" stroke-width="2.5" stroke-linecap="round" filter="url(#neonLangGlow)"/>

  <!-- Card Header -->
  <g transform="translate(25, 28)">
    <circle cx="6" cy="6" r="4" fill="#00B4AB" filter="url(#neonLangGlow)"/>
    <text x="18" y="10" class="card-title">Top Languages by Codebase</text>
  </g>

  {rows_str}
</svg>'''

def main():
    print("Fetching live data from GitHub API...")
    user = fetch_data()
    repos = user['repositories']['nodes']
    total_repos = user['repositories']['totalCount']
    contribs = user['contributionsCollection']
    total_commits = contribs['totalCommitContributions']
    total_prs = contribs['totalPullRequestContributions']
    total_issues = contribs['totalIssueContributions']
    calendar = contribs['contributionCalendar']
    total_contribs = calendar['totalContributions']

    # Streaks
    days = []
    for w in calendar['weeks']:
        for d in w['contributionDays']:
            days.append((d['date'], d['contributionCount']))
    days.sort(key=lambda x: x[0])

    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    t_start = None
    l_start, l_end = "", ""

    for date, count in days:
        if count > 0:
            if temp_streak == 0:
                t_start = date
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
                l_start = t_start
                l_end = date
        else:
            temp_streak = 0

    rev_days = list(reversed(days))
    for i, (date, count) in enumerate(rev_days):
        if count > 0:
            current_streak += 1
        else:
            if i == 0:
                continue
            else:
                break

    def fmt_date(d_str):
        if not d_str: return ""
        dt = datetime.strptime(d_str, "%Y-%m-%d")
        return dt.strftime("%b %d")

    # Languages
    lang_map = {}
    for r in repos:
        for edge in r['languages']['edges']:
            name = edge['node']['name']
            color = edge['node']['color']
            size = edge['size']
            if name not in lang_map:
                lang_map[name] = {'size': 0, 'color': color}
            lang_map[name]['size'] += size

    total_size = sum(v['size'] for v in lang_map.values())
    sorted_langs = sorted(lang_map.items(), key=lambda x: x[1]['size'], reverse=True)

    # Write and validate SVGs
    streak_svg = generate_streak_svg(total_contribs, current_streak, longest_streak, fmt_date(l_start), fmt_date(l_end))
    stats_svg = generate_stats_svg(total_commits, total_repos, total_prs, total_issues, total_contribs)
    langs_svg = generate_languages_svg(sorted_langs, total_size)

    for name, content in [('streak.svg', streak_svg), ('stats.svg', stats_svg), ('languages.svg', langs_svg)]:
        ET.fromstring(content)
        with open(name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated and validated {name} ({len(content)} bytes)")

    print("All profile stats SVGs successfully updated!")

if __name__ == '__main__':
    main()
