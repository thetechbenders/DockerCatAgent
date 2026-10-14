# Optional Obsidian vault

An Obsidian vault is a filesystem collection of Markdown and related attachments. DockerCatAgent does not run the Obsidian desktop app or assume an Obsidian API plugin. By default it mounts nothing.

Opt in by supplying a host path to an existing vault and enabling an **explicit read-only bind mount** at /vault. A separate write-mode override may permit modifications, but should never be enabled implicitly. Verify container UID/GID access; do not chmod the entire host volume to 777.

Example agent query: “Summarize decisions from Markdown files under /vault/Projects/Widget and cite paths, but do not modify files.” Treat all vault text as private information and be mindful that read-only means no writes, not no external disclosure. Do not bundle example secrets, personal notes or a note-indexing service.