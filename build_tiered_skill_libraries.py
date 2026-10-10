# -*- coding: utf-8 -*-
"""
build_tiered_skill_libraries.py
Compiles and verifies the tiered skill libraries across all 3 applications:
- Tier 0 App (aws_basics_studio_app.html): ONLY Tier 0 Skills (7 AWS Cloud Primitives)
- Tier 1 App (agent_kernel_studio_app.html): BOTH Tier 0 and Tier 1 Skills (14 Skills: 7 Kernel + 7 AWS)
- Tier 2 App (multi_agent_system_studio_app.html): Tier 0, Tier 1, and Tier 2 Skills (20 Skills: 6 Swarm + 7 Kernel + 7 AWS)
"""

import json
from update_aws_basics_studio import SKILLS_DATA

# Filter skills for each tier
TIER_0_SKILLS = [s for s in SKILLS_DATA if s.get('tierCode') == 'L0']
TIER_1_SKILLS = [s for s in SKILLS_DATA if s.get('tierCode') in ['L0', 'L1']]
TIER_2_SKILLS = list(SKILLS_DATA)

print(f"Tier 0 App Skills Count: {len(TIER_0_SKILLS)} (Target: 7)")
print(f"Tier 1 App Skills Count: {len(TIER_1_SKILLS)} (Target: 14)")
print(f"Tier 2 App Skills Count: {len(TIER_2_SKILLS)} (Target: 20)")

# -------------------------------------------------------------
# 1. BUILD TIER 0 APP: aws_basics_studio_app.html (7 Skills Only)
# -------------------------------------------------------------
with open('build_aws_basics_studio.py', 'r', encoding='utf-8') as f:
    orig_script = f.read()

start_marker = "HTML_CONTENT = r'''"
end_marker = "'''\n\nwith open('aws_basics_studio_app.html'"
start_pos = orig_script.find(start_marker) + len(start_marker)
end_pos = orig_script.find(end_marker)
base_html_0 = orig_script[start_pos:end_pos]

old_tabs_0 = '''        <button class="tab-btn" id="tabBtnCode" onclick="switchStage('code')">💻 Boto3 & CDK Script</button>
        <button class="tab-btn" id="tabBtnRunbook" onclick="switchStage('runbook')">📜 Level 0 Skill Directives</button>'''

new_tabs_0 = '''        <button class="tab-btn" id="tabBtnCode" onclick="switchStage('code')">💻 Boto3 & CDK Script</button>
        <button class="tab-btn" id="tabBtnRunbook" onclick="switchStage('runbook')">📜 Level 0 Directives</button>
        <button class="tab-btn" id="tabBtnSkills" onclick="switchStage('skills')">📚 SKILL.md Library (7 AWS Skills)</button>'''
base_html_0 = base_html_0.replace(old_tabs_0, new_tabs_0)

skills_stage_0 = '''
      <!-- TAB 6: LEVEL 0 AWS SKILLS LIBRARY (7 SKILLS ONLY) -->
      <div class="stage-content" id="stageSkills" style="display: none; height: 100%;">
        <div style="background: var(--bg-panel); border: 1px solid var(--border-subtle); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; min-height: 580px; box-shadow: var(--card-shadow);">
          <!-- TOOLBAR -->
          <div style="padding: 12px 18px; background: var(--bg-panel-subtle); border-bottom: 1px solid var(--border-subtle); display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <span style="font-weight: 800; font-size: 0.82rem; font-family: var(--font-display); color: var(--text-primary); margin-right: 4px;">AWS PRIMITIVES:</span>
              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--aws-orange); background: #fff7ed; color: #c2410c;">All AWS Operations (7)</button>
              <button class="theme-toggle-btn" id="filterRing0" onclick="filterSkills('Ring 0')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Ring 0 Gate & Vaults (5)</button>
              <button class="theme-toggle-btn" id="filterRing3" onclick="filterSkills('Ring 3')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Ring 3 Proposals & Sandboxes (2)</button>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
              <input type="text" id="skillSearchInput" placeholder="🔍 Search 7 AWS skills..." oninput="searchSkills()" style="padding: 5px 10px; border-radius: 6px; border: 1px solid var(--border-subtle); background: var(--bg-panel); font-size: 0.75rem; color: var(--text-primary); width: 170px;">
              <button class="theme-toggle-btn" onclick="copyCurrentSkillMd()" title="Copy active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">📋 Copy SKILL.md</button>
              <button class="theme-toggle-btn" onclick="downloadCurrentSkillMd()" title="Download active SKILL.md" style="padding: 5px 10px; font-size: 0.72rem;">⬇️ Download</button>
              <button class="btn-action" onclick="downloadAllSkillsBundle()" style="padding: 5px 12px; font-size: 0.72rem;"><span>📦 Export L0 JSON</span></button>
            </div>
          </div>

          <!-- SPLIT VIEW -->
          <div style="display: flex; flex: 1; min-height: 500px; overflow: hidden;">
            <!-- SIDEBAR LIST -->
            <div id="skillsListPane" style="width: 290px; border-right: 1px solid var(--border-subtle); overflow-y: auto; background: var(--bg-canvas); padding: 10px; display: flex; flex-direction: column; gap: 6px;"></div>

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
base_html_0 = base_html_0.replace('<!-- TAB 5: RUNBOOK -->', skills_stage_0 + '\n      <!-- TAB 5: RUNBOOK -->')

switch_func_0 = '''    function switchStage(stage) {
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
base_html_0 = base_html_0.replace('''    function switchStage(stage) {
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
    }''', switch_func_0)

js_skills_data_0 = json.dumps(TIER_0_SKILLS, indent=2)
js_lib_0 = f'''
    // ==========================================
    // TIER 0 AWS PRIMITIVES SKILL.MD LIBRARY (7 SKILLS)
    // ==========================================
    const SKILLS_LIBRARY = {js_skills_data_0};
    let currentSelectedSkillId = "aws-bedrock";
    let activeTierFilter = "all";

    function initSkillsLibrary() {{
      renderSkillsList();
      selectSkill(currentSelectedSkillId);
    }}

    function filterSkills(filterVal) {{
      activeTierFilter = filterVal;
      ['filterAll', 'filterRing0', 'filterRing3'].forEach(id => {{
        const btn = document.getElementById(id);
        if (btn) {{
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }}
      }});
      const targetId = filterVal === 'all' ? 'filterAll' : (filterVal === 'Ring 0' ? 'filterRing0' : 'filterRing3');
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
        const matchesFilter = activeTierFilter === 'all' || s.ring.includes(activeTierFilter);
        const matchesQuery = s.name.toLowerCase().includes(query) ||
                             s.title.toLowerCase().includes(query) ||
                             s.service.toLowerCase().includes(query) ||
                             s.description.toLowerCase().includes(query);
        return matchesFilter && matchesQuery;
      }});

      if (filtered.length === 0) {{
        pane.innerHTML = '<div style="padding: 14px; font-size: 0.75rem; color: var(--text-muted); text-align: center;">No matching AWS skills found.</div>';
        return;
      }}

      pane.innerHTML = filtered.map(s => {{
        const isSelected = s.id === currentSelectedSkillId;
        const bgStyle = isSelected ? 'background: #fff7ed; border-color: var(--aws-orange);' : 'background: var(--bg-panel); border-color: var(--border-subtle);';
        return `
          <div onclick="selectSkill('${{s.id}}')" style="cursor: pointer; padding: 9px 11px; border-radius: 8px; border: 1.5px solid; ${{bgStyle}} display: flex; flex-direction: column; gap: 3px; transition: all 0.15s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-family: var(--font-mono); font-weight: 700; font-size: 0.76rem; color: var(--text-primary);">${{s.name}}</span>
              <span style="font-size: 0.62rem; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: #ea580c15; color: #ea580c;">AWS &bull; L0</span>
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
      document.getElementById('skillBadgeTier').textContent = "LEVEL 0";
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
        title: "Level 0 AWS Cloud Primitives Skills Manifest",
        tier: "Level 0",
        count: SKILLS_LIBRARY.length,
        exportedAt: new Date().toISOString(),
        skills: SKILLS_LIBRARY
      }};
      const blob = new Blob([JSON.stringify(bundle, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'level_0_aws_skills_manifest.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`📦 Exported 7 Level 0 AWS SKILL.md specs in JSON manifest!`);
    }}
'''
base_html_0 = base_html_0.replace("loadPreset(0);", "loadPreset(0);\n      initSkillsLibrary();")
base_html_0 = base_html_0.replace("function showToast(msg) {", js_lib_0 + "\n    function showToast(msg) {")

with open('aws_basics_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(base_html_0)
print("Updated aws_basics_studio_app.html with ONLY Tier 0 skills (7 skills).")


# -------------------------------------------------------------
# 2. BUILD TIER 1 APP: agent_kernel_studio_app.html (Tier 0 + Tier 1 = 14 Skills)
# -------------------------------------------------------------
with open('agent_kernel_studio_app.html', 'r', encoding='utf-8') as f:
    html_1 = f.read()

# Replace the KERNEL_SKILLS_LIBRARY with TIER_1_SKILLS (14 skills)
idx_start = html_1.find("const KERNEL_SKILLS_LIBRARY = ")
idx_end = html_1.find("let currentSelectedSkillId = ", idx_start)

new_skills_json_1 = f"const KERNEL_SKILLS_LIBRARY = {json.dumps(TIER_1_SKILLS, indent=2)};\n    "
html_1 = html_1[:idx_start] + new_skills_json_1 + html_1[idx_end:]

# Update toolbar filters in stageSkills for Tier 1
old_toolbar_1 = '''              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterKernelSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--accent-blue); background: #eff6ff; color: #1d4ed8;">All (7)</button>
              <button class="theme-toggle-btn" id="filterExecutive" onclick="filterKernelSkills('Executive Control')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Executive Suite (4)</button>
              <button class="theme-toggle-btn" id="filterMemory" onclick="filterKernelSkills('Multi-Store Memory')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Memory Suite (3)</button>'''

new_toolbar_1 = '''              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterKernelSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--accent-blue); background: #eff6ff; color: #1d4ed8;">All (14)</button>
              <button class="theme-toggle-btn" id="filterL1" onclick="filterKernelSkills('L1')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 1: Kernel (7)</button>
              <button class="theme-toggle-btn" id="filterL0" onclick="filterKernelSkills('L0')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 0: AWS Basics (7)</button>'''

html_1 = html_1.replace(old_toolbar_1, new_toolbar_1)

# Update tab button title
html_1 = html_1.replace('📚 Dedicated SKILL.md Library (7 Skills)', '📚 SKILL.md Library (14 Skills: Kernel + AWS)')

# Update filtering JS logic in Tier 1
old_filter_js_1 = '''    function filterKernelSkills(suite) {
      activeSuiteFilter = suite;
      ['filterAll', 'filterExecutive', 'filterMemory'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }
      });
      const targetId = suite === 'all' ? 'filterAll' : (suite === 'Executive Control' ? 'filterExecutive' : 'filterMemory');
      const activeBtn = document.getElementById(targetId);
      if (activeBtn) {
        activeBtn.style.borderColor = 'var(--accent-blue)';
        activeBtn.style.background = '#eff6ff';
        activeBtn.style.color = '#1d4ed8';
      }
      renderKernelSkillsList();
    }'''

new_filter_js_1 = '''    function filterKernelSkills(tierFilter) {
      activeSuiteFilter = tierFilter;
      ['filterAll', 'filterL1', 'filterL0'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }
      });
      const targetId = tierFilter === 'all' ? 'filterAll' : (tierFilter === 'L1' ? 'filterL1' : 'filterL0');
      const activeBtn = document.getElementById(targetId);
      if (activeBtn) {
        activeBtn.style.borderColor = 'var(--accent-blue)';
        activeBtn.style.background = '#eff6ff';
        activeBtn.style.color = '#1d4ed8';
      }
      renderKernelSkillsList();
    }'''

html_1 = html_1.replace(old_filter_js_1, new_filter_js_1)

# Update matching filter in renderKernelSkillsList
old_match_1 = "const matchesSuite = activeSuiteFilter === 'all' || s.suite === activeSuiteFilter;"
new_match_1 = "const matchesSuite = activeSuiteFilter === 'all' || s.tierCode === activeSuiteFilter;"
html_1 = html_1.replace(old_match_1, new_match_1)

# Update card badge in Tier 1
old_badge_1 = "${s.suite === 'Executive Control' ? 'EXEC' : 'MEM'} &bull; RING 0"
new_badge_1 = "${s.tierCode === 'L1' ? 'KERNEL &bull; L1' : 'AWS &bull; L0'}"
html_1 = html_1.replace(old_badge_1, new_badge_1)

with open('agent_kernel_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html_1)
print("Updated agent_kernel_studio_app.html with BOTH Tier 0 and Tier 1 skills (14 skills).")


# -------------------------------------------------------------
# 3. BUILD TIER 2 APP: multi_agent_system_studio_app.html (Tier 0, 1, 2 = 20 Skills)
# -------------------------------------------------------------
with open('multi_agent_system_studio_app.html', 'r', encoding='utf-8') as f:
    html_2 = f.read()

# Replace the SWARM_SKILLS_LIBRARY with TIER_2_SKILLS (20 skills)
idx_start_2 = html_2.find("const SWARM_SKILLS_LIBRARY = ")
idx_end_2 = html_2.find("let currentSelectedSkillId = ", idx_start_2)

new_skills_json_2 = f"const SWARM_SKILLS_LIBRARY = {json.dumps(TIER_2_SKILLS, indent=2)};\n    "
html_2 = html_2[:idx_start_2] + new_skills_json_2 + html_2[idx_end_2:]

# Update toolbar filters in stageSkills for Tier 2
old_toolbar_2 = '''              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterSwarmSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--accent-purple); background: #faf5ff; color: #6d28d9;">All (6)</button>
              <button class="theme-toggle-btn" id="filterArch" onclick="filterSwarmSkills('Swarm Architecture')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Architecture (2)</button>
              <button class="theme-toggle-btn" id="filterGov" onclick="filterSwarmSkills('Swarm Governance')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Governance &amp; BFT (4)</button>'''

new_toolbar_2 = '''              <button class="theme-toggle-btn active-filter" id="filterAll" onclick="filterSwarmSkills('all')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700; border-color: var(--accent-purple); background: #faf5ff; color: #6d28d9;">All (20)</button>
              <button class="theme-toggle-btn" id="filterL2" onclick="filterSwarmSkills('L2')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 2: Swarm (6)</button>
              <button class="theme-toggle-btn" id="filterL1" onclick="filterSwarmSkills('L1')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 1: Kernel (7)</button>
              <button class="theme-toggle-btn" id="filterL0" onclick="filterSwarmSkills('L0')" style="padding: 4px 10px; font-size: 0.72rem; font-weight: 700;">Level 0: AWS (7)</button>'''

html_2 = html_2.replace(old_toolbar_2, new_toolbar_2)

# Update tab button title
html_2 = html_2.replace('📚 Dedicated SKILL.md Library (6 Skills)', '📚 SKILL.md Library (All 20 Skills: Swarm + Kernel + AWS)')

# Update filtering JS logic in Tier 2
old_filter_js_2 = '''    function filterSwarmSkills(category) {
      activeCategoryFilter = category;
      ['filterAll', 'filterArch', 'filterGov'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }
      });
      const targetId = category === 'all' ? 'filterAll' : (category === 'Swarm Architecture' ? 'filterArch' : 'filterGov');
      const activeBtn = document.getElementById(targetId);
      if (activeBtn) {
        activeBtn.style.borderColor = 'var(--accent-purple)';
        activeBtn.style.background = '#faf5ff';
        activeBtn.style.color = '#6d28d9';
      }
      renderSwarmSkillsList();
    }'''

new_filter_js_2 = '''    function filterSwarmSkills(tierCode) {
      activeCategoryFilter = tierCode;
      ['filterAll', 'filterL2', 'filterL1', 'filterL0'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) {
          btn.style.borderColor = 'var(--border-subtle)';
          btn.style.background = 'var(--bg-panel-subtle)';
          btn.style.color = 'var(--text-secondary)';
        }
      });
      const targetId = tierCode === 'all' ? 'filterAll' : 'filter' + tierCode;
      const activeBtn = document.getElementById(targetId);
      if (activeBtn) {
        activeBtn.style.borderColor = 'var(--accent-purple)';
        activeBtn.style.background = '#faf5ff';
        activeBtn.style.color = '#6d28d9';
      }
      renderSwarmSkillsList();
    }'''

html_2 = html_2.replace(old_filter_js_2, new_filter_js_2)

# Update matching filter in renderSwarmSkillsList
old_match_2 = """let filtered = SWARM_SKILLS_LIBRARY.filter(s => {
        const matchesCat = activeCategoryFilter === 'all' ||
                           (activeCategoryFilter === 'Swarm Architecture' && (s.category.includes('Architecture') || s.category.includes('Routing'))) ||
                           (activeCategoryFilter === 'Swarm Governance' && (s.category.includes('Governance') || s.category.includes('Consensus') || s.category.includes('Cascade') || s.category.includes('State')));"""

new_match_2 = """let filtered = SWARM_SKILLS_LIBRARY.filter(s => {
        const matchesCat = activeCategoryFilter === 'all' || s.tierCode === activeCategoryFilter;"""

html_2 = html_2.replace(old_match_2, new_match_2)

# Update badge in Tier 2 list
old_badge_2 = '<span style="font-size: 0.62rem; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: #7c3aed15; color: #7c3aed;">SWARM &bull; L2</span>'
new_badge_2 = '''<span style="font-size: 0.62rem; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: ${s.tierCode === 'L2' ? '#7c3aed15' : (s.tierCode === 'L1' ? '#2563eb15' : '#05966915')}; color: ${s.tierCode === 'L2' ? '#7c3aed' : (s.tierCode === 'L1' ? '#2563eb' : '#059669')};">${s.tierCode === 'L2' ? 'SWARM &bull; L2' : (s.tierCode === 'L1' ? 'KERNEL &bull; L1' : 'AWS &bull; L0')}</span>'''
html_2 = html_2.replace(old_badge_2, new_badge_2)

# Fix lineage line in card
old_lineage_line = "<div style=\"font-size: 0.62rem; color: var(--text-muted); font-family: var(--font-mono);\">Lineage: ${s.kernelLineage.split('+')[0].trim()}</div>"
new_lineage_line = "<div style=\"font-size: 0.62rem; color: var(--text-muted); font-family: var(--font-mono);\">${s.kernelLineage ? 'Lineage: ' + s.kernelLineage.split('+')[0].trim() : (s.service || s.category || s.tier)}</div>"
html_2 = html_2.replace(old_lineage_line, new_lineage_line)

# Fix selectSwarmSkill header meta
old_meta_line = "document.getElementById('swarmSkillHeaderMeta').textContent = `Level 2 • ${skill.category} • Kernel: ${skill.kernelLineage} • AWS: ${skill.awsLineage}`;"
new_meta_line = "document.getElementById('swarmSkillHeaderMeta').textContent = `${skill.tier || 'Level 2'} • ${skill.ring} • ${skill.kernelLineage ? 'Kernel: ' + skill.kernelLineage : (skill.service || skill.category)}`;"
html_2 = html_2.replace(old_meta_line, new_meta_line)

old_badge_call = "document.getElementById('swarmSkillBadge').textContent = \"LEVEL 2\";"
new_badge_call = "document.getElementById('swarmSkillBadge').textContent = (skill.tier || 'LEVEL 2').toUpperCase();"
html_2 = html_2.replace(old_badge_call, new_badge_call)

with open('multi_agent_system_studio_app.html', 'w', encoding='utf-8') as f:
    f.write(html_2)
print("Updated multi_agent_system_studio_app.html with Tier 0, 1, and 2 skills (20 skills).")
