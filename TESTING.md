# Time Warp Testing Framework

A comprehensive testing framework for the Time Warp educational programming environment, providing thorough coverage of all features and ensuring code quality, security, and performance.

## 🧪 Test Suite Overview

### Core Test Categories

- **Core Interpreter Tests** (`test_core_interpreter.py`)
  - Variable assignment and interpolation
  - Conditional matching and jumps
  - Subroutine calls and returns
  - Mathematical expressions
  - Program flow control

- **Logo Turtle Graphics Tests** (`test_logo_graphics.py`)
  - Turtle movement and drawing
  - Logo macro definitions
  - Repeat structures and loops
  - Canvas manipulation
  - Complex geometric patterns

- **Modern UI Tests** (`test_modern_ui.py`)
  - Theme system and color schemes
  - Dark/Light mode switching
  - Status bar and notifications
  - Settings and preferences
  - Responsive design elements

- **IoT & Robotics Tests** (`test_iot_robotics.py`)
  - Device discovery and control
  - Sensor data collection and analysis
  - Robot navigation and control
  - Smart home automation
  - Machine learning integration

- **Performance Tests** (`test_performance.py`)
  - Execution speed benchmarks
  - Memory usage optimization
  - Stress testing with large programs
  - Concurrent execution simulation
  - Resource limit enforcement

- **Security Tests** (`test_security.py`)
  - Code injection prevention
  - Eval() security and sandboxing
  - Input validation and sanitization
  - Resource limit enforcement
  - Environment isolation

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Basic Tests

```bash
python test_runner.py --basic
```

### Run Comprehensive Test Suite

```bash
python test_runner.py --comprehensive
```

### Run Complete CI/CD Pipeline

```bash
python test_runner.py --ci
```

## 📊 Test Runner Options

The `test_runner.py` provides multiple testing modes:

```bash
# Basic functionality tests
python test_runner.py --basic

# Comprehensive tests with coverage
python test_runner.py --comprehensive

# Performance benchmarks
python test_runner.py --performance

# Parallel execution (4 workers)
python test_runner.py --parallel 4

# Integration tests only
python test_runner.py --integration

# UI tests only
python test_runner.py --ui

# Stress tests
python test_runner.py --stress

# Security tests
python test_runner.py --security

# Code quality checks
python test_runner.py --quality

# Generate test report
python test_runner.py --report
```

## 🎯 Test Categories and Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.ui` - User interface tests
- `@pytest.mark.performance` - Performance benchmarks
- `@pytest.mark.security` - Security tests
- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.stress` - Stress tests
- `@pytest.mark.hardware` - Hardware integration tests
- `@pytest.mark.iot` - IoT functionality tests
- `@pytest.mark.robotics` - Robotics tests

### Running Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only performance tests
pytest -m performance

# Skip slow tests
pytest -m "not slow"

# Run IoT and robotics tests
pytest -m "iot or robotics"
```

## 📈 Coverage and Reporting

### Coverage Reports

The framework generates comprehensive coverage reports:

- **HTML Coverage Report**: `test_reports/coverage_html/index.html`
- **Terminal Coverage**: Shows missing lines and percentages
- **Coverage Threshold**: Enforces minimum 80% coverage

### Performance Reports

- **Benchmark Report**: `test_reports/benchmark_report.html`
- **Memory Usage**: Tracks memory consumption
- **Execution Time**: Measures performance across operations

### Test Reports

- **HTML Test Report**: `test_reports/test_report.html`
- **Test Summary**: `test_reports/test_summary.md`
- **CI/CD Pipeline Results**: Complete pipeline status

## 🔧 Configuration

### pytest.ini

Comprehensive pytest configuration with:
- Test discovery patterns
- Output formatting
- Coverage settings
- Marker definitions
- Warning filters

### conftest.py

Shared fixtures and utilities:
- `interpreter` - Clean Time Warp interpreter instance
- `mock_output` - Mock output widget for testing
- `headless_ide` - UI instance without actual windows
- `temp_project_dir` - Temporary directory for file operations
- `sample_*_program` - Pre-built test programs
- `mock_hardware` - Hardware simulation for testing

## 🏗️ Test Architecture

### Base Test Class

The `TestCase` class provides utility methods:

```python
class TestCase:
    def run_program_and_capture_output(self, interpreter, program)
    def assert_variables_equal(self, interpreter, expected_vars)
    def assert_turtle_position(self, interpreter, x, y, heading=None)
```

### Fixtures and Mocking

Comprehensive fixture system for:
- Interpreter instances
- UI components (headless)
- Hardware simulation
- File system operations
- Network mocking

### Test Data Management

- Sample programs for different languages (PILOT, Logo, BASIC)
- Complex test scenarios
- Edge cases and error conditions
- Performance test datasets

## 🔒 Security Testing

### Code Injection Prevention

Tests for:
- `eval()` security and sandboxing
- Variable name sanitization
- Expression parsing safety
- Template injection prevention

### Resource Protection

- Memory usage limits
- Execution time limits
- Recursion depth protection
- Infinite loop detection

### Environment Isolation

- File system access prevention
- Network access blocking
- Environment variable isolation
- Import restrictions

## ⚡ Performance Testing

### Benchmarks

- Interpreter startup time
- Program execution speed
- Graphics rendering performance
- Memory usage optimization
- Large program handling

### Stress Testing

- Many iterations and loops
- Large variable sets
- Deep subroutine calls
- Concurrent execution simulation
- Memory leak detection

## 🤖 Hardware and IoT Testing

### Simulation Mode

All hardware tests run in simulation mode:
- Arduino controller simulation
- Raspberry Pi GPIO simulation
- Sensor data simulation
- Robot behavior simulation

### Integration Testing

- Device discovery and control
- Sensor data collection
- Automation workflows
- Multi-device coordination
- Cloud connectivity simulation

## 📋 Test Maintenance

### Adding New Tests

1. Choose appropriate test file based on category
2. Use proper pytest markers
3. Follow naming conventions (`test_*`)
4. Include docstrings explaining test purpose
5. Use fixtures for setup/teardown

### Test Quality Guidelines

- **Arrange-Act-Assert** pattern
- **Independent tests** (no shared state)
- **Descriptive names** explaining what is tested
- **Edge cases** and error conditions
- **Performance considerations**

### Continuous Integration

The framework supports CI/CD integration:
- Automated test execution
- Coverage reporting
- Performance monitoring
- Security scanning
- Quality gate enforcement

## 📚 Examples

### Basic Test Example

```python
def test_variable_assignment(self, interpreter):
    """Test basic variable assignment"""
    program = '''U:X=42
    T:Value is *X*
    END'''
    
    result, output = self.run_program_and_capture_output(interpreter, program)
    assert result == True
    assert 'Value is 42' in output
    self.assert_variables_equal(interpreter, {'X': 42})
```

### Performance Test Example

```python
@pytest.mark.performance
@pytest.mark.benchmark(group="execution")
def test_program_execution_speed(self, benchmark, interpreter):
    """Benchmark program execution speed"""
    program = "T:Hello World!\nEND"
    
    def run_program():
        return interpreter.run_program(program)
    
    result = benchmark(run_program)
    assert result == True
```

### UI Test Example

```python
def test_theme_switching(self, headless_ide):
    """Test theme switching functionality"""
    original_theme = headless_ide.current_theme_name
    
    headless_ide.switch_theme('Ocean')
    assert headless_ide.current_theme_name == 'Ocean'
    
    headless_ide.switch_theme(original_theme)
    assert headless_ide.current_theme_name == original_theme
```

## 🎯 Goals and Benefits

### Quality Assurance

- **Comprehensive Coverage**: Tests all major features and edge cases
- **Regression Prevention**: Catches breaking changes early
- **Performance Monitoring**: Ensures optimal performance
- **Security Validation**: Prevents vulnerabilities

### Development Support

- **Fast Feedback**: Quick test execution for development
- **Clear Reporting**: Detailed reports for debugging
- **CI/CD Integration**: Automated quality gates
- **Documentation**: Self-documenting test suite

### Educational Value

- **Code Examples**: Tests serve as usage examples
- **Best Practices**: Demonstrates testing methodologies  
- **Quality Standards**: Shows professional development practices
- **Learning Tool**: Students can learn from test structure

This testing framework ensures Time Warp maintains high quality, security, and performance standards while supporting educational goals and professional development practices.