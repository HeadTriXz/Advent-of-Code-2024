import numpy as np

def read_input(file: str) -> str:
    with open(file, "r") as f:
        return f.read().strip()

def get_blocks(data: str) -> np.ndarray:
    blocks = []
    for i, char in enumerate(data):
        block_size = int(char)
        block_idx = i // 2 if i % 2 == 0 else -1

        blocks.extend([block_idx] * block_size)

    return np.array(blocks)

def get_indices(blocks: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    curr_idx = 0
    curr_start = 0

    block_indices = []
    empty_indices = []

    for i, block in enumerate(blocks):
        if block != curr_idx:
            if curr_idx == -1:
                empty_indices.append((curr_start, i))
            else:
                block_indices.append((curr_idx, curr_start, i))

            curr_idx = block
            curr_start = i

    if curr_idx == -1:
        empty_indices.append((curr_start, len(blocks)))
    else:
        block_indices.append((curr_idx, curr_start, len(blocks)))

    return np.array(block_indices), np.array(empty_indices)

def part1(data: str) -> int:
    blocks = get_blocks(data)
    empty_blocks = np.where(blocks == -1)[0].tolist()

    for i in range(len(blocks) -1, -1, -1):
        if blocks[i] == -1:
            continue

        if len(empty_blocks) == 0:
            break

        new_idx = empty_blocks.pop(0)
        if new_idx > i:
            break

        blocks[new_idx] = blocks[i]
        blocks[i] = -1

    cleaned = blocks[blocks != -1].astype(np.uint32)
    return (cleaned * np.arange(0, len(cleaned))).sum()

def part2(data: str) -> int:
    blocks = get_blocks(data)
    block_indices, empty_indices = get_indices(blocks)

    for idx, start, end in block_indices[::-1]:
        for j, (empty_start, empty_end) in enumerate(empty_indices):
            if empty_start > start:
                break

            empty_size = empty_end - empty_start
            full_size = end - start

            if empty_size < full_size:
                continue

            blocks[empty_start:empty_start + full_size] = blocks[start:end]
            blocks[start:end] = -1

            empty_indices[j] = (empty_start + full_size, empty_end)
            break

    blocks[blocks == -1] = 0
    return (blocks.astype(np.uint32) * np.arange(0, len(blocks))).sum()

if __name__ == "__main__":
    data = read_input("input.txt")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
