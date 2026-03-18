SPHINXBUILD   ?= sphinx-build
SPHINXOPTS    ?=
SOURCEDIR     = .
BUILDDIR      = _build
PORT          ?= 8001

.PHONY: revealjs serve livehtml

revealjs:
	$(SPHINXBUILD) -b revealjs $(SOURCEDIR) $(BUILDDIR)/revealjs $(SPHINXOPTS)

serve: revealjs
	@echo "Serving at http://localhost:$(PORT)"
	uv run python -m http.server -d $(BUILDDIR)/revealjs $(PORT)

livehtml:
	uv run sphinx-autobuild -b revealjs $(SOURCEDIR) $(BUILDDIR)/revealjs $(SPHINXOPTS)
