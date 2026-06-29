import math

opposite = float(input("請輸入直角三角形的對邊長度:"))
hypotenuse = float(input("請輸入直角三角形的斜邊長度:"))
radian = math.asin(opposite / hypotenuse)
degree = math.degrees(radian)
print("夾角的弧度:", radian, "弧度")
print("夾角的角度:", degree, "度")
