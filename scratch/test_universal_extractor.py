# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

sample_gatsby = """In my younger and more vulnerable years my father gave me some advice that I have been turning over in my mind ever since.
Whenever you feel like criticizing any one, he told me, just remember that all the people in this world have not had the advantages that you have had.
In consequence, I am inclined to reserve all judgements, a habit that has opened up many curious natures to me and also made me the victim of not a few veteran bores.
Reserving judgements is a matter of infinite hope. I am still a little afraid of missing something if I forget that a sense of the fundamental decencies is parcelled out unequally at birth.
And, after boasting this way of my tolerance, I come to the admission that it has a limit. Conduct may be founded on the hard rock or the wet marshes, but after a certain point I do not care what it is founded on.
When I came back from the East last autumn I felt that I wanted the world to be in uniform and at a sort of moral attention forever; I wanted no more riotous excursions with privileged glimpses into the human heart.
Only Gatsby, the man who gives his name to this book, was exempt from my reaction — Gatsby, who represented everything for which I have an unaffected scorn."""

def extract_universal_invariants(raw_text):
    text = re.sub(r'\[.*?\]\(.*?\)|<.*?>', '', raw_text)
    paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 30]
    sentences = []
    for p in paragraphs:
        for s in re.split(r'(?<=[.!?])\s+', p):
            s = s.strip()
            if len(s) > 20:
                sentences.append(s)
    
    bounds = [s for s in sentences if re.search(r'\b\d+(\.\d+)?\b|\bhours?\b|\bminutes?\b|\bpercent|\$|million|thousand|limit|unequally\b', s, re.I)]
    negations = [s for s in sentences if re.search(r'\bnever\b|\bprohibited\b|\bnot\b|\bno more\b|\bexempt\b|\bcannot\b|\bmust\b|\bshall\b|\blimit\b', s, re.I)]
    settings = [s for s in sentences if re.search(r'\bworld\b|\bcity\b|\beast\b|\bwest\b|\bmountain\b|\bhouse\b|\bland\b|\bplace\b|\bvillage\b', s, re.I)]
    
    print('Total sentences:', len(sentences))
    print('\nBounds candidates:')
    for b in bounds[:3]:
        print(' -', b)
    print('\nNegations / Invariants candidates:')
    for n in negations[:3]:
        print(' -', n)
    print('\nSettings / Context candidates:')
    for st in settings[:3]:
        print(' -', st)

extract_universal_invariants(sample_gatsby)
