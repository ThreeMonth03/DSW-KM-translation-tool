# DSW KM Translation Tool

Python tooling for maintaining DSW Knowledge Model translations.

This repository is the tooling side of the translation workflow. It does not
own production translation text. Production text comes from Localize/Weblate and
is mirrored into a dedicated translation repository where maintainers can review
the tree, final PO, generated KM bundle, and reports.

## What This Tool Does

- Pull Localize/Weblate PO exports into a Git translation tree.
- Rebuild final PO and translated KM bundles.
- Validate translation repository configuration.
- Report Weblate quality checks and repository output alignment.
- Guard KM source-version updates before they are committed.

## Start Here

| Role or task | Read |
| --- | --- |
| First-time maintainer | [First-Time Maintainer Guide](docs/first-time-maintainer.md) |
| Day-to-day operator | [Command Reference](docs/command-reference.md) |
| Developer changing code | [Development Guidelines](docs/development-guidelines.md) |
| Localize/Weblate sync | [Localize Sync Runbook](docs/localize-sync-runbook.md) |
| KM version update | [KM Update Runbook](docs/km-update-runbook.md) |
| Full document map | [Documentation Index](docs/README.md) |

## Quick Setup

```shell
make install-dev
make check
```

`make install-dev` creates `.venv` and installs dependencies from
`config/requirements.txt`. `make check` runs formatting checks, linting, Python
compilation, tests, docs build, and whitespace checks.

## Common Commands

Use Make targets for normal work:

```shell
make help
make help-all
make repo-align REPO=/path/to/translation-repo
make repo-sync REPO=/path/to/translation-repo
```

`REPO=/path/to/translation-repo` is the preferred short form. The older
`REPO=/path/to/translation-repo` variable still works for
existing workflows.

Read the [Command Reference](docs/command-reference.md) before running targets
that rebuild translation output files or write Git commits. Configure workflow
secrets from [Security and Permissions](docs/security-and-permissions.md).

## Local Translation Tree Tools

Local tree commands are available for development, inspection, and repair. By
default they write to the ignored local workspace `translation/zh_Hant/`.
Production translation repositories use their own `translation-config.yml` and
repository layout; see [examples/translation-config.yml](examples/translation-config.yml).
