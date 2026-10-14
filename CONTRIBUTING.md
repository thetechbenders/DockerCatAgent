# Contributing

Check the [roadmap](ROADMAP.md) and [issues](https://github.com/thetechbenders/DockerCatAgent/issues) before beginning work. Keep pull requests focused, document observed behavior and acceptance tests, and avoid posting credentials, real private vault data, personal paths, or secret-bearing logs.

A good issue describes the problem, concrete reproduction, host platform, expected versus actual behavior, and the outcome that would close it. Enhancement proposals should include scope, security impact, and the reason they belong in the base image rather than a separate opt-in profile.

Reviewers should see exact validation commands and results. Shell/Compose static checks are useful, but they do not replace building the image and performing a real SSH, persistence or authentication test.

Do not assume a redistribution license. Maintainers have not yet selected one; ask before contributing code subject to licensing constraints.