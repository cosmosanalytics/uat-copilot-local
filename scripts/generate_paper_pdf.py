import os
import re
import base64
import subprocess
import markdown

def encode_image_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"

def clean_markdown_math(text):
    # Fix standard LaTeX math that might get mangled by standard markdown
    # Replace common symbols for cleaner typesetting
    return text

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    repo_dir = os.path.join(root_dir, "repo")
    figures_dir = os.path.join(repo_dir, "results", "figures")
    
    # Load markdown text
    md_path = os.path.join(root_dir, "RESEARCH_PAPER.md")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    # Prepare base64 images
    img_e0 = encode_image_base64(os.path.join(figures_dir, "reliability_e0.png"))
    img_rlcr = encode_image_base64(os.path.join(figures_dir, "reliability_rlcr.png"))
    img_e3 = encode_image_base64(os.path.join(figures_dir, "reliability_e3.png"))
    img_e4c = encode_image_base64(os.path.join(figures_dir, "reliability_e4c.png"))
    img_risk = encode_image_base64(os.path.join(figures_dir, "risk_coverage_curve.png"))
    img_n_removed = encode_image_base64(os.path.join(figures_dir, "confidence_by_n_removed.png"))
    
    # HTML figure blocks with compact heights
    figures_html_1 = f"""
    <div class="figure-block page-break-avoid">
        <div class="grid-2x2">
            <div class="grid-item">
                <img src="{img_e0}" />
                <div class="img-subcap">(a) E0: Prompted Base LLM (Severe Overconfidence)</div>
            </div>
            <div class="grid-item">
                <img src="{img_rlcr}" />
                <div class="img-subcap">(b) E1: RLCR Policy Gradient (Paper Method)</div>
            </div>
            <div class="grid-item">
                <img src="{img_e3}" />
                <div class="img-subcap">(c) E3: Zhao's Code Scorer (Convex LR, 3.0% ECE)</div>
            </div>
            <div class="grid-item">
                <img src="{img_e4c}" />
                <div class="img-subcap">(d) E4c: Hybrid Verifier (Judge + Code, 2.6% ECE)</div>
            </div>
        </div>
        <p class="figure-caption"><strong>Figure 1: Reliability Diagrams Across Evaluated Architectures.</strong> Bars represent empirical accuracy for 10 confidence bins ($M=10$). Red dashed lines indicate the ideal diagonal ($y=x$). Base LLM exhibits extreme overconfidence with a 76.7% gap in bin [0.9, 1.0], while E3 and E4c achieve near-perfect calibration around empirical accuracy.</p>
    </div>
    """
    
    figures_html_2 = f"""
    <div class="figure-block page-break-avoid">
        <div class="grid-1x2">
            <div class="grid-item">
                <img src="{img_risk}" />
                <div class="img-subcap">(a) Selective Prediction Risk-Coverage Curves</div>
            </div>
            <div class="grid-item">
                <img src="{img_n_removed}" />
                <div class="img-subcap">(b) Epistemic Degradation vs. Evidence Removed</div>
            </div>
        </div>
        <p class="figure-caption"><strong>Figure 2: Risk-Coverage & Epistemic Uncertainty Profiling.</strong> (a) Risk (1 - accuracy) as coverage increases from 10% to 100%. Calibrated verifiers maintain near-zero error at high coverage. (b) Mean verbalized confidence as gold evidence is removed ($n_{{\\text{{removed}}}} \\in \\{{0, 1, 2\\}}$). The uncalibrated base LLM shows pathological confidence inversion ($0.605 \\to 0.626$), whereas E4c depresses confidence to $0.002$ when evidence is missing.</p>
    </div>
    """
    
    # Process markdown
    md_processed = clean_markdown_math(md_text)
    html_body = markdown.markdown(md_processed, extensions=['tables', 'fenced_code'])
    
    # Insert visual figures after relevant sections
    target_token_1 = "<h3>5.2 Key Empirical Takeaways</h3>"
    if target_token_1 in html_body:
        html_body = html_body.replace(target_token_1, figures_html_1 + "\n" + target_token_1)
        
    target_token_2 = "<h2>7. Controlled Epistemic Ablation: Unanswerability Detection</h2>"
    if target_token_2 in html_body:
        html_body = html_body.replace(target_token_2, target_token_2 + "\n" + figures_html_2)

    # CSS for publication PDF
    custom_css = """
    @page {
        size: letter;
        margin: 18mm 16mm 18mm 16mm;
        @bottom-right {
            content: "Page " counter(page);
            font-size: 8.5pt;
            font-family: "Georgia", "Times New Roman", serif;
            color: #666;
        }
        @bottom-left {
            content: "Antigravity AI Engineering Lab & Zhao (2026)";
            font-size: 8.5pt;
            font-family: "Georgia", "Times New Roman", serif;
            color: #666;
        }
        @top-right {
            content: "Empirical Stability & Calibration of LLM Agents";
            font-size: 8pt;
            font-family: "Georgia", "Times New Roman", serif;
            font-style: italic;
            color: #888;
        }
    }
    *, *:before, *:after {
        box-sizing: border-box;
    }
    body {
        font-family: "Georgia", "Cambria", "Times New Roman", serif;
        font-size: 10pt;
        line-height: 1.48;
        color: #222;
        margin: 0;
        padding: 0;
    }
    h1 {
        font-size: 18pt;
        line-height: 1.25;
        text-align: center;
        margin-top: 6pt;
        margin-bottom: 6pt;
        font-weight: bold;
        color: #111;
    }
    .header-block {
        text-align: center;
        margin-bottom: 16pt;
        border-bottom: 1px solid #ddd;
        padding-bottom: 10pt;
    }
    .subtitle {
        font-size: 11.5pt;
        font-weight: normal;
        color: #444;
        margin-bottom: 8pt;
    }
    .authors {
        font-size: 9.5pt;
        font-weight: bold;
        color: #333;
        margin-bottom: 2pt;
    }
    .affil {
        font-size: 8.5pt;
        color: #666;
        font-style: italic;
    }
    h2 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 12pt;
        border-bottom: 1.5px solid #222;
        padding-bottom: 2pt;
        margin-top: 16pt;
        margin-bottom: 6pt;
        font-weight: 700;
        color: #111;
        page-break-after: avoid;
    }
    h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 10.5pt;
        margin-top: 10pt;
        margin-bottom: 4pt;
        font-weight: 600;
        color: #222;
        page-break-after: avoid;
    }
    h4 {
        font-size: 9.5pt;
        margin-top: 8pt;
        margin-bottom: 3pt;
        font-weight: 600;
        page-break-after: avoid;
    }
    p {
        margin-top: 0;
        margin-bottom: 6pt;
        text-align: justify;
        text-justify: inter-word;
    }
    ul, ol {
        margin-top: 0;
        margin-bottom: 6pt;
        padding-left: 18pt;
    }
    li {
        margin-bottom: 3pt;
    }
    blockquote {
        margin: 8pt 16pt;
        padding: 5pt 10pt;
        border-left: 3px solid #4a6fa5;
        background: #f8fafc;
        font-style: italic;
        font-size: 9.5pt;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10pt 0;
        font-size: 8pt;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        page-break-inside: auto;
    }
    tr {
        page-break-inside: avoid;
    }
    th, td {
        padding: 4.5pt 5pt;
        text-align: left;
        vertical-align: middle;
    }
    thead th {
        border-top: 2px solid #222;
        border-bottom: 1px solid #222;
        font-weight: 600;
        background-color: #f8f9fa;
        color: #111;
    }
    tbody tr {
        border-bottom: 0.5px solid #e2e8f0;
    }
    tbody tr:last-child {
        border-bottom: 2px solid #222;
    }
    pre {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 6pt 8pt;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 7.5pt;
        line-height: 1.35;
        overflow-x: auto;
        page-break-inside: avoid;
        margin: 8pt 0;
    }
    code {
        font-family: "Consolas", "Courier New", monospace;
        font-size: 8.5pt;
        background: #f1f5f9;
        padding: 1px 3pt;
        border-radius: 2px;
        color: #0f172a;
    }
    .figure-block {
        margin: 10pt 0 14pt 0;
        text-align: center;
        page-break-inside: avoid;
        background: #fff;
    }
    .grid-2x2 {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 8px;
    }
    .grid-2x2 .grid-item {
        width: 48.5%;
        text-align: center;
    }
    .grid-2x2 img {
        width: 100%;
        max-height: 185px;
        object-fit: contain;
        border: 1px solid #e2e8f0;
        border-radius: 3px;
        background: #fafafa;
    }
    .grid-1x2 {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    .grid-1x2 .grid-item {
        width: 48.5%;
        text-align: center;
    }
    .grid-1x2 img {
        width: 100%;
        max-height: 195px;
        object-fit: contain;
        border: 1px solid #e2e8f0;
        border-radius: 3px;
        background: #fafafa;
    }
    .img-subcap {
        font-size: 7.5pt;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-weight: 500;
        margin-top: 2pt;
        margin-bottom: 4pt;
        color: #475569;
        text-align: center;
    }
    .figure-caption {
        font-size: 8pt;
        line-height: 1.35;
        color: #334155;
        margin-top: 4pt;
        text-align: justify;
        padding: 0 4pt;
    }
    .page-break-avoid {
        page-break-inside: avoid;
    }
    """
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Beyond Policy Gradients: Empirical Stability, Calibration, and Invariance in Language Model Uncertainty Estimation</title>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
  }},
  svg: {{
    fontCache: 'global'
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
{custom_css}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    
    html_output_path = os.path.join(root_dir, "RESEARCH_PAPER.html")
    pdf_output_path = os.path.join(root_dir, "RESEARCH_PAPER.pdf")
    repo_pdf_path = os.path.join(repo_dir, "RESEARCH_PAPER.pdf")
    
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Generated clean HTML: {html_output_path}")
    
    edge_executable = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_executable):
        edge_executable = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        
    cmd = [
        edge_executable,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={pdf_output_path}",
        "--no-pdf-header-footer",
        html_output_path
    ]
    
    print("Compiling publication PDF via Headless Edge...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_output_path) and os.path.getsize(pdf_output_path) > 1000:
        size_kb = os.path.getsize(pdf_output_path) / 1024
        print(f"Successfully generated PDF: {pdf_output_path} ({size_kb:.1f} KB)")
        
        with open(pdf_output_path, "rb") as src, open(repo_pdf_path, "wb") as dst:
            dst.write(src.read())
        print(f"Copied to repo workspace: {repo_pdf_path}")
    else:
        print("PDF compilation failed.")
        print("STDERR:", res.stderr)

if __name__ == "__main__":
    main()
