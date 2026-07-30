extends Node
class_name NPCDecisionTrace

@export var enabled := true
var records: Array[Dictionary] = []

func record(agent_id: StringName, state: StringName, reason: String, target_id: StringName = &"", stimulus: StringName = &"", scores: Dictionary = {}) -> void:
    if not enabled:
        return
    records.append({
        "time_ms": Time.get_ticks_msec(),
        "agent_id": String(agent_id),
        "state": String(state),
        "reason": reason,
        "target_id": String(target_id),
        "stimulus": String(stimulus),
        "scores": scores.duplicate(true),
    })
    if records.size() > 256:
        records.pop_front()

func latest_for(agent_id: StringName) -> Dictionary:
    for index in range(records.size() - 1, -1, -1):
        if records[index].get("agent_id") == String(agent_id):
            return records[index]
    return {}
