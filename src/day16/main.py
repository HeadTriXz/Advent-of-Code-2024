from enum import IntEnum

import heapq
import numpy as np


class TileType(IntEnum):
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


TILE_MAP = {
    ".": TileType.EMPTY,
    "#": TileType.WALL,
    "S": TileType.START,
    "E": TileType.END
}

OFFSETS = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0)
}

DIRECTIONS = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]


def read_input(file: str) -> np.ndarray:
    with open(file, "r") as f:
        return np.array([[TILE_MAP[c] for c in line.strip()] for line in f])

def find_start(data: np.ndarray) -> tuple[int, int]:
    return tuple(np.argwhere(data == TileType.START)[0][::-1])

def find_end(data: np.ndarray) -> tuple[int, int]:
    return tuple(np.argwhere(data == TileType.END)[0][::-1])

def dijkstra(data: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    height, width = data.shape
    directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

    distances = {}
    heap = []

    distances[(start[0], start[1], Direction.EAST)] = 0
    heap.append((0, start[0], start[1], Direction.EAST))

    while heap:
        cost, x, y, current_direction = heap.pop(0)
        if (x, y) == end:
            return int(cost)

        if distances.get((x, y, current_direction), np.inf) < cost:
            continue

        for new_direction in directions:
            dx, dy = OFFSETS[new_direction]
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height:
                if data[ny, nx] != TileType.WALL:
                    move_cost = 1
                    if new_direction != current_direction:
                        move_cost += 1000

                    new_cost = cost + move_cost
                    if new_cost < distances.get((nx, ny, new_direction), np.inf):
                        distances[(nx, ny, new_direction)] = new_cost
                        heap.append((new_cost, nx, ny, new_direction))

    return -1

def part1(data: np.ndarray) -> int:
    start = find_start(data)
    end = find_end(data)

    cost, _ = dijkstra(data, start, end)
    return cost

def part2(data: np.ndarray) -> int:
    start = find_start(data)
    end = find_end(data)

    # IDE has reset my dijsktra function, too lazy to do it again
    _, paths = dijkstra(data, start, end)

    visited = set()
    for path in paths:
        for x, y in path:
            visited.add((x, y))

    return len(visited)

if __name__ == "__main__":
    data = read_input("example.txt")
    print(part1(data))
    print(part2(data))
