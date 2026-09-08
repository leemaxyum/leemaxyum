# Visual assets

- `ascii-signal.gif`: eight-frame, grayscale primary hero; 9 second loop with a long settled hold.
- `ascii-signal.svg`: standalone static equivalent, also explicitly linked in the README.
- `hero/reference assets/`: preserved reference and provenance.
- `github-stats.svg`: timestamped public API snapshot; refreshed by `metrics.yml`.
- `hero.png`, `tplaytv.svg`, `phantom.svg`: retained original assets; the Phantom provider label is corrected.

Rebuild the hero with Python and Pillow: `python scripts/build_hero.py`.
The reduced-motion picture source is progressive enhancement; GitHub or other renderers may sanitize media queries.
The explicit static link always provides a motion-free version. GIF viewers that freeze the first black frame cannot be controlled; the final frame is fully composed.

Reference refinement: 1200 × 650, eight frames, 82,581 bytes. The source is `scripts/hero_composition.py`; `scripts/build_hero.py` remains the rebuild entry point. A shared grayscale palette and cropped frame updates keep the GIF below 100 KB. Palette remapping is disabled to preserve text across frames.
