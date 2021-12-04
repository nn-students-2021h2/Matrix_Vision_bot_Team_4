def strange_amount(num):
    sum = 0
    for i in range(int(num)):
        for j in range(int(num), 0, -1):
            sum = sum + i
    return sum
