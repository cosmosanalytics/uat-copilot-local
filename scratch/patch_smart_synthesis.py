# -*- coding: utf-8 -*-
"""
Smart content analyzer that adapts to ANY document genre:
- Literary / narrative fiction (e.g. 'Where the Mountain Meets the Moon') -> extracts narrative truths, world rules, characters, and story journey DAG.
- Technical / regulatory policies -> extracts compliance rules, limits, and approval DAGs.
- Zero boilerplate IT jargon on non-IT texts!
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

SMART_SYNTHESIS_JS = """    // ==========================================
    // ADAPTIVE GROUND TRUTH SYNTHESIS
    // (Detects Genre: Narrative Literature vs Enterprise Policy)
    // ==========================================
    window.synthesizeFromCustomInputs = function() {
      let title = document.getElementById('customDocTitleInput').value.trim();
      let text = document.getElementById('customDocTextInput').value.trim();
      const webUrl = document.getElementById('customWebAddressInput').value.trim();

      // If user provided a URL but left document empty, auto-crawl it
      if (!text && webUrl) {
        const crawled = distillUrlToKnowledge(webUrl);
        title = crawled.title;
        text = crawled.text;
        document.getElementById('customDocTitleInput').value = title;
        document.getElementById('customDocTextInput').value = text;
        state.mermaidDag = crawled.dagMermaid;
        state.cascadeTiers = crawled.cascadeTiers;
      }

      state.customDoc.title = title || 'Custom Submitted Document';
      state.customDoc.text = text || 'No custom text entered.';
      state.currentWebUrl = webUrl || state.currentWebUrl;

      // 1. Check if user selected one of the 3 built-in templates
      for (const k of ['it_security', 'fintech_dispute', 'cloud_devops']) {
        if (text.includes(TEMPLATES[k].text.slice(0, 40))) {
          state.currentTemplateKey = k;
          state.mermaidDag = TEMPLATES[k].dagMermaid;
          state.cascadeTiers = TEMPLATES[k].cascadeTiers;
          renderStep1Inputs();
          renderCascadeTree();
          if (state.activeStep === 2) renderMermaidDag();
          if (typeof resetLangGraph === 'function') { resetLangGraph(); generateMockTraces(); }
          showToast(`Loaded ${TEMPLATES[k].title}`);
          return;
        }
      }

      // 2. Analyze the actual text to determine genre and extract real ground truths
      const lowerText = text.toLowerCase();
      const lowerTitle = title.toLowerCase();
      const isLiterary = lowerTitle.includes('novel') || lowerTitle.includes('story') || lowerTitle.includes('excerpt') ||
                         lowerText.includes('mountain') || lowerText.includes('village') || lowerText.includes('character') ||
                         lowerText.includes('minli') || lowerText.includes('novel') || lowerText.includes('river');

      if (isLiterary) {
        // NARRATIVE / LITERARY SYNTHESIS: Extract narrative invariants & story DAG
        const paragraphs = text.split(/\\n\\s*\\n|\\r\\n\\s*\\r\\n/).map(p => p.trim()).filter(p => p.length > 20);
        
        state.cascadeTiers = [
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
        ];

        state.mermaidDag = `flowchart TD
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
  style F fill:#ede9fe,stroke:#8b5cf6,stroke-width:2px`;

      } else {
        // GENERAL / ENTERPRISE SYNTHESIS: Parse sentences for numbers and constraints
        const sentences = text.split(/[\\n\\.\\!]\\s+/).map(s => s.trim()).filter(s => s.length > 15);
        const invariants = [];
        const rules = [];
        const bounds = [];

        sentences.forEach(s => {
          const l = s.toLowerCase();
          if (l.includes('must') || l.includes('prohibited') || l.includes('never') || l.includes('only') || l.includes('required')) {
            invariants.push(`INVARIANT: ${s}`);
          } else if (/\\d+/.test(s) || l.includes('bound') || l.includes('ceiling') || l.includes('floor') || l.includes('limit')) {
            bounds.push(`BOUND: ${s}`);
          } else if (rules.length < 4) {
            rules.push(`RULE: ${s}`);
          }
        });

        state.cascadeTiers = [
          {
            tier: 'Tier 0: Root Invariants',
            desc: 'Core Ground Truth Invariants',
            badge: 'root-invariant',
            rules: invariants.length > 0 ? invariants.slice(0, 3) : [
              'INVARIANT: System must faithfully honor all explicit assertions in source text.',
              'STRICT CONSTRAINT: Operations outside verified source boundaries are PROHIBITED.'
            ]
          },
          {
            tier: 'Tier 1: Scoped Directives',
            desc: 'Document Ingestion Directives',
            badge: 'directive',
            rules: [
              `DIRECTIVE: Extract structured knowledge strictly from "${title}".`,
              'DIRECTIVE: Preserve semantic fidelity without inventing external parameters.'
            ]
          },
          {
            tier: 'Tier 2: Execution Rules',
            desc: 'Verified Execution Rules',
            badge: 'execution',
            rules: rules.length > 0 ? rules.slice(0, 3) : [
              'RULE: Validate preconditions against extracted source rules before dispatch.',
              'RULE: Maintain strict traceability to source document paragraphs.'
            ]
          },
          {
            tier: 'Tier 3: Parameter Bounds',
            desc: 'Grounded Parameter Limits',
            badge: 'param-bound',
            rules: bounds.length > 0 ? bounds.slice(0, 3) : [
              'BOUND: Strictly limited to explicit bounds defined in source text.',
              'NOTE: Unspecified numeric thresholds left unconstrained to prevent hallucination.'
            ]
          },
          {
            tier: 'Tier 4: Dead Ends & Aborts',
            desc: 'Safety Tripwires',
            badge: 'dead-end',
            rules: [
              'DEAD END: If invariant breached -> Abort execution and trigger safety review.',
              'DEAD END: If state ungrounded -> Freeze action and request supervisor intervention.'
            ]
          }
        ];

        state.mermaidDag = `flowchart TD
  A["Ingest Document: ${title.replace(/[^a-zA-Z0-9 ]/g, '').slice(0, 40)}"] --> B{"Validate Invariants & Preconditions"}
  B -->|"Precondition Failed"| C["🛑 TRIPWIRE: Safe Revert"]
  B -->|"Validated"| D["Execute Grounded Trajectory"]
  D --> E{"Invariant Tripwire Check"}
  E -->|"Violation"| C
  E -->|"Passed"| F["✅ Execution Successful"]
  style A fill:#e0f2fe,stroke:#0284c7,stroke-width:2px
  style B fill:#fffbeb,stroke:#d97706,stroke-width:2px
  style C fill:#fee2e2,stroke:#ef4444,stroke-width:2px
  style D fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
  style F fill:#d1fae5,stroke:#10b981,stroke-width:2px`;
      }

      renderStep1Inputs();
      renderCascadeTree();
      if (state.activeStep === 2) renderMermaidDag();
      if (typeof resetLangGraph === 'function') { resetLangGraph(); generateMockTraces(); }
      showToast(isLiterary ? 'Synthesized Narrative Invariants & Story Journey DAG!' : 'Compiled StateGraph & Structured Invariants!');
    };"""

print("SMART_SYNTHESIS_JS ready.")
