def change(money):
    coins = money // 10
    money = money % 10
    if money >= 5:
        coins += 1
        money -= 5
    coins += money
    return coins


if __name__ == '__main__':
    m = int(input())
    print(change(m))