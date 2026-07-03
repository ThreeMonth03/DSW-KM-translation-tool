# First-Time Maintainer Guide

Use this page when you need to understand the repository before changing code
or operating a translation sync.

## Mental Model

For production zh-Hant work, Localize/Weblate owns the latest translation text.
This tooling turns that website state into files that can be reviewed, tested,
and committed in Git:

```text
Localize/Weblate PO -> tree/ -> final PO -> translated KM -> Git commit
```

The tooling repository contains reusable code, tests, workflow templates, and
documentation. A dedicated translation repository contains the actual
translation config and generated translation artifacts.

## First Hour

1. Read [Architecture](architecture.md) to learn which layer owns each
   behavior.
2. Read [Command Reference](command-reference.md) to identify whether a command
   is read-only or writes generated files.
3. Read the relevant runbook before touching production automation:
   [Localize Sync Runbook](localize-sync-runbook.md) for Weblate-to-Git sync, or
   [KM Update Runbook](km-update-runbook.md) for source KM updates.
4. Set up the tooling repo locally:

   ```shell
   make install-dev
   make test
   make docs
   ```

5. When changing behavior, find the thin CLI script in `src/*.py`, then follow
   it into `src/dsw_translation_tool/` for the reusable implementation.

## Safe vs. Writing Commands

Use read-only commands while getting oriented. They are enough to validate a
checkout, inspect Weblate status, and confirm artifact alignment.

Read-only report commands inspect state and write only report files in the
current checkout. They do not upload to Weblate and do not push Git commits
unless a workflow explicitly does so.

Writer commands rebuild translation artifacts and may commit/push when run by
the configured GitHub Actions workflow. Before changing a writer, read its
runbook and its tests.

The [Command Reference](command-reference.md) marks common external-repository
commands by safety level.

## Common Change Paths

Use these paths to find the first module and test area for a change. For a
complete ownership map, see [Architecture](architecture.md).

### Translation Tree or Generated PO/KM Output

Start with:

- `src/dsw_translation_tool/workflow.py`
- `src/dsw_translation_tool/tree.py`
- `src/dsw_translation_tool/sync.py`
- `src/dsw_translation_tool/knowledge_model_service.py`

Test with:

- `tests/translation/`

### Shared Strings

Start with:

- `src/dsw_translation_tool/shared_blocks.py`
- `src/sync_shared_strings.py`

Test with:

- `tests/translation/test_shared_string_sync.py`
- `tests/infra/test_cli_sync.py`

### Weblate Download, Merge, or Sync Commits

Start with:

- `src/dsw_translation_tool/localize_sync.py`
- `src/dsw_translation_tool/localize_merge.py`
- `src/dsw_translation_tool/repository_ci_sync.py`
- `src/dsw_translation_tool/ci_sync.py`

Test with:

- `tests/infra/test_localize_sync.py`
- `tests/infra/test_localize_merge.py`
- `tests/infra/test_ci_sync.py`

### Translation Repository Config

Start with:

- `src/dsw_translation_tool/translation_repository_config.py`

Test with:

- `tests/infra/test_translation_repository_config.py`

### KM Registry Discovery or Guarded KM Updates

Start with:

- `src/dsw_translation_tool/km_registry.py`
- `src/dsw_translation_tool/km_bundle_sync.py`
- `src/dsw_translation_tool/km_latest_sync.py`

Test with:

- `tests/infra/test_km_registry.py`
- `tests/infra/test_km_bundle_sync.py`
- `tests/infra/test_km_latest_sync.py`

### GitHub Workflow Wiring

Start with:

- `examples/github-actions/`

Test with:

- `tests/infra/test_github_workflows.py`

If the right place is unclear, add or adjust a small test that describes the
behavior you expect. The module ownership usually becomes obvious from there.
