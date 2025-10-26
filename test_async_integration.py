#!/usr/bin/env python3
"""Test script for asyncio integration in Time Warp IDE"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.async_support import (
    init_async_support,
    get_async_runner,
    AsyncInterpreterRunner,
)
from Time_Warp import TimeWarpInterpreter


async def test_async_execution():
    """Test async program execution"""
    print("Testing asyncio integration...")

    # Initialize async support
    init_async_support()
    runner = get_async_runner()

    # Create interpreter
    interpreter = TimeWarpInterpreter()

    # Create async runner
    async_runner = AsyncInterpreterRunner(interpreter.__class__, runner)

    # Test program
    test_program = [
        "T:Hello from async execution!",
        "U:x=42",
        "T:The value of x is *x*",
        "END",
    ]

    # Execute program asynchronously
    try:
        result = await async_runner.execute_program_async(test_program, {})
        print("✅ Async execution completed successfully")
        print(f"Variables: {result.get('variables', {})}")
        return True
    except Exception as e:
        print(f"❌ Async execution failed: {e}")
        return False


def main():
    """Run the test"""
    print("Time Warp IDE Asyncio Integration Test")
    print("=" * 40)

    # Run async test
    result = asyncio.run(test_async_execution())

    if result:
        print("\n🎉 All tests passed! Asyncio integration is working.")
    else:
        print("\n💥 Tests failed. Check the implementation.")


if __name__ == "__main__":
    main()
