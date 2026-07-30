class_name EncounterIntensityDirector
extends Node

## Generic pacing signal, not a hidden difficulty cheat.
## Feed stable gameplay evidence; consumers may change spawn frequency, music layers or support drops.

signal intensity_state_changed(previous: StringName, current: StringName, score: float)

enum State { BUILDUP, PEAK, RELAX }

@export_range(0.0, 1.0) var peak_enter := 0.75
@export_range(0.0, 1.0) var peak_exit := 0.50
@export_range(0.0, 1.0) var relax_exit := 0.25
@export var minimum_peak_s := 4.0
@export var minimum_relax_s := 8.0
@export var pressure_decay_per_s := 0.12

var pressure := 0.0
var state: State = State.BUILDUP
var time_in_state := 0.0

func report_pressure(amount: float) -> void:
    pressure = clampf(maxf(pressure, amount), 0.0, 1.0)

func _process(delta: float) -> void:
    time_in_state += delta
    pressure = maxf(0.0, pressure - pressure_decay_per_s * delta)
    var next_state := state
    match state:
        State.BUILDUP:
            if pressure >= peak_enter:
                next_state = State.PEAK
        State.PEAK:
            if time_in_state >= minimum_peak_s and pressure <= peak_exit:
                next_state = State.RELAX
        State.RELAX:
            if time_in_state >= minimum_relax_s and pressure <= relax_exit:
                next_state = State.BUILDUP
    if next_state != state:
        var previous_name := _state_name(state)
        state = next_state
        time_in_state = 0.0
        intensity_state_changed.emit(previous_name, _state_name(state), pressure)

func _state_name(value: int) -> StringName:
    match value:
        State.PEAK: return &"peak"
        State.RELAX: return &"relax"
        _: return &"buildup"
