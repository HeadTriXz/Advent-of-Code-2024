import numpy as np

OFFSETS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def read_input(file: str) -> np.ndarray:
    with open(file, "r") as f:
        return np.array([list(map(int, line.strip())) for line in f])

def get_trailheads(data: np.ndarray) -> np.ndarray:
    return np.argwhere(data == 0)

def dfs(data: np.ndarray, x: int, y: int, visited: np.ndarray | None) -> int:
    if data[x, y] == 9:
        if visited is None:
            return 1

        if visited[x, y]:
            return 0

        visited[x, y] = True
        return 1

    total = 0
    for dx, dy in OFFSETS:
        nx, ny = x + dx, y + dy
        if nx < 0 or nx >= data.shape[0] or ny < 0 or ny >= data.shape[1]:
            continue

        if data[nx, ny] == data[x, y] + 1:
            total += dfs(data, nx, ny, visited)

    return total

def part1(data: np.ndarray) -> int:
    trailheads = get_trailheads(data)
    total = 0

    for x, y in trailheads:
        total += dfs(data, x, y, np.zeros(data.shape, dtype=bool))

    return total

def part2(data: np.ndarray) -> int:
    trailheads = get_trailheads(data)
    total = 0

    for x, y in trailheads:
        total += dfs(data, x, y, None)

    return total

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
