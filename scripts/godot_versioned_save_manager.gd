extends Node
class_name VersionedSaveManager

const CURRENT_VERSION := 3
@export var save_path := "user://savegame.json"
@export var backup_path := "user://savegame.backup.json"

func save_snapshot(snapshot: Dictionary) -> Error:
    var payload := snapshot.duplicate(true)
    payload["schema_version"] = CURRENT_VERSION
    var temp_path := save_path + ".tmp"
    var file := FileAccess.open(temp_path, FileAccess.WRITE)
    if file == null:
        return FileAccess.get_open_error()
    file.store_string(JSON.stringify(payload))
    file.close()
    if FileAccess.file_exists(save_path):
        DirAccess.copy_absolute(ProjectSettings.globalize_path(save_path), ProjectSettings.globalize_path(backup_path))
    var err := DirAccess.rename_absolute(ProjectSettings.globalize_path(temp_path), ProjectSettings.globalize_path(save_path))
    return err

func load_snapshot() -> Dictionary:
    var payload := _read_json(save_path)
    if payload.is_empty():
        payload = _read_json(backup_path)
    return _migrate(payload)

func _read_json(path: String) -> Dictionary:
    if not FileAccess.file_exists(path):
        return {}
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return {}
    var parsed = JSON.parse_string(file.get_as_text())
    return parsed if parsed is Dictionary else {}

func _migrate(payload: Dictionary) -> Dictionary:
    var version := int(payload.get("schema_version", 1))
    var result := payload.duplicate(true)
    while version < CURRENT_VERSION:
        match version:
            1:
                result = _migrate_1_to_2(result)
            2:
                result = _migrate_2_to_3(result)
            _:
                push_error("Unsupported save schema: %s" % version)
                return {}
        version += 1
        result["schema_version"] = version
    return result

func _migrate_1_to_2(data: Dictionary) -> Dictionary:
    data.get_or_add("quests", {})
    return data

func _migrate_2_to_3(data: Dictionary) -> Dictionary:
    data.get_or_add("settings", {})
    return data
