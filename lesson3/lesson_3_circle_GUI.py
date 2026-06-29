import tkinter as tk
from tkinter import ttk

PI = 3.14159


def calculate_volume():
    """計算圓柱體體積並顯示結果"""
    try:
        radius = float(radius_entry.get())
        height = float(height_entry.get())
    except ValueError:
        result_label.config(text="請輸入有效的數字！", foreground="red")
        return

    volume = PI * radius**2 * height
    result_label.config(
        text=f"體積 = {volume:.2f} 立方公分",
        foreground="#1a1a1a",
    )


def clear_inputs():
    """清空所有輸入欄位與結果"""
    radius_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")


# ── 建立主視窗 ──────────────────────────────────
root = tk.Tk()
root.title("圓柱體體積計算機")
root.resizable(False, False)

# ── 主框架（留邊距） ─────────────────────────────
main_frame = ttk.Frame(root, padding="24 20")
main_frame.pack()

# ── 標題 ────────────────────────────────────────
title_label = ttk.Label(
    main_frame,
    text="圓柱體體積計算機",
    font=("Helvetica", 18, "bold"),
)
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 16))

# ── 示意圖（以文字呈現） ──────────────────────────
canvas = tk.Canvas(
    main_frame, width=200, height=130, bg="#f8f9fa", highlightthickness=0
)
canvas.grid(row=1, column=0, columnspan=3, pady=(0, 12))

# 畫圓柱體示意
cx, cy = 100, 40
r = 50
# 上橢圓
canvas.create_oval(cx - r, cy - 20, cx + r, cy + 20, outline="#4a90d9", width=2)
# 下橢圓
canvas.create_oval(cx - r, cy + 40, cx + r, cy + 80, outline="#4a90d9", width=2)
# 左側連接線
canvas.create_line(cx - r, cy, cx - r, cy + 60, fill="#4a90d9", width=2)
# 右側連接線
canvas.create_line(cx + r, cy, cx + r, cy + 60, fill="#4a90d9", width=2)
# 標示 r
canvas.create_text(
    cx + r + 28, cy + 30, text="r", font=("Helvetica", 11, "italic"), fill="#e67e22"
)
canvas.create_line(
    cx, cy + 30, cx + r, cy + 30, fill="#e67e22", width=1.5, arrow=tk.LAST
)
# 標示 h
canvas.create_text(
    cx + r + 22, cy + 70, text="h", font=("Helvetica", 11, "italic"), fill="#e67e22"
)
canvas.create_line(
    cx + r + 10, cy, cx + r + 10, cy + 60, fill="#e67e22", width=1.5, arrow=tk.LAST
)

# ── 公式顯示 ────────────────────────────────────
formula_label = ttk.Label(
    main_frame,
    text="V = π × r² × h",
    font=("Helvetica", 12),
    foreground="#555555",
)
formula_label.grid(row=2, column=0, columnspan=3, pady=(0, 12))

# ── 輸入欄位 ────────────────────────────────────
ttk.Label(main_frame, text="半徑 (cm)", font=("Helvetica", 12)).grid(
    row=3, column=0, sticky="w", padx=(0, 8), pady=6
)
radius_entry = ttk.Entry(main_frame, width=14, font=("Helvetica", 12))
radius_entry.grid(row=3, column=1, columnspan=2, sticky="ew", pady=6)

ttk.Label(main_frame, text="高 (cm)", font=("Helvetica", 12)).grid(
    row=4, column=0, sticky="w", padx=(0, 8), pady=6
)
height_entry = ttk.Entry(main_frame, width=14, font=("Helvetica", 12))
height_entry.grid(row=4, column=1, columnspan=2, sticky="ew", pady=6)

# ── 按鈕 ────────────────────────────────────────
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=5, column=0, columnspan=3, pady=(12, 4))

calculate_btn = ttk.Button(button_frame, text="計算體積", command=calculate_volume)
calculate_btn.pack(side=tk.LEFT, padx=(0, 10))

clear_btn = ttk.Button(button_frame, text="清空", command=clear_inputs)
clear_btn.pack(side=tk.LEFT)

# ── 結果顯示 ────────────────────────────────────
result_label = ttk.Label(
    main_frame,
    text="",
    font=("Helvetica", 14, "bold"),
    foreground="#1a1a1a",
)
result_label.grid(row=6, column=0, columnspan=3, pady=(12, 0))

# ── Enter 鍵綁定 ────────────────────────────────
root.bind("<Return>", lambda e: calculate_volume())

# ── 啟動事件循環 ────────────────────────────────
root.mainloop()
