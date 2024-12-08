type Shape = tuple[int, int]
type Coordinate = tuple[int, int]
type Grid = dict[str, list[Coordinate]]

def is_valid_antenna(char: str) -> bool:
    return char.isalnum()

def is_within_bounds(coordinate: Coordinate, shape: Shape) -> bool:
    return 0 <= coordinate[0] < shape[0] and 0 <= coordinate[1] < shape[1]

def read_input(file: str) -> tuple[Grid, Shape]:
    grid: Grid = {}
    with open(file, "r") as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                if not is_valid_antenna(char):
                    continue

                if char not in grid:
                    grid[char] = []

                grid[char].append((x, y))

    return grid, (x + 1, y + 1)

def part1(data: tuple[Grid, Shape]) -> int:
    antinodes = set()
    for char, coordinates in data[0].items():
        if len(coordinates) < 2:
            continue

        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                dx = coordinates[i][0] - coordinates[j][0]
                dy = coordinates[i][1] - coordinates[j][1]

                antinode = coordinates[i][0] + dx, coordinates[i][1] + dy
                if is_within_bounds(antinode, data[1]):
                    antinodes.add(antinode)

                antinode = coordinates[j][0] - dx, coordinates[j][1] - dy
                if is_within_bounds(antinode, data[1]):
                    antinodes.add(antinode)

    return len(antinodes)

def part2(data: tuple[Grid, Shape]) -> int:
    antinodes = set()
    for char, coordinates in data[0].items():
        if len(coordinates) < 2:
            continue

        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                dx = coordinates[i][0] - coordinates[j][0]
                dy = coordinates[i][1] - coordinates[j][1]

                antinodes.add(coordinates[i])
                antinodes.add(coordinates[j])

                antinode = coordinates[i][0], coordinates[i][1]
                while is_within_bounds(antinode, data[1]):
                    antinode = antinode[0] + dx, antinode[1] + dy
                    if is_within_bounds(antinode, data[1]):
                        antinodes.add(antinode)

                antinode = coordinates[j][0], coordinates[j][1]
                while is_within_bounds(antinode, data[1]):
                    antinode = antinode[0] - dx, antinode[1] - dy
                    if is_within_bounds(antinode, data[1]):
                        antinodes.add(antinode)

    return len(antinodes)

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
