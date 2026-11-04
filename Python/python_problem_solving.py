"""Original example solutions for introductory Python problem solving."""


def find_max(numbers):
    """Return the largest number in a nonempty list."""
    if not numbers:
        raise ValueError('numbers must not be empty')
    largest = numbers[0]
    for number in numbers[1:]:
        if number > largest:
            largest = number
    return largest


def count_peaks(numbers):
    """Count elements strictly larger than both immediate neighbors."""
    peaks = 0
    for i in range(1, len(numbers) - 1):
        if numbers[i] > numbers[i - 1] and numbers[i] > numbers[i + 1]:
            peaks += 1
    return peaks


def is_prime(n):
    """Return whether n is prime, testing divisors up to sqrt(n)."""
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def two_summers(numbers, target):
    """Find a pair in a sorted list whose sum is target, or None."""
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return (numbers[left], numbers[right])
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def deduplicate(text):
    """Remove consecutive duplicate characters."""
    result = ''
    for char in text:
        if not result or char != result[-1]:
            result += char
    return result


def run_tests():
    assert find_max([3, 9, 2]) == 9
    assert count_peaks([1, 3, 2, 4, 1]) == 2
    assert is_prime(49) is False
    assert is_prime(47) is True
    assert two_summers([1, 2, 3, 4, 5], 9) == (4, 5)
    assert two_summers([1, 2, 3], 10) is None
    assert deduplicate('aabbccc') == 'abc'
    print('All 7 tests passed!')


if __name__ == '__main__':
    run_tests()
