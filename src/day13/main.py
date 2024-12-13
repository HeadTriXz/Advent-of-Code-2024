import re


class Coordinate:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class ClawMachine:
    a: Coordinate
    b: Coordinate
    prize: Coordinate

    def calculate_pushes(self, addition: int = 0) -> tuple[int, int]:
        ay = self.b.x * self.a.y
        by = self.b.y * self.a.x

        px = (self.prize.x + addition) * self.a.y
        py = (self.prize.y + addition) * self.a.x

        b = (px - py) / (ay - by)
        a = (self.prize.x + addition - self.b.x * b) / self.a.x

        if a.is_integer() and b.is_integer():
            return int(a), int(b)

        return -1, -1

def read_input(file: str) -> list[ClawMachine]:
    machines = []
    with open(file, "r") as f:
        machine = ClawMachine()

        for line in f:
            if match := re.search(r"Button A: X\+(\d+), Y\+(\d+)", line):
                machine.a = Coordinate(int(match.group(1)), int(match.group(2)))
            elif match := re.search(r"Button B: X\+(\d+), Y\+(\d+)", line):
                machine.b = Coordinate(int(match.group(1)), int(match.group(2)))
            elif match := re.search(r"Prize: X=(\d+), Y=(\d+)", line):
                machine.prize = Coordinate(int(match.group(1)), int(match.group(2)))

                machines.append(machine)
                machine = ClawMachine()

    return machines

def part1(data: list[ClawMachine]) -> int:
    cost = 0
    for machine in data:
        a, b = machine.calculate_pushes()
        if a == -1 or b == -1:
            continue

        cost += 3 * a + b

    return cost

def part2(data: list[ClawMachine]) -> int:
    cost = 0
    for machine in data:
        a, b = machine.calculate_pushes(10 ** 13)
        if a == -1 or b == -1:
            continue

        cost += 3 * a + b

    return cost

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
