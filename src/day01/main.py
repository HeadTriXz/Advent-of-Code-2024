def read_input(file: str) -> tuple[list[int], list[int]]:
    all_left = []
    all_right = []

    for line in open(file, "r"):
        left, right = line.strip().split()

        all_left.append(int(left))
        all_right.append(int(right))

    return all_left, all_right

def part1() -> int:
    left, right = read_input("input.txt")

    # Sort the lists
    left.sort()
    right.sort()

    # Compare the lists
    diff = 0
    for l, r in zip(left, right):
        diff += abs(l - r)

    return diff

def part2() -> int:
    left, right = read_input("input.txt")

    # Count the occurrences of each location in the right list
    occurrences = {}
    for r in right:
        occurrences[r] = occurrences.get(r, 0) + 1

    # Calculate the similarity score
    score = 0
    for l in left:
        score += l * occurrences.get(l, 0)

    return score

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
