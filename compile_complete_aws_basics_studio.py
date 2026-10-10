# -*- coding: utf-8 -*-
"""
compile_complete_aws_basics_studio.py
Generates the complete aws_basics_studio_app.html with:
1. Pure light-mode professional AWS UI.
2. WebGPU, Groq LPU, and intelligent client simulation engine.
3. 7 foundational AWS Level 0 operations (Bedrock, AgentCore, S3 Vault, Database, Lambda, Step Functions, Client API).
4. Live DynamoDB CAS mutex table & S3 WORM receipt verification.
5. Interactive Step Functions HFSM visualizer.
6. Generated Boto3 / CDK script.
7. ALL 20 production-grade SKILL.md specification files across all 3 tiers:
   - Level 0 (7 AWS Base Primitives)
   - Level 1 (7 Agent OS Kernel Skills)
   - Level 2 (6 Small-World Swarm Coordination Skills)
   with interactive filtering, live search, 1-click copy, and JSON export.
"""

import os
import json

from update_aws_basics_studio import SKILLS_DATA

# Read base HTML before the previous update
# Or build cleanly
with open('build_aws_basics_studio.py', 'r', encoding='utf-8') as f:
    orig_script = f.read()

# Extract HTML_CONTENT from build_aws_basics_studio.py
start_marker = "HTML_CONTENT = r'''"
end_marker = "'''\n\nwith open('aws_basics_studio_app.html'"

start_pos = orig_script.find(start_marker) + len(start_marker)
end_pos = orig_script.find(end_marker)
base_html = orig_script[start_pos:end_pos]

# 1. Update tab navigation
old_tabs = '''        <button class="tab-btn" id="tabBtnCode" onclick="switchStage('code')">💻 Boto3 & CDK Script</button>
        <button class="tab-btn" id="tabBtnRunbook" onclick="switchStage('runbook')">📜 Level 0 Skill Directives</button>'''

new_tabs = '''        <button class="tab-btn" id="tabBtnCode" onclick="switchStage('code')">💻 Boto3 & CDK Script</button>
        <button class="tab-btn" id="tabBtnRunbook" onclick="switchStage('runbook')">📜 Level 0 Directives</button>
        <button class="tab-btn" id="tabBtnSkills" onclick="switchStage('skills')">📚 SKILL.md Library (All 20 Skills)</button>'''

base_html = base_html.replace(old_tabs, new_tabs)

# 2. Add stageSkills container
skills_stage_html = '''
      <!-- TAB 6: COMPLETE SKILL.MD LIBRARY (ALL 20 SKILLS) -->
      <div class="stage-content" id="stageSkills" style="display: none; height: 100%;">
        <div style="background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; min-height: 580px; box-shadow: var(--card-shadow);">
          <!-- TOOLBAR -->
          <div style="padding: 12px 18px; background: var(--bg-panel-subtle); border-bottom: 1px solid var(--border-subtle); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <span style="font-weight: 800; font-size: 0.82rem; font-family: var(--font-display); color: var(--text-primary); margin-right: 4px;">TIER:</span>
              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--aws-orange); background: #fff7ed; color: #c2410c;">All (20)</button>
              <button class="theme-toggle-btn" id="filterL0" onclick="filterSkills('L0')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 0: AWS (7)</button>
              <button class="theme-toggle-btn" id="filterL1" onclick="filterSkills('L1')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 1: Kernel (7)</button>
              <button class="theme-toggle-btn" id="filterL2" onclick="filterSkills('L2')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 2: Swarm (6)</button>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <input type="text" id="skillSearchInput" placeholder="🔍 Search 20 skills..." oninput="searchSkills()" style="padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border-subtle); background: var(--bg-panel); font-size: 0.75rem; color: var(--text-primary); width: 170px;">
              <button class="theme-toggle-btn" onclick="copyCurrentSkillMd()" title="Copy active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">📋 Copy SKILL.md</button>
              <button class="theme-toggle-btn" onclick="downloadCurrentSkillMd()" title="Download active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">⬇️ Download</button>
              <button class="btn-action" onclick="downloadAllSkillsBundle()" style="padding: 5px 12px; font-size: 0.72rem;"><span>📦 Export All JSON</span></button>
            </div>
          </div>

          <!-- SPLIT VIEW -->
          <div style="display: flex; flex: 1; min-height: 500px; overflow: hidden;">
            <!-- SIDEBAR LIST -->
            <div id="skillsListPane" style="width: 290px; border-right: 1px solid var(--border-subtle); overflow-y: auto; background: var(--bg-canvas); padding: 10px; display: flex; flex-direction: column; gap: 6px;">
            </div>

            <!-- PREVIEW PANE -->
            <div style="flex: 1; display: flex; flex-direction: column; overflow: hidden; background: var(--bg-panel);">
              <div id="skillDetailHeader" style="padding: 12px 18px; border-bottom: 1px solid var(--border-subtle); background: var(--bg-panel-subtle); display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <div id="skillHeaderTitle" style="font-weight: 800; font-size: 1rem; font-family: var(--font-display); color: var(--text-primary);">aws-bedrock/SKILL.md</div>
                  <div id="skillHeaderMeta" style="font-size: 0.74rem; color: var(--text-muted); margin-top: 2px;">Level 0 &bull; Ring 3 (Untrusted Proposal Space) &bull; Amazon Bedrock</div>
                </div>
                <div id="skillBadgeTier" class="badge-skill" style="font-size: 0.7rem; background: #fff7ed; color: #c2410c; border: 1px solid #ffedd5;">LEVEL 0</div>
              </div>
              <div style="flex: 1; overflow-y: auto; padding: 16px;">
                <pre class="code-view" id="skillContentPre" style="margin: 0; min-height: 100%; font-size: 0.76rem; line-height: 1.48;"></pre>
              </div>
            </div>
          </div>
        </div>
      </div>
'''

base_html = base_html.replace('<!-- TAB 5: RUNBOOK -->', skills_stage_html + '\n      <!-- TAB 5: RUNBOOK -->')

# 3. Update switchStage function in JS
old_switch_func = '''    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('stageArch').style.display = stage === 'arch' ? 'flex' : 'none';
      document.getElementById('stageLocks').style.display = stage === 'locks' ? 'flex' : 'none';
      document.getElementById('stageHfsm').style.display = stage === 'hfsm' ? 'flex' : 'none';
      document.getElementById('stageCode').style.display = stage === 'code' ? 'flex' : 'none';
      document.getElementById('stageRunbook').style.display = stage === 'runbook' ? 'flex' : 'none';

      if (stage === 'arch') document.getElementById('tabBtnArch').classList.add('active');
      if (stage === 'locks') document.getElementById('tabBtnLocks').classList.add('active');
      if (stage === 'hfsm') document.getElementById('tabBtnHfsm').classList.add('active');
      if (stage === 'code') document.getElementById('tabBtnCode').classList.add('active');
      if (stage === 'runbook') document.getElementById('tabBtnRunbook').classList.add('active');
    }'''

new_switch_func = '''    function switchStage(stage) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('stageArch').style.display = stage === 'arch' ? 'flex' : 'none';
      document.getElementById('stageLocks').style.display = stage === 'locks' ? 'flex' : 'none';
      document.getElementById('stageHfsm').style.display = stage === 'hfsm' ? 'flex' : 'none';
      document.getElementById('stageCode').style.display = stage === 'code' ? 'flex' : 'none';
      document.getElementById('stageRunbook').style.display = stage === 'runbook' ? 'flex' : 'none';
      const skillsEl = document.getElementById('stageSkills');
      if (skillsEl) skillsEl.style.display = stage === 'skills' ? 'block' : 'none';

      if (stage === 'arch') document.getElementById('tabBtnArch')?.classList.add('active');
      if (stage === 'locks') document.getElementById('tabBtnLocks')?.classList.add('active');
      if (stage === 'hfsm') document.getElementById('tabBtnHfsm')?.classList.add('active');
      if (stage === 'code') document.getElementById('tabBtnCode')?.classList.add('active');
      if (stage === 'runbook') document.getElementById('tabBtnRunbook')?.classList.add('active');
      if (stage === 'skills') {
        document.getElementById('tabBtnSkills')?.classList.add('active');
        if (typeof initSkillsLibrary === 'function') initSkillsLibrary();
      }
    }'''

base_html = base_html.replace(old_switch_func, new_switch_func)

# 4. Inject SKILLS_DATA and JS logic
js_skills_data = json.dumps(SKILLS_DATA, indent=2)

js_library_logic = f'''
    // ==========================================
    // EMBEDDED 3-TIER SKILL.MD LIBRARY (20 SKILLS)
    // ==========================================
    const SKILLS_LIBRARY = {js_skills_data};
    let currentSelectedSkillId = "aws-bedrock";
    let activeTierFilter = "all";

    function initSkillsLibrary() {{
      renderSkillsList();
      selectSkill(currentSelectedSkillId);
    }}

    function filterSkills(tier) {{
      activeTierFilter = tier;
      ['filterAll', 'filterL0', 'filterL1', 'filterL2'].forEach(id => {{
        const btn = document.getElementById(id);
        if (btn) {{
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }}
      }});
      const targetId = tier === 'all' ? 'filterAll' : 'filter' + tier;
      const activeBtn = document.getElementById(targetId);
      if (activeBtn) {{
        activeBtn.style.borderColor = 'var(--aws-orange)';
        activeBtn.style.background = '#fff7ed';
        activeBtn.style.color = '#c2410c';
      }}
      renderSkillsList();
    }}

    function searchSkills() {{
      renderSkillsList();
    }}

    function renderSkillsList() {{
      const pane = document.getElementById('skillsListPane');
      if (!pane) return;
      const query = (document.getElementById('skillSearchInput')?.value || '').toLowerCase();

      let filtered = SKILLS_LIBRARY.filter(s => {{
        const matchesTier = activeTierFilter === 'all' || s.tierCode === activeTierFilter;
        const matchesQuery = s.name.toLowerCase().includes(query) ||
                             s.title.toLowerCase().includes(query) ||
                             s.service.toLowerCase().includes(query) ||
                             s.description.toLowerCase().includes(query);
        return matchesTier && matchesQuery;
      }});

      if (filtered.length === 0) {{
        pane.innerHTML = '<div style="padding: 14px; font-size: 0.75rem; color: var(--text-muted); text-align: center;">No matching skills found.</div>';
        return;
      }}

      pane.innerHTML = filtered.map(s => {{
        const isSelected = s.id === currentSelectedSkillId;
        const bgStyle = isSelected ? 'background: #fff7ed; border-color: var(--aws-orange);' : 'background: var(--bg-panel); border-color: var(--border-subtle);';
        const tierColor = s.tierCode === 'L0' ? '#ea580c' : (s.tierCode === 'L1' ? '#2563eb' : '#7c3aed');
        return `
          <div onclick="selectSkill('${{s.id}}')" style="cursor: pointer; padding: 9px 11px; border-radius: 8px; border: 1.5px solid; ${{bgStyle}} display: flex; flex-direction: column; gap: 3px; transition: all 0.15s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-family: var(--font-mono); font-weight: 700; font-size: 0.76rem; color: var(--text-primary);">${{s.name}}</span>
              <span style="font-size: 0.62rem; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: ${{tierColor}}15; color: ${{tierColor}};">${{s.tierCode}}</span>
            </div>
            <div style="font-size: 0.68rem; color: var(--text-secondary); line-height: 1.25;">${{s.title}}</div>
            <div style="font-size: 0.62rem; color: var(--text-muted); font-family: var(--font-mono);">${{s.ring.split(' ')[0]}}</div>
          </div>
        `;
      }}).join('');
    }}

    function selectSkill(skillId) {{
      const skill = SKILLS_LIBRARY.find(s => s.id === skillId);
      if (!skill) return;
      currentSelectedSkillId = skillId;

      document.getElementById('skillHeaderTitle').textContent = `${{skill.name}}/SKILL.md`;
      document.getElementById('skillHeaderMeta').textContent = `${{skill.tier}} • ${{skill.ring}} • ${{skill.service}}`;
      document.getElementById('skillBadgeTier').textContent = skill.tier.toUpperCase();
      document.getElementById('skillContentPre').textContent = skill.content.trim();

      renderSkillsList();
    }}

    function copyCurrentSkillMd() {{
      const skill = SKILLS_LIBRARY.find(s => s.id === currentSelectedSkillId);
      if (!skill) return;
      navigator.clipboard.writeText(skill.content.trim()).then(() => {{
        showToast(`✅ Copied ${{skill.name}}/SKILL.md to clipboard!`);
      }});
    }}

    function downloadCurrentSkillMd() {{
      const skill = SKILLS_LIBRARY.find(s => s.id === currentSelectedSkillId);
      if (!skill) return;
      const blob = new Blob([skill.content.trim()], {{ type: 'text/markdown' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${{skill.name}}.SKILL.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`💾 Downloaded ${{skill.name}}.SKILL.md`);
    }}

    function downloadAllSkillsBundle() {{
      const bundle = {{
        title: "The 3-Tier Enterprise Agent Skills Bundle",
        count: SKILLS_LIBRARY.length,
        exportedAt: new Date().toISOString(),
        skills: SKILLS_LIBRARY
      }};
      const blob = new Blob([JSON.stringify(bundle, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'three_tier_agent_skills_manifest.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`📦 Exported all 20 SKILL.md specifications in JSON manifest!`);
    }}
'''

target_init = "loadPreset(0);"
replacement_init = "loadPreset(0);\n      initSkillsLibrary();"
base_html = base_html.replace(target_init, replacement_init, 1)

target_toast = "function showToast(msg) {"
base_html = base_html.replace(target_toast, js_library_logic + "\n    function showToast(msg) {", 1)

with open('aws_basics_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(base_html)

print("Generated aws_basics_studio_app.html with complete 20 SKILL.md library successfully!")
