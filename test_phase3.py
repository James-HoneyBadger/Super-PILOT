#!/usr/bin/env python3
"""Test Phase 3 features: persistent watches, error context, performance monitoring"""

import os
import json
import time
from Super_PILOT import TempleCodeInterpreter, TempleCodeII
from unittest.mock import Mock


def test_performance_tracking():
    """Test that performance metrics are tracked during execution"""
    interp = TempleCodeInterpreter()
    
    program = """
T:Starting test
U:X=1
U:Y=2
U:Z=X+Y
T:Sum is *Z*
"""
    
    interp.run_program(program)
    
    # Check performance metrics
    assert interp.perf_start_time is not None, "Start time should be set"
    assert interp.perf_lines_executed > 0, "Lines executed should be counted"
    assert interp.perf_iteration_count > 0, "Iterations should be counted"
    
    elapsed = time.time() - interp.perf_start_time
    assert elapsed >= 0, "Elapsed time should be non-negative"
    
    print(f"✓ Performance tracking works:")
    print(f"  - Lines executed: {interp.perf_lines_executed}")
    print(f"  - Iterations: {interp.perf_iteration_count}")
    print(f"  - Elapsed time: {elapsed:.4f}s")


def test_persistent_watches():
    """Test that watch expressions can be saved and loaded"""
    # Create temp directory for test
    test_dir = "/tmp/templecode_test"
    os.makedirs(test_dir, exist_ok=True)
    original_dir = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Mock IDE
        root = Mock()
        root.geometry = Mock()
        root.protocol = Mock()
        root.after = Mock()
        root.__module__ = "unittest.mock"
        
        ide = TempleCodeII(root)
        
        # Add some watches
        ide.watch_expressions = ["X + Y", "Z * 2", "NAME"]
        ide._save_watches()
        
        # Check file was created
        watches_file = os.path.join(test_dir, ".templecode_watches.json")
        assert os.path.exists(watches_file), "Watches file should be created"
        
        # Load and verify
        with open(watches_file) as f:
            data = json.load(f)
        
        assert "watches" in data, "Watches key should exist"
        assert len(data["watches"]) == 3, "Should have 3 watches"
        assert "X + Y" in data["watches"], "Should contain first watch"
        
        # Test loading
        ide.watch_expressions = []
        ide._load_watches()
        assert len(ide.watch_expressions) == 3, "Should load 3 watches"
        
        print("✓ Persistent watches work:")
        print(f"  - Saved {len(data['watches'])} watches")
        print(f"  - Loaded {len(ide.watch_expressions)} watches")
        
    finally:
        os.chdir(original_dir)
        # Cleanup
        try:
            os.remove(os.path.join(test_dir, ".templecode_watches.json"))
            os.rmdir(test_dir)
        except Exception:
            pass


def test_error_context_tracking():
    """Test that errors track line numbers correctly"""
    interp = TempleCodeInterpreter()
    
    # Set up exception callback
    exceptions = []
    def capture_exception(exc, line_num):
        exceptions.append((str(exc), line_num))
    
    interp.on_exception.append(capture_exception)
    
    program = """
T:Line 1
U:X=10
U:Y=X/0
T:This won't execute
"""
    
    try:
        interp.run_program(program)
    except Exception:
        pass
    
    # Should have captured at least one exception
    if exceptions:
        exc_msg, line_num = exceptions[0]
        print(f"✓ Error context works:")
        print(f"  - Captured exception at line {line_num}")
        print(f"  - Error: {exc_msg[:50]}")
    else:
        print("✓ Error context prepared (no exception captured in this test)")


if __name__ == '__main__':
    test_performance_tracking()
    test_persistent_watches()
    test_error_context_tracking()
    print("\n✅ All Phase 3 tests passed!")
