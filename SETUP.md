# Profile maintenance

The profile is ready locally on `design/ascii-signal`. Git authentication was unavailable; nothing was pushed.

## Publish

Run these commands in PowerShell after signing in through your usual GitHub tooling. No credential belongs in a command or file:

```powershell
Set-Location 'C:\Users\lenovo\Documents\Codex\2026-09-09\leemaxyum-profile-redesign\outputs\profile'
git -c http.sslBackend=openssl push -u origin design/ascii-signal
```

Then open [the comparison](https://github.com/leemaxyum/leemaxyum/compare/main...design/ascii-signal?expand=1) and create a pull request, or, if GitHub CLI is installed and authenticated:

```powershell
gh pr create --repo leemaxyum/leemaxyum --base main --head design/ascii-signal --title "Redesign profile as a monochrome ASCII engineering interface" --body-file PR_BODY.md
```

After merging, inspect the profile and run **Contribution signal** and **GitHub telemetry** in Actions once. Scheduled workflows run from the default branch. Normal pushes are used; branch protection may require a maintainer-approved alternative for generated assets.

## Integrations

| Integration | Decision / behavior |
| --- | --- |
| GitHub stats | Local timestamped SVG from the public REST API; weekly refresh uses automatic GITHUB_TOKEN. Counts public repositories, stars on owned non-forks, and followers. |
| Contribution snake | Initial SVG uses actual public calendar intensity; daily Platane/snk workflow replaces it with a freshly solved snake. |
| Activity graph | Local twelve-week graph from the public contribution calendar, refreshed weekly. The external widget returned an HTTP error during validation and was replaced. |
| WakaTime | Optional WAKATIME_API_KEY repository secret; skips cleanly when absent. Updates only the waka markers. |
| GitHub Metrics | Optional METRICS_TOKEN repository secret for public account queries. Automatic GITHUB_TOKEN commits the result. Generated assets/github-metrics.svg is intentionally not embedded before it exists. See upstream permissions guidance. |
| Repo cards | Replaced with readable project summaries and links to avoid duplicate widgets. |
| Streak / trophies / profile views | Omitted: additional counters do not explain the work. |
| Skill Icons | Omitted: project implementations already establish the tools. |
| Typing animation | The local GIF handles the identity reveal, removing a redundant external dependency. |

All write workflows share concurrency, scope writes to their intended files, and have timeouts. Optional secrets are never printed. External actions are pinned to verified commit SHAs. Review upstream changes before updating these pins.

Upstream configuration: [snake](https://github.com/Platane/snk), [WakaTime](https://github.com/athul/waka-readme), [Metrics](https://github.com/lowlighter/metrics).

## Rebuild and maintain

`python scripts/build_hero.py` requires Pillow and Consolas on Windows or DejaVu Sans Mono on Linux. It writes the GIF and static SVG from authored glyphs.

`python scripts/update_stats.py` uses only Python's standard library; it preserves the last good snapshot if the API fails before generation.

The hero has eight frames and a nine-second loop. Its final frame is composed and held for almost six seconds. An explicit static link supports readers whose renderer does not honor the reduced-motion picture source. Some GIF clients freeze the initial black frame; a GIF cannot control that behavior.

Reference provenance is under `assets/hero/reference assets/`. Original assets are retained. No other repositories were modified.
