class RobotArm:
    def __init__(self, rectangle, input_points):
        self.rectangle = rectangle
        self.input_points = input_points
        self.visited_points = []
        self.error_points = []

    def run(self):
        for point in self.input_points:
            if self.is_point_within_rectangle(point):
                self.move_to_point(point)
            else:
                self.error_points.append(point)
                print(f"Point {point} is outside the rectangle and will be skipped.")
        return self.visited_points, self.error_points

    def move_to_point(self, point):
        print("-" * 50)
        print(f"Moving to point {point}... SUCCESS")
        # Simulate the movement of the robot arm to the point
        # In a real implementation, this would involve controlling the hardware of the robot arm
        # For this example, we will just print the action and append the coord to the visited points list
        self.visited_points.append(point)

    def is_point_within_rectangle(self, point):
        x_cords = []
        y_cords = []
        for vertex in self.rectangle:
            x_cords.append(vertex[0])
            y_cords.append(vertex[1])
        min_x = min(x_cords)
        max_x = max(x_cords)
        min_y = min(y_cords)
        max_y = max(y_cords)
        if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
            return True
        return False
