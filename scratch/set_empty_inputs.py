# -*- coding: utf-8 -*-
"""
Sets both inputs (custom document & web address) completely empty initially across:
1. truth_policy_flowchart_studio.html (App 8)
2. truth_langgraph_langsmith_studio.html (App 9)

Provides clean empty-state placeholders on Step 1 and Step 2 so that when the user opens
the application, it is completely fresh and ready for their custom document / URL input.
"""
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def set_inputs_empty(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Clear HTML input attribute values
    html = re.sub(
        r'<input type="text" id="customDocTitleInput"[^>]*>',
        '<input type="text" id="customDocTitleInput" class="custom-input-box" placeholder="Document Title (e.g. The Great Gatsby, SOP-402, etc.)" value="" />',
        html
    )

    html = re.sub(
        r'<input type="text" id="customWebAddressInput"[^>]*>',
        '<input type="text" id="customWebAddressInput" class="custom-input-box" style="margin-bottom: 0;" placeholder="Paste any excerpt link or portal URL (e.g. https://...)" value="" />',
        html
    )

    # 2. Clear initial JavaScript state
    old_state_pattern = r"state\s*=\s*\{[^}]*?customDoc:\s*\{[^}]*?text:\s*`.*?`"
    # Find start of state
    idx_state = html.find('state = {')
    idx_templates = html.find('const TEMPLATES =', idx_state)
    if idx_state != -1 and idx_templates != -1:
        new_state = """state = {
      activeStep: 1,
      inputViewMode: 'side_by_side',
      highlightDocInvariants: true,
      currentWebUrl: '',
      currentTemplateKey: null,
      customDoc: {
        title: '',
        text: ''
      },
      cascadeTiers: [],
      mermaidDag: ''
    };

    """
        html = html[:idx_state] + new_state + html[idx_templates:]
        print(f"[{filepath}] Updated initial state to empty.")
    else:
        print(f"[{filepath}] Could not locate state block.")

    # 3. Update renderStep1Inputs to handle empty state gracefully
    old_render_inputs = "renderStep1Inputs = function() {"
    idx_render = html.find(old_render_inputs)
    idx_render_end = html.find("renderCascadeTree = function()", idx_render)
    if idx_render != -1 and idx_render_end != -1:
        new_render_inputs = """renderStep1Inputs = function() {
      const container = document.getElementById('step1InputsContainer');
      if (!container) return;

      const hasDoc = state.customDoc.title || state.customDoc.text;
      const docHtml = hasDoc ? `
        <div class="doc-page">
          <div class="doc-header-banner">
            <div class="doc-logo-title">
              <span style="font-size: 26px;">📄</span>
              <div>
                <div class="doc-company">${escapeHtml(state.customDoc.title || 'Untitled Document')}</div>
                <div class="doc-subtitle">Active Ground Truth Ingestion</div>
              </div>
            </div>
            <div class="doc-stamp approved">AUDIT READY</div>
          </div>
          <div class="doc-body">
            <div class="doc-section">
              <div class="doc-section-heading">§ Ingested Content &amp; Invariants</div>
              <div style="font-size: 12px; line-height: 1.6; color: #334155; white-space: pre-wrap;">${highlightInvariantsInText(escapeHtml(state.customDoc.text))}</div>
            </div>
          </div>
        </div>
      ` : `
        <div style="height: 100%; min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 30px; text-align: center; color: #64748b;">
          <div style="font-size: 40px; margin-bottom: 12px;">📄</div>
          <div style="font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 6px;">Input 1 is Empty</div>
          <div style="font-size: 12px; max-width: 320px; line-height: 1.5;">Paste any text excerpt, SOP, or policy document into Input 1 on the left, or connect a web URL in Input 2.</div>
        </div>
      `;

      const hasUrl = Boolean(state.currentWebUrl);
      const webHtml = hasUrl ? `
        <div class="browser-frame" style="height: 100%;">
          <div class="browser-toolbar">
            <div class="browser-dots">
              <span class="dot dot-red"></span>
              <span class="dot dot-yellow"></span>
              <span class="dot dot-green"></span>
            </div>
            <div class="browser-url-bar">${escapeHtml(state.currentWebUrl)}</div>
          </div>
          <div class="browser-viewport" style="padding: 16px;">
            <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">Connected Target Endpoint</div>
            <div style="font-size: 11px; color: #0284c7; word-break: break-all; margin-bottom: 14px;">Target: ${escapeHtml(state.currentWebUrl)}</div>
            <div class="panel-card" style="background: #f0fdf4; border-color: #bbf7d0; padding: 12px;">
              <div style="font-size: 12px; font-weight: 700; color: #166534; margin-bottom: 4px;">✅ Observation Channel Ready</div>
              <div style="font-size: 11px; color: #15803d; line-height: 1.5;">Live telemetry channel open. System will verify all agent actions and invariants against this target interface.</div>
            </div>
          </div>
        </div>
      ` : `
        <div style="height: 100%; min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 30px; text-align: center; color: #64748b;">
          <div style="font-size: 40px; margin-bottom: 12px;">🌐</div>
          <div style="font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 6px;">Input 2 is Empty</div>
          <div style="font-size: 12px; max-width: 320px; line-height: 1.5;">Enter any web address or excerpt link in Input 2 and click Connect to crawl live content automatically.</div>
        </div>
      `;

      let contentHtml = '';
      if (state.inputViewMode === 'documents') {
        contentHtml = docHtml;
      } else if (state.inputViewMode === 'web_pages') {
        contentHtml = webHtml;
      } else {
        contentHtml = `
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; height: 100%;">
            <div style="overflow-y: auto;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; padding: 0 4px;">
                <span style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Input 1: Document</span>
                <span class="pill blue" style="font-size: 9px;">Text Ingest</span>
              </div>
              ${docHtml}
            </div>
            <div style="overflow-y: auto;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; padding: 0 4px;">
                <span style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Input 2: Web Address</span>
                <span class="pill purple" style="font-size: 9px;">Endpoint</span>
              </div>
              ${webHtml}
            </div>
          </div>
        `;
      }

      container.innerHTML = contentHtml;
    };

    """
        html = html[:idx_render] + new_render_inputs + html[idx_render_end:]
        print(f"[{filepath}] Updated renderStep1Inputs with empty states.")

    # 4. Update renderCascadeTree and renderMermaidDag empty states
    old_cascade = "renderCascadeTree = function() {"
    idx_cas = html.find(old_cascade)
    idx_cas_end = html.find("renderMermaidDag = function()", idx_cas)
    if idx_cas != -1 and idx_cas_end != -1:
        new_cascade = """renderCascadeTree = function() {
      const container = document.getElementById('cascadeTreeContainer');
      if (!container) return;

      if (!state.cascadeTiers || state.cascadeTiers.length === 0) {
        container.innerHTML = `
          <div style="height: 100%; min-height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 30px; text-align: center; color: #64748b;">
            <div style="font-size: 40px; margin-bottom: 12px;">📑</div>
            <div style="font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 6px;">No Invariants Extracted Yet</div>
            <div style="font-size: 12px; max-width: 320px; line-height: 1.5;">Provide a document or web address on Step 1, or click one of the quick starter templates below to compile the policy tree.</div>
          </div>
        `;
        return;
      }

      let htmlTiers = '';
      state.cascadeTiers.forEach((tier, index) => {
        let borderClass = 'tier-0';
        if (index === 1) borderClass = 'tier-1';
        if (index === 2) borderClass = 'tier-2';
        if (index === 3) borderClass = 'tier-3';
        if (index === 4) borderClass = 'tier-4';

        htmlTiers += `
          <div class="tier-card ${borderClass}">
            <div class="tier-header">
              <span class="tier-title">${escapeHtml(tier.tier)}</span>
              <span class="tier-badge ${tier.badge}">${escapeHtml(tier.desc)}</span>
            </div>
            <div class="tier-rules">
              ${tier.rules.map(rule => `<div class="tier-rule-item">${escapeHtml(rule)}</div>`).join('')}
            </div>
          </div>
        `;
      });

      container.innerHTML = htmlTiers;
    };

    """
        html = html[:idx_cas] + new_cascade + html[idx_cas_end:]
        print(f"[{filepath}] Updated renderCascadeTree with empty state.")

    # 5. Update renderMermaidDag empty state
    old_dag = "renderMermaidDag = function() {"
    idx_dag = html.find(old_dag)
    idx_dag_end = html.find("// ============================", idx_dag)
    if idx_dag != -1 and idx_dag_end != -1:
        new_dag = """renderMermaidDag = function() {
      const el = document.getElementById('mermaidGraphEl');
      if (!el) return;

      if (!state.mermaidDag) {
        el.innerHTML = `
          <div style="height: 100%; min-height: 480px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; padding: 30px; text-align: center; color: #64748b;">
            <div style="font-size: 40px; margin-bottom: 12px;">🔑</div>
            <div style="font-size: 14px; font-weight: 700; color: #334155; margin-bottom: 6px;">No Flowchart DAG Compiled Yet</div>
            <div style="font-size: 12px; max-width: 320px; line-height: 1.5;">Enter an excerpt link or custom text on Step 1, or click one of the quick starter templates to compile the topological decision graph.</div>
          </div>
        `;
        return;
      }

      el.removeAttribute('data-processed');
      el.innerHTML = state.mermaidDag;
      try {
        mermaid.init(undefined, el);
        const svg = el.querySelector('svg');
        if (svg) {
          svg.style.width = '100%';
          svg.style.height = '100%';
          svg.style.maxWidth = '100%';
          svg.style.minHeight = '520px';
        }
      } catch (err) {
        console.warn('Mermaid render error:', err);
      }
    };

    """
        html = html[:idx_dag] + new_dag + html[idx_dag_end:]
        print(f"[{filepath}] Updated renderMermaidDag with empty state.")

    # 6. Update DOMContentLoaded: do not auto-run synthesizeFromCustomInputs on initial load!
    html = html.replace(
        "synthesizeFromCustomInputs();\n    });",
        "renderStep1Inputs();\n      renderCascadeTree();\n      renderMermaidDag();\n    });"
    )
    html = html.replace(
        "synthesizeFromCustomInputs();\r\n    });",
        "renderStep1Inputs();\r\n      renderCascadeTree();\r\n      renderMermaidDag();\r\n    });"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[{filepath}] Successfully updated and saved!")

set_inputs_empty('truth_policy_flowchart_studio.html')
set_inputs_empty('truth_langgraph_langsmith_studio.html')
