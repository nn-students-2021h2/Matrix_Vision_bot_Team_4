
def fib(n):
    if n in (0, 1):
        return n
    n -= 2 # elem number
    fib1 = 1
    fib2 = 1
    while n > 0:
        fib1, fib2 = fib2, fib1 + fib2
        n -= 1
    return fib2