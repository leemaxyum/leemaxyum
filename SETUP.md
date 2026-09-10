# Profile v3 setup

This package is designed for the public repository:

`leemaxyum/leemaxyum`

The visual direction is intentionally broader than a degree/discipline label:
**building in public, systems, interfaces, experiments, open source.**

## 1. Replace the profile repository

Copy the contents of this package into your existing `leemaxyum/leemaxyum` repository.

Keep:
- `README.md`
- `assets/`
- `.github/workflows/`
- `output/`

## 2. Contribution matrix

The `Contribution Matrix` workflow generates `output/github-snake-dark.svg` from your GitHub contributions. It runs automatically after pushes to this repository and can also be started manually from GitHub Actions.

## 3. WakaTime

Create a WakaTime account and install the WakaTime editor extension.

Then add this repository secret:

`WAKATIME_API_KEY`

GitHub:
Settings → Secrets and variables → Actions → New repository secret

The workflow will update your coding telemetry.

## 4. GitHub Metrics

`metrics.yml` is included as an optional extra telemetry layer.

If you want the profile cleaner, remove that workflow and the README does not depend on it.

## 5. External widgets

The README uses:
- readme-typing-svg
- GitHub Readme Stats
- GitHub Streak Stats
- GitHub Profile Trophy
- GitHub Activity Graph
- Skill Icons
- profile views
- Capsule Render

These are intentionally limited to visual/telemetry components that support the profile instead of turning it into a widget wall.

## 6. Personalize the build log

Edit only the `~/build-log` section as your projects evolve.

Do not rewrite the whole profile every time you learn a new library.

## 7. Add projects

When a project becomes genuinely interesting, give it:
- one sentence describing what it is
- architecture/problem bullets
- repository link
- optionally one custom diagram in `assets/`

That keeps the profile evergreen.

## Design rule

The profile should become **more interesting as the GitHub account becomes more interesting**.

Do not add labels just because they sound impressive.
Let repositories, architecture diagrams, commits, contributions, and experiments advertise the skill.
