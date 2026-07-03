# Security and Permissions

Use this page when configuring GitHub Actions, repository settings, or secrets
for a production translation repository.

## Source of Truth

Latest zh-Hant translation text is governed by Localize/Weblate. The Git
translation repository is a reproducible mirror for automation, review, and
visual inspection.

Scheduled automation pulls from Weblate into Git and uses download-only access.

## Required Workflow Permissions

| Workflow template | GitHub permission | Secrets | Writes translations? |
| --- | --- | --- | --- |
| `examples/github-actions/localize_auto_sync_template.yml` | `contents: write` | none | Writes Git only |
| `examples/github-actions/localize_status_report_template.yml` | `contents: read` | optional `LOCALIZE_API_TOKEN` | No |
| `examples/github-actions/localize_alignment_report_template.yml` | `contents: read` | none | No |
| `examples/github-actions/km_version_auto_update_template.yml` | `contents: write` | `DSW_REGISTRY_TOKEN` only when a newer KM exists | Writes Git only after validation |

## Secret Placement

Configure secrets in the production translation repository:

```text
Settings -> Secrets and variables -> Actions -> Repository secrets
```

The tooling repository does not need these secrets for documentation builds or
unit tests. Local maintainer runs read the same names from shell environment
variables.

The workflow templates in `examples/github-actions/`
show where GitHub Actions injects these secrets.

The normal sync and alignment workflows use download-only Weblate access.

`LOCALIZE_API_TOKEN` is optional for the status report. It is used only for the
read-only Weblate checks API; when absent, the report falls back to anonymous
access.

`DSW_REGISTRY_TOKEN` is required when the guarded KM version auto-update
workflow is enabled. It is used only to download a newly published source KM
bundle. It is not used for Weblate access.

## Token Handling

- Store tokens as GitHub Actions repository secrets.
- Keep tokens out of `translation-config.yml`, workflow files, logs, and
  generated reports.

## Public History

Use forward commits for workflow, build output, report, or documentation fixes
on public branches.
