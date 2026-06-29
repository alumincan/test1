# 步驟 1:設定圓周率變數 pi,值為 3.14159

PI = 3.14159

# 步驟 2:讀取使用者輸入的半徑(公分),用 float() 轉成數字,存入變數 radius
radius = float(input("輸入半徑(公分)"))

# 步驟 3:讀取使用者輸入的高(公分),用 float() 轉成數字,存入變數 height
height = float(input("輸入高(公分)"))

# 步驟 4:用公式「pi × 半徑 × 半徑 × 高」計算體積,存入變數 volume
volume = PI * radius**2 * height

# 步驟 5:用 print() 印出體積,並加上「立方公分」單位

print("體積 = ", volume, "立方公分")