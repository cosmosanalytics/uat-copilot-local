# -*- coding: utf-8 -*-
"""
Updates cleanNode / formatNode in truth_policy_flowchart_studio.html and
truth_langgraph_langsmith_studio.html so that ALL contents in every block
of the flowchart are shown in full, wrapped with <br/>, without any '...' truncation!
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

def update_node_formatting(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()

    # Define formatFullNode function: preserves full text, escapes quotes, wraps lines with <br/>
    format_helper = """
        // Formats the full content of any block with word-wrapping, never truncating with '...'
        const formatFullNode = (header, content, wordsPerLine = 6) => {
          const raw = (content || header || '').replace(/["\\\`]/g, "'").replace(/<[^>]*>/g, '').trim();
          if (!raw) return `<b>${header}</b>`;
          const words = raw.split(/\\s+/);
          const lines = [];
          for (let i = 0; i < words.length; i += wordsPerLine) {
            lines.push(words.slice(i, i + wordsPerLine).join(' '));
          }
          const body = lines.join('<br/>');
          return header ? `<b>${header}</b><br/><small>${body}</small>` : body;
        };
"""

    # 1. Replace the narrative cleanNode block
    old_narrative_block = """        const cleanNode = (t, maxLen=42) => {
          if (!t) return 'Node';
          const c = t.replace(/["'\\\\]/g, '').replace(/<[^>]*>/g, '').trim();
          return c.length > maxLen ? c.slice(0, maxLen) + '...' : c;
        };

        const nSetting = cleanNode(settingPoints[0] || title || 'Setting Invariant');
        const nProtagonist = cleanNode(characterTraits[0] || 'Protagonist Axiom');
        const nDilemma = cleanNode(conflicts[0] || 'Core Narrative Dilemma');
        const nStagnate = cleanNode(negations[0] || 'Passive Resignation');
        const nAction = cleanNode(characterTraits[1] || 'Active Pursuits');
        const nResolution = cleanNode(tripwire2 || 'Transformative Journey');

        dagMermaid = `flowchart TD
  A["Setting: ${nSetting}"] --> B["Protagonist: ${nProtagonist}"]
  B --> C{"Dilemma: ${nDilemma}"}
  C -->|"Resignation / Compromise"| D["🛑 Stagnation: ${nStagnate}"]
  C -->|"Follow Invariant Drive"| E["✨ Action Catalyst: ${nAction}"]
  E --> F["Resolution: ${nResolution}"]"""

    new_narrative_block = format_helper + """
        const nSetting = formatFullNode('Setting', settingPoints[0] || title || 'Setting Invariant', 7);
        const nProtagonist = formatFullNode('Protagonist', characterTraits[0] || 'Protagonist Axiom', 7);
        const nDilemma = formatFullNode('Core Dilemma', conflicts[0] || 'Core Narrative Conflict', 5);
        const nStagnate = formatFullNode('🛑 Stagnation', negations[0] || 'Passive Resignation', 6);
        const nAction = formatFullNode('✨ Action Catalyst', characterTraits[1] || 'Active Pursuits', 6);
        const nResolution = formatFullNode('Resolution', tripwire2 || 'Transformative Journey', 6);

        dagMermaid = `flowchart TD
  A["${nSetting}"] --> B["${nProtagonist}"]
  B --> C{"${nDilemma}"}
  C -->|"Resignation / Compromise"| D["${nStagnate}"]
  C -->|"Follow Invariant Drive"| E["${nAction}"]
  E --> F["${nResolution}"]"""

    if old_narrative_block in html:
        html = html.replace(old_narrative_block, new_narrative_block)
        print(f"[{fname}] Replaced narrative cleanNode with formatFullNode.")
    else:
        print(f"[{fname}] Could not find old narrative cleanNode block.")

    # 2. Replace the technical cleanNode block
    old_tech_block = """        const cleanNode = (t, maxLen=38) => {
          if (!t) return 'Gate';
          const c = t.replace(/["'\\\\]/g, '').replace(/<[^>]*>/g, '').trim();
          return c.length > maxLen ? c.slice(0, maxLen) + '...' : c;
        };

        const nIngest = cleanNode(title || 'Source Ingest');
        const nGate = cleanNode(rule1);
        const nRevert = cleanNode(trip1);
        const nExec = cleanNode(dir2);
        const nDone = cleanNode(bound1);

        dagMermaid = `flowchart TD
  A["Ingest: ${nIngest}"] --> B{"Verify Precondition:<br/>${nGate}"}
  B -->|"Violation or Infeasible"| C["🛑 TRIPWIRE: Safe Reversion<br/>(${nRevert})"]
  B -->|"Grounded"| D["Execute Action:<br/>${nExec}"]
  D --> E{"Invariant Check"}
  E -->|"Breach"| C
  E -->|"Passed"| F["✅ Execution Verified<br/>(${nDone})"]"""

    new_tech_block = """        const nIngest = formatFullNode('Ingest', title || 'Source Ingest', 7);
        const nGate = formatFullNode('Verify Precondition', rule1, 6);
        const nRevert = formatFullNode('🛑 TRIPWIRE: Safe Reversion', trip1, 6);
        const nExec = formatFullNode('Execute Action', dir2, 6);
        const nDone = formatFullNode('✅ Execution Verified', bound1, 6);

        dagMermaid = `flowchart TD
  A["${nIngest}"] --> B{"${nGate}"}
  B -->|"Violation or Infeasible"| C["${nRevert}"]
  B -->|"Grounded"| D["${nExec}"]
  D --> E{"Invariant Check"}
  E -->|"Breach"| C
  E -->|"Passed"| F["${nDone}"]"""

    if old_tech_block in html:
        html = html.replace(old_tech_block, new_tech_block)
        print(f"[{fname}] Replaced technical cleanNode with formatFullNode.")
    else:
        print(f"[{fname}] Could not find old technical cleanNode block.")

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[{fname}] Saved successfully!")

update_node_formatting('truth_policy_flowchart_studio.html')
update_node_formatting('truth_langgraph_langsmith_studio.html')
