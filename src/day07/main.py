type Equations = list[tuple[int, list[int]]]

OPERATORS = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y
}

def read_input(file: str) -> Equations:
    equations = []
    for line in open(file, "r"):
        parts = line.strip().split(": ")
        equations.append((int(parts[0]), list(map(int, parts[1].split()))))

    return equations

def dfs(target: int, current: int, numbers: list[int], operators: list[str]) -> bool:
    if len(numbers) == 0:
        return current == target

    for operator, fn in OPERATORS.items():
        result = fn(current, numbers[0])
        if result > target:
            continue

        if dfs(target, result, numbers[1:], operators):
            return True

    return False

def part1(data: Equations) -> int:
    sum = 0

    for target, equation in data:
        if dfs(target, equation[0], equation[1:], []):
            sum += target

    return sum

def part2(data: Equations) -> int:
    OPERATORS["||"] = lambda x, y: int(f"{x}{y}")
    sum = 0

    for target, equation in data:
        if dfs(target, equation[0], equation[1:], []):
            sum += target

    return sum

if __name__ == "__main__":
    data = read_input("input.txt")
    print(part1(data))
    print(part2(data))
