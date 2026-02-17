import pytest
import logging

from robot_arm_tests.helpers.file_parser import parse_output_file, get_expected_and_error_coords_from_input_file, \
    log_test_results_to_file
from robot_arm_tests.tests.conftest import PATH_TO_TEST_DIR


class TestRobotArm:

    logger = logging.getLogger("TestRobotArm")

    test_data = [
        ("system_input_all_points_within_bound.txt", None),
        ("system_input_mix_coords.txt", None),
        ("system_input_with_outside_points.txt", None),
        ("system_input_without_boundry_rectangle.txt", "ValueError"),
        ("system_input_with_invalid_boundry.txt", "ValueError"),
        ("system_input_with_invalid_file_type.pdf", "ValueError"),
        ("file_not_found.txt", FileNotFoundError.__name__)
    ]

    @pytest.mark.parametrize("input_file, error", test_data)
    def test_robot_arm_valid_input_file(self, run_robot_arm, test_result_file,
                                        input_file,
                                        error):

        result = run_robot_arm(f"{PATH_TO_TEST_DIR}/resources/{input_file}")

        if error:
            log_test_results_to_file(test_result_file, None, None, None, None, "Fail")

            try:
                assert result.returncode == 1, f"Process should have failed with return code 1, but got {result.returncode}. Stderr: {result.stderr}"
                assert result.stderr.find(error) != -1, f"Expected '{error}' in stderr, but got: {result.stderr}"
            except AssertionError as e:
                self.logger.error(f"Test failed for input file {input_file}. Expected error: {error}, but got return code: {result.returncode} and stderr: {result.stderr}")
                raise e
            return

        expected_visited_coords, expected_error_coords = get_expected_and_error_coords_from_input_file(input_file)

        assert result.returncode == 0, f"Process should have succeeded with return code 0, but got {result.returncode}. Stderr: {result.stderr}"
        result_stdout = result.stdout.strip()
        assert result_stdout.find("Robot arm system completed.") != -1, \
            f"Expected 'Robot arm system completed.' in stdout, but got '{result.stdout.strip()}'"

        # Extract output file from stdout
        output_file = result_stdout.split("system completed, output is stored in the ")[1]
        assert output_file, "Output file name should be present in the stdout"

        # Extract actual visited_coords and error_coords from the extracted output file
        visited_coords, error_coords = parse_output_file(output_file)

        try:
            assert visited_coords == expected_visited_coords, \
                f"Expected visited coordinates {expected_visited_coords}, but got {visited_coords}"
            assert error_coords == expected_error_coords, \
                f"Expected error coordinates {expected_error_coords}, but got {error_coords}"
            log_test_results_to_file(test_result_file,
                                     expected_visited_coords,
                                     visited_coords,
                                     expected_error_coords,
                                     error_coords,
                                     "Pass")
        except AssertionError as e:
            log_test_results_to_file(test_result_file,
                                     expected_visited_coords,
                                     visited_coords,
                                     expected_error_coords,
                                     error_coords,
                                     "Fail")
            self.logger.error(f"Test failed for input file {input_file}. "
                         f"Expected visited coordinates: {expected_visited_coords}, "
                         f"Actual visited coordinates: {visited_coords}. "
                         f"Expected error coordinates: {expected_error_coords}, "
                         f"Actual error coordinates: {error_coords}")
            raise e
