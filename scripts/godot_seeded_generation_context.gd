class_name SeededGenerationContext
extends RefCounted

## Keeps independent RNG streams so layout changes do not silently change loot or encounters.
## Store master_seed and generator_version with every run report.

var master_seed: int
var generator_version: String
var _streams: Dictionary = {}

func _init(p_master_seed: int, p_generator_version: String = "1.0") -> void:
    master_seed = p_master_seed
    generator_version = p_generator_version

func stream(label: String) -> RandomNumberGenerator:
    if not _streams.has(label):
        var rng := RandomNumberGenerator.new()
        rng.seed = _derive_seed(label)
        _streams[label] = rng
    return _streams[label] as RandomNumberGenerator

func snapshot() -> Dictionary:
    var states: Dictionary = {}
    for label in _streams:
        states[label] = (_streams[label] as RandomNumberGenerator).state
    return {
        "master_seed": master_seed,
        "generator_version": generator_version,
        "stream_states": states,
    }

func restore(snapshot_data: Dictionary) -> void:
    master_seed = int(snapshot_data.get("master_seed", master_seed))
    generator_version = str(snapshot_data.get("generator_version", generator_version))
    _streams.clear()
    var states: Dictionary = snapshot_data.get("stream_states", {})
    for label in states:
        var rng := RandomNumberGenerator.new()
        rng.seed = _derive_seed(str(label))
        rng.state = int(states[label])
        _streams[str(label)] = rng

func _derive_seed(label: String) -> int:
    # Version the derivation if changing this function; old seeds otherwise change output.
    return int(hash("%s|%s|%s" % [generator_version, master_seed, label]))
