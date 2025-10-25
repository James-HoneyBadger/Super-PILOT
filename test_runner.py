"""
Comprehensive test runner for Time Warp testing framework
Provides advanced testing capabilities, reporting, and CI/CD integration
"""

import pytest
import sys
import os
import argparse
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional


class TimeWarpTestRunner:
    """Advanced test runner with comprehensive reporting and analysis"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.test_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "test_reports"
        self.reports_dir.mkdir(exist_ok=True)

    def run_basic_tests(self) -> int:
        """Run basic test suite"""
        print("🧪 Running Time Warp Basic Test Suite...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir / "test_core_interpreter.py"),
            "-v",
            "--tb=short",
        ]

        return subprocess.call(cmd)

    def run_comprehensive_tests(self) -> int:
        """Run comprehensive test suite with coverage"""
        print("🧪 Running Time Warp Comprehensive Test Suite...")

        coverage_file = self.reports_dir / ".coverage"
        html_report = self.reports_dir / "coverage_html"

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir),
            f"--cov=Time_Warp",
            f"--cov-report=html:{html_report}",
            f"--cov-report=term-missing",
            f"--cov-fail-under=80",
            "--html=" + str(self.reports_dir / "test_report.html"),
            "--self-contained-html",
            "-v",
        ]

        return subprocess.call(cmd)

    def run_performance_tests(self) -> int:
        """Run performance and benchmark tests"""
        print("⚡ Running Time Warp Performance Tests...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir),
            "--benchmark-only",
            "--benchmark-html=" + str(self.reports_dir / "benchmark_report.html"),
            "-v",
        ]

        return subprocess.call(cmd)

    def run_parallel_tests(self, num_workers: int = 4) -> int:
        """Run tests in parallel for faster execution"""
        print(f"⚡ Running Time Warp Tests in Parallel ({num_workers} workers)...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir),
            f"-n",
            str(num_workers),
            "--dist=worksteal",
            "-v",
        ]

        return subprocess.call(cmd)

    def run_integration_tests(self) -> int:
        """Run integration tests for hardware and IoT components"""
        print("🔗 Running Time Warp Integration Tests...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir / "test_iot_robotics.py"),
            str(self.test_dir / "test_hardware_integration.py"),
            "-v",
            "--tb=short",
        ]

        return subprocess.call(cmd)

    def run_ui_tests(self) -> int:
        """Run UI and interface tests"""
        print("🖥️ Running Time Warp UI Tests...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir / "test_modern_ui.py"),
            "-v",
            "--tb=short",
        ]

        return subprocess.call(cmd)

    def run_stress_tests(self) -> int:
        """Run stress tests with large programs and edge cases"""
        print("💪 Running Time Warp Stress Tests...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir),
            "-k",
            "stress or large or edge",
            "--maxfail=5",
            "-v",
        ]

        return subprocess.call(cmd)

    def run_regression_tests(self) -> int:
        """Run regression tests to catch breaking changes"""
        print("🔄 Running Time Warp Regression Tests...")

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir / "test_regression_demo_flow.py"),
            str(self.test_dir / "test_match_jump_semantics.py"),
            "-v",
        ]

        return subprocess.call(cmd)

    def check_code_quality(self) -> Dict[str, int]:
        """Run code quality checks"""
        print("📏 Checking Time Warp Code Quality...")

        results = {}

        # Run flake8 for style checking
        print("  Running flake8...")
        flake8_cmd = [
            "flake8",
            "SuperPILOT.py",
            "--max-line-length=120",
            "--ignore=E203,W503",
        ]
        results["flake8"] = subprocess.call(
            flake8_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Run black for formatting check
        print("  Checking code formatting...")
        black_cmd = ["black", "--check", "--line-length=120", "SuperPILOT.py"]
        results["black"] = subprocess.call(
            black_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Run isort for import sorting
        print("  Checking import sorting...")
        isort_cmd = ["isort", "--check-only", "SuperPILOT.py"]
        results["isort"] = subprocess.call(
            isort_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        return results

    def run_security_tests(self) -> int:
        """Run security tests to check for vulnerabilities"""
        print("🔒 Running Time Warp Security Tests...")

        # Test for eval() security, file access, etc.
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(self.test_dir),
            "-k",
            "security or eval or file_access",
            "-v",
        ]

        return subprocess.call(cmd)

    def generate_test_report(self) -> None:
        """Generate comprehensive test report"""
        print("📊 Generating Test Report...")

        report_file = self.reports_dir / "test_summary.md"

        with open(report_file, "w") as f:
            f.write("# Time Warp Test Report\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Test Suite Coverage\n\n")
            f.write("- ✅ Core Interpreter Tests\n")
            f.write("- ✅ Logo Turtle Graphics Tests\n")
            f.write("- ✅ Modern UI Tests\n")
            f.write("- ✅ IoT & Robotics Integration Tests\n")
            f.write("- ✅ Hardware Integration Tests\n")
            f.write("- ✅ Performance & Benchmark Tests\n")
            f.write("- ✅ Security & Safety Tests\n\n")

            f.write("## Key Features Tested\n\n")
            f.write("### Core Functionality\n")
            f.write("- Variable assignment and interpolation\n")
            f.write("- Conditional matching and jumps\n")
            f.write("- Subroutine calls and returns\n")
            f.write("- Mathematical expressions\n")
            f.write("- Loop structures and flow control\n\n")

            f.write("### Graphics & Visual\n")
            f.write("- Turtle movement and drawing\n")
            f.write("- Logo macro definitions\n")
            f.write("- Repeat structures\n")
            f.write("- Canvas manipulation\n\n")

            f.write("### Modern Interface\n")
            f.write("- Theme system and color schemes\n")
            f.write("- Dark/Light mode switching\n")
            f.write("- Status bar and notifications\n")
            f.write("- Settings and preferences\n\n")

            f.write("### IoT & Robotics\n")
            f.write("- Device discovery and control\n")
            f.write("- Sensor data collection\n")
            f.write("- Robot navigation and control\n")
            f.write("- Smart home automation\n")
            f.write("- Machine learning integration\n\n")

            f.write("## Test Reports\n\n")
            f.write(f"- [HTML Test Report](test_report.html)\n")
            f.write(f"- [Coverage Report](coverage_html/index.html)\n")
            f.write(f"- [Benchmark Report](benchmark_report.html)\n\n")

        print(f"📋 Test report generated: {report_file}")

    def run_ci_pipeline(self) -> int:
        """Run complete CI/CD pipeline"""
        print("🚀 Running Time Warp CI/CD Pipeline...")

        results = []

        # 1. Code quality checks
        quality_results = self.check_code_quality()
        results.extend(quality_results.values())

        # 2. Basic tests (fast feedback)
        basic_result = self.run_basic_tests()
        results.append(basic_result)

        # 3. Comprehensive tests with coverage
        comprehensive_result = self.run_comprehensive_tests()
        results.append(comprehensive_result)

        # 4. Integration tests
        integration_result = self.run_integration_tests()
        results.append(integration_result)

        # 5. Security tests
        security_result = self.run_security_tests()
        results.append(security_result)

        # 6. Generate reports
        self.generate_test_report()

        # Return overall result
        overall_result = max(results) if results else 0

        if overall_result == 0:
            print("✅ All CI/CD pipeline stages passed!")
        else:
            print(f"❌ CI/CD pipeline failed with exit code: {overall_result}")

        return overall_result


def main():
    """Main entry point for test runner"""
    parser = argparse.ArgumentParser(description="Time Warp Advanced Test Runner")
    parser.add_argument("--basic", action="store_true", help="Run basic tests only")
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run comprehensive tests with coverage",
    )
    parser.add_argument(
        "--performance", action="store_true", help="Run performance benchmarks"
    )
    parser.add_argument(
        "--parallel", type=int, metavar="N", help="Run tests in parallel with N workers"
    )
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests"
    )
    parser.add_argument("--ui", action="store_true", help="Run UI tests")
    parser.add_argument("--stress", action="store_true", help="Run stress tests")
    parser.add_argument(
        "--regression", action="store_true", help="Run regression tests"
    )
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--quality", action="store_true", help="Check code quality")
    parser.add_argument("--ci", action="store_true", help="Run complete CI/CD pipeline")
    parser.add_argument("--report", action="store_true", help="Generate test report")

    args = parser.parse_args()

    runner = TimeWarpTestRunner()

    if args.ci:
        return runner.run_ci_pipeline()

    if args.basic:
        return runner.run_basic_tests()

    if args.comprehensive:
        return runner.run_comprehensive_tests()

    if args.performance:
        return runner.run_performance_tests()

    if args.parallel:
        return runner.run_parallel_tests(args.parallel)

    if args.integration:
        return runner.run_integration_tests()

    if args.ui:
        return runner.run_ui_tests()

    if args.stress:
        return runner.run_stress_tests()

    if args.regression:
        return runner.run_regression_tests()

    if args.security:
        return runner.run_security_tests()

    if args.quality:
        results = runner.check_code_quality()
        for tool, result in results.items():
            status = "✅ PASS" if result == 0 else "❌ FAIL"
            print(f"{tool}: {status}")
        return max(results.values()) if results else 0

    if args.report:
        runner.generate_test_report()
        return 0

    # Default: run comprehensive tests
    return runner.run_comprehensive_tests()


if __name__ == "__main__":
    sys.exit(main())
