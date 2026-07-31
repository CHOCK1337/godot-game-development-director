extends Node
class_name AdaptiveMusicDirector

## Minimal horizontal music director for Godot 4.
## Configure two AudioStreamPlayer nodes and dictionaries in the Inspector.
## Verify against the exact Godot version used by the project.

@export var player_a: AudioStreamPlayer
@export var player_b: AudioStreamPlayer
@export var state_streams: Dictionary = {}
@export var state_bpm: Dictionary = {}
@export var state_beats_per_bar: Dictionary = {}
@export_range(0.0, 10.0, 0.05) var crossfade_seconds := 0.6

var current_state: StringName = &""
var _active: AudioStreamPlayer
var _inactive: AudioStreamPlayer
var _pending_state: StringName = &""
var _pending_at_seconds := -1.0

func _ready() -> void:
    if player_a == null or player_b == null:
        push_error("AdaptiveMusicDirector requires player_a and player_b")
        set_process(false)
        return
    _active = player_a
    _inactive = player_b

func request_state(next_state: StringName, quantization: StringName = &"bar") -> void:
    if next_state == current_state or not state_streams.has(next_state):
        return
    _pending_state = next_state
    if not _active.playing or quantization == &"immediate":
        _pending_at_seconds = _clock_seconds()
        return
    var bpm: float = float(state_bpm.get(current_state, 120.0))
    var beats_per_bar: float = float(state_beats_per_bar.get(current_state, 4.0))
    var beat_seconds: float = 60.0 / maxf(bpm, 1.0)
    var quantum: float = beat_seconds
    if quantization == &"bar":
        quantum *= beats_per_bar
    elif quantization == &"phrase":
        quantum *= beats_per_bar * 4.0
    var position: float = _active.get_playback_position()
    var wait_seconds: float = quantum - fmod(position, quantum)
    _pending_at_seconds = _clock_seconds() + wait_seconds

func _process(_delta: float) -> void:
    if _pending_at_seconds >= 0.0 and _clock_seconds() >= _pending_at_seconds:
        _commit_pending()

func _commit_pending() -> void:
    var stream: AudioStream = state_streams.get(_pending_state)
    if stream == null:
        _pending_state = &""
        _pending_at_seconds = -1.0
        return
    _inactive.stream = stream
    _inactive.volume_db = -80.0
    _inactive.play()
    var tween := create_tween().set_parallel(true)
    tween.tween_property(_active, "volume_db", -80.0, crossfade_seconds)
    tween.tween_property(_inactive, "volume_db", 0.0, crossfade_seconds)
    var old_active := _active
    _active = _inactive
    _inactive = old_active
    current_state = _pending_state
    _pending_state = &""
    _pending_at_seconds = -1.0
    await tween.finished
    _inactive.stop()

func _clock_seconds() -> float:
    return Time.get_ticks_msec() / 1000.0
