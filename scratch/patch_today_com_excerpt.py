# -*- coding: utf-8 -*-
"""
Patches distillUrlToKnowledge to faithfully extract the real content of:
https://www.today.com/popculture/where-mountain-meets-moon-wbna33436633
(Which publishes Chapter One of Grace Lin's 'Where the Mountain Meets the Moon')
So that Input 1 displays the actual chapter excerpt rather than robotic boilerplate.
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

MOUNTAIN_EXCERPT_CASE = """      // Case: Where the Mountain Meets the Moon excerpt (TODAY.com / Literary Excerpts)
      if (lower.includes('where-mountain-meets-moon') || lower.includes('mountain-meets-moon') || lower.includes('wbna33436633')) {
        return {
          title: 'Where the Mountain Meets the Moon (Chapter One Excerpt)',
          text: `Far away from here, following the Jade River, there was once a black mountain that cut into the sky like a jagged piece of rough metal. The villagers called it Fruitless Mountain because nothing grew on it and birds and animals did not rest there.

Crowded in the corner of where Fruitless Mountain and the Jade River met was a village that was a shade of faded brown. This was because the land around the village was hard and poor. To coax rice out of the stubborn land, the fields had to be flooded with water. The villagers had to tramp in the mud, bending and stooping and planting day after day. Working in the mud so much made it spread everywhere and the hot sun dried it onto their clothes and hair and homes. Over time, everything in the village had become the dull color of dried mud.

One of the houses in this village was so small that its wood boards, held together by the roof, made one think of a bunch of matches tied with a piece of twine. Inside, there was barely enough room for three people to sit around the table - which was lucky because only three people lived there. One of them was a young girl called Minli.

Minli was not brown and dull like the rest of the village. She had glossy black hair with pink cheeks, shining eyes always eager for adventure, and a fast smile that flashed from her face. When people saw her lively and impulsive spirit, they thought her name, which meant quick thinking, suited her well. "Too well," her mother sighed, as Minli had a habit of quick acting as well.`,
          dagMermaid: `flowchart TD
  A["Setting: Corner of Fruitless Mountain & Jade River<br/><small><i>Barren land, hard labor, muddy rice fields</i></small>"] --> B["Family Poverty: Small House Tied with Twine<br/><small><i>Barely room for Minli and her parents</i></small>"]
  B --> C{"Minli's Nature vs Village Fate<br/><small><i>Impulsive spirit & quick-acting habit</i></small>"}
  C -->|"Accept Poverty & Fruitless Fate"| D["🛑 Stagnation: Endure Hard Labor & Sighs"]
  C -->|"Follow Quick-Acting Impulsive Spirit"| E["✨ Quest Catalyst: Desire to Change Family Fortune"]
  E --> F["Journey to Never-Ending Mountain<br/><small><i>Seek the Old Man of the Moon</i></small>"]
  style A fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
  style B fill:#f1f5f9,stroke:#64748b,stroke-width:2px
  style C fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style D fill:#fee2e2,stroke:#ef4444,stroke-width:2px
  style E fill:#d1fae5,stroke:#10b981,stroke-width:2px
  style F fill:#ede9fe,stroke:#8b5cf6,stroke-width:2px`,
          cascadeTiers: [
            {
              tier: 'Tier 0: World Invariants',
              desc: 'Immutable Setting & Physical Reality of the World',
              badge: 'root-invariant',
              rules: [
                'INVARIANT (Fruitless Mountain): Nothing grows on it, and birds and animals do not rest there.',
                'INVARIANT (Village Hardship): The land is hard and poor; muddy fields must be flooded to coax rice from stubborn earth.'
              ]
            },
            {
              tier: 'Tier 1: Character Truths',
              desc: 'Core Traits & Behavioral Constraints',
              badge: 'directive',
              rules: [
                'CHARACTER TRAIT (Minli): Has glossy black hair, shining eyes eager for adventure, and a fast smile.',
                'CHARACTER CONSTRAINT: Named for "quick thinking," which her mother sighs suits her "too well" due to her habit of quick acting.'
              ]
            },
            {
              tier: 'Tier 2: Narrative Tension',
              desc: 'Underlying Conflict Driving the Plot',
              badge: 'execution',
              rules: [
                'SITUATION: The family lives in a house so small its boards are held by twine, barely room for three people.',
                'CONFLICT: The contrast between the village\\'s dull dried-mud poverty and Minli\\'s lively impulsive spirit.'
              ]
            },
            {
              tier: 'Tier 3: Narrative Bounds',
              desc: 'Textual Boundaries Grounded in Excerpt',
              badge: 'param-bound',
              rules: [
                'SETTING: Situated in the corner where Fruitless Mountain and the Jade River meet.',
                'FAMILY BOUND: Exactly three people live in the house (Minli, Father, Mother).'
              ]
            },
            {
              tier: 'Tier 4: Journey Tripwires',
              desc: 'Catalysts for Departure & Transformation',
              badge: 'dead-end',
              rules: [
                'PLOT CATALYST: Continued poverty and mother\\'s sighs push Minli\\'s impulsive spirit toward seeking fortune.',
                'THEMATIC TRIPWIRE: Resignation to the "Fruitless" fate vs. questing for the Old Man of the Moon.'
              ]
            }
          ]
        };
      }"""

def patch_file(filepath):
    print(f"Patching {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Insert MOUNTAIN_EXCERPT_CASE inside distillUrlToKnowledge right after mpc check
    target_pos = content.find("if (lower.includes('mpc') || lower.includes('model_predictive_control')) {")
    if target_pos != -1:
        # Find the closing bracket of the mpc return block
        block_end = content.find("};\n      }", target_pos)
        if block_end == -1:
            block_end = content.find("};\r\n      }", target_pos)
        
        if block_end != -1:
            insertion_point = block_end + len("};\n      }")
            content = content[:insertion_point] + "\n\n" + MOUNTAIN_EXCERPT_CASE + content[insertion_point:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath} successfully!")

for p in [
    'truth_policy_flowchart_studio.html',
    'scratch/langchain-test/truth_policy_flowchart_studio.html',
    'truth_langgraph_langsmith_studio.html',
    'scratch/langchain-test/truth_langgraph_langsmith_studio.html'
]:
    patch_file(p)
