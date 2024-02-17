import cv2
import numpy as np
import threading
from Turns import count_turns

class PixelPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return PixelPoint(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class MazeSolver:
    def __init__(self):
        self.image = None
        self.height = None
        self.width = None
        self.radius = 2
        self.point_count = 0
        self.start_point = PixelPoint()
        self.end_point = PixelPoint()
        self.directions = [PixelPoint(0, -1), PixelPoint(0, 1), PixelPoint(1, 0), PixelPoint(-1, 0)]
        self.path_taken = []

    # Breadth-first search algorithm to find the path
    def breadth_first_search(self, start, end):
        const = 10000
        found = False
        queue = []
        visited = [[0 for _ in range(self.width)] for _ in range(self.height)]
        parent = [[PixelPoint() for _ in range(self.width)] for _ in range(self.height)]

        queue.append(start)
        visited[start.y][start.x] = 1
        while len(queue) > 0:
            current_point = queue.pop(0)
            for direction in self.directions:
                neighbor = current_point + direction
                if (
                    0 <= neighbor.x < self.width
                    and 0 <= neighbor.y < self.height
                    and visited[neighbor.y][neighbor.x] == 0
                    and (
                        self.image[neighbor.y][neighbor.x][0] != 0
                        or self.image[neighbor.y][neighbor.x][1] != 0
                        or self.image[neighbor.y][neighbor.x][2] != 0
                    )
                ):
                    queue.append(neighbor)
                    visited[neighbor.y][neighbor.x] = visited[current_point.y][current_point.x] + 1
                    self.image[neighbor.y][neighbor.x] = [0, 255, 0]
                    
                    parent[neighbor.y][neighbor.x] = current_point
                    if neighbor == end:
                        found = True
                        del queue[:]
                        break

        path = []
        if found:
            current_point = end
            while current_point != start:
                path.append(current_point)
                current_point = parent[current_point.y][current_point.x]
            path.append(current_point)
            path.reverse()

            for p in path:
                print(p.x,p.y)
                self.image[p.y][p.x] = [255, 255, 255]
            print("Path Found")
        else:
            print("Path Not Found")
        
        return count_turns(path) 
        
    # Function to handle mouse events for selecting start and end points
    def handle_mouse_event(self, event, pX, pY, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            if self.point_count == 0:
                cv2.rectangle(
                    self.image,
                    (pX - self.radius, pY - self.radius),
                    (pX + self.radius, pY + self.radius),
                    (0, 0, 255),
                    -1,
                )
                self.start_point = PixelPoint(pX, pY)
                print("start = ", self.start_point.x, self.start_point.y)
                self.point_count += 1
            elif self.point_count == 1:
                cv2.rectangle(
                    self.image,
                    (pX - self.radius, pY - self.radius),
                    (pX + self.radius, pY + self.radius),
                    (0, 200, 50),
                    -1,
                )
                self.end_point = PixelPoint(pX, pY)
                print("end = ", self.end_point.x, self.end_point.y)
                self.point_count += 1

    # Function to display the maze image and handle mouse events
    def display_image(self):
        cv2.imshow("Maze Image", self.image)
        cv2.setMouseCallback("Maze Image", self.handle_mouse_event)
        while True:
            cv2.imshow("Maze Image", self.image)
            cv2.waitKey(1)

    # Function to solve the maze
    def solve_maze(self, image_path, output_file):
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.height, self.width = self.image.shape[:2]
        self.image = cv2.resize(self.image, (int(self.width * 0.5), int(self.height * 0.5)))

        cv2.imshow("Original Maze Image", self.image)
        cv2.waitKey(0)
        self.image = cv2.adaptiveThreshold(
            self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
        )
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)

        print(self.height, self.width)
        print("Select start and end points: ")
        t = threading.Thread(target=self.display_image, args=())
        t.daemon = True
        t.start()

        while self.point_count < 2:
            pass

        no_of_turns= self.breadth_first_search(self.start_point, self.end_point)
        print(no_of_turns )
        cv2.waitKey(0)
        
        with open(output_file, 'w') as f:
            f.write(str(len(no_of_turns)) + '\n')
            f.write(str(self.width * self.height) + '\n')

if __name__ == "__main__":
    maze_solver = MazeSolver()
    maze_solver.solve_maze("mazes\Screenshot_20240212_183051.png", "output.txt")
