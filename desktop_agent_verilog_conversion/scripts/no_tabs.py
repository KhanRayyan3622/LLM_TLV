#! /usr/bin/env python3

# Replace tabs with spaces in the given file (default wip.tlv).
# The most common tab widths are 2, 4, and 8 spaces. We take these as assumptions and
# test each, scoring it, and going with the best score.
#
# We use two indicators of indentation:
# 1. Lines following ones ending in "begin" should be indented.
# 2. // comments on successive lines are likely to be indented the same amount.
#
# For each tab width, we keep:
# 1. A dictionary of indentation depths after begin lines (indent_depth_cnt).
# 2. A count of how many lines have consistent //-comment indentation on successive lines (comment_cnt).
#
# For each assumption, we determine the highest value in its indent_depth_cnt (for any
# indentation depth) (max_cnt).
#
# An overall score is calculated for each assumption as:
#   score = max_cnt * DEPTH_WEIGHT + comment_cnt
#
# The assumption with the highest score is used to replace tabs with spaces.

import sys
import re
from collections import defaultdict


def score_file(lines, tab_width):
  DEPTH_WEIGHT = 4
  BEGIN_RE = re.compile(r".*\bbegin\s*(:\s*\w+\s*)?(//.*)?$")  # Match lines ending in "begin" (possibly followed by a name (: name) and a possible comment)
  INDENTATION_RE = re.compile(r"^(?P<indent>\s*)\S")
  COMMENT_RE = re.compile(r"^(?P<pre>.*)//")
  TAB_RE = re.compile(r'^(?P<pre>[^\t]*)\t(?P<post>.*)$')

  # Running counts:
  comment_cnt = 0  # Count of matching comment indentations
  align_cnt = 0  # Count of matching whitespace end alignments
  indent_depth_cnt = defaultdict(int)  # [1] is the number of times 'begin' resulted in an indentation increase of 1, etc.
  
  # For comparison between lines:
  comment_indent = -1   # -1 for no comment
  prev_comment_indent = -1
  whitespace_end = []   # Positions in the line at which a string of multiple whitespaces ends.
  prev_whitespace_end = []
  indentation = None
  prev_indentation = None
  after_begin = False
  # Bias more popular tab widths by initializing comment_cnt (which has lower weight than indent_depth_cnt).
  comment_cnt = 2 if tab_width == 4 else 1 if tab_width in (2, 8) else 0
  for line in lines:
    # From previous line
    prev_indentation = indentation
    prev_comment_indent = comment_indent
    prev_whitespace_end = whitespace_end

    # Replace tabs in line with spaces according to tab_width
    # For each tab, replace with enough spaces to reach the next tab stop
    while m := re.match(TAB_RE, line):
      if m is not None:
        align = len(m.group("pre")) % tab_width
        spaces = tab_width - align
        line = line.replace('\t', ' ' * spaces, 1)
    
    # Get indentation of this line (if any)
    indentation = INDENTATION_RE.match(line).group("indent") if INDENTATION_RE.match(line) else None

    # Increment count for begin indentation depth
    if after_begin and indentation is not None and prev_indentation is not None:
      # Add a count to this indentation depth
      ind = len(indentation) - len(prev_indentation)
      if ind > 0:
        indent_depth_cnt[ind] += 1

    # Increment count for matching comment indentation
    comment_match = COMMENT_RE.match(line)
    if comment_match is not None:
      comment_indent = len(comment_match.group("pre"))
      if comment_indent == prev_comment_indent:
        comment_cnt += 1
    else:
      comment_indent = -1

    # Find ends of whitespace runs
    whitespace_end = [m.end() for m in re.finditer(r'\s{2,}', line)]
    # Increment count for matching whitespace runs
    for wend in whitespace_end:
      if wend in prev_whitespace_end:
        align_cnt += 1
    
    after_begin = bool(BEGIN_RE.match(line))
  
  # Score this tab width
  # Number of begins with proper indentation (for the maximal assumption of "proper") +
  #    number of aligned comments + number of aligned whitespace runs (which double counts comments)
  max_cnt = max(indent_depth_cnt.values()) if indent_depth_cnt else 0
  print(f"Tab width {tab_width}: max begin indent count {max_cnt}, comment count {comment_cnt}, align count {align_cnt}, total score {max_cnt * DEPTH_WEIGHT + comment_cnt + align_cnt}")
  return max_cnt * DEPTH_WEIGHT + comment_cnt + align_cnt


def replace_tabs(lines, tab_width):
  new_lines = []
  for line in lines:
    while m := re.match(r'^(?P<pre>[^\t]*)\t(?P<post>.*)$', line):
        align = len(m.group("pre")) % tab_width
        spaces = tab_width - align
        line = line.replace('\t', ' ' * tab_width)
    new_lines.append(line)
  return new_lines


def main():
  TAB_WIDTHS = [2, 3, 4, 6, 8]
  FILENAME = "wip.tlv" if len(sys.argv) < 2 else sys.argv[1]

  with open(FILENAME, "r") as f:
    lines = f.readlines()

  tab_count = sum(line.count('\t') for line in lines)

  # Early exit if too few tabs
  if tab_count < 3:
    print(f"{tab_count} tabs found in {FILENAME}; not replacing.")
    return 0

  # Score each tab width
  # Determine the best and second-best scores
  scores = {}
  best_tab_width = None
  best_score = -1
  second_best_score = -1
  for tab_width in TAB_WIDTHS:
    score = score_file(lines, tab_width)
    scores[tab_width] = score
    if score > best_score:
      second_best_score = best_score
      best_score = score
      best_tab_width = tab_width
    elif score > second_best_score:
      second_best_score = score
  print(f"Scores: {scores}, best: {best_tab_width}-wide with score {best_score}, second best: {second_best_score}")

  # If the best score isn't better than the next best by at least 2 + tab-count/20,
  # do not substitute.
  if best_score < second_best_score + 2 + tab_count / 20:
    print(f"It is not clear which tab width is best; not replacing tabs in {FILENAME}.")
    return 0

  new_lines = replace_tabs(lines, best_tab_width)

  with open(FILENAME, "w") as f:
    f.writelines(new_lines)
  print(f"Replaced tabs with {best_tab_width} spaces in {FILENAME}")
  return 0

if __name__ == "__main__":
  sys.exit(main())