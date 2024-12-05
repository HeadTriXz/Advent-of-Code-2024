type Rules = dict[int, list[int]]
type Updates = list[list[int]]

def read_input(file: str) -> tuple[Rules, Updates]:
    rules: Rules = {}
    updates: Updates = []

    reading_rules = True
    for line in open(file, "r"):
        if not line.strip():
            reading_rules = False
            continue

        if reading_rules:
            left, right = map(int, line.strip().split("|"))
            if left not in rules:
                rules[left] = []

            rules[left].append(right)
        else:
            updates.append(list(map(int, line.strip().split(","))))

    return rules, updates

def check_updates(rules: Rules, updates: Updates) -> tuple[Updates, Updates]:
    valid_updates = []
    invalid_updates = []

    for update in updates:
        isValid = True
        for i, page in enumerate(update):
            if i == 0 or not isValid:
                continue

            if page not in rules:
                continue

            for prev_page in update[:i]:
                if prev_page in rules[page]:
                    isValid = False
                    break

        if isValid:
            valid_updates.append(update)
        else:
            invalid_updates.append(update)

    return valid_updates, invalid_updates

def part1(rules: Rules, updates: Updates) -> int:
    sum = 0

    valid, invalid = check_updates(rules, updates)
    for update in valid:
        sum += update[len(update) // 2]

    return sum

def part2(rules: Rules, updates: Updates) -> int:
    sum = 0

    valid, invalid = check_updates(rules, updates)
    for update in invalid:
        for i, page in enumerate(update):
            if i == 0 or page not in rules:
                continue

            for j in range(i):
                if update[j] in rules[page]:
                    update.insert(j, update.pop(i))
                    break

        sum += update[len(update) // 2]

    return sum

if __name__ == "__main__":
    rules, updates = read_input("input.txt")
    print(f"Part 1: {part1(rules, updates)}")
    print(f"Part 2: {part2(rules, updates)}")
