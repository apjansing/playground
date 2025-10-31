import math
import random
import inspect
import re


def extract_function_expression(func):
    """
    Extract the expression from a lambda function or return the function name.

    Args:
        func: A function (lambda or named)

    Returns:
        String representation of the function expression
    """
    # For regular named functions, just return the name
    if hasattr(func, "__name__") and func.__name__ != "<lambda>":
        return func.__name__

    try:
        # Get the source lines of the function
        source_lines, _ = inspect.getsourcelines(func)

        # Find the line containing the lambda
        for line in source_lines:
            if "lambda" in line:
                # Extract everything after 'lambda x, y: '
                match = re.search(
                    r'lambda\s+[^:]+:\s*(.+?)(?:,\s*["\']|,\s*\)|\)\s*,)', line
                )
                if match:
                    return match.group(1).strip()

                # Fallback: try simpler extraction
                match = re.search(r"lambda\s+[^:]+:\s*(.+)", line)
                if match:
                    expr = match.group(1).strip()
                    # Remove trailing punctuation like , ) ] "
                    expr = re.sub(r'[,\)\]"\'].*$', "", expr).strip()
                    return expr

        return "<lambda>"
    except (OSError, TypeError, IndexError):
        return "<lambda>"


class MarkovChain:
    def __init__(
        self, transition_matrix, functions_matrix, function_names=None, state=0
    ):
        self.transition_matrix = transition_matrix
        self.functions_matrix = functions_matrix

        # Auto-generate function names if not provided
        if function_names is None:
            self.function_names = [
                extract_function_expression(func) for func in functions_matrix
            ]
        else:
            self.function_names = function_names

        self.state = state

    def update_state(self):
        probabilities = self.transition_matrix[self.state]
        next_state = random.choices(range(len(probabilities)), probabilities)[0]
        self.state = next_state


def markov(initial_values, steps, initial_state=0, num_states=4):
    """
    Generate a Markov chain sequence with random transition matrix and functions.

    Args:
        initial_values: Starting values for the sequence
        steps: Number of steps to generate
        initial_state: Starting state for the Markov chain
        num_states: Number of states (and functions) to generate
    """
    # Create a Markov chain instance with random transition matrix
    # Generate random transition probabilities (non-diagonal emphasis)
    transition_matrix = []

    for i in range(num_states):
        # Generate random values for each state
        row = [random.random() for _ in range(num_states)]

        # Reduce the diagonal element (self-transition) to emphasize state changes
        row[i] *= 0.2  # Make self-transition less likely

        # Normalize to ensure probabilities sum to 1
        row_sum = sum(row)
        row = [p / row_sum for p in row]

        transition_matrix.append(row)

    # Print the generated transition matrix for reference
    print("Generated Transition Matrix:")
    for i, row in enumerate(transition_matrix):
        print(f"  State {i}: {[f'{p:.3f}' for p in row]}")
    print()

    # Generate random functions based on num_states
    # Pool of possible operations to randomly select from
    # Each tuple: (function, description)
    operation_pool = [
        (lambda x, y: x + y, "x + y"),
        (lambda x, y: x - y, "x - y"),
        (lambda x, y: y - x, "y - x"),
        (lambda x, y: x + y + 1, "x + y + 1"),
        (lambda x, y: x - y + 1, "x - y + 1"),
        (lambda x, y: abs(x - y), "abs(x - y)"),
        (lambda x, y: (x + y) // 2, "(x + y) // 2"),
        (
            lambda x, y: (x - y) // 2 if (x - y) % 2 == 0 else (x - y + 1) // 2,
            "(x - y) // 2",
        ),
        (
            lambda x, y: (y - x) // 2 if (y - x) % 2 == 0 else (y - x + 1) // 2,
            "(y - x) // 2",
        ),
        (lambda x, y: max(x, y), "max(x, y)"),
        (lambda x, y: min(x, y), "min(x, y)"),
        (lambda x, y: x * 2, "x * 2"),
        (lambda x, y: y * 2, "y * 2"),
        (lambda x, y: (x + y) * 2, "(x + y) * 2"),
        (lambda x, y: x // (y if y != 0 else 1), "x // y"),
        (lambda x, y: y // (x if x != 0 else 1), "y // x"),
    ]

    # Randomly select num_states functions from the pool
    selected_operations = random.sample(
        operation_pool, min(num_states, len(operation_pool))
    )

    functions_matrix = [op[0] for op in selected_operations]
    function_names = [op[1] for op in selected_operations]

    # If we need more functions than the pool, cycle through and add variations
    if num_states > len(operation_pool):
        # Add more functions with random constants
        for i in range(num_states - len(operation_pool)):
            c = random.randint(1, 5)
            functions_matrix.append(lambda x, y, c=c: x + y + c)
            function_names.append(f"x + y + {c}")

    # Pass the function names explicitly

    markov_chain = MarkovChain(
        transition_matrix,
        functions_matrix,
        function_names=function_names,  # Use our explicit names
        state=initial_state,
    )

    # Print the selected functions
    print("Selected Functions:")
    for i, func_name in enumerate(markov_chain.function_names):
        print(f"  State {i}: {func_name}")
    print()

    sequence = initial_values.copy()
    for step in range(1, steps):
        function = markov_chain.functions_matrix[markov_chain.state]
        function_name = markov_chain.function_names[markov_chain.state]
        sequence.append(
            function(sequence[-1], sequence[-2])
        )  # Use last two values for the function
        markov_chain.update_state()
        print(
            f"Step {step}: State={markov_chain.state}, Function={function_name}, Sequence={sequence[-2:]}"
        )
    return sequence


if __name__ == "__main__":
    initial_values = [2, 3]
    steps = 100
    initial_state = 0
    num_states = 10  # Try changing this to 6, 8, 10, etc.!

    sequence = markov(initial_values, steps, initial_state, num_states)
    print(f"Generated Markov sequence: {sequence}")
