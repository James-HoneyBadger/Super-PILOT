#!/usr/bin/env python3
"""
Refine C: to handle both Compute (with expression) and Return (empty)
"""

with open('Super_PILOT.py', 'r') as f:
    content = f.read()

# Replace the C: gosub return section to check if body exists
old_c_return = '''            if prefix == "C":
                if self.stack:
                    return f"jump:{self.stack.pop()}"
                return "continue"'''

new_c_handling = '''            if prefix == "C":
                # C: with expression = Compute (set match_flag)
                # C: without expression = Return from gosub
                if body.strip():
                    try:
                        val = self.evaluate_expression(body)
                        self.match_flag = bool(val)
                    except Exception:
                        self.match_flag = False
                    self._last_match_set = True
                    return "continue"
                else:
                    # Empty C: = return from gosub
                    if self.stack:
                        return f"jump:{self.stack.pop()}"
                    return "continue"'''

content = content.replace(old_c_return, new_c_handling)

with open('Super_PILOT.py', 'w') as f:
    f.write(content)

print("Updated C: to handle both Compute (with expr) and Return (empty)")
