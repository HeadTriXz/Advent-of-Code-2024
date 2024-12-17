import re

OPCODES = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv"
}

class Program:
    a: int
    b: int
    c: int

    pc: int = 0
    instructions: list[int]
    output: list[int]

    def __init__(self, a: int, b: int, c: int, instructions: list[int]) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.instructions = instructions
        self.output = []

    def copy(self) -> "Program":
        return Program(self.a, self.b, self.c, self.instructions)

    def run(self) -> None:
        while self.pc < len(self.instructions):
            opcode = self.instructions[self.pc]
            operand = self.instructions[self.pc + 1]

            getattr(self, OPCODES[opcode])(operand)
            self.pc += 2

    def get_combo_operand(self, operand: int) -> int:
        if operand < 4:
            return operand

        if operand == 4:
            return self.a

        if operand == 5:
            return self.b

        if operand == 6:
            return self.c

        raise ValueError(f"Invalid operand: {operand}")

    def adv(self, operand: int) -> None:
        self.a //= 2 ** self.get_combo_operand(operand)

    def bxl(self, operand: int) -> None:
        self.b ^= operand

    def bst(self, operand: int) -> None:
        self.b = self.get_combo_operand(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.a == 0:
            return

        self.pc = operand - 2

    def bxc(self, operand: int) -> None:
        self.b ^= self.c

    def out(self, operand: int) -> None:
        self.output.append(self.get_combo_operand(operand) % 8)

    def bdv(self, operand: int) -> None:
        self.b = self.a // 2 ** self.get_combo_operand(operand)

    def cdv(self, operand: int) -> None:
        self.c = self.a // 2 ** self.get_combo_operand(operand)

    def __repr__(self) -> str:
        return f"Program(a={self.a}, b={self.b}, c={self.c})"


def read_input(file: str) -> Program:
    with open(file, "r") as f:
        content = f.read()
        a, b, c = map(int, re.findall(r"Register [A-C]: (\d+)", content))
        instructions = list(map(int, re.search(r"Program: ([\d,]+)", content).group(1).split(",")))

        return Program(a, b, c, instructions)

def part1(program: Program) -> str:
    program.run()

    return ",".join(map(str, program.output))

def part2(program: Program) -> int:
    instructions_inv = reversed(program.instructions)

    possible_values = [0]
    for opcode in instructions_inv:
        new_queue = []
        for value in possible_values:
            for i in range(8):
                a = (value << 3) | i

                clone = Program(a, program.b, program.c, program.instructions)
                clone.run()

                if clone.output[0] == opcode:
                    new_queue.append(a)

        possible_values = new_queue

    return min(possible_values)

if __name__ == "__main__":
    program = read_input("input.txt")
    print(part1(program.copy()))
    print(part2(program.copy()))
