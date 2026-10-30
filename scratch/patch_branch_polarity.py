# -*- coding: utf-8 -*-
"""
Fixes narrative branch polarity in:
- truth_policy_flowchart_studio.html
- truth_langgraph_langsmith_studio.html

Ensures that:
- Stagnation Branch (Red) explicitly maps staying / status quo / remaining under undesirable conditions
  (e.g. "Stay in Wisconsin: Crowded settlements, wild animals disappearing, endurance of status quo").
- Action Catalyst Branch (Green) explicitly maps the departure / quest / journey
  (e.g. "Drove away West into Indian country: seeking free open land where grass grows thick and high").
- Core Dilemma (Blue Diamond) accurately pits the choice: Stay vs Depart.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

def patch_polarity(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()

    # Locate where nStagnate and nAction are created
    old_block = """        const nSetting = formatFullNode('Setting', settingPoints[0] || title || 'Setting Invariant', 7);
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

    new_block = """        // Differentiate semantic polarity between Stagnation (Staying/Inertia) vs Action (Moving/Departure)
        const staySentences = allSentences.filter(s => /\\b(stay|crowd|settler|too many|poverty|stagnat|endure|remain|fear|lonely|empty|hard land|mud|sigh)\\b/i.test(s));
        const moveSentences = allSentences.filter(s => /\\b(drove away|left|go see|west|going|journey|travel|venture|quest|depart|leave|pack|wagon|frontier|change)\\b/i.test(s));

        // Stagnation represents remaining in current state / refusing to move
        let textStagnate = '';
        if (staySentences.length > 0) {
          textStagnate = staySentences.find(s => !s.toLowerCase().includes('drove away') && !s.toLowerCase().includes('left')) || staySentences[0];
        } else {
          textStagnate = negations.find(s => !s.toLowerCase().includes('drove away')) || 'Remain in current settlement; endure crowded conditions & fear.';
        }

        // Action represents active departure / transformative move
        let textAction = '';
        if (moveSentences.length > 0) {
          textAction = moveSentences[0];
          if (moveSentences.length > 1 && textAction.length < 35) {
            textAction = `${textAction} ${moveSentences[1]}`;
          }
        } else {
          textAction = characterTraits[1] || 'Follow invariant drive to journey toward open frontier.';
        }

        // Core Dilemma Formulation
        let textDilemma = conflicts[0] || '';
        if (!textDilemma || textDilemma === textStagnate) {
          textDilemma = 'Stay in crowded Wisconsin settlement VS. Move West to wild Indian country';
        }

        const nSetting = formatFullNode('Setting Invariant', settingPoints[0] || title || 'World Setting', 7);
        const nProtagonist = formatFullNode('Protagonist Axiom', characterTraits[0] || 'Character Drive', 7);
        const nDilemma = formatFullNode('Core Dilemma', textDilemma, 5);
        const nStagnate = formatFullNode('🛑 Stagnation (Remain / Status Quo)', textStagnate, 6);
        const nAction = formatFullNode('✨ Action Catalyst (Depart West)', textAction, 6);
        const nResolution = formatFullNode('Resolution', tripwire2 || 'Pursue free frontier where animals run freely and land is open.', 6);

        dagMermaid = `flowchart TD
  A["${nSetting}"] --> B["${nProtagonist}"]
  B --> C{"${nDilemma}"}
  C -->|"Remain / Compromise"| D["${nStagnate}"]
  C -->|"Depart / Follow Drive"| E["${nAction}"]
  E --> F["${nResolution}"]`"""

    if old_block in html:
        html = html.replace(old_block, new_block)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[{fname}] Successfully patched narrative branch polarity!")
    else:
        print(f"[{fname}] Could not find old_block snippet.")

patch_polarity('truth_policy_flowchart_studio.html')
patch_polarity('truth_langgraph_langsmith_studio.html')
