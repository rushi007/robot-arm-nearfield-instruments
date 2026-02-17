import sys

from app.file_parser import read_system_input, write_system_output
from robot_arm.robot_arm import RobotArm

def main(input_file):
    print(input_file)
    rectangle, points = read_system_input(input_file)
    print("*" * 50)
    print(f"Rectangle: {rectangle}")
    print(f"Points: {points}")
    print("*" * 50)
    print("|\n| Starting the robot arm system...\n|")
    arm = RobotArm(rectangle, points)
    visited_points, error_points = arm.run()
    print("|\n| Robot arm system completed.\n|")
    output_file = write_system_output(visited_points, error_points)
    print(f"system completed, output is stored in the /system_output/{output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("The system needs 1 argument. <input_file>")
    else:
        main(sys.argv[1])
