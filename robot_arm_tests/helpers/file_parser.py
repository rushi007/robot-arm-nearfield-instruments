import ast
import warnings

from robot_arm_tests.tests.conftest import PATH_TO_ROOT, PATH_TO_TEST_DIR


# Output file parser method to be used in the tests to parse the output file
# and extract the visited points and error points for assertions
def parse_output_file(output_file_path):
    try:
        with open(f"{PATH_TO_ROOT}/{output_file_path}", 'r') as f:
            output_content = [line.strip() for line in f]
            error_line_index = output_content.index("error")
            visited_points = output_content[0:error_line_index]
            visited_coords = [ast.literal_eval(ln) for ln in visited_points if ln.strip()]

            error_points = output_content[error_line_index + 1:]
            error_coords = [ast.literal_eval(ln) for ln in error_points if ln.strip()]
    except (FileNotFoundError) as e:
        raise FileNotFoundError(f"Output file {output_file_path} not found")
    except (Exception) as e:
        raise ValueError(f"Failed to parse output file: {output_file_path}")
    return visited_coords, error_coords

# Method to extract the Rectangle coordinates from the input file and validate them,
# the method returns the Rectangle coordinates if they are valid, otherwise it returns None and logs a warning
# The method checks for the presence of the "Rectangle" keyword in the input file, and if found, it attempts to parse the next line as a list of coordinates.
def get_boundry_rectangle(file_lines):
    rectangle_index = file_lines.index("Rectangle")
    points = None
    xs = set()
    ys = set()
    try:
        points = ast.literal_eval(file_lines[rectangle_index+1])
    except Exception as e:
        warnings.warn(f"Invalid Rectangle coordinates input, the system will not be able to determine the work area and will skip all points. {e}")
        return None

    if rectangle_index == -1:
        warnings.warn("No Rectangle specified in the input file, the system will not be able to determine the work area and will skip all points.")
        return None
    if len(points) != 4:
        warnings.warn("Invalid number of coordinates specified for the Rectangle, the system will not be able to determine the work area and will skip all points.")
        return None
    for p in points:
        xs.add(p[0])
        ys.add(p[1])
        if not (isinstance(p, tuple) and len(p) == 2):
            warnings.warn(f"Invalid coordinate format for the given Rectangle: {p}, the system will not be able to determine the work area and will skip all points.")
            return None
        if not all(isinstance(coord, (int, float)) for coord in p):
            warnings.warn(f"Non-Numeric coordinate in: {p}, the system will not be able to determine the work area and will skip all points.")
            return None
    if len(xs) != 2 or len(ys) != 2:
        warnings.warn("The provided work area coordinates doesn't form a Rectangle, the system will not be able to determine the work area and will skip all points.")
        return None
    return points

# Method to extract the expected visited coordinates and error coordinates from the input file based on the Rectangle coordinates and the input points,
# the method returns two lists, one for the expected visited coordinates and another for the expected error coordinates,
# the method checks if the input points are within the Rectangle defined by the Rectangle coordinates, and
# if they are within the Rectangle, they are added to the expected visited coordinates list, otherwise they are added to the expected error coordinates list
def get_expected_and_error_coords_from_input_file(input_file_path):
    expected_coords = []
    error_coords = []
    try:
        with open(f"{PATH_TO_TEST_DIR}/resources/{input_file_path}", 'r') as f:
            input_content = [line.strip() for line in f]
            boundry_points = get_boundry_rectangle(input_content)

            points_line_index = input_content.index("Points")
            input_points = input_content[points_line_index + 1:]
            input_coords = [ast.literal_eval(ln) for ln in input_points if ln.strip()]

            if boundry_points:
                for coord in input_coords:
                    if is_point_within_rectangle(boundry_points, coord):
                        expected_coords.append(coord)
                    else:
                        error_coords.append(coord)
    except FileNotFoundError as e:
        warnings.warn(f"Input file not found, the system will not be able to run. {e}")
        return None, None
    except Exception as e:
        warnings.warn(f"Failed to parse input file, the system will not be able to run. {e}")
        return None, None
    return expected_coords, error_coords

# Method to check if a given point is within the Rectangle defined by the Rectangle coordinates,
# the method takes the Rectangle coordinates and the point as input, and returns True if the point is within
# the Rectangle, otherwise it returns False
def is_point_within_rectangle(rectangle, point):
    x_cords = []
    y_cords = []
    for vertex in rectangle:
        x_cords.append(vertex[0])
        y_cords.append(vertex[1])
    min_x = min(x_cords)
    max_x = max(x_cords)
    min_y = min(y_cords)
    max_y = max(y_cords)
    if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
        return True
    return False

def log_test_results_to_file(output_file_path,
                             expected_visited_coords=None,
                             actual_visited_coords=None,
                             expected_error_coords=None,
                             actual_error_coords=None,
                             result="Fail"):
    try:
        with open(output_file_path, 'a') as f:
            f.write(f"{expected_visited_coords}\t{actual_visited_coords}\t{expected_error_coords}\t{actual_error_coords}\t{result}\n")
    except Exception as e:
        raise Exception(f"Failed to write output file: {output_file_path}. Error: {str(e)}")
