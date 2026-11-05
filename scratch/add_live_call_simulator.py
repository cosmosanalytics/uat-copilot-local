# -*- coding: utf-8 -*-
"""
add_live_call_simulator.py
Adds the 5th tab: "5. 📞 Real-Time Live Call" with:
- Live inbound call simulator
- Sample question triggers
- Dual-graph grounding (SOP KG + Call Records CG)
- Business Graph (BG) reconciliation and policy drift feedback loop
- Speech synthesis and waveform animation
"""

import sys

def main():
    with open('callcenter_ai_voice_agents.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update navigation tab
    nav_old = '''      <button onclick="switchTab('bg')" id="tab-bg" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-chart-line"></i>
        <span>4. Business Goals &amp; ROI Graph</span>
      </button>'''

    nav_new = '''      <button onclick="switchTab('bg')" id="tab-bg" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-chart-line"></i>
        <span>4. Business Goals &amp; ROI Graph</span>
      </button>
      <button onclick="switchTab('call')" id="tab-call" class="tab-btn px-3 py-1.5 rounded-lg font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition flex items-center space-x-1.5">
        <i class="fa-solid fa-phone-arrow-down-left text-emerald-500"></i>
        <span>5. 📞 Real-Time Live Call</span>
      </button>'''

    if nav_old not in html:
        print("ERROR: nav_old not found!")
        return
    html = html.replace(nav_old, nav_new, 1)

    # 2. Insert view-call right after view-bg
    view_bg_marker = '''        <div class="flex-1 relative bg-slate-950" id="bg-canvas-container">
          <div id="bg-network" class="w-full h-full"></div>
          <div class="absolute bottom-3 left-3 bg-slate-900/90 border border-slate-800 rounded-lg p-2.5 text-[11px] text-white shadow pointer-events-none">
            <div class="font-bold text-slate-400 uppercase text-[9px] mb-1">BG Legend</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span><span>Strategic Enterprise Goal</span></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span>Operational KPI Outcome</span></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span>Financial Dollar Value</span></div>
          </div>
        </div>
      </div>'''

    view_call_html = '''        <div class="flex-1 relative bg-slate-950" id="bg-canvas-container">
          <div id="bg-network" class="w-full h-full"></div>
          <div class="absolute bottom-3 left-3 bg-slate-900/90 border border-slate-800 rounded-lg p-2.5 text-[11px] text-white shadow pointer-events-none">
            <div class="font-bold text-slate-400 uppercase text-[9px] mb-1">BG Legend</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span><span>Strategic Enterprise Goal</span></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span><span>Operational KPI Outcome</span></div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span><span>Financial Dollar Value</span></div>
          </div>
        </div>
      </div>

      <!-- ================================================================= -->
      <!-- VIEW 5: REAL-TIME LIVE CALL SIMULATOR (GROUNDED IN KG & CG)       -->
      <!-- ================================================================= -->
      <div id="view-call" class="view-panel flex-1 flex flex-col hidden overflow-y-auto p-4 sm:p-6 space-y-4">
        
        <!-- LIVE CALL CONTROL BAR -->
        <div class="bg-gradient-to-r from-slate-900 via-slate-850 to-slate-900 border border-slate-700/80 rounded-2xl p-4 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="flex items-center space-x-3.5">
            <div class="relative">
              <div class="w-11 h-11 rounded-2xl bg-emerald-500/20 border border-emerald-500/50 flex items-center justify-center text-emerald-400 text-lg shadow-inner">
                <i class="fa-solid fa-headset animate-pulse"></i>
              </div>
              <span class="absolute -top-1 -right-1 flex h-3.5 w-3.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-emerald-500"></span>
              </span>
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <span class="text-xs font-black uppercase tracking-wider text-emerald-400">Live Voice Agent Active</span>
                <span class="text-slate-500">•</span>
                <span id="call-timer" class="font-mono text-xs text-slate-300 font-bold">Call Duration: 00:18</span>
              </div>
              <div class="text-sm font-bold text-white flex items-center space-x-2 mt-0.5">
                <span id="caller-id-display">Caller: Sarah Jenkins (Acct #48291 • LTV $2,400)</span>
                <span id="caller-tier-badge" class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">VIP Tier</span>
              </div>
            </div>
          </div>

          <!-- Audio Waveform & Speech Toggle Controls -->
          <div class="flex items-center space-x-3 w-full md:w-auto justify-between md:justify-end">
            <!-- Animated Audio Waveform -->
            <div id="audio-wave-container" class="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700">
              <span class="text-[10px] font-mono text-slate-400 mr-1.5 uppercase tracking-wider">Audio:</span>
              <div id="wave-1" class="waveform-bar w-1 h-3 bg-emerald-400 rounded-full transition-all duration-150"></div>
              <div id="wave-2" class="waveform-bar w-1 h-5 bg-emerald-400 rounded-full transition-all duration-150"></div>
              <div id="wave-3" class="waveform-bar w-1 h-2 bg-emerald-400 rounded-full transition-all duration-150"></div>
              <div id="wave-4" class="waveform-bar w-1 h-6 bg-emerald-400 rounded-full transition-all duration-150"></div>
              <div id="wave-5" class="waveform-bar w-1 h-3 bg-emerald-400 rounded-full transition-all duration-150"></div>
            </div>

            <!-- Speech Synthesis Toggle -->
            <button id="btn-toggle-speech" onclick="toggleVoiceSpeech()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-600 transition flex items-center space-x-1.5">
              <i id="voice-icon" class="fa-solid fa-volume-high text-emerald-400"></i>
              <span id="voice-toggle-text">Speech: ON</span>
            </button>

            <!-- Reset Call Button -->
            <button onclick="resetLiveCall()" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition flex items-center space-x-1.5">
              <i class="fa-solid fa-arrows-rotate"></i>
              <span>New Call</span>
            </button>
          </div>
        </div>

        <!-- SAMPLE QUESTIONS PICKER (ASKED BY SAMPLE QUESTIONS) -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-xs">
          <div class="flex items-center justify-between mb-2.5">
            <div class="flex items-center space-x-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h3 class="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                Simulate Inbound Customer Call &bull; Click Sample Question or Ask Custom
              </h3>
            </div>
            <span class="text-[11px] text-slate-400">Grounds real-time Agent reasoning directly in SOP KG &amp; Call Records CG</span>
          </div>

          <!-- Quick Question Pills -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-2.5 mb-3">
            <button onclick="simulateSampleCall('billing')" id="sample-btn-billing" class="text-left p-3 rounded-xl border border-amber-300 dark:border-amber-800 bg-amber-50/70 dark:bg-amber-950/30 hover:bg-amber-100/70 transition group shadow-2xs">
              <div class="flex items-center justify-between mb-1">
                <span class="text-[11px] font-bold text-amber-800 dark:text-amber-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-file-invoice-dollar"></i>
                  <span>1. Billing Dispute &amp; Fee Waiver</span>
                </span>
                <span class="text-[9px] uppercase font-mono px-1.5 py-0.5 rounded bg-amber-200/80 dark:bg-amber-900 text-amber-900 dark:text-amber-200 font-bold">SOP-04</span>
              </div>
              <p class="text-xs text-slate-700 dark:text-slate-300 font-medium group-hover:text-slate-900 dark:group-hover:text-white">
                &ldquo;I was charged a $150 international roaming fee on my last bill that I didn't authorize. Can you waive it?&rdquo;
              </p>
            </button>

            <button onclick="simulateSampleCall('outage')" id="sample-btn-outage" class="text-left p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-sky-300 dark:hover:border-sky-700 hover:bg-sky-50/50 dark:hover:bg-sky-950/20 transition group shadow-2xs">
              <div class="flex items-center justify-between mb-1">
                <span class="text-[11px] font-bold text-sky-800 dark:text-sky-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-wifi"></i>
                  <span>2. Broadband Hardware Outage</span>
                </span>
                <span class="text-[9px] uppercase font-mono px-1.5 py-0.5 rounded bg-sky-200/60 dark:bg-sky-900 text-sky-900 dark:text-sky-200 font-bold">SOP-12</span>
              </div>
              <p class="text-xs text-slate-700 dark:text-slate-300 font-medium group-hover:text-slate-900 dark:group-hover:text-white">
                &ldquo;My fiber router has had a blinking red optical light for 2 hours and my team is offline. Can you dispatch a tech today?&rdquo;
              </p>
            </button>

            <button onclick="simulateSampleCall('retention')" id="sample-btn-retention" class="text-left p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-emerald-300 dark:hover:border-emerald-700 hover:bg-emerald-50/50 dark:hover:bg-emerald-950/20 transition group shadow-2xs">
              <div class="flex items-center justify-between mb-1">
                <span class="text-[11px] font-bold text-emerald-800 dark:text-emerald-300 flex items-center space-x-1.5">
                  <i class="fa-solid fa-handshake"></i>
                  <span>3. Enterprise Churn &amp; Renewal</span>
                </span>
                <span class="text-[9px] uppercase font-mono px-1.5 py-0.5 rounded bg-emerald-200/60 dark:bg-emerald-900 text-emerald-900 dark:text-emerald-200 font-bold">SOP-28</span>
              </div>
              <p class="text-xs text-slate-700 dark:text-slate-300 font-medium group-hover:text-slate-900 dark:group-hover:text-white">
                &ldquo;We have been a loyal client for 8 years, but our renewal rate jumped 25%. I want to cancel our $18,000/yr enterprise account today.&rdquo;
              </p>
            </button>
          </div>

          <!-- Custom Input Row -->
          <div class="flex items-center space-x-2">
            <div class="relative flex-1">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <i class="fa-solid fa-microphone text-xs"></i>
              </div>
              <input type="text" id="custom-caller-input" placeholder="Or type a custom caller question/request (e.g. 'Can I get a credit for yesterday\'s internet disruption?')" class="w-full pl-9 pr-3 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 font-medium">
            </div>
            <button onclick="askCustomCallerQuestion()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition shadow-xs flex items-center space-x-1.5 shrink-0">
              <i class="fa-solid fa-phone"></i>
              <span>Simulate Caller</span>
            </button>
          </div>
        </div>

        <!-- MAIN REAL-TIME CALL CONSOLE (2 COLUMNS) -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 flex-1">

          <!-- LEFT COLUMN: LIVE CONVERSATION STREAM & AGENT VOICE OUTPUT -->
          <div class="lg:col-span-6 flex flex-col space-y-3.5">
            <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-xs flex-1 flex flex-col">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800 shrink-0">
                <div class="flex items-center space-x-2">
                  <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
                  <span class="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">Live Call Audio Transcript</span>
                </div>
                <span class="text-[10px] font-mono text-slate-400">Real-Time Inbound Voice Stream</span>
              </div>

              <!-- Conversation Bubbles Container -->
              <div id="call-transcript-container" class="flex-1 overflow-y-auto py-3.5 space-y-3.5 min-h-[320px]">
                <!-- Initial Caller Question Bubble -->
                <div class="flex items-start space-x-3">
                  <div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-slate-700 dark:text-slate-300 shrink-0 text-xs font-bold">
                    <i class="fa-solid fa-user"></i>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-1">
                      <span class="text-xs font-bold text-slate-900 dark:text-white" id="caller-name-tag">Sarah Jenkins</span>
                      <span class="text-[10px] text-slate-400 font-mono">10:42:15 AM</span>
                      <span id="caller-intent-tag" class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300">Dispute</span>
                    </div>
                    <div class="p-3 rounded-2xl rounded-tl-xs bg-slate-100 dark:bg-slate-800 text-xs text-slate-800 dark:text-slate-200 leading-relaxed font-medium" id="caller-speech-text">
                      &ldquo;I was charged a $150 international roaming fee on my last bill that I didn't authorize. Can you waive it?&rdquo;
                    </div>
                  </div>
                </div>

                <!-- Agent Reasoning Pill -->
                <div id="agent-thinking-hud" class="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 text-[11px] text-indigo-700 dark:text-indigo-300 font-medium">
                  <i class="fa-solid fa-brain fa-spin text-indigo-500"></i>
                  <span id="thinking-status-text">Knowledge Graph (SOP-04) &amp; Context Graph (Sarah Jenkins LTV $2.4k) reconciled</span>
                </div>

                <!-- AI Voice Agent Spoken Response Bubble -->
                <div class="flex items-start space-x-3">
                  <div class="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center shrink-0 text-xs font-bold shadow-xs">
                    <i class="fa-solid fa-headset"></i>
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center justify-between mb-1">
                      <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400">AI Voice Agent (Grounded)</span>
                        <span class="text-[10px] text-slate-400 font-mono">10:42:16 AM</span>
                        <span id="agent-sop-tag" class="px-1.5 py-0.2 rounded text-[9px] font-bold bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300">Verified SOP-04</span>
                      </div>
                      <button onclick="speakCurrentResponse()" class="text-[11px] text-emerald-600 dark:text-emerald-400 hover:underline flex items-center space-x-1 font-bold">
                        <i class="fa-solid fa-volume-high"></i>
                        <span>Replay Audio</span>
                      </button>
                    </div>
                    <div class="p-3.5 rounded-2xl rounded-tl-xs bg-emerald-50/70 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/80 text-xs text-slate-800 dark:text-slate-100 leading-relaxed font-medium shadow-xs" id="agent-response-text">
                      &ldquo;Hello Sarah, I completely understand your concern regarding the $150 roaming fee. Because you have been a valued customer with us for 6 years and maintain an exceptional account standing, I am applying our VIP Hardship Exception under SOP-04 Section 4.2 to waive the full $150 right now. Your balance has been adjusted to $0, and no supervisor transfer is required.&rdquo;
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: DUAL GRAPH GROUNDING HUD (KG + CG -> BG) -->
          <div class="lg:col-span-6 flex flex-col space-y-3.5">

            <!-- HUD CARD 1: GROUNDED IN SOP KNOWLEDGE GRAPH (WHAT SHOULD HAPPEN) -->
            <div class="bg-white dark:bg-slate-900 border-2 border-indigo-200 dark:border-indigo-900/60 rounded-2xl p-4 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 right-0 px-2.5 py-0.5 rounded-bl-lg bg-indigo-600 text-white font-mono text-[9px] font-bold uppercase tracking-wider">
                Knowledge Graph (KG)
              </div>
              <div class="flex items-center space-x-2 mb-2">
                <i class="fa-solid fa-book-bookmark text-indigo-500"></i>
                <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-tight">
                  1. Grounded in SOP Rulebook (What SHOULD Happen)
                </h4>
              </div>
              <div class="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
                <div class="p-2 rounded-lg bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/40">
                  <div class="font-bold text-indigo-900 dark:text-indigo-300 text-[11px]" id="hud-kg-sop-name">SOP-04: Inbound Billing &amp; Roaming Disputes</div>
                  <div class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5" id="hud-kg-rule1">
                    &bull; <strong>Standard Rule:</strong> Tier-1 Agent max waiver limit is $50.
                  </div>
                  <div class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5" id="hud-kg-rule2">
                    &bull; <strong>Section 4.2 Exception:</strong> Hardship/VIP accounts (LTV &gt; $2k, &gt; 3 yrs tenure) allow up to $250 credit with automated authorization.
                  </div>
                </div>
                <div class="flex items-center justify-between pt-1">
                  <span class="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center space-x-1" id="hud-kg-decision-badge">
                    <i class="fa-solid fa-circle-check"></i>
                    <span>SOP Match: Clause 4.2 Approved ($150 &le; $250)</span>
                  </span>
                  <button onclick="inspectInGraph('kg')" class="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 hover:underline">
                    View in SOP Graph &rarr;
                  </button>
                </div>
              </div>
            </div>

            <!-- HUD CARD 2: GROUNDED IN CALL RECORDS CONTEXT GRAPH (WHAT ACTUALLY HAPPENED) -->
            <div class="bg-white dark:bg-slate-900 border-2 border-amber-200 dark:border-amber-900/60 rounded-2xl p-4 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 right-0 px-2.5 py-0.5 rounded-bl-lg bg-amber-500 text-white font-mono text-[9px] font-bold uppercase tracking-wider">
                Context Graph (CG)
              </div>
              <div class="flex items-center space-x-2 mb-2">
                <i class="fa-solid fa-address-card text-amber-500"></i>
                <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-tight">
                  2. Grounded in Call Records &amp; State (What ACTUALLY Happened)
                </h4>
              </div>
              <div class="space-y-1.5 text-xs text-slate-700 dark:text-slate-300">
                <div class="p-2 rounded-lg bg-amber-50/50 dark:bg-amber-950/20 border border-amber-100 dark:border-amber-900/40">
                  <div class="font-bold text-amber-900 dark:text-amber-300 text-[11px]" id="hud-cg-caller-name">Customer Context: Sarah Jenkins (Acct #48291)</div>
                  <div class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5" id="hud-cg-metrics">
                    &bull; <strong>Tenure &amp; Value:</strong> 6.2 years &bull; Lifetime Value: $2,400 &bull; Plan: Unlimited International
                  </div>
                  <div class="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5" id="hud-cg-history">
                    &bull; <strong>Historical Diary:</strong> 0 billing disputes in past 24 months. Churn probability if denied: 82%.
                  </div>
                </div>
                <div class="flex items-center justify-between pt-1">
                  <span class="text-[11px] font-bold text-amber-700 dark:text-amber-300 flex items-center space-x-1" id="hud-cg-status-badge">
                    <i class="fa-solid fa-id-badge"></i>
                    <span>Profile Validated: High Retention Priority</span>
                  </span>
                  <button onclick="inspectInGraph('cg')" class="text-[10px] font-bold text-amber-600 dark:text-amber-400 hover:underline">
                    View in Call Diary Graph &rarr;
                  </button>
                </div>
              </div>
            </div>

            <!-- HUD CARD 3: REAL-TIME BUSINESS GRAPH IMPACT & FEEDBACK LOOP -->
            <div class="bg-white dark:bg-slate-900 border-2 border-emerald-200 dark:border-emerald-900/60 rounded-2xl p-4 shadow-xs relative overflow-hidden">
              <div class="absolute top-0 right-0 px-2.5 py-0.5 rounded-bl-lg bg-emerald-600 text-white font-mono text-[9px] font-bold uppercase tracking-wider">
                Business Graph (BG)
              </div>
              <div class="flex items-center space-x-2 mb-2">
                <i class="fa-solid fa-chart-pie text-emerald-500"></i>
                <h4 class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-tight">
                  3. Business Graph Reconciliation &amp; Feedback Loop
                </h4>
              </div>

              <!-- 4 Live Synthesis Outcomes Grid -->
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-100 dark:border-emerald-900/50">
                  <span class="text-[9px] font-extrabold uppercase text-emerald-700 dark:text-emerald-400">Net Value Preserved</span>
                  <div class="font-extrabold text-sm text-emerald-700 dark:text-emerald-300" id="hud-bg-netvalue">+$2,250</div>
                  <span class="text-[10px] text-slate-500 dark:text-slate-400">$2.4k LTV - $150 credit</span>
                </div>

                <div class="p-2 rounded-lg bg-sky-50 dark:bg-sky-950/30 border border-sky-100 dark:border-sky-900/50">
                  <span class="text-[9px] font-extrabold uppercase text-sky-700 dark:text-sky-400">Handle Time &amp; FCR</span>
                  <div class="font-extrabold text-sm text-sky-700 dark:text-sky-300" id="hud-bg-aht">42s &bull; 100% FCR</div>
                  <span class="text-[10px] text-slate-500 dark:text-slate-400">0s human wait queue</span>
                </div>
              </div>

              <div class="mt-2 p-2 rounded-lg bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-[11px] text-slate-600 dark:text-slate-300">
                <div class="flex items-center space-x-1.5 text-indigo-600 dark:text-indigo-400 font-bold mb-0.5">
                  <i class="fa-solid fa-arrows-spin"></i>
                  <span>Policy Drift Loop to SOP Knowledge Graph:</span>
                </div>
                <div id="hud-bg-drift-feedback">
                  Logged Exception #48 &bull; Business Graph automatically recommends raising standard Tier-1 SOP-04 limit from $50 &rarr; $150 for LTV &gt; $2,000.
                </div>
              </div>

              <div class="flex items-center justify-end pt-2">
                <button onclick="inspectInGraph('bg')" class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 hover:underline">
                  View in Business Goals Graph &rarr;
                </button>
              </div>

            </div>

          </div>

        </div>

      </div>'''

    if view_bg_marker not in html:
        print("ERROR: view_bg_marker not found!")
        return
    html = html.replace(view_bg_marker, view_call_html, 1)

    # 3. Update tabs list in switchTab
    tab_list_old = "const tabs = ['hierarchy', 'kg', 'cg', 'bg'];"
    tab_list_new = "const tabs = ['hierarchy', 'kg', 'cg', 'bg', 'call'];"
    if tab_list_old not in html:
        print("ERROR: tab_list_old not found!")
        return
    html = html.replace(tab_list_old, tab_list_new, 1)

    # 4. Add Live Call Simulator JS functions
    js_call_logic = '''
    // =========================================================================
    // REAL-TIME CALL SIMULATOR (GROUNDED IN KG & CG)
    // =========================================================================
    let callTimerInterval = null;
    let callSeconds = 18;
    let voiceSpeechEnabled = true;
    let currentAgentTextToSpeak = "Hello Sarah, I completely understand your concern regarding the $150 roaming fee. Because you have been a valued customer with us for 6 years and maintain an exceptional account standing, I am applying our VIP Hardship Exception under SOP-04 Section 4.2 to waive the full $150 right now. Your balance has been adjusted to $0, and no supervisor transfer is required.";

    const CALL_PRESETS = {
      billing: {
        scenarioKey: "billing_dispute",
        callerId: "Caller: Sarah Jenkins (Acct #48291 • LTV $2,400)",
        tier: "VIP Tier",
        callerName: "Sarah Jenkins",
        intent: "Dispute",
        question: "I was charged a $150 international roaming fee on my last bill that I didn't authorize. Can you waive it?",
        thinking: "Reconciling SOP-04 with Sarah Jenkins (LTV $2.4k, 6 yrs tenure)... Approved Clause 4.2 exception ($150 ≤ $250).",
        agentResponse: "Hello Sarah, I completely understand your concern regarding the $150 roaming fee. Because you have been a valued customer with us for 6 years and maintain an exceptional account standing, I am applying our VIP Hardship Exception under SOP-04 Section 4.2 to waive the full $150 right now. Your balance has been adjusted to $0, and no supervisor transfer is required.",
        sopTag: "Verified SOP-04",
        kgName: "SOP-04: Inbound Billing & Roaming Disputes",
        kgRule1: "• <strong>Standard Rule:</strong> Tier-1 Agent max waiver limit is $50.",
        kgRule2: "• <strong>Section 4.2 Exception:</strong> Hardship/VIP accounts (LTV > $2k, > 3 yrs tenure) allow up to $250 credit with automated authorization.",
        kgBadge: '<i class="fa-solid fa-circle-check"></i> <span>SOP Match: Clause 4.2 Approved ($150 ≤ $250)</span>',
        cgCaller: "Customer Context: Sarah Jenkins (Acct #48291)",
        cgMetrics: "• <strong>Tenure & Value:</strong> 6.2 years • Lifetime Value: $2,400 • Plan: Unlimited International",
        cgHistory: "• <strong>Historical Diary:</strong> 0 billing disputes in past 24 months. Churn probability if denied: 82%.",
        cgBadge: '<i class="fa-solid fa-id-badge"></i> <span>Profile Validated: High Retention Priority</span>',
        bgNetValue: "+$2,250",
        bgAht: "42s • 100% FCR",
        bgDrift: "Logged Exception #48 • Business Graph automatically recommends raising standard Tier-1 SOP-04 limit from $50 → $150 for LTV > $2,000."
      },
      outage: {
        scenarioKey: "tech_outage",
        callerId: "Caller: Marcus Vance (Acct #91024 • Fiber Gigabit)",
        tier: "Business Pro",
        callerName: "Marcus Vance",
        intent: "Hardware Failure",
        question: "My fiber router has had a blinking red optical light for 2 hours and my team is offline. Can you dispatch a tech today?",
        thinking: "Reconciling SOP-12 with Marcus Vance ONT telemetry (Optical Loss: 31.4dB > 28dB threshold)...",
        agentResponse: "I'm so sorry for the interruption to your home office, Marcus. I just ran real-time line telemetry on your ONT and detected an optical signal loss of 31.4dB on the fiber drop, indicating an exterior physical drop fault rather than inside hardware. Under SOP-12 Rule 3, I have bypassed the 180-second manual restart checklist and immediately dispatched our field technician for today between 1:00 PM and 3:00 PM. Dispatch ID #TX-9041 is confirmed.",
        sopTag: "Verified SOP-12",
        kgName: "SOP-12: Broadband Hardware & Signal Attenuation",
        kgRule1: "• <strong>Standard Triage:</strong> 180s phone manual reboot sequence.",
        kgRule2: "• <strong>Rule 3 Telemetry Exception:</strong> Optical loss > 28dB mandates immediate direct truck roll bypass.",
        kgBadge: '<i class="fa-solid fa-circle-check"></i> <span>SOP Match: Telemetry Loss 31.4dB > 28dB</span>',
        cgCaller: "Customer Context: Marcus Vance (Acct #91024)",
        cgMetrics: "• <strong>Service:</strong> Gigabit Fiber Pro • Speed SLA: 99.9% • Account Age: 3.5 yrs",
        cgHistory: "• <strong>Real-time Telemetry:</strong> Red LOS Alarm • Optical Rx: -31.4 dBm • Line Loop Test: FAILED",
        cgBadge: '<i class="fa-solid fa-triangle-exclamation text-amber-500"></i> <span>Hardware Fault Validated</span>',
        bgNetValue: "+$450 Saved",
        bgAht: "12s • 100% FCR",
        bgDrift: "Bottleneck Eliminated • Slashed triage hold time by 168s; zero repeat calls or fruitless customer reboots."
      },
      retention: {
        scenarioKey: "vip_retention",
        callerId: "Caller: Elena Rostova (Apex Logistics • ARR $18,000)",
        tier: "Enterprise Tier",
        callerName: "Elena Rostova",
        intent: "Churn Risk",
        question: "We have been a loyal client for 8 years, but our renewal rate jumped 25%. I want to cancel our $18,000/yr enterprise account today.",
        thinking: "Reconciling SOP-28 with Elena Rostova (8.4 yrs client, $18k ARR)... Matching Executive Loyalty 15% discount limit.",
        agentResponse: "Elena, thank you for being a cornerstone enterprise client with us for over 8 years. We deeply value our partnership with Apex Logistics. Under SOP-28 Executive Retention guidelines for tenured enterprise accounts, I can immediately lock in a 15% discount across a 2-year renewal term, preserving your annual rate at $15,300 with guaranteed priority SLAs. May I send over the renewal addendum for your digital signature right now?",
        sopTag: "Verified SOP-28",
        kgName: "SOP-28: Enterprise Contract Retention & Churn Prevention",
        kgRule1: "• <strong>Standard Limit:</strong> Tier-1 Agent max discretionary discount is 5%.",
        kgRule2: "• <strong>Executive Clause 2.4:</strong> Tenured accounts (> 5 yrs, ARR > $15k) permit up to 15% discount on 2-yr renewals.",
        kgBadge: '<i class="fa-solid fa-circle-check"></i> <span>SOP Match: Clause 2.4 Approved (15% Max)</span>',
        cgCaller: "Customer Context: Elena Rostova (Apex Logistics Corp)",
        cgMetrics: "• <strong>Tenure & ARR:</strong> 8.4 years • Current ARR: $18,000 • Tier: Tier-1 Enterprise",
        cgHistory: "• <strong>Churn Diary:</strong> Competitor quote received. Account churn probability without concession: 94%.",
        cgBadge: '<i class="fa-solid fa-crown text-indigo-400"></i> <span>High ARR Enterprise Verified</span>',
        bgNetValue: "+$27,900 ARR",
        bgAht: "58s • Retained 2-Yr",
        bgDrift: "Compliance Reconciled • Concession ROI: $2,700 annual discount protects $30,600 2-yr contract value."
      }
    };

    function startCallTimer() {
      if (callTimerInterval) clearInterval(callTimerInterval);
      callTimerInterval = setInterval(() => {
        callSeconds++;
        const mins = String(Math.floor(callSeconds / 60)).padStart(2, '0');
        const secs = String(callSeconds % 60).padStart(2, '0');
        const el = document.getElementById('call-timer');
        if (el) el.textContent = `Call Duration: ${mins}:${secs}`;
      }, 1000);
    }

    function toggleVoiceSpeech() {
      voiceSpeechEnabled = !voiceSpeechEnabled;
      const icon = document.getElementById('voice-icon');
      const text = document.getElementById('voice-toggle-text');
      if (voiceSpeechEnabled) {
        icon.className = "fa-solid fa-volume-high text-emerald-400";
        text.textContent = "Speech: ON";
      } else {
        icon.className = "fa-solid fa-volume-xmark text-slate-400";
        text.textContent = "Speech: OFF";
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      }
    }

    function speakCurrentResponse() {
      if (!voiceSpeechEnabled || !('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(currentAgentTextToSpeak);
      utterance.rate = 1.05;
      utterance.pitch = 1.0;
      
      const waveBars = [
        document.getElementById('wave-1'),
        document.getElementById('wave-2'),
        document.getElementById('wave-3'),
        document.getElementById('wave-4'),
        document.getElementById('wave-5')
      ];

      const waveInterval = setInterval(() => {
        waveBars.forEach(b => {
          if (b) b.style.height = `${Math.floor(Math.random() * 16) + 4}px`;
        });
      }, 120);

      utterance.onend = () => {
        clearInterval(waveInterval);
        waveBars.forEach((b, i) => {
          if (b) b.style.height = `${[12, 20, 8, 24, 12][i]}px`;
        });
      };

      window.speechSynthesis.speak(utterance);
    }

    function simulateSampleCall(type) {
      const p = CALL_PRESETS[type];
      if (!p) return;

      // Update Active Scenario Preset across the entire app
      loadScenarioPreset(p.scenarioKey);
      const presetSelect = document.getElementById('preset-select');
      if (presetSelect) presetSelect.value = p.scenarioKey;

      // Highlight active sample button
      ['billing', 'outage', 'retention'].forEach(k => {
        const btn = document.getElementById(`sample-btn-${k}`);
        if (btn) {
          if (k === type) {
            btn.className = "text-left p-3 rounded-xl border-2 border-emerald-500 bg-emerald-50/80 dark:bg-emerald-950/40 shadow-xs transition group";
          } else {
            btn.className = "text-left p-3 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-900 transition group shadow-2xs";
          }
        }
      });

      // Update Call Bar Header
      document.getElementById('caller-id-display').textContent = p.callerId;
      document.getElementById('caller-tier-badge').textContent = p.tier;

      // Update Transcript
      document.getElementById('caller-name-tag').textContent = p.callerName;
      document.getElementById('caller-intent-tag').textContent = p.intent;
      document.getElementById('caller-speech-text').innerHTML = `&ldquo;${p.question}&rdquo;`;

      // Update Agent Thinking HUD
      document.getElementById('thinking-status-text').textContent = p.thinking;

      // Update Agent Spoken Response
      currentAgentTextToSpeak = p.agentResponse;
      document.getElementById('agent-sop-tag').textContent = p.sopTag;
      document.getElementById('agent-response-text').innerHTML = `&ldquo;${p.agentResponse}&rdquo;`;

      // Update KG Card
      document.getElementById('hud-kg-sop-name').textContent = p.kgName;
      document.getElementById('hud-kg-rule1').innerHTML = p.kgRule1;
      document.getElementById('hud-kg-rule2').innerHTML = p.kgRule2;
      document.getElementById('hud-kg-decision-badge').innerHTML = p.kgBadge;

      // Update CG Card
      document.getElementById('hud-cg-caller-name').textContent = p.cgCaller;
      document.getElementById('hud-cg-metrics').innerHTML = p.cgMetrics;
      document.getElementById('hud-cg-history').innerHTML = p.cgHistory;
      document.getElementById('hud-cg-status-badge').innerHTML = p.cgBadge;

      // Update BG Card
      document.getElementById('hud-bg-netvalue').textContent = p.bgNetValue;
      document.getElementById('hud-bg-aht').textContent = p.bgAht;
      document.getElementById('hud-bg-drift-feedback').textContent = p.bgDrift;

      // Voice Playback
      speakCurrentResponse();
    }

    function askCustomCallerQuestion() {
      const input = document.getElementById('custom-caller-input');
      const q = input.value.trim();
      if (!q) return;

      const lower = q.toLowerCase();
      if (lower.includes('outage') || lower.includes('router') || lower.includes('internet') || lower.includes('fiber') || lower.includes('light')) {
        simulateSampleCall('outage');
      } else if (lower.includes('cancel') || lower.includes('renew') || lower.includes('contract') || lower.includes('enterprise') || lower.includes('discount')) {
        simulateSampleCall('retention');
      } else {
        simulateSampleCall('billing');
      }

      document.getElementById('caller-speech-text').innerHTML = `&ldquo;${q}&rdquo;`;
      input.value = '';
    }

    function resetLiveCall() {
      callSeconds = 0;
      simulateSampleCall('billing');
    }

    function inspectInGraph(tabKey) {
      switchTab(tabKey);
    }
'''

    # Insert JS logic right before </script>
    script_end = '  </script>'
    if script_end not in html:
        print("ERROR: </script> not found!")
        return
    html = html.replace(script_end, js_call_logic + '\n' + script_end, 1)

    with open('callcenter_ai_voice_agents.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: Successfully integrated Live Call Simulator into callcenter_ai_voice_agents.html!")

if __name__ == '__main__':
    main()
