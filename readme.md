# DSW Translation Tool

Python tooling for DSW Knowledge Model translation maintenance.

For zh-Hant production work, the latest translation state is maintained in
Localize/Weblate. This repository provides automation and visualization around
that workflow:

- mirror Weblate PO exports into a Git translation tree
- rebuild final PO and KM bundles
- validate translation repository configuration
- report Weblate PO health and artifact alignment
- update to a newer published source KM after validation passes

## Documentation

The documentation workflow publishes the maintainer docs and API reference when
GitHub Pages is enabled for the repository.

Start here:

- [Documentation Index](docs/README.md)
- [Architecture](docs/architecture.md)
- [Development Guidelines](docs/development-guidelines.md)
- [Localize Sync Runbook](docs/localize-sync-runbook.md)
- [KM Update Runbook](docs/km-update-runbook.md)
- [Command Reference](docs/command-reference.md)

## Setup

```shell
make install-dev
```

This creates `.venv` and installs the Python dependencies listed in
`config/requirements.txt`.

## Common Commands

Validate a translation repository config:

```shell
.venv/bin/python src/validate_translation_config.py \
  --config /path/to/translation-repo/translation-config.yml
```

Run Weblate-to-Git sync for a translation repository:

```shell
.venv/bin/python src/sync_from_localize.py \
  --host-repo /path/to/translation-repo \
  --tooling-repo /path/to/DSW_Translation_tool \
  --config translation-config.yml \
  --translation-root . \
  --target-ref master \
  --mode schedule
```

Run the test suite:

```shell
make test
```

Format and lint Python code:

```shell
make format
make lint
```

Check Python syntax:

```shell
make compile
```

## Local Translation Tree Tools

The local tree commands are available for development, inspection, and repair:

```shell
make export-tree
make sync
make sync-watch
make tree-to-po
make po-to-km
make status
make test-translation
```

By default these commands write to the ignored local workspace
`translation/zh_Hant/`. Production translation repositories use their own
`translation-config.yml` and repository layout.
