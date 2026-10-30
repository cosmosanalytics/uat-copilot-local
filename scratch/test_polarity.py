# -*- coding: utf-8 -*-
"""
Intelligent Semantic Categorizer for Narrative & Story Dilemmas:
Distinguishes between:
1. Status Quo / Inertia / Stagnation: sentences about staying, crowding, remaining, enduring existing conditions.
   e.g. "Pa said there were too many people in Wisconsin now... Pa didn't want to stay."
        "Stay in Wisconsin: crowded settlements, disappearing wild animals."
2. Transformative Departure / Action Catalyst: sentences about leaving, traveling, journeying West.
   e.g. "They drove away and left it lonely and empty among the big trees... going to Indian country."
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

sample_ingalls = """The Ingalls family goes West. A long time ago, Pa and Ma and Mary and Laura and Baby Carrie left their little house in Wisconsin. They drove away and left it lonely and empty among the big trees, and they never saw that little house again. They were going to Indian country.
Pa said there were too many people in Wisconsin now. Wild animals did not stay in a country where there were so many people, so Pa didn't want to stay. He liked a country where the animals lived without fear. He liked to see them looking at him in the forest and eating fruit from the trees.
In the long winter evenings Pa talked to Ma about the Western country. "Let's go see the West," he said. "The land is flat and the grass grows thick and high. Animals run freely and there are no settlers. Only Indians live there."""

def analyze_narrative_polarity(text):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 15]

    stagnate_cands = []
    action_cands = []

    for s in sentences:
        l = s.toLowerCase() if hasattr(s, 'toLowerCase') else s.lower()
        # Signals of remaining, current condition, stagnation, or reluctance to stay
        if re.search(r'\b(stay|crowd|too many people|poverty|stagnat|endure|remain|settle|fear|old|lonely|empty|without|hard land)\b', l):
            stagnate_cands.append(s)
        # Signals of movement, journey, departure, adventure, quest
        if re.search(r'\b(drove away|left|go see|west|going|journey|travel|venture|quest|depart|leave|pack|wagon|frontier)\b', l):
            action_cands.append(s)

    print("Stagnation / Status Quo Candidates:")
    for s in stagnate_cands:
        print("  -", s)

    print("\nAction Catalyst / Departure Candidates:")
    for a in action_cands:
        print("  -", a)

analyze_narrative_polarity(sample_ingalls)
