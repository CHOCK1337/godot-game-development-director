extends SceneTree

const SCRIPT_FILES := [
    "godot_accessibility_settings.gd",
    "godot_adaptive_music_director.gd",
    "godot_audio_cue_router.gd",
    "godot_camera_impulse_director.gd",
    "godot_encounter_intensity_director.gd",
    "godot_motion_capture.gd",
    "godot_npc_decision_trace.gd",
    "godot_seeded_generation_context.gd",
    "godot_versioned_save_manager.gd",
]


func _initialize() -> void:
    var source_root := _argument_value("--source-root")
    if source_root.is_empty():
        push_error("Missing --source-root argument")
        quit(2)
        return

    var loaded: Dictionary = {}
    for filename in SCRIPT_FILES:
        var path := source_root.path_join("scripts").path_join(filename)
        var source := FileAccess.get_file_as_string(path)
        if source.is_empty():
            push_error("Could not read shipped GDScript: %s" % path)
            quit(1)
            return
        var candidate := GDScript.new()
        candidate.source_code = source
        var error := candidate.reload()
        if error != OK:
            push_error("GDScript compile failed (%s): %s" % [error, filename])
            quit(1)
            return
        loaded[filename] = candidate

    if not _run_smoke_assertions(loaded):
        quit(1)
        return
    loaded.clear()
    print("GODOT_PACKAGE_SMOKE_OK scripts=%s" % SCRIPT_FILES.size())
    quit(0)


func _run_smoke_assertions(loaded: Dictionary) -> bool:
    var accessibility: Resource = loaded["godot_accessibility_settings.gd"].new()
    accessibility.reduced_motion = true
    if not is_equal_approx(accessibility.apply_to_camera_impulse(1.0), 0.25):
        push_error("AccessibilitySettings reduced-motion smoke assertion failed")
        return false

    var camera: Node = loaded["godot_camera_impulse_director.gd"].new()
    camera.reduced_motion = true
    var impulse: Dictionary = camera.resolve_impulse(1.0, 1.0, 1.0)
    if float(impulse.get("translation", -1.0)) > camera.max_translation * 0.25:
        push_error("CameraImpulseDirector reduced-motion clamp failed")
        return false

    var trace: Node = loaded["godot_npc_decision_trace.gd"].new()
    trace.record(&"guard_1", &"search", "heard_noise")
    if trace.latest_for(&"guard_1").get("reason") != "heard_noise":
        push_error("NPCDecisionTrace record lookup failed")
        return false

    var seeded: RefCounted = loaded["godot_seeded_generation_context.gd"].new(42, "smoke")
    var first: int = seeded.stream("layout").randi()
    var second_context: RefCounted = loaded["godot_seeded_generation_context.gd"].new(42, "smoke")
    if first != second_context.stream("layout").randi():
        push_error("SeededGenerationContext is not deterministic")
        return false
    accessibility = null
    camera.free()
    trace.free()
    seeded = null
    second_context = null
    return true


func _argument_value(flag: String) -> String:
    var args := OS.get_cmdline_user_args()
    for index in range(args.size() - 1):
        if args[index] == flag:
            return args[index + 1]
    return ""
