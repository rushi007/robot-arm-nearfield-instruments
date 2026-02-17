import os
import time
import ast

def read_system_input(input_file):
    if not is_txt_file(input_file):
        raise ValueError("File must be a .txt file")

    print(f"reading the input file {input_file}")

    try:
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f]
    except FileNotFoundError:
        raise FileNotFoundError(f"File {input_file} not found")
    except Exception as e:
        raise Exception(f"Error reading file {input_file}: {str(e)}")
    return validate_system_input_file(lines)

def is_txt_file(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower() == ".txt"

def validate_work_area_points(file_lines):
    rectangle_index = file_lines.index("Rectangle")
    points = None
    xs = set()
    ys = set()
    try:
        points = ast.literal_eval(file_lines[rectangle_index+1])
    except:
        raise ValueError("Invalid Rectangle coordinates input")

    if rectangle_index == -1:
        raise ValueError("File must contain the Rectangle")
    if len(points) != 4:
        raise ValueError("File must contain 4 coordinates of the work area specified under Rectangle")
    for p in points:
        xs.add(p[0])
        ys.add(p[1])
        if not (isinstance(p, tuple) and len(p) == 2):
            raise ValueError("Invalid coordinate format for the given Rectangle")
        if not all(isinstance(coord, (int, float)) for coord in p):
            raise ValueError(f"Non-Numeric coordinate in: {p}")
    if len(xs) != 2 or len(ys) != 2:
        raise ValueError("The provided work area coordinates doesn't form a Rectangle")
    return points

def validate_navigation_points(file_lines):
    points_index = file_lines.index("Points")
    if points_index == -1:
        raise ValueError("File must contain the Points")
    navigation_lines = file_lines[points_index + 1:]

    if not navigation_lines:
        raise ValueError("File must contain at least one navigation point specified under Points")

    # navigation_coords = [
    #     ast.literal_eval(line) for line in navigation_lines if line.strip() and all(isinstance(ln, (int, float)) for ln in line)
    # ]

    navigation_coords = []
    for i, line in enumerate(navigation_lines):
        try:
            coord = ast.literal_eval(line)
        except(ValueError, SyntaxError):
            raise ValueError(f"Invalid coordinate format for the given navigation point: {line}")

        if not isinstance(coord, (tuple)) or len(coord) != 2:
            raise ValueError(f"Invalid coordinate format for the given navigation point: {line}")

        if not all(isinstance(point, (int, float)) for point in coord):
            raise ValueError(f"Non-Numeric coordinate in: {line}")
        navigation_coords.append(coord)

    if not navigation_coords:
        raise ValueError("File must contain at least one valid navigation point specified under Points")
    return navigation_coords


def validate_system_input_file(file_lines):
    work_area_coords = validate_work_area_points(file_lines)
    navigation_coords = validate_navigation_points(file_lines)

    print("Valid system input file")
    return work_area_coords, navigation_coords

def write_system_output(visited_points, error_points):
    output_dir = "system_output"
    os.makedirs(output_dir, exist_ok=True)

    output_file = "system_output_file_{}.txt".format(time.time() * 1000)
    print(f"Visited points {visited_points}"
          f"\nError points {error_points}")
    with open(f"{output_dir}/{output_file}", 'w') as f:
        for s_point in visited_points:
            f.write(f"{s_point}\n")
        f.write("error\n")
        for e_point in error_points:
            f.write(f"{e_point}\n")
    return output_file
