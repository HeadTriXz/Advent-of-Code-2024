import math


def read_input(file: str) -> list[int]:
    with open(file, "r") as f:
        return [int(x) for x in f.readline().strip().split()]

# Part 1
def get_num_length(n: int) -> int:
    return math.trunc(math.log10(n) + 1)

def blink_once(data: list[int]) -> list[int]:
    new_data = []
    for i, stone in enumerate(data):
        if stone == 0:
            new_data.append(1)
            continue

        length = get_num_length(stone)
        if length % 2 == 0:
            left = stone // (10 ** (length // 2))
            right = stone % (10 ** (length // 2))

            new_data.append(right)
            new_data.append(left)
            continue

        new_data.append(stone * 2024)

    return new_data

# Part 2
def initialize_map(data: list[int]) -> dict[int, int]:
    data_map = {}
    for stone in data:
        data_map[stone] = data_map.get(stone, 0) + 1

    return data_map

def count_map(data: dict[int, int]) -> int:
    total = 0
    for count in data.values():
        total += count

    return total

def blink_once_fast(data: dict[int, int]) -> dict[int, int]:
    new_data = {}
    for stone, count in data.items():
        if stone == 0:
            new_data[1] = new_data.get(1, 0) + count
            continue

        length = get_num_length(stone)
        if length % 2 == 0:
            left = stone // (10 ** (length // 2))
            right = stone % (10 ** (length // 2))

            new_data[left] = new_data.get(left, 0) + count
            new_data[right] = new_data.get(right, 0) + count
            continue

        new_data[stone * 2024] = new_data.get(stone * 2024, 0) + count

    return new_data

def part1(data: list[int]) -> int:
    stones = initialize_map(data)

    for _ in range(25):
        stones = blink_once_fast(stones)

    return count_map(stones)

def part2(data: list[int]) -> int:
    stones = initialize_map(data)

    for _ in range(75):
        stones = blink_once_fast(stones)

    return count_map(stones)

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
