OFFSETS = [(-1, 1), (0, 1), (1, 1), (1, 0)]
TO_FIND = "XMAS"
TO_FIND_R = TO_FIND[::-1]

def read_input(file: str) -> list[str]:
    return [line.strip() for line in open(file, "r")]

def check_direction(data: list[str], x: int, y: int, dx: int, dy: int, word: str) -> bool:
    for i in range(len(word)):
        x2 = x + dx * i
        y2 = y + dy * i

        if x2 < 0 or x2 >= len(data) or y2 < 0 or y2 >= len(data[x2]):
            return False

        neighbour = data[x2][y2]
        if neighbour != word[i]:
            return False

    return True

def part1(data: list[str]) -> int:
    found = 0

    for x, line in enumerate(data):
        for y, char in enumerate(line):
            for dx, dy in OFFSETS:
                if check_direction(data, x, y, dx, dy, TO_FIND) or check_direction(data, x, y, dx, dy, TO_FIND_R):
                    found += 1

    return found

def part2(data: list[str]) -> int:
    found = 0

    for x, line in enumerate(data):
        for y, char in enumerate(line):
            if char != "A":
                continue

            if x == 0 or x == len(data) - 1 or y == 0 or y == len(line) - 1:
                continue

            tl = data[x - 1][y - 1]
            tr = data[x - 1][y + 1]
            bl = data[x + 1][y - 1]
            br = data[x + 1][y + 1]

            on_left = (tr == "M" and bl == "S") or (tr == "S" and bl == "M")
            on_right = (tl == "M" and br == "S") or (tl == "S" and br == "M")

            if on_left and on_right:
                found += 1

    return found

if __name__ == "__main__":
    data = read_input("input.txt")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
