# Security and Permissions

Use this page when configuring GitHub Actions, repository settings, or secrets
for a production translation repository.

## Source of Truth

Latest zh-Hant translation text is governed by Localize/Weblate. The Git
translation repository is a reproducible mirror for automation, review, and
visual inspection.

Scheduled automation pulls from Weblate into Git and uses download-only access.

## Required Workflow Permissions

| Workflow | GitHub permission | Secrets | Writes translations? |
| --- | --- | --- | --- |
| Localize auto sync | `contents: write` | none | Writes Git only |
| Localize status report | `contents: read` | none | No |
| Localize alignment report | `contents: read` | none | No |
| KM version auto update | `contents: write` | `DSW_REGISTRY_TOKEN` only when a newer KM exists | Writes Git only after validation |

The auto-sync writer currently supports direct commits to the tracking branch.
If branch protection prevents direct writer pushes, keep Weblate as the source
of truth and switch to one of these equivalent strategies:

- grant a narrow bot exception for the sync workflow; or
- have CI open/update a sync pull request and enable auto-merge.

Both strategies preserve the same policy: Weblate changes flow into Git without
manual translation editing in Git.

## Secret Placement

The normal sync, status, and alignment workflows use download-only Weblate
access.

`DSW_REGISTRY_TOKEN` belongs in the production translation repository when the
guarded KM version auto-update workflow is enabled. It is used only to download
a newly published source KM bundle. It is not used for Weblate access.

## Token Handling

- Store tokens as GitHub Actions repository secrets.
- Keep tokens out of `translation-config.yml`, workflow files, logs, and
  generated reports.

## Branch Protection and History

Use forward commits for workflow or generated-artifact corrections on public
branches.

If GitHub branch-protection APIs are unavailable or return not-found responses
for the current account, rely on observed workflow behavior and repository
settings visible to maintainers. Direct scheduled sync commits are acceptable
only while repository settings allow them.
