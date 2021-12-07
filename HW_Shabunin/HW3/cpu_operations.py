def factorial(n: int) -> int:
    if n in (0, 1):
        return 1
    return factorial(n - 1) * n