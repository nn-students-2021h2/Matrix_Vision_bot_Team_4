def all_eq(lst : list[str]) -> list[str]:
    max_len = len(max(lst, key=len))
    res = [word.ljust(max_len, "_") for word in lst]
    return res


a = list(input().split())
print(all_eq(a))
