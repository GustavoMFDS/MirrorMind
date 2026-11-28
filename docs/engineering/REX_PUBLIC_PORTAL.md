# REX-11/12 - Public portfolio site and documentation index

The public landing page is a curated entrypoint, not a mirror of the
repository or a hosted MirrorMind API. It links to technical guides at the
exact source revision, includes a Portuguese section and uses the existing
offline interactive report. The alpha comparison SVG is historical and
identified as such. No live inference, analytics, cookies or external JS.

## Build and inspect

From a clean reviewed checkout, with Python 3.11+:

```bash
python -m pip install -e .
python -m examples.build_portfolio_site --output public-site --source-sha "$(git rev-parse HEAD)"
```

Use a new output directory. The builder copies exactly two reviewed SVGs,
renders the curated landing page with the source SHA, generates the
fixed synthetic report (seed 317, two replications), and writes a
path-free build manifest plus .nojekyll. It refuses non-synthetic evidence,
non-false authorization flags and a WorldKernel execution. The caller
must supply the actual checked-out revision; syntax validation alone
does not attest the tree or cleanliness.

The six-file allowlist excludes source workbooks, arbitrary documentation
copies, local data, logs, credentials, caches and private engine artifacts.

The landing page provides a keyboard skip link and responsive guide cards.
Check keyboard navigation and document overflow at narrow and desktop
viewports; this is not a comprehensive accessibility certification.
The builder is not a generic file publisher. See the
[builder](../../examples/build_portfolio_site.py),
[landing template](../assets/portfolio_site.html),
[report guide](PORTFOLIO_DEMO.md) and
[tests](../../tests/integration/test_portfolio_site.py).

## Deployment

The [Pages workflow](../../.github/workflows/pages.yml) builds on PRs
with read-only contents access. Only an explicit dispatch on main
can upload a Pages artifact and deploy. First verify the exact main
commit and all official checks. The deploy job alone receives pages
and OIDC write permissions. Configure the public GitHub Pages source
as Actions, with no paid services or custom domain. Read back the
deployment status and verify the public URL and its build manifest.

No automatic deployment on unreviewed PRs. If the site is unavailable,
the immutable first alpha HTML download remains usable. No new API,
LLM provider, source access, release or package distribution is implied.
The technical guide pages remain on GitHub; this initial portal is a
curated index, not a fully rendered documentation system.
