def all_eq(lst):
    max_length = 0
    max_id = 0
    for i in range(len(lst)):
        if max_length < len(lst[i]):
            max_length = len(lst[i])
            max_id = i
    for i in range(len(lst)):
        if len(lst[i]) != max_length:
            lst[i] = lst[i] + ("_" * (max_length - len(lst[i])))
    return(lst)