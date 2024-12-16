from enum import IntEnum

import numpy as np


class TileType(IntEnum):
    FLOOR = 0
    WALL = 1
    ROBOT = 2
    BOX = 3

    # Wide boxes
    BOX_L = 4
    BOX_R = 5


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


TILE_MAP = {
    ".": TileType.FLOOR,
    "#": TileType.WALL,
    "O": TileType.BOX,
    "@": TileType.ROBOT
}

DIRECTION_MAP = {
    "^": Direction.NORTH,
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST
}

OFFSETS = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0)
}

EXPAND_MAP = {
    TileType.FLOOR: (TileType.FLOOR, TileType.FLOOR),
    TileType.WALL: (TileType.WALL, TileType.WALL),
    TileType.BOX: (TileType.BOX_L, TileType.BOX_R),
    TileType.ROBOT: (TileType.ROBOT, TileType.FLOOR)
}

TILE_TO_CHAR = {
    TileType.FLOOR: ".",
    TileType.WALL: "#",
    TileType.ROBOT: "@",
    TileType.BOX: "O",
    TileType.BOX_L: "[",
    TileType.BOX_R: "]"
}

def print_grid(grid: np.ndarray) -> None:
    for row in grid:
        print("".join(TILE_TO_CHAR[tile] for tile in row))

def read_input(file: str) -> tuple[np.ndarray, list[Direction]]:
    with open(file, "r") as f:
        lines = f.readlines()

    width = len(lines[0].strip())
    height = sum(1 for line in lines if line[0] == "#")

    grid = np.zeros((height, width), dtype=int)
    for y in range(height):
        line = lines[y].strip()
        for x, char in enumerate(line):
            grid[y, x] = TILE_MAP.get(char, TileType.FLOOR)

    directions = []
    for line in lines[height + 1:]:
        for char in line.strip():
            if char in DIRECTION_MAP:
                directions.append(DIRECTION_MAP[char])

    return grid, directions

def get_position(grid: np.ndarray) -> tuple[int, int]:
    return tuple(np.argwhere(grid == TileType.ROBOT)[0][::-1])

def expand_grid(grid: np.ndarray) -> np.ndarray:
    new_grid = np.zeros((grid.shape[0], grid.shape[1] * 2), dtype=int)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            new_grid[y, x * 2] = EXPAND_MAP[grid[y, x]][0]
            new_grid[y, x * 2 + 1] = EXPAND_MAP[grid[y, x]][1]

    return new_grid

def can_move_big_box_v(grid: np.ndarray, position: tuple[int, int], direction: Direction) -> bool:
    lx, ly = position
    rx, ry = position

    if grid[ly, lx] == TileType.BOX_L:
        rx += 1
    elif grid[ly, lx] == TileType.BOX_R:
        lx -= 1

    dx, dy = OFFSETS[direction]

    nlx, nly = lx + dx, ly + dy
    nrx, nry = rx + dx, ry + dy

    if grid[nly, nlx] == TileType.WALL or grid[nry, nrx] == TileType.WALL:
        return False

    if grid[nly, nlx] in (TileType.BOX_L, TileType.BOX_R):
        if not can_move_big_box_v(grid, (nlx, nly), direction):
            return False

    if grid[nry, nrx] in (TileType.BOX_L, TileType.BOX_R) and grid[nly, nlx] != TileType.BOX_L:
        if not can_move_big_box_v(grid, (nrx, nry), direction):
            return False

    return True

def move_big_box(grid: np.ndarray, position: tuple[int, int], direction: Direction) -> None:
    lx, ly = position
    rx, ry = position

    if grid[ly, lx] == TileType.BOX_L:
        rx += 1

    if grid[ly, lx] == TileType.BOX_R:
        lx -= 1

    dx, dy = OFFSETS[direction]

    nlx, nly = lx + dx, ly + dy
    nrx, nry = rx + dx, ry + dy

    if grid[nly, nlx] in (TileType.BOX_L, TileType.BOX_R):
        move_big_box(grid, (nlx, nly), direction)

    if grid[nry, nrx] in (TileType.BOX_L, TileType.BOX_R) and grid[nly, nlx] != TileType.BOX_L:
        move_big_box(grid, (nrx, nry), direction)

    # Move the box
    grid[nly, nlx] = grid[ly, lx]
    grid[nry, nrx] = grid[ry, rx]

    # Clear the old box
    grid[ly, lx] = TileType.FLOOR
    grid[ry, rx] = TileType.FLOOR

def swap_box_side(grid: np.ndarray, position: tuple[int, int]) -> None:
    x, y = position
    if grid[y, x] == TileType.BOX_L:
        grid[y, x] = TileType.BOX_R
    elif grid[y, x] == TileType.BOX_R:
        grid[y, x] = TileType.BOX_L

def move(grid: np.ndarray, position: tuple[int, int], direction: Direction) -> tuple[int, int]:
    x, y = position
    dx, dy = OFFSETS[direction]

    nx, ny = x + dx, y + dy
    if grid[ny, nx] == TileType.WALL:
        return position

    if grid[ny, nx] == TileType.BOX:
        bx, by = nx, ny
        while grid[by, bx] == TileType.BOX:
            bx, by = bx + dx, by + dy

        if grid[by, bx] == TileType.WALL:
            return position

        grid[by, bx] = TileType.BOX

    if grid[ny, nx] in (TileType.BOX_L, TileType.BOX_R):
        if dx == 0:
            if not can_move_big_box_v(grid, (nx, ny), direction):
                return position

            move_big_box(grid, (nx, ny), direction)
        else:
            bx, by = nx, ny
            while grid[by, bx] in (TileType.BOX_L, TileType.BOX_R):
                bx, by = bx + dx, by + dy

            if grid[by, bx] == TileType.WALL:
                return position

            bx, by = nx, ny
            while grid[by, bx] in (TileType.BOX_L, TileType.BOX_R):
                swap_box_side(grid, (bx, by))
                bx, by = bx + dx, by + dy

            grid[ny, nx] = TileType.FLOOR
            if dx == 1:
                grid[by, bx] = TileType.BOX_R
            else:
                grid[by, bx] = TileType.BOX_L

    grid[y, x] = TileType.FLOOR
    grid[ny, nx] = TileType.ROBOT

    return nx, ny

def part1(grid: np.ndarray, directions: list[Direction]) -> int:
    position = get_position(grid)

    for direction in directions:
        position = move(grid, position, direction)

    box_indices = np.argwhere(grid == TileType.BOX)
    box_indices[:, 0] *= 100

    return int(np.sum(box_indices))

def part2(grid: np.ndarray, directions: list[Direction]) -> int:
    grid = expand_grid(grid)
    position = get_position(grid)

    for direction in directions:
        position = move(grid, position, direction)

    box_indices = np.argwhere(grid == TileType.BOX_L)
    box_indices[:, 0] *= 100

    return int(np.sum(box_indices))

if __name__ == "__main__":
    grid, directions = read_input("input.txt")
    print(part1(grid.copy(), directions))
    print(part2(grid.copy(), directions))
