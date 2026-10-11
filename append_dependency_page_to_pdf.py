# -*- coding: utf-8 -*-
"""
append_dependency_page_to_pdf.py
Appends a 21st page to 20_Agentic_Skills_Explained_For_4th_Graders.pdf:
- Page 21: "The Master Map: How All 3 Tiers & 20 Skills Fit Together"
- Embeds the crisp, high-resolution three_tier_skill_dependency_graph.png directly on the page!
- Includes 4th-grader friendly callout notes explaining the 3 layers:
  1. Top Floor (Purple): Level 2 Swarms (The Playground Clubhouse Teams)
  2. Middle Floor (Blue): Level 1 Agent Kernel (The Individual Robot Brains)
  3. Ground Floor (Green): Level 0 Physical AWS (The Unbreakable Steel Foundation)
"""

import os
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import generate_20_skills_4th_grader_pdf

PDF_FILENAME = "20_Agentic_Skills_Explained_For_4th_Graders.pdf"
GRAPH_PNG = "three_tier_skill_dependency_graph.png"

def generate_complete_21_page_pdf():
    # 1. First run the standard 20 pages generator
    print("Generating base 20 pages...")
    generate_20_skills_4th_grader_pdf.build_pdf()

    # 2. Open PDF with PyMuPDF to append the 21st Page in crisp landscape format
    import fitz
    doc = fitz.open(PDF_FILENAME)
    print(f"Base doc pages: {len(doc)}")

    # Create temporary PDF for Page 21 (Landscape letter: 792 x 612)
    p21_pdf = "temp_page_21_dependency.pdf"
    c = canvas.Canvas(p21_pdf, pagesize=landscape(letter))
    w, h = landscape(letter) # 792 x 612

    # Background clean white
    c.setFillColor(colors.HexColor("#ffffff"))
    c.rect(0, 0, w, h, stroke=0, fill=1)

    # Top Header Band
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.rect(0, h - 54, w, 54, stroke=0, fill=1)

    # Header Badge
    c.setFillColor(colors.white)
    c.roundRect(24, h - 42, 60, 28, 6, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#7c3aed"))
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(54, h - 33, "MAP")

    # Header Title
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(96, h - 34, "The Master Blueprint: How All 3 Tiers & 20 Skills Connect")

    # Page info on right
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(w - 24, h - 28, "THE COMPLETE 3-TIER STACK")
    c.setFont("Helvetica", 8.5)
    c.drawRightString(w - 24, h - 42, "Summary Page • Page 21 of 21")

    # Sub-header explanation for 4th graders
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(24, h - 74, "How to Read This Map: Bottom-Up Building Blocks!")

    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("Helvetica", 8.5)
    c.drawString(24, h - 88, "Just like a 3-story LEGO building: Ground Floor (Green AWS) holds the locks, Middle Floor (Blue Kernel) is the thinking brain, and Top Floor (Purple Swarm) coordinates the team!")

    # Draw the High-Res Graphic Image (three_tier_skill_dependency_graph.png)
    # Available area: x=24, y=55, w=744, h=445
    img_x = 24
    img_y = 52
    img_w = w - 48 # 744
    img_h = 440

    # Draw border around graphic
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.setLineWidth(1)
    c.roundRect(img_x, img_y, img_w, img_h, 8, stroke=1, fill=0)

    # Embed PNG image
    c.drawImage(GRAPH_PNG, img_x + 2, img_y + 2, width=img_w - 4, height=img_h - 4, preserveAspectRatio=True, anchor='c')

    # Footer Line
    c.setStrokeColor(colors.HexColor("#e2e8f0"))
    c.setLineWidth(1)
    c.line(24, 34, w - 24, 34)

    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(24, 22, "THE 3-TIER ENTERPRISE AGENT STACK -- 20 SKILLS DEPENDENCY BLUEPRINT")
    c.drawRightString(w - 24, 22, "Page 21 of 21 (Final Master Map)")

    c.save()

    # Append to PyMuPDF document
    doc_p21 = fitz.open(p21_pdf)
    doc.insert_pdf(doc_p21)
    doc.save("20_Agentic_Skills_Explained_For_4th_Graders_Full.pdf")
    doc.close()
    doc_p21.close()

    # Replace original PDF
    os.replace("20_Agentic_Skills_Explained_For_4th_Graders_Full.pdf", PDF_FILENAME)
    if os.path.exists(p21_pdf):
        os.remove(p21_pdf)

    print(f"Successfully appended Page 21! Final PDF has 21 pages: {PDF_FILENAME}")

if __name__ == "__main__":
    generate_complete_21_page_pdf()
