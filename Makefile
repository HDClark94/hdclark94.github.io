# Entry points for working on this site.
#
#   make assets   regenerate every generated figure and data file
#   make serve    run the site locally
#   make format   apply the formatting the CI check enforces
#
# Generated assets are committed, so you only need `make assets` when changing
# a figure. See scripts/README.md for what each script does and the decisions
# baked into them.

PYTHON ?= python3

.PHONY: help assets figures banner github serve build format check clean

help:
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

assets: figures banner github ## Regenerate all generated assets

figures: ## Manifold schematic -> assets/img/ideas/manifold-states-{light,dark}.svg
	$(PYTHON) scripts/manifold_schematic.py

banner: ## About-page banner -> assets/img/banner-{light,dark}.svg
	$(PYTHON) scripts/banner.py

github: ## Refresh _data/github.yml from the GitHub API
	$(PYTHON) scripts/fetch_github.py

serve: ## Serve locally at http://localhost:4000 (needs Ruby 3.x + ImageMagick)
	bundle exec jekyll serve --livereload

build: ## Production build into _site
	JEKYLL_ENV=production bundle exec jekyll build

format: ## Apply Prettier formatting (CI enforces this)
	npx prettier . --write

check: ## Check formatting without writing (what CI runs)
	npx prettier . --check

clean: ## Remove build output and local raster previews
	rm -rf _site .jekyll-cache
	rm -f assets/img/banner-*.png assets/img/ideas/*.png
