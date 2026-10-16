#!/usr/bin/env python3
"""locate_lines.py — locate phrases in an acmart PDF and report margin line numbers.

Implements the "line-number anchor" method described in the chi-review skill (§5):
pymupdf search_for(phrase) -> line rect y-center -> nearest pure-number span in
the left margin (x1 < 60pt, the red manuscript line numbers) with |dy| < 7pt.

Usage / 用法:
    python locate_lines.py paper.pdf "phrase one" "phrase two" ...

Output / 输出:
    One line per hit:  p.<page> L<line>  "<phrase>"  <snippet>
    Phrases that straddle a line break with no margin number in range are
    reported as NO-LINE (fall back to section anchors per §5: a wrong line
    number hurts credibility more than no line number).

Requires: Python 3.8+, pymupdf>=1.24
"""
import sys

import pymupdf

MARGIN_GAP = 2          # pt; a margin number's x1 may slightly exceed the line x0
Y_TOLERANCE = 7.0       # pt; vertical tolerance when pairing number <-> line


def locate(doc, phrase):
    hits = []
    for pno, page in enumerate(doc, start=1):
        for rect in page.search_for(phrase):
            y = (rect.y0 + rect.y1) / 2
            best, best_dy = None, Y_TOLERANCE
            for b in page.get_text("words"):
                x0, yy0, x1, yy1, word = b[:5]
                # acmart puts line numbers in the left margin of EACH column,
                # i.e. to the left of the hit line, not at a fixed x.
                if x1 > rect.x0 + MARGIN_GAP or not word.isdigit():
                    continue
                dy = abs((yy0 + yy1) / 2 - y)
                if dy < best_dy:
                    best, best_dy = word, dy
            snippet = page.get_textbox(
                pymupdf.Rect(max(0, rect.x0 - 4), rect.y0 - 1, page.rect.x1, rect.y1 + 1)
            ).replace("\n", " ").strip()
            hits.append((pno, best, snippet[:90]))
    return hits


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    doc = pymupdf.open(sys.argv[1])
    for phrase in sys.argv[2:]:
        hits = locate(doc, phrase)
        if not hits:
            print(f'NOT FOUND   "{phrase}"')
        for pno, line, snippet in hits:
            label = f"p.{pno} L{line}" if line else f"p.{pno} NO-LINE"
            print(f'{label:14s} "{phrase}"  {snippet}')


if __name__ == "__main__":
    main()
