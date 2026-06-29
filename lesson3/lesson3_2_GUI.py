import tkinter as tk
from tkinter import ttk


def calculate_area():
    """計算梯形面積並顯示結果"""
    try:
        top = float(top_entry.get())
        bottom = float(bottom_entry.get())
        height = float(height_entry.get())
    except ValueError:
        result_label.config(text="請輸入有效的數字！", foreground="red")
        return

    area = (top + bottom) * height / 2
    result_label.config(
        text=f"梯形的面積 = {area:.2f} 平方公分",
        foreground="#1a1a1a",
    )


def clear_inputs():
    """清空所有輸入欄位與結果"""
    top_entry.delete(0, tk.END)
    bottom_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="")


# ── 建立主視窗 ──────────────────────────────────
root = tk.Tk()
root.title("梯形面積計算機")
root.resizable(False, False)

# ── 主框架（留邊距） ─────────────────────────────
main_frame = ttk.Frame(root, padding="24 20")
main_frame.pack()

# ── 標題 ────────────────────────────────────────
title_label = ttk.Label(
    main_frame,
    text="梯形面積計算機",
    font=("Helvetica", 18, "bold"),
)
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 16))

# ── 輸入欄位 ────────────────────────────────────
labels = ["上底 (cm)", "下底 (cm)", "高 (cm)"]
entries = []
for i, text in enumerate(labels):
    ttk.Label(main_frame, text=text, font=("Helvetica", 12)).grid(
        row=i + 1, column=0, sticky="w", padx=(0, 8), pady=6
    )
    entry = ttk.Entry(main_frame, width=14, font=("Helvetica", 12))
    entry.grid(row=i + 1, column=1, columnspan=2, sticky="ew", pady=6)
    entries.append(entry)

top_entry, bottom_entry, height_entry = entries

# ── 按鈕 ────────────────────────────────────────
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=4, column=0, columnspan=3, pady=(12, 4))

calculate_btn = ttk.Button(button_frame, text="計算面積", command=calculate_area)
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
result_label.grid(row=5, column=0, columnspan=3, pady=(12, 0))

# ── Enter 鍵綁定 ────────────────────────────────
root.bind("<Return>", lambda e: calculate_area())

# ── 啟動事件循環 ────────────────────────────────
root.mainloop()
