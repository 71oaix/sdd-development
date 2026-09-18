# Repository Instructions

## Role

This repository is the authoritative editable source for the `sdd-development` skill.
It consumes an approved Specification Package and the versioned SDD Handoff Contract from `three-space-development`.

SDD may report a Specification Change Request upstream, but it does not redefine the upstream specification contract.

## Source and runtime

- Edit this source repository only.
- The copy under the Codex user skills directory is an installed runtime artifact.
- Never use an installed runtime copy as the source of truth.
- Do not treat a project-local legacy copy as an active source.

## GitHub workflow

- Work from a non-`main` branch.
- Open a pull request for every change.
- Do not push directly to `main` or force-push it.
- Run the repository quality checks before requesting merge.
- State the supported Handoff Contract version and compatibility impact in relevant PRs.
- Use Squash Merge after the required checks pass.

## Verification

Run the following from the repository root:

```text
python -m compileall -q scripts
python scripts/validate_public_surface.py
```

When the Task Graph and structured run-log protocol files are present on the
current branch, also run:

```text
python scripts/validate_task_graph.py templates/task-graph.json
python scripts/validate_run_log.py .run-log.jsonl
```

## Versioning

- Patch: wording, examples, or non-semantic corrections;
- Minor: compatible fields or behavior;
- Major: removed fields, changed semantics, or changed execution flow.

After merge, tag the source commit before synchronizing the runtime copy.
