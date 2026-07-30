extends Node
class_name CameraImpulseDirector

@export var max_translation := 0.25
@export var max_rotation_degrees := 2.0
@export var reduced_motion_scale := 0.25
var reduced_motion := false

func resolve_impulse(base_strength: float, distance_factor: float, priority_factor: float) -> Dictionary:
    var scale := reduced_motion_scale if reduced_motion else 1.0
    var strength := clampf(base_strength * distance_factor * priority_factor * scale, 0.0, 1.0)
    return {
        "translation": max_translation * strength,
        "rotation_degrees": max_rotation_degrees * strength,
    }
