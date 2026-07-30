from pathlib import Path
import json, py_compile, re, sys

ROOT=Path(__file__).parents[1]
required=[
'SKILL.md','README.md','SOURCES.md','CHANGELOG.md',
'agents/orchestrator.md','agents/routing-table.md','agents/godot-game-feel-swarm.yaml',
'agents/review-contract.json','agents/specialist-report.schema.json','agents/dispatch-plan.schema.json',
'skills/designing-godot-gameplay/SKILL.md','skills/directing-interactive-game-music/SKILL.md','skills/designing-godot-levels-balance-randomness/SKILL.md',
'skills/producing-game-content/SKILL.md','skills/authoring-narrative-quests-cinematics/SKILL.md','skills/designing-npc-ai-simulation/SKILL.md',
'skills/polishing-game-presentation-accessibility/SKILL.md','skills/building-godot-content-pipelines/SKILL.md',
'agents/gameplay-spec.schema.json','agents/music-state-map.schema.json','agents/event-contract.schema.json','agents/level-spec.schema.json','agents/balance-model.schema.json','agents/generator-spec.schema.json',
'agents/quest-spec.schema.json','agents/npc-ai-spec.schema.json','agents/content-budget.schema.json','agents/accessibility-localization.schema.json','agents/save-schema.schema.json',
'agents/specialists/content-production-scope.md','agents/specialists/narrative-quest-cinematics.md','agents/specialists/npc-ai-simulation.md',
'agents/specialists/gameplay-camera-composition.md','agents/specialists/technical-art-rendering.md','agents/specialists/sound-design-voice-mix.md',
'agents/specialists/ux-accessibility-localization.md','agents/specialists/content-architecture-save-tools.md','agents/specialists/content-qa-automation.md',
'knowledge/27-content-production-scope.md','knowledge/28-narrative-quest-cinematics.md','knowledge/29-npc-ai-simulation.md','knowledge/30-gameplay-camera-composition.md',
'knowledge/31-technical-art-rendering.md','knowledge/32-sound-design-voice-mix.md','knowledge/33-ux-accessibility-localization.md','knowledge/34-content-architecture-save-tools.md','knowledge/35-content-qa-automation.md','knowledge/36-content-team-routing.md',
'checklists/content-production-scope.md','checklists/narrative-quest.md','checklists/npc-ai.md','checklists/gameplay-camera.md','checklists/technical-art.md','checklists/sound-design.md','checklists/ux-accessibility-localization.md','checklists/content-architecture-save.md','checklists/content-qa.md','checklists/content-completion-rubric.md',
'templates/content-milestone.md','templates/quest-spec.template.json','templates/npc-ai-spec.template.json','templates/content-budget.template.json','templates/accessibility-localization.template.json','templates/save-schema.template.json','templates/camera-mode-plan.md','templates/audio-cue-sheet.md','templates/content-test-matrix.md',
'scripts/build_dispatch_plan.py','scripts/validate_quest_spec.py','scripts/validate_npc_ai_spec.py','scripts/validate_content_budget.py','scripts/validate_accessibility_localization.py','scripts/validate_save_schema.py','scripts/audit_content_coverage.py',
'scripts/godot_versioned_save_manager.gd','scripts/godot_npc_decision_trace.gd','scripts/godot_accessibility_settings.gd','scripts/godot_audio_cue_router.gd','scripts/godot_camera_impulse_director.gd',
'examples/20-content-milestone.md','examples/21-quest-spec.json','examples/22-npc-ai-spec.json','examples/23-content-budget.json','examples/24-accessibility-localization.json','examples/25-save-schema.json','examples/26-camera-mode-plan.md','examples/27-audio-cue-sheet.md','examples/28-content-team-orchestration.md','examples/29-dispatch-brief-content-team.json','examples/30-content-coverage.csv',
'codex/README.md','codex/AGENTS.md.example','workflows/cross-discipline-pipeline.md','workflows/parallel-swarm.md',
'docs/superpowers/specs/2026-07-28-content-team-v6-design.md','docs/superpowers/plans/2026-07-28-content-team-v6.md'
]
missing=[x for x in required if not (ROOT/x).is_file()]
if missing: raise SystemExit(f'Missing files: {missing}')

skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
if not re.match(r'^---\n(.*?)\n---',skill,re.S): raise SystemExit('root SKILL frontmatter missing')
for phrase in ['name: directing-godot-game-feel','27 个专家','Quest Spec','NPC AI Spec','Content Budget','Save Schema','不处理发行']:
    if phrase not in skill: raise SystemExit(f'SKILL missing: {phrase}')

subskills=sorted((ROOT/'skills').glob('*/SKILL.md'))
if len(subskills)!=8: raise SystemExit(f'Expected 8 installable skills, found {len(subskills)}')
for path in subskills:
    text=path.read_text(encoding='utf-8')
    if not re.match(r'^---\n.*?description: Use when.*?\n---',text,re.S): raise SystemExit(f'Bad subskill frontmatter: {path.relative_to(ROOT)}')

for path in ROOT.rglob('*.json'):
    if '__pycache__' not in path.parts:
        json.loads(path.read_text(encoding='utf-8'))

try:
    import yaml
    for path in ROOT.rglob('*.yaml'):
        yaml.safe_load(path.read_text(encoding='utf-8'))
except ImportError:
    print('warning: PyYAML unavailable; YAML parse skipped',file=sys.stderr)

for path in (ROOT/'scripts').glob('*.py'):
    py_compile.compile(str(path),doraise=True)

specialists=sorted((ROOT/'agents/specialists').glob('*.md'))
if len(specialists)!=27: raise SystemExit(f'Expected 27 specialists, found {len(specialists)}')

swarm=(ROOT/'agents/godot-game-feel-swarm.yaml').read_text(encoding='utf-8')
for name in ['content_production_scope','narrative_quest_cinematics','npc_ai_simulation','gameplay_camera_composition','technical_art_rendering','sound_design_voice_mix','ux_accessibility_localization','content_architecture_save_tools','content_qa_automation']:
    if name not in swarm: raise SystemExit(f'Swarm missing specialist: {name}')

for path in [ROOT/'scripts/godot_versioned_save_manager.gd',ROOT/'scripts/godot_npc_decision_trace.gd',ROOT/'scripts/godot_accessibility_settings.gd',ROOT/'scripts/godot_audio_cue_router.gd',ROOT/'scripts/godot_camera_impulse_director.gd']:
    text=path.read_text(encoding='utf-8')
    if not text.startswith('extends '): raise SystemExit(f'GDScript missing extends: {path.name}')
    if 'TODO' in text or 'TBD' in text: raise SystemExit(f'Placeholder in GDScript: {path.name}')

file_count=sum(1 for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
print(f'package validation passed: {file_count} deliverable files, {len(specialists)} specialists, {len(subskills)} skills')
