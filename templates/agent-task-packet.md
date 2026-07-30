# Agent Task Packet

- task_id:
- assigned_agent:
- objective:
- scope_in:
- scope_out:
- experience_goal:
- source_ids / evidence_ranges:
- known_facts:
- hypotheses_not_facts:
- user_constraints:
- Godot_version_and_context:
- gameplay_state_and_event_context:
- files_or_media:
- do_not_modify:
- required_output_schema: agents/specialist-report.schema.json
- confidence_requirement:
- completion_condition:

任务包必须自包含但只包含该专家需要的上下文。不要粘贴完整会话，不要让专家“顺便检查其他方面”。共享 Event、状态或文件只允许提出变更建议，由编排器合并。
