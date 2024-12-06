ORIENTATIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def read_input(file: str) -> list[str]:
    return [line.strip() for line in open(file, "r")]

def update_orientation(orientation: int) -> int:
    return (orientation + 1) % len(ORIENTATIONS)

def find_position(data: list[str]) -> tuple[int, int]:
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "^":
                return x, y

    return -1, -1

def move(data: list[str], x: int, y: int, orientation: int):
    dx, dy = ORIENTATIONS[orientation]
    x += dx
    y += dy

    if x < 0 or x >= len(data) or y < 0 or y >= len(data[x]):
        return -1, -1

    return x, y

def get_visited(data: list[str], x: int, y: int) -> set[tuple[int, int]]:
    visited: set[tuple[int, int]] = {(x, y)}
    orientation = 0

    while True:
        nx, ny = move(data, x, y, orientation)
        if nx == -1:
            break

        if data[ny][nx] == "#":
            orientation = update_orientation(orientation)
            continue

        visited.add((nx, ny))
        x, y = nx, ny

    return visited

def part1(data: list[str]) -> int:
    x, y = find_position(data)

    return len(get_visited(data, x, y))

def part2(data: list[str]) -> int:
    start_x, start_y = find_position(data)
    visited_path = get_visited(data, start_x, start_y)

    # Only check the places where he'd actually walk.
    possible_positions = set()
    for ox, oy in visited_path:
        obstructions = set()
        orientation = 0

        cx, cy = start_x, start_y
        while True:
            nx, ny = move(data, cx, cy, orientation)
            if nx == -1:
                break

            if data[ny][nx] == "#" or (nx == ox and ny == oy):
                # If we have visited this place before, we are stuck in a loop.
                if (cx, cy, nx, ny) in obstructions:
                    possible_positions.add((ox, oy))
                    break

                orientation = update_orientation(orientation)
                obstructions.add((cx, cy, nx, ny))
            else:
                cx, cy = nx, ny

    return len(possible_positions)

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
