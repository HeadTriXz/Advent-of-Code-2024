def read_input(file: str) -> list[list[int]]:
    reports = []

    for line in open(file, "r"):
        report = list(map(int, line.strip().split()))
        reports.append(report)

    return reports

def is_safe(report: list[int]) -> bool:
    increasing: bool | None = None

    for i in range(len(report) - 1):
        diff = report[i] - report[i + 1]
        if abs(diff) > 3 or abs(diff) < 1:
            return False

        if increasing is None:
            increasing = diff > 0
        elif increasing != (diff > 0):
            return False

    return True

def part1() -> int:
    reports = read_input("input.txt")

    safe = 0
    for report in reports:
        if is_safe(report):
            safe += 1

    return safe

def part2() -> int:
    reports = read_input("input.txt")

    safe = 0
    for report in reports:
        if is_safe(report):
            safe += 1
            continue

        for i in range(len(report)):
            if is_safe(report[:i] + report[i + 1:]):
                safe += 1
                break

    return safe

if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
