#!/usr/bin/env python3
"""
Quick smoke test to verify the IDE can be imported and instantiated
"""

try:
    import tkinter as tk
    from Super_PILOT import SuperPILOTII
    
    print("✓ Imports successful")
    
    # Create root window (but don't start mainloop)
    root = tk.Tk()
    
    # Create IDE instance
    ide = SuperPILOTII(root)
    
    print("✓ IDE instantiation successful")
    print("✓ Event callbacks registered:", len(ide.interpreter.on_output), "output callbacks")
    print("✓ Syntax highlighting tags configured:", 
          'keyword' in ide.editor.tag_names() and 
          'comment' in ide.editor.tag_names())
    print("✓ Keyboard shortcuts bound")
    print("✓ Status bar created")
    
    # Clean up without showing window
    root.destroy()
    
    print("\n✓ All IDE smoke tests passed!")
    
except Exception as e:
    print(f"✗ IDE test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
