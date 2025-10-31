"""
Basic sequence generator with interactive controls.
A mathematician's playground for exploring simple sequences.
"""

import sys
import math
from typing import Callable, Any, List, Union, Dict
from dataclasses import dataclass


@dataclass
class SequenceState:
    """Encapsulates the state needed for sequence generation."""

    current_value: Union[float, List[float]]
    step: float = 1
    extra_params: Dict[str, Any] = None

    def __post_init__(self):
        if self.extra_params is None:
            self.extra_params = {}


# ============================================================================
# SEQUENCE GENERATORS
# ============================================================================


def count_by_step(state: SequenceState, num_steps: int = 1) -> List[float]:
    """
    Generate a sequence by counting with a fixed step size.

    Args:
        state: Current state with a single numeric value
        num_steps: Number of steps to generate

    Returns:
        List of values in the sequence
    """
    if isinstance(state.current_value, list):
        current = state.current_value[-1]
    else:
        current = state.current_value

    return [current + (i + 1) * state.step for i in range(num_steps)]


def fibonacci(state: SequenceState, num_steps: int = 1) -> List[float]:
    """
    Generate Fibonacci sequence values.

    Args:
        state: Current state with a list of at least 2 values
        num_steps: Number of Fibonacci numbers to generate

    Returns:
        List of next Fibonacci numbers
    """
    if not isinstance(state.current_value, list) or len(state.current_value) < 2:
        raise ValueError("Fibonacci sequence requires at least two initial values.")

    values = state.current_value.copy()
    next_values = []

    for _ in range(num_steps):
        next_value = values[-1] + values[-2]
        next_values.append(next_value)
        values.append(next_value)

    return next_values


def geometric_sequence(state: SequenceState, num_steps: int = 1) -> List[float]:
    """
    Generate a geometric sequence (multiply by a constant ratio).

    Args:
        state: Current state (step is used as the ratio)
        num_steps: Number of values to generate

    Returns:
        List of values in geometric sequence
    """
    if isinstance(state.current_value, list):
        current = state.current_value[-1]
    else:
        current = state.current_value

    ratio = state.step if state.step != 0 else 2
    return [current * (ratio ** (i + 1)) for i in range(num_steps)]


def square_sequence(state: SequenceState, num_steps: int = 1) -> List[float]:
    """
    Generate perfect squares starting from the current position.

    Args:
        state: Current state (represents the current n value)
        num_steps: Number of squares to generate

    Returns:
        List of perfect squares
    """
    if isinstance(state.current_value, list):
        n = int(state.current_value[-1] ** 0.5) if state.current_value[-1] >= 0 else 0
    else:
        n = int(state.current_value**0.5) if state.current_value >= 0 else 0

    return [(n + i + 1) ** 2 for i in range(num_steps)]


def prime_sequence(state: SequenceState, num_steps: int = 1) -> List[int]:
    """
    Generate the next prime numbers.

    Args:
        state: Current state with the last prime found
        num_steps: Number of primes to generate

    Returns:
        List of next prime numbers
    """

    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    if isinstance(state.current_value, list):
        current = int(state.current_value[-1])
    else:
        current = int(state.current_value)

    primes = []
    candidate = current + 1

    while len(primes) < num_steps:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1

    return primes


def collatz_sequence(state: SequenceState, num_steps: int = 1) -> List[int]:
    """
    Generate the Collatz sequence (3n+1 problem).
    If n is even: n/2
    If n is odd: 3n+1

    Args:
        state: Current state with current number
        num_steps: Number of steps to generate

    Returns:
        List of next values in Collatz sequence
    """
    if isinstance(state.current_value, list):
        current = int(state.current_value[-1])
    else:
        current = int(state.current_value)

    sequence = []
    for _ in range(num_steps):
        if current == 1:
            sequence.append(1)  # Stays at 1
        elif current % 2 == 0:
            current = current // 2
            sequence.append(current)
        else:
            current = 3 * current + 1
            sequence.append(current)

    return sequence


def tribonacci(state: SequenceState, num_steps: int = 1) -> List[float]:
    """
    Generate Tribonacci sequence (sum of previous three values).

    Args:
        state: Current state with a list of at least 3 values
        num_steps: Number of values to generate

    Returns:
        List of next Tribonacci numbers
    """
    if not isinstance(state.current_value, list) or len(state.current_value) < 3:
        raise ValueError("Tribonacci sequence requires at least three initial values.")

    values = state.current_value.copy()
    next_values = []

    for _ in range(num_steps):
        next_value = values[-1] + values[-2] + values[-3]
        next_values.append(next_value)
        values.append(next_value)

    return next_values


def factorial_sequence(state: SequenceState, num_steps: int = 1) -> List[int]:
    """
    Generate factorial sequence: n!

    Args:
        state: Current state with current n value
        num_steps: Number of factorials to generate

    Returns:
        List of factorial values
    """
    if isinstance(state.current_value, list):
        # If it's a list of factorials, find n from the last factorial
        n = 1
        fact = 1
        while fact < state.current_value[-1]:
            n += 1
            fact *= n
    else:
        # Find n from the factorial value
        n = 1
        fact = 1
        while fact < state.current_value:
            n += 1
            fact *= n

    factorials = []
    for i in range(1, num_steps + 1):
        n += 1
        fact *= n
        factorials.append(fact)

    return factorials


def custom_recurrence(state: SequenceState, num_steps: int = 1) -> List[float]:
    """
    Generate sequence using a custom recurrence relation.
    By default: a(n) = 2*a(n-1) - a(n-2) + step

    Args:
        state: Current state with at least 2 values
        num_steps: Number of values to generate

    Returns:
        List of next values
    """
    if not isinstance(state.current_value, list) or len(state.current_value) < 2:
        raise ValueError("Custom recurrence requires at least two initial values.")

    values = state.current_value.copy()
    next_values = []

    # Custom recurrence: a(n) = 2*a(n-1) - a(n-2) + step
    for _ in range(num_steps):
        next_value = 2 * values[-1] - values[-2] + state.step
        next_values.append(next_value)
        values.append(next_value)

    return next_values


# ============================================================================
# INTERACTIVE RUNNER
# ============================================================================


def run_sequence(
    sequence_func: Callable[[SequenceState, int], List[float]],
    initial_value: Union[float, List[float]] = 0,
    initial_step: float = 1,
    sequence_name: str = "Sequence",
):
    """
    Interactive sequence generator that works with any sequence function.

    Args:
        sequence_func: A function that takes (SequenceState, num_steps)
                      and returns a list of next values
        initial_value: Starting value(s) for the sequence
        initial_step: Initial step size parameter
        sequence_name: Name of the sequence for display

    Controls:
    - Press Enter: generate 1 next value
    - Enter a number N: generate N next values and display all of them
    - Press 'x' or 'X': exit
    - Press Ctrl+C: exit
    """
    state = SequenceState(current_value=initial_value, step=initial_step)
    iteration = 0

    print("=" * 70)
    print(f"🔢 {sequence_name} Generator 🔢")
    print("=" * 70)

    # Display initial value(s)
    if isinstance(state.current_value, list):
        print(f"Starting values: {state.current_value}")
        print(f"Current position: {state.current_value[-1]}")
    else:
        print(f"Starting value: {state.current_value}")

    print(f"Step parameter: {state.step}")
    print(f"Sequence function: {sequence_func.__name__}")
    print("\n📝 Controls:")
    print("  - Press Enter to generate 1 next value")
    print("  - Enter a number N to generate N next values")
    print("  - Press 'x' or 'X' to exit")
    print("  - Press Ctrl+C to exit")
    print("=" * 70)
    print()

    try:
        while True:
            # Format current value for display
            if isinstance(state.current_value, list):
                display_current = (
                    state.current_value[-1] if state.current_value else "N/A"
                )
                if len(state.current_value) > 3:
                    display_state = f"[...{state.current_value[-3:]}"
                else:
                    display_state = str(state.current_value)
            else:
                display_current = state.current_value
                display_state = str(state.current_value)

            user_input = input(
                f"\n[{iteration}] Current: {display_current} | Step: {state.step}\nAction (Enter/N/x): "
            ).strip()

            # Check for exit command
            if user_input.lower() == "x":
                print("\n" + "=" * 70)
                print("👋 Exiting sequence generator")
                if isinstance(state.current_value, list):
                    print(f"Final value: {state.current_value[-1]}")
                    if len(state.current_value) <= 10:
                        print(f"Complete sequence: {state.current_value}")
                    else:
                        print(f"Last 10 values: {state.current_value[-10:]}")
                else:
                    print(f"Final value: {state.current_value}")
                print(f"Total iterations: {iteration}")
                print("=" * 70)
                break

            # Determine number of steps to generate
            num_steps = 1
            if user_input:
                try:
                    num_steps = int(user_input)
                    if num_steps <= 0:
                        print("⚠️  Please enter a positive number.")
                        continue
                except ValueError:
                    print(
                        f"⚠️  Invalid input '{user_input}'. Enter a number, 'x' to exit, or press Enter."
                    )
                    continue

            # Generate next value(s) using the sequence function
            try:
                next_values = sequence_func(state, num_steps=num_steps)

                if next_values:
                    # Update state based on sequence type
                    if isinstance(state.current_value, list):
                        # For sequences that maintain history (Fibonacci, Tribonacci, etc.)
                        state.current_value.extend(next_values)
                    else:
                        # For sequences that only need the current value
                        state.current_value = next_values[-1]

                    iteration += 1

                    # Display generated values
                    print(f"\n  ✨ Generated {len(next_values)} value(s):")

                    # Format output nicely
                    if len(next_values) <= 10:
                        # Show all values if 10 or fewer
                        for i, val in enumerate(next_values, 1):
                            print(f"     {i:3d}. {val}")
                    else:
                        # Show first 5 and last 5 if more than 10
                        print(f"     First 5:")
                        for i, val in enumerate(next_values[:5], 1):
                            print(f"       {i:3d}. {val}")
                        print(f"     ... ({len(next_values) - 10} more) ...")
                        print(f"     Last 5:")
                        for i, val in enumerate(next_values[-5:], len(next_values) - 4):
                            print(f"       {i:3d}. {val}")

                    # Show summary
                    if isinstance(state.current_value, list):
                        print(f"\n  📊 Current position: {state.current_value[-1]}")
                        print(f"  📈 Sequence length: {len(state.current_value)}")
                    else:
                        print(f"\n  📊 Current value: {state.current_value}")

            except Exception as e:
                print(f"❌ Error generating sequence: {e}")
                print("   Continuing with previous value...")

    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("⚠️  Interrupted! Exiting sequence generator.")
        if isinstance(state.current_value, list):
            print(f"Final value: {state.current_value[-1]}")
        else:
            print(f"Final value: {state.current_value}")
        print(f"Iterations: {iteration}")
        print("=" * 70)
        sys.exit(0)
    except EOFError:
        print("\n\n" + "=" * 70)
        print("⚠️  EOF detected. Exiting sequence generator.")
        if isinstance(state.current_value, list):
            print(f"Final value: {state.current_value[-1]}")
        else:
            print(f"Final value: {state.current_value}")
        print(f"Iterations: {iteration}")
        print("=" * 70)
        sys.exit(0)


# ============================================================================
# MENU SYSTEM
# ============================================================================

AVAILABLE_SEQUENCES = {
    "1": ("Count by Step", count_by_step, 0, 1),
    "2": ("Fibonacci", fibonacci, [0, 1], 1),
    "3": ("Geometric Sequence", geometric_sequence, 1, 2),
    "4": ("Perfect Squares", square_sequence, 0, 1),
    "5": ("Prime Numbers", prime_sequence, 1, 1),
    "6": ("Collatz Sequence", collatz_sequence, 10, 1),
    "7": ("Tribonacci", tribonacci, [0, 0, 1], 1),
    "8": ("Factorial", factorial_sequence, 1, 1),
    "9": ("Custom Recurrence", custom_recurrence, [1, 2], 1),
}


def show_menu():
    """Display the sequence selection menu."""
    print("\n" + "=" * 70)
    print("🎓 MATHEMATICIAN'S SEQUENCE PLAYGROUND 🎓")
    print("=" * 70)
    print("\nAvailable Sequences:")
    print()

    for key, (name, _, init_val, init_step) in AVAILABLE_SEQUENCES.items():
        init_display = (
            f"{init_val}" if not isinstance(init_val, list) else f"{init_val}"
        )
        print(f"  {key}. {name:25s} (start: {init_display}, step: {init_step})")

    print(f"\n  x. Exit")
    print("=" * 70)


def main():
    """Main entry point with menu selection."""
    while True:
        show_menu()
        choice = input("\nSelect a sequence (1-9, or x to exit): ").strip()

        if choice.lower() == "x":
            print("\n👋 Goodbye! Happy exploring sequences!")
            break

        if choice in AVAILABLE_SEQUENCES:
            name, func, init_val, init_step = AVAILABLE_SEQUENCES[choice]
            print(f"\n🚀 Starting {name}...\n")
            run_sequence(
                sequence_func=func,
                initial_value=init_val,
                initial_step=init_step,
                sequence_name=name,
            )
        else:
            print(f"\n⚠️  Invalid choice '{choice}'. Please select 1-9 or x.")


if __name__ == "__main__":
    main()
