def spy_game(a):
    if len(a) < 3:
        return False
    
    for i in range(len(a) - 2):
        if a[i] == 0 and a[i+1] == 0 and a[i+2] == 7:
            return True
    return False

x = list(map(int, input().split()))
print(spy_game(x))

