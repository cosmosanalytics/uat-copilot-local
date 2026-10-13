import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_page():
    with open("all_extracted_linkedin_posts.json", "r", encoding="utf-8") as f:
        raw_posts = json.load(f)

    # Deduplicate and enrich
    posts = []
    seen = set()

    # Category classification rules
    def get_category(title, text, file):
        combo = (title + " " + text + " " + file).lower()
        if any(k in combo for k in ["brain", "cognitive pyramid", "connectome", "41 functions", "memory index", "forget slider", "4-slot", "second look", "neuroscience", "hippocampus"]):
            return "🧠 Brain & Cognitive AI"
        elif any(k in combo for k in ["war room", "chess", "grand strategy", "network optimization", "menu pricing", "sop", "whiteboard", "multi-agent", "society of mind", "swarm"]):
            return "🤖 Multi-Agent Systems"
        elif any(k in combo for k in ["skill #", "skills", "mcp", "academy-guide", "doc-coauthoring", "docx", "pdf studio", "pptx", "xlsx", "brand-guidelines", "canvas-design", "theme-factory", "algorithmic-art", "slack-gif"]):
            return "🛠️ Agentic Skills (1–20)"
        elif any(k in combo for k in ["3d game", "comic", "browser control", "sketch", "novel", "progressive", "chore", "troubleshoot", "meeting", "art transmuter", "game"]):
            return "🎨 In-Browser AI Apps"
        else:
            return "🔬 Theory & Research"

    for p in raw_posts:
        # Ignore non-fixed gif summary if fixed exists
        if p["source_file"] == "post_gif_summary_to_linkedin.py":
            continue
        text = p["text"].strip()
        norm = re.sub(r'\s+', ' ', text)
        if norm in seen:
            continue
        seen.add(norm)

        urls = re.findall(r'https://cosmosanalytics\.github\.io/[^\s\"\'\)]+|https://github\.com/[^\s\"\'\)]+', text)
        url = p.get("url") or (urls[0] if urls else "")
        # Remove trailing punctuation from url
        if url:
            url = url.rstrip('.,;)"\'')

        title = p.get("title", "").strip()
        if not title or len(title) < 5 or title.startswith("Post "):
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            title = lines[0] if lines else "LinkedIn Post"
            title = re.sub(r'^[🚀🧠⚡💡🎮🎨🌐✍️📚🛡️🔍•\-#]+\s*', '', title)
            title = title[:85]

        # Extract hashtags
        hashtags = re.findall(r'#([A-Za-z0-9_]+)', text)

        cat = get_category(title, text, p["source_file"])

        posts.append({
            "id": len(posts) + 1,
            "title": title,
            "category": cat,
            "text": text,
            "url": url,
            "hashtags": hashtags[:6],
            "file": p["source_file"]
        })

    # Sort posts logically: Brain & Cognitive first, then Multi-Agent, then Skills, then Apps, then Theory
    cat_order = {
        "🧠 Brain & Cognitive AI": 1,
        "🤖 Multi-Agent Systems": 2,
        "🛠️ Agentic Skills (1–20)": 3,
        "🎨 In-Browser AI Apps": 4,
        "🔬 Theory & Research": 5
    }
    posts.sort(key=lambda x: (cat_order.get(x["category"], 9), x["id"]))
    # Re-index
    for idx, p in enumerate(posts, 1):
        p["id"] = idx

    print(f"Total curated posts: {len(posts)}")

    # HTML Template
    posts_json = json.dumps(posts, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>All LinkedIn Posts & In-Browser AI Showcase | Cosmos Analytics</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-page: #F8FAFC;
    --bg-card: #FFFFFF;
    --bg-subtle: #F1F5F9;
    --border: #E2E8F0;
    --border-hover: #CBD5E1;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #64748B;
    --accent: #2563EB;
    --accent-light: #EFF6FF;
    --accent-hover: #1D4ED8;
    --aws-orange: #FF9900;
    --emerald: #059669;
    --emerald-bg: #ECFDF5;
    --purple: #7C3AED;
    --purple-bg: #F5F3FF;
    --amber: #D97706;
    --amber-bg: #FFFBEB;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
  }}

  body.dark-mode {{
    --bg-page: #0B0F19;
    --bg-card: #111827;
    --bg-subtle: #1F2937;
    --border: #374151;
    --border-hover: #4B5563;
    --text-primary: #F9FAFB;
    --text-secondary: #D1D5DB;
    --text-muted: #9CA3AF;
    --accent: #3B82F6;
    --accent-light: #1E3A8A33;
    --accent-hover: #60A5FA;
    --emerald: #10B981;
    --emerald-bg: #064E3B33;
    --purple: #8B5CF6;
    --purple-bg: #581C8733;
    --amber: #F59E0B;
    --amber-bg: #78350F33;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-page);
    color: var(--text-primary);
    line-height: 1.5;
    transition: background-color 0.2s, color 0.2s;
  }}

  /* HEADER */
  header {{
    position: sticky;
    top: 0;
    z-index: 50;
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow-sm);
  }}
  .nav-container {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }}
  .nav-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: var(--text-primary);
  }}
  .nav-logo {{
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 800;
    font-size: 16px;
  }}
  .nav-title {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.02em;
  }}
  .nav-actions {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .nav-link {{
    font-size: 13.5px;
    font-weight: 600;
    color: var(--text-secondary);
    text-decoration: none;
    padding: 6px 12px;
    border-radius: 6px;
    transition: all 0.15s;
    border: 1px solid transparent;
  }}
  .nav-link:hover {{
    color: var(--text-primary);
    background: var(--bg-subtle);
    border-color: var(--border);
  }}
  .theme-toggle {{
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    width: 36px;
    height: 36px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    transition: all 0.15s;
  }}
  .theme-toggle:hover {{
    border-color: var(--border-hover);
    color: var(--text-primary);
  }}

  /* HERO */
  .hero {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 40px 24px 24px;
  }}
  .hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-light);
    border: 1px solid var(--accent);
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 12px;
  }}
  .hero h1 {{
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin-bottom: 8px;
  }}
  .hero p {{
    font-size: 16px;
    color: var(--text-secondary);
    max-width: 780px;
    margin-bottom: 24px;
  }}

  /* STATS PILLS */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }}
  .stat-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: var(--shadow-sm);
  }}
  .stat-num {{
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-primary);
  }}
  .stat-label {{
    font-size: 13px;
    font-weight: 600;
    color: var(--text-muted);
  }}

  /* CONTROLS (SEARCH & CATEGORIES) */
  .controls-bar {{
    position: sticky;
    top: 57px;
    z-index: 40;
    background: var(--bg-page);
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
  }}
  .controls-wrap {{
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .search-input-wrap {{
    position: relative;
    width: 100%;
  }}
  .search-input-wrap span {{
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 16px;
    color: var(--text-muted);
    pointer-events: none;
  }}
  .search-input {{
    width: 100%;
    padding: 12px 16px 12px 42px;
    font-size: 14.5px;
    font-family: inherit;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--bg-card);
    color: var(--text-primary);
    box-shadow: var(--shadow-sm);
    outline: none;
    transition: all 0.15s;
  }}
  .search-input:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-light);
  }}
  .cat-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .cat-pill {{
    font-size: 13px;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.15s;
  }}
  .cat-pill:hover {{
    border-color: var(--border-hover);
    color: var(--text-primary);
  }}
  .cat-pill.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: #FFFFFF;
  }}

  /* POSTS GRID */
  .posts-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(370px, 1fr));
    gap: 24px;
    margin-bottom: 60px;
  }}
  .post-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
  }}
  .post-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: var(--border-hover);
  }}
  .post-header {{
    padding: 16px 18px 12px;
    border-bottom: 1px solid var(--border);
    background: var(--bg-subtle);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }}
  .post-cat {{
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    color: var(--accent);
  }}
  .post-id {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    font-weight: 600;
    color: var(--text-muted);
  }}
  .post-body {{
    padding: 18px;
    flex: 1;
    display: flex;
    flex-direction: column;
  }}
  .post-title {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--text-primary);
    margin-bottom: 12px;
    line-height: 1.35;
  }}
  .post-text {{
    font-size: 13.5px;
    line-height: 1.6;
    color: var(--text-secondary);
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 230px;
    overflow-y: hidden;
    position: relative;
    margin-bottom: 12px;
  }}
  .post-text.expanded {{
    max-height: none;
    overflow-y: visible;
  }}
  .post-text-fade {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: linear-gradient(to bottom, transparent, var(--bg-card));
    pointer-events: none;
  }}
  .post-text.expanded .post-text-fade {{
    display: none;
  }}
  .toggle-btn {{
    background: none;
    border: none;
    color: var(--accent);
    font-size: 12.5px;
    font-weight: 600;
    cursor: pointer;
    padding: 0;
    margin-bottom: 14px;
    text-align: left;
    display: inline-block;
  }}
  .toggle-btn:hover {{
    text-decoration: underline;
  }}

  /* HASHTAGS */
  .tags-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 16px;
  }}
  .tag-pill {{
    font-size: 11.5px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    background: var(--bg-subtle);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid var(--border);
  }}

  /* ACTIONS FOOTER */
  .post-footer {{
    padding: 14px 18px;
    border-top: 1px solid var(--border);
    background: var(--bg-card);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: auto;
  }}
  .btn-action {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 12.5px;
    font-weight: 600;
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-primary);
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s;
  }}
  .btn-action:hover {{
    background: var(--bg-subtle);
    border-color: var(--border-hover);
  }}
  .btn-action.primary {{
    background: var(--accent);
    border-color: var(--accent);
    color: #FFFFFF;
  }}
  .btn-action.primary:hover {{
    background: var(--accent-hover);
    border-color: var(--accent-hover);
  }}

  /* TOAST NOTIFICATION */
  .toast {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #0F172A;
    color: #FFFFFF;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 13.5px;
    font-weight: 600;
    box-shadow: var(--shadow-lg);
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 100;
    opacity: 0;
    transform: translateY(12px);
    pointer-events: none;
    transition: opacity 0.2s, transform 0.2s;
  }}
  .toast.show {{
    opacity: 1;
    transform: translateY(0);
  }}

  /* EMPTY STATE */
  .empty-state {{
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
    grid-column: 1 / -1;
    display: none;
  }}
  .empty-state h3 {{
    font-size: 18px;
    color: var(--text-primary);
    margin-bottom: 6px;
  }}

  @media (max-width: 640px) {{
    .posts-grid {{
      grid-template-columns: 1fr;
    }}
    .nav-container {{
      flex-direction: column;
      align-items: stretch;
    }}
  }}
</style>
</head>
<body>

<header>
  <div class="nav-container">
    <a href="index.html" class="nav-brand">
      <div class="nav-logo">⚡</div>
      <div class="nav-title">Cosmos Analytics &bull; UAT Copilot</div>
    </a>
    <div class="nav-actions">
      <a href="index.html" class="nav-link">← Copilot Home</a>
      <a href="brain_ai_all_41_functions.html" class="nav-link">🧠 41 Brain Functions Studio</a>
      <a href="AWS_41_Brain_Functions_Developer_Guide.pdf" target="_blank" class="nav-link">📄 AWS Field Guide PDF</a>
      <a href="https://github.com/cosmosanalytics/uat-copilot-local" target="_blank" class="nav-link">GitHub Repo</a>
      <button class="theme-toggle" id="themeToggle" title="Toggle Light/Dark Theme">🌙</button>
    </div>
  </div>
</header>

<main class="hero">
  <div class="hero-badge">🚀 Unified Showcase & Archive</div>
  <h1>All LinkedIn Posts &amp; Live In-Browser AI Apps</h1>
  <p>The complete archive of all architectural LinkedIn posts, real-time in-browser WebGPU/WebLLM interactive apps, open-source agentic skills, and biological cognitive models. One-click copy and instant live app demo.</p>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-num" id="totalPostsCount">{len(posts)}</div>
      <div class="stat-label">Total Curated Posts</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">{len([p for p in posts if p.get('url')])}</div>
      <div class="stat-label">Live In-Browser Web Apps</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">5</div>
      <div class="stat-label">Pillars &amp; Skill Series</div>
    </div>
    <div class="stat-card">
      <div class="stat-num">100%</div>
      <div class="stat-label">Zero-Install HTML / Pure Client</div>
    </div>
  </div>

  <div class="controls-bar">
    <div class="controls-wrap">
      <div class="search-input-wrap">
        <span>🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Search posts by topic, algorithm, skill, or keyword (e.g. 'hippocampus', 'chess', 'pdf', 'webgpu')...">
      </div>
      <div class="cat-pills" id="catPills">
        <button class="cat-pill active" data-cat="ALL">All Categories ({len(posts)})</button>
        <button class="cat-pill" data-cat="🧠 Brain & Cognitive AI">🧠 Brain &amp; Cognitive AI</button>
        <button class="cat-pill" data-cat="🤖 Multi-Agent Systems">🤖 Multi-Agent Systems</button>
        <button class="cat-pill" data-cat="🛠️ Agentic Skills (1–20)">🛠️ Agentic Skills (1–20)</button>
        <button class="cat-pill" data-cat="🎨 In-Browser AI Apps">🎨 In-Browser AI Apps</button>
        <button class="cat-pill" data-cat="🔬 Theory & Research">🔬 Theory &amp; Research</button>
      </div>
    </div>
  </div>

  <div class="posts-grid" id="postsGrid">
    <!-- Populated by JavaScript -->
    <div class="empty-state" id="emptyState">
      <h3>No matching posts found</h3>
      <p>Try clearing your search query or selecting a different category.</p>
    </div>
  </div>
</main>

<div class="toast" id="toast">
  <span>✅</span>
  <span id="toastMsg">Post copied to clipboard!</span>
</div>

<script>
  const POSTS_DATA = {posts_json};

  let activeCategory = 'ALL';
  let searchQuery = '';

  const postsGrid = document.getElementById('postsGrid');
  const emptyState = document.getElementById('emptyState');
  const searchInput = document.getElementById('searchInput');
  const catPills = document.getElementById('catPills');
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toastMsg');
  const themeToggle = document.getElementById('themeToggle');

  function showToast(text) {{
    toastMsg.textContent = text;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
  }}

  function copyPost(idx) {{
    const p = POSTS_DATA.find(x => x.id === idx);
    if (!p) return;
    navigator.clipboard.writeText(p.text).then(() => {{
      showToast(`Copied post #${{idx}} to clipboard!`);
    }}).catch(err => {{
      showToast('Failed to copy: ' + err);
    }});
  }}

  function toggleExpand(id) {{
    const el = document.getElementById(`post-text-${{id}}`);
    const btn = document.getElementById(`toggle-btn-${{id}}`);
    if (!el || !btn) return;
    if (el.classList.contains('expanded')) {{
      el.classList.remove('expanded');
      btn.textContent = 'Read more ↓';
    }} else {{
      el.classList.add('expanded');
      btn.textContent = 'Collapse ↑';
    }}
  }}

  function renderPosts() {{
    const filtered = POSTS_DATA.filter(p => {{
      const matchCat = (activeCategory === 'ALL' || p.category === activeCategory);
      const q = searchQuery.toLowerCase();
      const matchQuery = !q || (
        p.title.toLowerCase().includes(q) ||
        p.text.toLowerCase().includes(q) ||
        p.category.toLowerCase().includes(q) ||
        (p.hashtags && p.hashtags.some(h => h.toLowerCase().includes(q)))
      );
      return matchCat && matchQuery;
    }});

    // Remove old cards (except empty state)
    const cards = postsGrid.querySelectorAll('.post-card');
    cards.forEach(c => c.remove());

    if (filtered.length === 0) {{
      emptyState.style.display = 'block';
      return;
    }}
    emptyState.style.display = 'none';

    filtered.forEach(p => {{
      const card = document.createElement('div');
      card.className = 'post-card';
      
      const tagsHtml = (p.hashtags && p.hashtags.length) 
        ? `<div class="tags-row">${{p.hashtags.map(t => `<span class="tag-pill">#${{t}}</span>`).join('')}}</div>` 
        : '';

      const launchBtn = p.url 
        ? `<a href="${{p.url}}" target="_blank" class="btn-action primary">🚀 Launch Live App</a>` 
        : '';

      card.innerHTML = `
        <div class="post-header">
          <span class="post-cat">${{p.category}}</span>
          <span class="post-id">#${{p.id}}</span>
        </div>
        <div class="post-body">
          <h2 class="post-title">${{escapeHtml(p.title)}}</h2>
          <div class="post-text" id="post-text-${{p.id}}">
            ${{escapeHtml(p.text)}}
            <div class="post-text-fade"></div>
          </div>
          <button class="toggle-btn" id="toggle-btn-${{p.id}}" onclick="toggleExpand(${{p.id}})">Read more ↓</button>
          ${{tagsHtml}}
        </div>
        <div class="post-footer">
          <button class="btn-action" onclick="copyPost(${{p.id}})">📋 Copy Post</button>
          ${{launchBtn}}
        </div>
      `;
      postsGrid.appendChild(card);
    }});
  }}

  function escapeHtml(str) {{
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }}

  // Event Listeners
  searchInput.addEventListener('input', (e) => {{
    searchQuery = e.target.value.trim();
    renderPosts();
  }});

  catPills.addEventListener('click', (e) => {{
    const btn = e.target.closest('.cat-pill');
    if (!btn) return;
    catPills.querySelectorAll('.cat-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeCategory = btn.dataset.cat;
    renderPosts();
  }});

  themeToggle.addEventListener('click', () => {{
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    themeToggle.textContent = isDark ? '☀️' : '🌙';
  }});

  // Initial render
  renderPosts();
</script>

</body>
</html>
"""

    with open("linkedin_posts.html", "w", encoding="utf-8") as out:
        out.write(html_content)

    print(f"[SUCCESS] Generated linkedin_posts.html ({len(html_content)} bytes)")

if __name__ == "__main__":
    build_page()
