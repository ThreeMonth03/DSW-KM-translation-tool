DSW Translation Tooling
=======================

This Sphinx site documents stable Python modules used by the translation
tooling and GitHub Actions workflows.

Operational procedures stay in the Markdown runbooks under ``docs/``. Use this
site when changing package code, automation helpers, or generated artifact
logic.

.. toctree::
   :maxdepth: 2
   :caption: Maintainer Docs

   maintainer/docs-index
   maintainer/architecture
   maintainer/command-reference
   maintainer/development-guidelines
   maintainer/localize-sync-runbook
   maintainer/km-update-runbook
   maintainer/security-and-permissions

.. toctree::
   :maxdepth: 2
   :caption: Developer API

   api/translation-workflow
   api/localize-sync
   api/reports-and-km
   api/data-models
