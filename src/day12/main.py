OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def read_input(file: str) -> list[str]:
    with open(file) as f:
        return [line.strip() for line in f]

def is_outside(data: list[str], char: str, x: int, y: int) -> bool:
    if x < 0 or x >= len(data) or y < 0 or y >= len(data[0]):
        return True

    if data[y][x] != char:
        return True

    return False

def get_perimeters(data: list[str]) -> list[tuple[int, int, int]]:
    visited = set()
    plots = []

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if (x, y) in visited:
                continue

            area = 0
            perimeter = 0
            sides = 0

            queue = [(x, y)]
            while queue:
                cx, cy = queue.pop(0)
                if (cx, cy) in visited:
                    continue

                visited.add((cx, cy))
                area += 1

                for dx, dy in OFFSETS:
                    nx, ny = cx + dx, cy + dy
                    if not is_outside(data, char, nx, ny):
                        queue.append((nx, ny))
                        continue

                    perimeter += 1

                    rx, ry = -dy, dx
                    lx, ly = dx - dy, dx + dy

                    if is_outside(data, char, cx + rx, cy + ry) or not is_outside(data, char, cx + lx, cy + ly):
                        sides += 1

            plots.append((area, perimeter, sides))

    return plots

def part1(data: list[str]) -> int:
    plots = get_perimeters(data)
    cost = 0

    for area, perimeter, _ in plots:
        cost += area * perimeter

    return cost

def part2(data: list[str]) -> int:
    plots = get_perimeters(data)
    cost = 0

    for area, perimeter, sides in plots:
        cost += area * sides

    return cost

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
