extends Node
class_name AudioCueRouter

@export var players: Dictionary = {}
var last_event_serial: Dictionary = {}

func play_cue(cue_id: StringName, event_serial: int, position: Vector3 = Vector3.ZERO) -> void:
    if last_event_serial.get(cue_id, -1) == event_serial:
        return
    last_event_serial[cue_id] = event_serial
    var player = players.get(cue_id)
    if player == null:
        push_warning("Missing audio cue: %s" % cue_id)
        return
    if player is AudioStreamPlayer3D:
        player.global_position = position
    player.play()
