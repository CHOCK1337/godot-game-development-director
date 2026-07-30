extends Resource
class_name AccessibilitySettings

@export var subtitles_enabled := true
@export var subtitle_scale := 1.0
@export var speaker_labels := true
@export var reduced_motion := false
@export_range(0.0, 1.0, 0.05) var camera_shake_scale := 1.0
@export_range(0.0, 1.0, 0.05) var flash_scale := 1.0
@export var hold_to_toggle := false
@export var screen_reader_labels := true

func apply_to_camera_impulse(raw_strength: float) -> float:
    if reduced_motion:
        return raw_strength * min(camera_shake_scale, 0.25)
    return raw_strength * camera_shake_scale
