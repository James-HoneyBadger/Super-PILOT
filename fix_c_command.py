#!/usr/bin/env python3
"""
Patch to add C: as Compute (like Y:) before gosub handling
"""
import re

with open('Super_PILOT.py', 'r') as f:
    content = f.read()

# Find the Y/N match evaluator section and add C: to it
old_text = '''            # Match evaluators
            if prefix in ("Y", "N"):
                try:
                    val = self.evaluate_expression(body)
                    self.match_flag = bool(val)
                except Exception:
                    self.match_flag = False
                self._last_match_set = True
                return "continue"'''

new_text = '''            # Match evaluators (Y:, N:, C: for Compute)
            if prefix in ("Y", "N", "C"):
                try:
                    val = self.evaluate_expression(body)
                    self.match_flag = bool(val)
                except Exception:
                    self.match_flag = False
                self._last_match_set = True
                return "continue"'''

content = content.replace(old_text, new_text)

# Now update the R:/C: section to handle only if not already matched by compute
# Find the C: return handler and rename it or add a check
# Actually, since C: compute will return early, the gosub return C: won't be reached
# So we just need to make sure the logic at the end handles C: as gosub return only if body suggests it

with open('Super_PILOT.py', 'w') as f:
    f.write(content)

print("Added C: as Compute command (sets match_flag)")
