import re


CHRISTMAS_TREE = [
    ".............",
    "......#......",
    ".....###.....",
    "....#####....",
    "...#######...",
    "..#########..",
    ".###########.",
    ".....###.....",
    ".............",
]

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

class Robot:
    bounds: Position
    position: Position
    velocity: Velocity

    def __init__(self, position: Position, velocity: Velocity, bounds: Position):
        self.position = position
        self.velocity = velocity
        self.bounds = bounds

    def move(self, seconds: int = 1) -> None:
        self.position.x += self.velocity.dx * seconds
        self.position.y += self.velocity.dy * seconds

        if self.position.x < 0:
            self.position.x = (self.position.x + self.bounds.x) % self.bounds.x
        elif self.position.x >= self.bounds.x:
            self.position.x %= self.bounds.x

        if self.position.y < 0:
            self.position.y = (self.position.y + self.bounds.y) % self.bounds.y
        elif self.position.y >= self.bounds.y:
            self.position.y %= self.bounds.y

    def __repr__(self) -> str:
        return f"Robot({self.position.x}, {self.position.y})"

def expand_tree(tree: list[str], size: Position) -> list[str]:
    expanded = []

    original_width = len(tree[0])
    original_height = len(tree)

    x_scale = size.x / original_width
    y_scale = size.y / original_height

    for y in range(size.y):
        original_row = tree[int(y / y_scale)]

        row = ""
        for x in range(size.x):
            row += original_row[int(x / x_scale)]

        expanded.append(row)

    return expanded

def print_map(data: list[Robot]) -> None:
    bounds = data[0].bounds
    for y in range(bounds.y):
        row = ""
        for x in range(bounds.x):
            found = False
            for robot in data:
                if robot.position.x == x and robot.position.y == y:
                    row += "#"
                    found = True
                    break

            if not found:
                row += "."

        print(row)

def get_similarity(tree: list[str], data: list[Robot]) -> float:
    score = 0
    for robot in data:
        if tree[robot.position.y][robot.position.x] == "#":
            score += 1

    return score / len(data)

def read_input(file: str, bounds: Position) -> list[Robot]:
    robots = []
    with open(file, "r") as f:
        for row in f:
            match = re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", row)
            if match:
                position = Position(int(match.group(1)), int(match.group(2)))
                velocity = Velocity(int(match.group(3)), int(match.group(4)))

                robots.append(Robot(position, velocity, bounds))

    return robots

def part1(data: list[Robot]) -> int:
    bounds = data[0].bounds

    center_x = bounds.x // 2
    center_y = bounds.y // 2

    tl, tr, bl, br = 0, 0, 0, 0

    for robot in data:
        robot.move(100)

        if robot.position.x < center_x and robot.position.y < center_y:
            tl += 1
        elif robot.position.x > center_x and robot.position.y < center_y:
            tr += 1
        elif robot.position.x < center_x and robot.position.y > center_y:
            bl += 1
        elif robot.position.x > center_x and robot.position.y > center_y:
            br += 1

    return tl * tr * bl * br

def part2(data: list[Robot]) -> int:
    seconds = 0
    expanded = expand_tree(CHRISTMAS_TREE, data[0].bounds)

    while True:
        seconds += 1
        for robot in data:
            robot.move()

        similarity = get_similarity(expanded, data)
        if similarity >= 0.6:
            print_map(data)
            if input("Continue? (Y/n): ") == "n":
                break

    return seconds

if __name__ == "__main__":
    data = read_input("input.txt", Position(101, 103))
    print(part1(data))

    data = read_input("input.txt", Position(101, 103))
    print(part2(data))
