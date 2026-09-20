# hdclark94.github.io

Personal academic website for **Dr Harry Clark**, systems neuroscience researcher at the Medical University of Vienna.

Live at <https://hdclark94.github.io>.

Built with [Jekyll](https://jekyllrb.com/) on the [al-folio](https://github.com/alshedivat/al-folio) theme (MIT).

## Where the content lives

| What                                 | File                                 |
| ------------------------------------ | ------------------------------------ |
| About page, tagline, career sections | `_pages/about.md`                    |
| News items on the front page         | `_news/`                             |
| Long-form ideas posts                | `_ideas/`                            |
| Publications                         | `_bibliography/papers.bib`           |
| Publication thumbnails               | `assets/img/publication_preview/`    |
| Journal badges and colours           | `_data/venues.yml`                   |
| CV                                   | `_data/cv.yml`                       |
| Which GitHub profiles and repos show | `_data/repositories.yml`             |
| Their metadata (generated)           | `_data/github.yml`                   |
| Profile photo                        | `assets/img/prof_pic.jpg`            |
| About-page banner                    | `assets/img/banner-{light,dark}.svg` |
| Site title, socials, feature toggles | `_config.yml`                        |

## Generated assets

Figures and GitHub data are produced by Python scripts in [`scripts/`](scripts/)
and committed, so the site builds without running them. You only need them when
**changing** a figure rather than rebuilding one from scratch.

```bash
pip install -r scripts/requirements.txt
make assets          # regenerate everything
```

Output is deterministic: regenerating an unchanged figure produces a
byte-identical file, so a diff in git means the design actually changed.

**[`scripts/README.md`](scripts/README.md) documents what each script produces
and the decisions baked into them** — the validated colour palette, why the
manifold figure carries three manifolds rather than four, why its draw order is
pinned, and how the light/dark image swap works. Worth reading before editing a
figure, as several of those are easy to undo by accident.

## Adding a repository to the repositories page

Edit `_data/repositories.yml` — that is the only list to maintain — then:

```bash
make github          # refreshes _data/github.yml
```

Commit both files. The cards are rendered by the site itself rather than
hotlinked, because the third-party services the theme originally used went
offline.

## Running locally

Requires Ruby 3.x and [ImageMagick](https://imagemagick.org/) (for responsive images).

```bash
bundle install
make serve           # http://localhost:4000
```

Note that Homebrew no longer ships bottles for macOS 14, so `brew install ruby`
there compiles from source (pulling LLVM and Rust). Use a version manager
instead if you hit that.

## Deploying

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds the site
and publishes `_site` to the `gh-pages` branch. Nothing else is needed.

`.github/workflows/prettier.yml` checks formatting on every push:

```bash
make format          # apply it
make check           # what CI runs
```

Run `make` on its own to list every target.

## Gotchas

- **Do not post-date content.** Jekyll includes future-dated documents in the
  collection but does not write the page, so a listing links to a 404 while both
  workflows pass green.
- `scripts/` is in `exclude:` in `_config.yml` — tracked in git, never published.
- `scholar.first_name` in `_config.yml` is a match list for bolding Harry's name
  in the bibliography, not a display name. It must keep matching the `.bib`
  files ("Harry", "H."), so it does not track the site title.
