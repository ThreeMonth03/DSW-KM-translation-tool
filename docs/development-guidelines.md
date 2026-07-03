# Development Guidelines

These rules keep the tooling maintainable as Weblate sync, KM bundles, and
translation-tree behavior evolve.

## Source and Generated Files

Commit source and durable examples:

- `src/`
- `tests/`
- `config/`
- `examples/`
- `docs/`
- small fixture inputs under `files/`
- durable translation round-trip fixtures under `tests/fixtures/`

Local generated state stays out of normal tooling commits:

- `.venv/`
- Python caches
- `.pytest_cache/`
- `.ruff_cache/`
- local backup directories
- local `translation/` workspaces

Translation round-trip fixtures keep the checked-in tree, final PO, and review
diff. KM bundles are rebuilt by tests and workflows instead of stored in the
fixture tree.

Dedicated translation repositories may commit generated `tree/`, `builds/`, and
`reviews/` outputs because those files are the automation and visualization
workspace for translators and maintainers.

## Code Organization

- Keep root `src/*.py` files as command-line shims.
- Put reusable logic in `src/dsw_km_translation_tool/`.
- Keep GitHub Actions YAML thin. YAML should describe checkout, setup, and the
  one helper command it runs.
- Add or update tests under `tests/infra/` when a helper makes a Git, Weblate,
  config, or merge decision.
- Add or update tests under `tests/translation/` when a change affects
  translator-facing tree files or PO/KM output.
- Update docs in the same commit as behavior changes.
- Update Sphinx pages or docstrings when stable package APIs change.

## Localize/Weblate Safety

- Treat the latest Weblate state as authoritative for zh-Hant production sync.
- Keep production automation one-way from Weblate to Git.
- Store Weblate and DSW API tokens as described in
  [Security and Permissions](security-and-permissions.md).
- Preserve Weblate review-state flags during sync.

## KM Version Policy

The current zh-Hant production policy is latest-only. Add a newer KM after it
is published by the DSW Registry and the translation repository config has been
reviewed.

## Standard Checks

Before pushing tooling changes:

```shell
make check
```

For workflow template changes, update the template and the production workflow
together, then let the normal repository CI validate both sides. For production
sync behavior changes, test against a disposable translation checkout before
touching the formal public repository.

[config-dir]: ../config
[docs-dir]: ../docs
[examples-dir]: ../examples
[files-dir]: ../files
[package-dir]: ../src/dsw_km_translation_tool
[src-dir]: ../src
[tests-dir]: ../tests
[tests-fixtures-dir]: ../tests/fixtures
[tests-infra-dir]: ../tests/infra
[tests-translation-dir]: ../tests/translation
