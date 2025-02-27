import tkinter as tk
import random
import time


class CasinoRoulette:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Roulette")

        #
        window_width = 600
        window_height = 700


        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()


        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.config(bg="#2E2E2E")

        self.balance = 1000
        self.bet_amount = tk.IntVar()
        self.bet_amount.set(100)
        self.bet_type = None
        self.number_buttons = []
        self.message_label = tk.Label(self.root, text="", bg="#2E2E2E", fg="white", font=("Arial", 12))
        self.message_label.pack(pady=5)
        self.create_widgets()

    def create_widgets(self):
        # Центрируем все элементы
        balance_frame = tk.Frame(self.root, bg="#2E2E2E")
        balance_frame.pack(anchor="center", pady=5)

        tk.Label(balance_frame, text="Баланс: $", bg="#2E2E2E", fg="white", font=("Arial", 14)).pack(side="left")
        self.balance_label = tk.Label(balance_frame, text=f"{self.balance}", bg="#2E2E2E", fg="white",
                                      font=("Arial", 14))
        self.balance_label.pack(side="left")

        tk.Label(self.root, text="Сумма ставки:", bg="#2E2E2E", fg="white", font=("Arial", 12)).pack(anchor="center")
        tk.Entry(self.root, textvariable=self.bet_amount, font=("Arial", 12), justify="center").pack(anchor="center",
                                                                                                     pady=5)

        self.result_label = tk.Label(self.root, text="Результат: ?", font=("Arial", 20), bg="#2E2E2E", fg="white")
        self.result_label.pack(anchor="center", pady=20)

        buttons_frame = tk.Frame(self.root, bg="#2E2E2E")
        buttons_frame.pack(pady=10)

        bets = ["Четное", "Нечетное", "Красное", "Черное", "1-й 12", "2-й 12", "3-й 12"]
        for bet in bets:
            btn = tk.Button(buttons_frame, text=bet, command=lambda b=bet: self.place_bet(b), bg="#4CAF50", fg="white",
                            font=("Arial", 10), padx=10, pady=5)
            btn.pack(side="left", padx=5)

        number_frame = tk.Frame(self.root, bg="#2E2E2E")
        number_frame.pack(pady=10)

        for i in range(37):
            btn = tk.Button(number_frame, text=str(i), command=lambda n=i: self.place_number_bet(n), bg="#757575",
                            fg="white", font=("Arial", 10), padx=10, pady=5)
            btn.grid(row=i // 10, column=i % 10, padx=5, pady=5)
            self.number_buttons.append(btn)

        self.spin_button = tk.Button(self.root, text="Крутить", command=self.spin, bg="#FFC107", fg="black",
                                     font=("Arial", 14), padx=10, pady=5)
        self.spin_button.pack(pady=20)

    def place_bet(self, bet):
        self.bet_type = bet
        self.message_label.config(text=f"Вы сделали ставку на {bet}")

    def place_number_bet(self, number):
        self.bet_type = number
        self.message_label.config(text=f"Вы сделали ставку на номер {number}")

    def spin(self):
        if self.bet_amount.get() > self.balance or self.bet_amount.get() <= 0:
            self.message_label.config(text="Неверная сумма ставки")
            return

        self.spin_button.config(state="disabled")
        self.animate_spin()
        number = random.randint(0, 36)
        color = "Красное" if number % 2 != 0 else "Черное"
        result_text = f"Результат: {number} ({color})"
        self.result_label.config(text=result_text)
        self.highlight_number(number)
        self.check_winnings(number, color)
        self.spin_button.config(state="normal")

    def animate_spin(self):
        for _ in range(40):
            num = random.randint(0, 36)
            color = "Красное" if num % 2 != 0 else "Черное"
            self.result_label.config(text=f"{num} ({color})")
            self.root.update()
            time.sleep(0.03)

    def highlight_number(self, number):
        for btn in self.number_buttons:
            btn.config(bg="#757575")
        self.number_buttons[number].config(bg="#FFD700")

    def check_winnings(self, number, color):
        win = False
        bet = self.bet_amount.get()
        if self.bet_type == "Четное" and number % 2 == 0 and number != 0:
            win = True
        elif self.bet_type == "Нечетное" and number % 2 != 0:
            win = True
        elif self.bet_type == "Красное" and color == "Красное":
            win = True
        elif self.bet_type == "Черное" and color == "Черное":
            win = True
        elif self.bet_type == "1-й 12" and 1 <= number <= 12:
            win = True
        elif self.bet_type == "2-й 12" and 13 <= number <= 24:
            win = True
        elif self.bet_type == "3-й 12" and 25 <= number <= 36:
            win = True
        elif self.bet_type == number:
            win = True
            bet *= 36

        if win:
            winnings = bet * 2 if isinstance(self.bet_type, str) else bet
            self.balance += winnings
            self.message_label.config(text=f"Вы выиграли ${winnings}!")
        else:
            self.balance -= bet
            self.message_label.config(text="Вы проиграли!")

        self.balance_label.config(text=f"{self.balance}")
        self.bet_type = None


if __name__ == "__main__":
    root = tk.Tk()
    app = CasinoRoulette(root)
    root.mainloop()
