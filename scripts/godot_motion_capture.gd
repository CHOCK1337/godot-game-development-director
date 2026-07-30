extends Node
## Debug-only recorder for world-space root/foot motion.
## Assign Marker3D nodes at the sole contact points and optional downward RayCast3D nodes.

@export var character_root: Node3D
@export var left_foot: Node3D
@export var right_foot: Node3D
@export var left_contact_ray: RayCast3D
@export var right_contact_ray: RayCast3D
@export_file("*.csv") var output_path: String = "user://motion_capture.csv"
@export var auto_start: bool = true

var _file: FileAccess
var _elapsed := 0.0
var _recording := false

func _ready() -> void:
    if auto_start:
        start_recording()

func start_recording() -> void:
    if character_root == null or left_foot == null or right_foot == null:
        push_error("Assign character_root, left_foot and right_foot before recording.")
        return
    _file = FileAccess.open(output_path, FileAccess.WRITE)
    if _file == null:
        push_error("Could not open motion capture CSV: %s" % output_path)
        return
    _file.store_line("time,root_x,root_y,root_z,left_x,left_y,left_z,right_x,right_y,right_z,left_contact,right_contact")
    _elapsed = 0.0
    _recording = true

func stop_recording() -> void:
    _recording = false
    if _file != null:
        _file.flush()
        _file.close()
        _file = null

func _physics_process(delta: float) -> void:
    if not _recording or _file == null:
        return
    _elapsed += delta
    var r := character_root.global_position
    var l := left_foot.global_position
    var rf := right_foot.global_position
    var lc := left_contact_ray != null and left_contact_ray.is_colliding()
    var rc := right_contact_ray != null and right_contact_ray.is_colliding()
    _file.store_csv_line(PackedStringArray([
        str(_elapsed), str(r.x), str(r.y), str(r.z),
        str(l.x), str(l.y), str(l.z),
        str(rf.x), str(rf.y), str(rf.z),
        "1" if lc else "0", "1" if rc else "0"
    ]))

func _exit_tree() -> void:
    stop_recording()
