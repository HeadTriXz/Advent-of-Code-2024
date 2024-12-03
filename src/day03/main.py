import re


def read_input(file: str) -> str:
    with open(file, "r") as f:
        return f.read().replace("\n", "")

def part1(data: str) -> int:
    results = re.findall(r"mul\((\d+),(\d+)\)", data)

    total = 0
    for a, b in results:
        total += int(a) * int(b)

    return total

def part2(data: str) -> int:
    all_enabled = [(m.start(0), True, None) for m in re.finditer(r"do\(\)", data)]
    all_disabled = [(m.start(0), False, None) for m in re.finditer(r"don't\(\)", data)]
    all_matches = [(m.start(0), m.group(1), m.group(2)) for m in re.finditer(r"mul\((\d+),(\d+)\)", data)]

    commands = sorted(all_enabled + all_disabled + all_matches, key=lambda x: x[0])

    total = 0
    enabled = True

    for idx, x, y in commands:
        if x is True:
            enabled = True
        elif x is False:
            enabled = False
        elif enabled:
            total += int(x) * int(y)

    return total


if __name__ == "__main__":
    data = read_input("input.txt")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
