# Output Contracts / 输出合同

## Evidence labels / 证据标签

- **Observed / 已观察:** directly reproduced or measured.
- **Inferred / 推断:** best explanation supported by current evidence.
- **Proposed / 建议:** a change not yet validated.
- **Unknown / 未知:** information that could change the decision.

## Required acceptance fields / 必填验收字段

Every implementation item should include:

- `owner`
- `affected_paths`
- `authoritative_state_or_event`
- `preconditions`
- `automated_check`
- `human_check`
- `pass_threshold`
- `rollback`
- `deferred_or_cut`

## Compact single-domain handoff / 单领域交付

1. Diagnosis and evidence.
2. Targeted change and Godot ownership boundary.
3. Automated plus human validation with thresholds.
4. Risk, rollback, unknowns, and deferred work.

## Cross-domain handoff / 跨领域交付

1. Player outcome and scope.
2. Evidence and confidence.
3. Up to three blocking root causes.
4. Causal chain plus authoritative state/event contract.
5. Selected domain contracts and owners.
6. Godot boundaries, shared files, migration order.
7. Budgets, degradation, and asset needs.
8. Tests, thresholds, acceptance, rollback.
9. Backlog and cuts.

Do not report “done” when only static validation passed. State which engine, scene, device, language, input, save, and playtest checks actually ran.
