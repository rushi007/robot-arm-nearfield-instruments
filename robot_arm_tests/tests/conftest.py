import subprocess
import os
import time
from pathlib import Path

import pytest

PATH_TO_ROOT = Path(__file__).parent.parent.parent
PATH_TO_TEST_DIR = Path(__file__).parent.parent

# Fixture to run the robot arm system with a given input file and capture the output for assertions in the tests
# The fixture returns a function that can be called with the input file path to execute the robot arm system,
# and return the result of the subprocess execution
# The fixture is scoped to "function" so that it can be used in multiple test cases without interference,
# and it ensures that the robot arm system is executed in a clean environment for each test case
@pytest.fixture(scope="function")
def run_robot_arm():
    def _run_robot_arm(input_file):
        # Make input_file path absolute if it's relative
        if not os.path.isabs(input_file):
            input_file = os.path.join(PATH_TO_ROOT, input_file)

        result = subprocess.run(
            ["python", "-m", "app.main", input_file],
            capture_output=True,
            text=True,
            cwd=PATH_TO_ROOT
        )
        # assert result.returncode == 0, f"Process failed with return code {result.returncode}. Stderr: {result.stderr}"
        return result
    return _run_robot_arm

# Fixture to create a test results file for logging test results,
# the fixture is scoped to "session" so that it creates a single test results file for the entire test session.
@pytest.fixture(scope="session")
def test_result_file():
    """Fixture to create a test results file for logging test results"""
    test_result_file_name = f"test_results_{time.time()}.txt"
    test_result_file_path = f"{PATH_TO_TEST_DIR}/output/{test_result_file_name}"
    # Create the test results file if it doesn't exist, otherwise clear its content
    with open(test_result_file_path, 'w') as f:
        f.write("Expected Visited Points\tActual Visited Points\tExpected Error Point\tActual Error Point\tTest Result\n")
    return test_result_file_path
