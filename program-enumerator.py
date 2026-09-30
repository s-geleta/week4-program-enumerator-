# Runs one generated program using the given x and y values
def evaluate(program, x, y):
    tokens = program.split()

    # Reads the program one token at a time
    def parse(i):
        t = tokens[i]

        # Base values
        if t == "x":
            return x, i + 1
        if t == "y":
            return y, i + 1
        if t in {"0", "1", "2"}:
            return int(t), i + 1

        # If the token is an operator, evaluate its two parts
        left, j = parse(i + 1)
        right, j = parse(j)

        if t == "+":
            return left + right, j
        if t == "-":
            return left - right, j

        return left * right, j

    return parse(0)[0]


# Finds the first program that matches every example
def synthesize(examples):

    # Programs with size 1
    programs = {1: ["x", "y", "0", "1", "2"]}
    size = 1

    while True:

        # Test every program of the current size
        for p in programs[size]:
            if all(evaluate(p, x, y) == out for x, y, out in examples):
                return p

        # Valid programs only have odd sizes: 1, 3, 5, 7, ...
        size += 2
        programs[size] = []

        # Build larger programs from smaller programs
        for left_size in range(1, size - 1, 2):
            right_size = size - 1 - left_size

            for op in ["+", "-", "*"]:
                for left in programs[left_size]:
                    for right in programs[right_size]:

                        # Polish notation puts the operator first
                        programs[size].append(f"{op} {left} {right}")


# Example input-output examples
examples = [
    (1, 2, 3),
    (4, 5, 9),
    (0, 7, 7)
]

# Find and print the matching program
print(synthesize(examples))