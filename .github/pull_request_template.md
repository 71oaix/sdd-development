## Summary

<!-- What changed and why? -->

## Scope

- [ ] SDD routing or references
- [ ] Task Graph or run-log protocol
- [ ] Handoff Contract compatibility
- [ ] Repository governance only

## Contract compatibility

- Supported Handoff Contract version: <!-- x.y.z -->
- Upstream impact on `three-space-development`: <!-- none / describe -->

## Verification

- [ ] `python -m compileall -q scripts`
- [ ] `python scripts/validate_public_surface.py`
- [ ] If present: `python scripts/validate_task_graph.py templates/task-graph.json`
- [ ] If present: `python scripts/validate_run_log.py .run-log.jsonl`
- [ ] Relevant references and templates were checked

## Source and runtime

- [ ] The editable source is this repository
- [ ] No installed runtime copy was edited directly
- [ ] Runtime synchronization is not required / will follow the merged tag

## Public-surface check

- [ ] No personal machine paths, credentials, private keys, or restricted material were added
