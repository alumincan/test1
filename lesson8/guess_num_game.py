import random
import tkinter as tk
from tkinter import messagebox


# ── 顏色主題 (Catppuccin Mocha) ──────────────────────
BG      = "#1e1e2e"
CARD    = "#313244"
ACCENT  = "#89b4fa"
BLUE    = "#89b4fa"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
YELLOW  = "#f9e2af"
ORANGE  = "#fab387"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"


class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 猜數字遊戲")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.answer = 0
        self.count = 0
        self.history = []
        self.low = 1
        self.high = 50
        self.max_tries = 999
        self.game_over = False
        self.diff_buttons = []

        self._build_ui()
        self._show_menu()

    # ================================================================
    #  UI 建構
    # ================================================================
    def _build_ui(self):
        # ── 標題 ──
        tk.Label(self.root, text="🎲 猜數字遊戲", font=("Arial", 24, "bold"),
                 bg=BG, fg=ACCENT).pack(pady=(18, 2))
        tk.Label(self.root, text="範圍 1 ~ 50", font=("Arial", 13),
                 bg=BG, fg=SUBTEXT).pack()

        # ── 中央卡片 ──
        self.card = tk.Frame(self.root, bg=CARD,
                             highlightbackground="#585b70", highlightthickness=1)
        self.card.pack(padx=28, pady=14, fill="x")

        # 資訊列
        info = tk.Frame(self.card, bg=CARD)
        info.pack(fill="x", padx=20, pady=(14, 4))
        self.diff_lbl = tk.Label(info, text="📊 難度：—", font=("Arial", 11),
                                 bg=CARD, fg=SUBTEXT)
        self.diff_lbl.pack(side="left")
        self.tries_lbl = tk.Label(info, text="🎯 剩餘：—", font=("Arial", 11),
                                  bg=CARD, fg=SUBTEXT)
        self.tries_lbl.pack(side="right")

        # 範圍條 Canvas
        self.bar_cv = tk.Canvas(self.card, height=36, bg=CARD, highlightthickness=0)
        self.bar_cv.pack(fill="x", padx=20, pady=(4, 2))
        self.bar_cv.bind("<Configure>", lambda e: self._draw_bar())

        # 範圍數字
        self.range_lbl = tk.Label(self.card, text="1 ──────────────────────────────────── 50",
                                  font=("Courier", 10), bg=CARD, fg=SUBTEXT)
        self.range_lbl.pack(padx=20, pady=(0, 6))

        # 提示訊息
        self.hint_lbl = tk.Label(self.card, text="", font=("Arial", 15, "bold"),
                                 bg=CARD, fg=TEXT, height=2)
        self.hint_lbl.pack(pady=(0, 8))

        # 輸入框 + 按鈕
        inp = tk.Frame(self.card, bg=CARD)
        inp.pack(pady=(0, 14))

        self.entry = tk.Entry(inp, font=("Arial", 20), width=8, justify="center",
                              bg="#585b70", fg=TEXT, insertbackground=TEXT,
                              relief="flat", bd=0)
        self.entry.pack(ipady=5)
        self.entry.bind("<Return>", lambda _: self._guess())

        self.guess_btn = tk.Button(inp, text="🔍 猜！", font=("Arial", 13, "bold"),
                                   bg=ACCENT, fg="#1e1e2e", activebackground="#b4d0fb",
                                   activeforeground="#1e1e2e", relief="flat",
                                   cursor="hand2", width=12, bd=0,
                                   command=self._guess)
        self.guess_btn.pack(pady=(8, 0), ipady=3)

        # ── 紀錄區 ──
        tk.Label(self.root, text="📝 猜測紀錄", font=("Arial", 11, "bold"),
                 bg=BG, fg=SUBTEXT, anchor="w").pack(fill="x", padx=35, pady=(4, 0))

        hist_frame = tk.Frame(self.root, bg=BG)
        hist_frame.pack(fill="both", expand=True, padx=28, pady=(0, 5))

        self.hist_cv = tk.Canvas(hist_frame, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(hist_frame, orient="vertical", command=self.hist_cv.yview)
        self.hist_inner = tk.Frame(self.hist_cv, bg=BG)
        self.hist_inner.bind("<Configure>",
                            lambda _: self.hist_cv.configure(scrollregion=self.hist_cv.bbox("all")))
        self.hist_cv.create_window((0, 0), window=self.hist_inner, anchor="nw")
        self.hist_cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.hist_cv.pack(side="left", fill="both", expand=True)

        # 重來按鈕（預藏）
        self.restart_btn = tk.Button(self.root, text="🔄 再來一局",
                                     font=("Arial", 13, "bold"), bg=GREEN, fg="#1e1e2e",
                                     activebackground="#c6f0c2", activeforeground="#1e1e2e",
                                     relief="flat", cursor="hand2", width=14, bd=0,
                                     command=self._restart)

    # ================================================================
    #  選單畫面
    # ================================================================
    def _show_menu(self):
        self.hint_lbl.config(text="選擇難度開始遊戲", fg=TEXT)
        self._set_input_state(False)
        self.diff_lbl.config(text="📊 難度：—")
        self.tries_lbl.config(text="🎯 剩餘：—", fg=SUBTEXT)
        self._clear_hist()
        self.bar_cv.delete("all")
        self.range_lbl.config(text="1 ──────────────────────────────────── 50")
        self.restart_btn.pack_forget()

        self._diff_frame = tk.Frame(self.card, bg=CARD)
        self._diff_frame.pack(pady=(0, 14))
        self.diff_buttons.clear()

        for text, name, tries, color in [
            ("🟢 簡單", "簡單", 999, GREEN),
            ("🟡 普通", "普通", 10, YELLOW),
            ("🔴 困難", "困難", 6, ORANGE),
        ]:
            b = tk.Button(self._diff_frame, text=text, font=("Arial", 12, "bold"),
                          bg=color, fg="#1e1e2e", activebackground=color,
                          relief="flat", cursor="hand2", width=8, bd=0,
                          command=lambda n=name, t=tries: self._start(n, t))
            b.pack(side="left", padx=8, ipady=4)
            self.diff_buttons.append(b)

    # ================================================================
    #  開始遊戲
    # ================================================================
    def _start(self, diff_name, max_tries):
        self.answer = random.randint(1, 50)
        self.count = 0
        self.history.clear()
        self.low = 1
        self.high = 50
        self.max_tries = max_tries
        self.game_over = False

        self.diff_lbl.config(text=f"📊 難度：{diff_name}")
        self._update_tries()
        self.hint_lbl.config(text="猜一個 1~50 的數字", fg=TEXT)

        self._set_input_state(True)
        self.entry.delete(0, "end")

        for b in self.diff_buttons:
            b.destroy()
        self._diff_frame.destroy()
        self.restart_btn.pack_forget()
        self._clear_hist()
        self._draw_bar()
        self.entry.focus()

    # ================================================================
    #  猜測邏輯
    # ================================================================
    def _guess(self):
        if self.game_over:
            return

        raw = self.entry.get().strip()
        if not raw.isdigit():
            messagebox.showwarning("提示", "請輸入有效的整數！")
            return

        guess = int(raw)
        if guess < 1 or guess > 50:
            messagebox.showwarning("提示", "數字範圍是 1 ~ 50！")
            return

        self.count += 1
        self.entry.delete(0, "end")

        if guess == self.answer:
            self.history.append((guess, "✅ 正確！"))
            self.hint_lbl.config(text=f"🎉 答對了！答案是 {self.answer}", fg=GREEN)
            self._add_hist_row(len(self.history), guess, "✅ 正確！", GREEN)
            self.game_over = True
            self._set_input_state(False)
            self.restart_btn.pack(pady=(8, 10))
            self._draw_bar(guess)
        elif guess < self.answer:
            self.low = max(self.low, guess + 1)
            self.history.append((guess, "⬆️ 太小"))
            self.hint_lbl.config(text="⬆️  太小了，再大一點！", fg=BLUE)
            self._add_hist_row(len(self.history), guess, "⬆️ 太小", BLUE)
        else:
            self.high = min(self.high, guess - 1)
            self.history.append((guess, "⬇️ 太大"))
            self.hint_lbl.config(text="⬇️  太大了，再小一點！", fg=RED)
            self._add_hist_row(len(self.history), guess, "⬇️ 太大", RED)

        self._update_tries()
        self._draw_bar(guess)

        # 次數用完
        if not self.game_over and self.count >= self.max_tries:
            self.game_over = True
            self.hint_lbl.config(text=f"💥 時間到！答案是 {self.answer}", fg=RED)
            self._set_input_state(False)
            self.restart_btn.pack(pady=(8, 10))

    # ================================================================
    #  範圍指示條
    # ================================================================
    def _draw_bar(self, last_guess=None):
        self.bar_cv.delete("all")
        self.bar_cv.update_idletasks()
        w = max(self.bar_cv.winfo_width(), 100)
        h = 36
        pad = 12
        bar_w = w - pad * 2

        # 背景
        self.bar_cv.create_rectangle(pad, 4, pad + bar_w, h - 4,
                                     fill="#585b70", outline="", width=0)

        # 已排除 - 左
        lx = int((self.low - 1) / 50 * bar_w)
        if lx > 0:
            self.bar_cv.create_rectangle(pad, 4, pad + lx, h - 4,
                                         fill="#3b3b52", outline="", width=0)

        # 已排除 - 右
        rx = int(self.high / 50 * bar_w)
        if rx < bar_w:
            self.bar_cv.create_rectangle(pad + rx, 4, pad + bar_w, h - 4,
                                         fill="#3b3b52", outline="", width=0)

        # 答案
        ax = int((self.answer - 1) / 50 * bar_w) + pad
        if self.game_over:
            self.bar_cv.create_text(ax, h // 2, text="★", fill=YELLOW,
                                    font=("Arial", 13, "bold"))
        else:
            self.bar_cv.create_text(ax, h // 2, text="?", fill=YELLOW,
                                    font=("Arial", 12, "bold"))

        # 猜測圓點
        if last_guess is not None:
            gx = int((last_guess - 1) / 50 * bar_w) + pad
            c = GREEN if last_guess == self.answer else (
                BLUE if last_guess < self.answer else RED)
            self.bar_cv.create_oval(gx - 8, 2, gx + 8, h - 2,
                                     fill=c, outline="white", width=2)

        self.range_lbl.config(text=f"{self.low} ──────────────────────────────────── {self.high}")

    # ================================================================
    #  紀錄
    # ================================================================
    def _add_hist_row(self, idx, num, label, color):
        row = tk.Frame(self.hist_inner, bg=BG)
        row.pack(fill="x", padx=8, pady=1)
        tk.Label(row, text=f"  {idx}.", font=("Arial", 11), bg=BG, fg=SUBTEXT,
                 width=4, anchor="e").pack(side="left")
        tk.Label(row, text=str(num), font=("Courier", 13, "bold"), bg=BG, fg=color,
                 width=5).pack(side="left")
        tk.Label(row, text=label, font=("Arial", 11), bg=BG, fg=color).pack(side="left")
        self.hist_cv.update_idletasks()
        self.hist_cv.yview_moveto(1.0)

    def _clear_hist(self):
        for w in self.hist_inner.winfo_children():
            w.destroy()

    def _update_tries(self):
        if self.max_tries >= 999:
            self.tries_lbl.config(text=f"🎯 已猜：{self.count} 次", fg=SUBTEXT)
        else:
            remain = self.max_tries - self.count
            c = TEXT if remain > 3 else (YELLOW if remain > 1 else RED)
            self.tries_lbl.config(text=f"🎯 剩餘：{remain}", fg=c)

    def _set_input_state(self, enabled):
        state = "normal" if enabled else "disabled"
        self.entry.config(state=state)
        self.guess_btn.config(state=state)

    def _restart(self):
        self.restart_btn.pack_forget()
        self._show_menu()


# ── 啟動 ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()
