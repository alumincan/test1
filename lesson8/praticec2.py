import random


def main():
    answer = random.randint(1, 50)
    count = 0

    print("🎮 歡迎來到猜數字遊戲！")
    print("請猜一個 1~50 之間的數字吧！\n")

    while True:
        guess = input("請輸入你的猜測：")

        if not guess.isdigit():
            print("⚠️  請輸入有效的整數！\n")
            continue

        guess = int(guess)

        if guess < 1 or guess > 50:
            print("⚠️  數字範圍是 1~50，請重新輸入！\n")
            continue

        count += 1

        if guess < answer:
            print("⬆️  太小了，再大一點！\n")
        elif guess > answer:
            print("⬇️  太大了，再小一點！\n")
        else:
            print(f"🎉 恭喜你答對了！答案就是 {answer}！")
            print(f"你總共猜了 {count} 次。")
            break


if __name__ == "__main__":
    main()
