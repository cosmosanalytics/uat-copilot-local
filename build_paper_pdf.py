"""
Render high-fidelity academic PDF for:
Agentic Model Predictive Control Paper
Using headless Edge with complete KaTeX math rendering, Mermaid diagrams, and typography.
"""

import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions

def generate_pdf():
    html_path = os.path.abspath("agentic_mpc_paper.html")
    pdf_path = os.path.abspath("agentic_mpc_paper.pdf")
    
    print(f"Loading source HTML: {html_path}")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--allow-file-access-from-files')
    options.add_argument('--enable-local-file-accesses')
    options.add_argument('--window-size=1280,1800')

    driver = webdriver.Edge(options=options)
    try:
        driver.get(f"file:///{html_path.replace(os.sep, '/')}")
        
        # Ensure light mode is forced for printing and remove web-only top navbar
        driver.execute_script("""
            document.documentElement.setAttribute('data-theme', 'light');
            const nav = document.getElementById('top-nav');
            if (nav) nav.remove();
        """)
        
        # Wait for KaTeX and Mermaid scripts to finish executing
        time.sleep(4)
        
        print_options = PrintOptions()
        print_options.background = True
        print_options.margin_top = 0.8
        print_options.margin_bottom = 0.8
        print_options.margin_left = 0.8
        print_options.margin_right = 0.8
        
        pdf_base64 = driver.print_page(print_options)
        pdf_bytes = base64.b64decode(pdf_base64)
        
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
            
        print(f"Successfully generated PDF at: {pdf_path} (size: {len(pdf_bytes)} bytes)")
    finally:
        driver.quit()

if __name__ == '__main__':
    generate_pdf()
