import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.grader.grader import grade_exact_match, grade_math, extract_tags

def test_exact_match():
    assert grade_exact_match("The Great Gatsby", "great gatsby")
    assert grade_exact_match("Arthur's Magazine", "Arthur's Magazine")
    assert grade_exact_match("  hello , world! ", "hello world")
    assert not grade_exact_match("Arthur", "Arthur's Magazine")

def test_math_verify():
    assert grade_math("10", "10")
    assert grade_math("10.0", "10")
    assert grade_math("1/2", "0.5")
    assert grade_math(r"\frac{1}{2}", "0.5")
    assert not grade_math("10", "11")

def test_extract_tags():
    sample = """<think>
Step 1: Check the two magazines.
Step 2: Compare dates.
</think>
<answer>
Arthur's Magazine
</answer>
<analysis>
Paragraph 4 confirms 1844, Paragraph 5 confirms 1989. Both relevant paragraphs are present.
</analysis>
<confidence>
95%
</confidence>"""

    extracted = extract_tags(sample)
    assert extracted["answer"] == "Arthur's Magazine"
    assert "Step 1" in extracted["think"]
    assert "Paragraph 4" in extracted["analysis"]
    assert extracted["confidence"] == "95%"
    assert pytest.approx(extracted["confidence_float"]) == 0.95
