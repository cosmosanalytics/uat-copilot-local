# -*- coding: utf-8 -*-
"""
Tests multi-line wrapped nodes in Mermaid to ensure full text is displayed without truncating with '...'.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

test_sentence = "The Ingalls family goes West. A long time ago, before all the cities and towns were built, a family lived in the Big Woods of Wisconsin."

def format_node_text(prefix, full_text, words_per_line=6):
    if not full_text:
        return prefix
    # Remove problematic characters for Mermaid labels
    clean = full_text.replace('"', "'").replace('\\', ' ').strip()
    words = clean.split()
    lines = []
    current_line = []
    for w in words:
        current_line.append(w)
        if len(current_line) >= words_per_line:
            lines.append(' '.join(current_line))
            current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    
    body = '<br/>'.join(lines)
    return f"<b>{prefix}</b><br/>{body}"

print(format_node_text("Setting", test_sentence))
