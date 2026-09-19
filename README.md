# hdclark94.github.io

Personal academic website for **Harry D. Clark**, postdoctoral researcher at the University of Edinburgh.

Live at <https://hdclark94.github.io>.

Built with [Jekyll](https://jekyllrb.com/) on the [al-folio](https://github.com/alshedivat/al-folio) theme (MIT).

## Where the content lives

| What                                 | File                              |
| ------------------------------------ | --------------------------------- |
| About page / intro text              | `_pages/about.md`                 |
| News items on the front page         | `_news/`                          |
| Publications                         | `_bibliography/papers.bib`        |
| Publication thumbnails               | `assets/img/publication_preview/` |
| Journal badges and colours           | `_data/venues.yml`                |
| CV                                   | `_data/cv.yml`                    |
| GitHub profiles and repos shown      | `_data/repositories.yml`          |
| Profile photo                        | `assets/img/prof_pic.jpg`         |
| Site title, socials, feature toggles | `_config.yml`                     |

## Running locally

Requires Ruby 3.x and [ImageMagick](https://imagemagick.org/) (for responsive images).

```bash
bundle install
bundle exec jekyll serve
```

The site is then at <http://localhost:4000>.

## Deploying

Pushing to `master` triggers `.github/workflows/deploy.yml`, which builds the site
and publishes `_site` to the `gh-pages` branch. Nothing else is needed.

`.github/workflows/prettier.yml` checks formatting on every push. To fix locally:

```bash
npx prettier . --write
```
