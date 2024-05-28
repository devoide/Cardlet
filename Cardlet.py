import tkinter as tk
from tkinter.filedialog import askopenfilename
import json
import os


class Cardlet(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        if os.path.exists("cards.json"):
            try:
                self.cards = json.load(open('cards.json'))
            except json.JSONDecodeError:
                self.cards = []
        else:
            self.cards = []

        self.current = 0
        self.back = False

        self.create_frames()
        self.card_widgets()
        self.control_widgets()

        self.master.bind("<Right>", self.next_card)
        self.master.bind("<Left>", self.prev_card)
        self.master.bind("<space>", self.turn_card)

    def create_frames(self):
        self.card_frame = tk.LabelFrame(self, text="Card", bg="black", fg="white", bd=5)
        self.card_frame.config(width=410, height=300)
        self.card_frame.grid(row=0, column=0)

        self.controls = tk.LabelFrame(self, bg="white", fg="white", bd=2)
        self.controls.config(width=410, height=80)
        self.controls.grid(row=2, column=0, pady=5, padx=10)

    def card_widgets(self):
        self.cards_label = tk.Label(self.card_frame, bg="black", fg="white", bd=3, wraplength=395)
        self.cards_label["text"] = self.cards[self.current]["text"] if self.cards else "No cards available"
        self.cards_label.place(x=0, y=1, relwidth=1, relheight=1)

        self.card_current = tk.Label(self.card_frame, bg="black", fg="white", bd=3)
        self.card_current["text"] = f"{self.current + 1}/{len(self.cards)}"
        self.card_current.place(x=0, y=0)

    def write_window(self):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Write")
        self.new_window.geometry("400x200")

        self.current = 0
        self.card_current_write = tk.Label(self.new_window)
        self.card_current_write["text"] = f"{self.current + 1}/{len(self.cards)}"
        self.card_current_write.pack()

        self.card_label_write = tk.Label(self.new_window, bd=3)
        self.card_label_write["text"] = self.cards[self.current]["text"]
        self.card_label_write.pack()


        self.entry = tk.Entry(self.new_window, width=20)
        self.entry.pack()
        self.entry.focus_set()

        self.answer_label = tk.Label(self.new_window)
        self.answer_label.pack()

        self.next_button = tk.Button(self.new_window, text="Next")
        self.next_button["command"] = self.next_card
        self.next_button.pack(side="right", padx=5, pady=5)

        self.prev_button = tk.Button(self.new_window, text="Prev")
        self.prev_button["command"] = self.prev_card
        self.prev_button.pack(side="left", padx=5, pady=5)

        self.entry.bind("<Return>", self.check_answer)
        self.new_window.bind("<Right>", self.next_card)
        self.new_window.bind("<Left>", self.prev_card)

    def check_answer(self, event=None):
        text = self.entry.get()
        answer = self.cards[self.current]["definition"].strip().lower()
        if text.strip().lower() == answer:
            self.answer_label.config(fg="lime", font=("Helvetica", 9, "bold"))
            self.answer_label["text"] = "Richtig!"
        else:
            self.answer_label.config(fg="red", font=("Helvetica", 9, "bold"))
            self.answer_label["text"] = f"Falsch: {answer}"

    def control_widgets(self):
        self.download_button = tk.Button(self.controls, text="Download")
        self.download_button["command"] = self.add_file
        self.download_button.grid(row=0, column=0)

        self.write_button = tk.Button(self.controls, text="Write")
        self.write_button["command"] = self.write_window
        self.write_button.grid(row=0, column=1)

    def next_card(self, event=None):
        if self.current < len(self.cards) - 1:
            self.current += 1
        else:
            self.current = 0
        self.cards_label["text"] = self.cards[self.current]["text"]
        self.card_current["text"] = f"{self.current + 1}/{len(self.cards)}"

        try:
            self.card_label_write["text"] = self.cards[self.current]["text"]
            self.answer_label["text"] = ""
            self.card_current_write["text"] = f"{self.current + 1}/{len(self.cards)}"
            self.entry.delete(0, "end")
        except (tk.TclError, AttributeError) as e:
            pass

    def prev_card(self, event=None):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = len(self.cards) - 1
        self.cards_label["text"] = self.cards[self.current]["text"]
        self.card_current["text"] = f"{self.current + 1}/{len(self.cards)}"

        try:
            self.card_label_write["text"] = self.cards[self.current]["text"]
            self.answer_label["text"] = ""
            self.card_current_write["text"] = f"{self.current + 1}/{len(self.cards)}"
            self.entry.delete(0, "end")
        except (tk.TclError, AttributeError) as e:
            pass

    def turn_card(self, event=None):
        if self.back:
            self.back = False
            self.cards_label["text"] = self.cards[self.current]["text"]
        else:
            self.back = True
            self.cards_label["text"] = self.cards[self.current]["definition"]

    def add_file(self):
        """
        extracts data and seperates text with definition by searching ":"
        :return card list:
        """
        try:
            filename = askopenfilename()
            f = open(filename, "r", encoding="utf-8")
            list_cards = f.read().split("$")
            for i, card in enumerate(list_cards):
                list_cards[i] = card.strip()
                if ":" in card:
                    list_cards[i] = card.split(":")
            self.cards = []
            for x in list_cards:
                if isinstance(x, list):
                    self.cards.append({"text": x[0], "definition": x[1]})
                else:
                    self.cards.append({"text": x, "definition": ""})

            with open('cards.json', 'w', encoding="utf-8") as file:
                json.dump(self.cards, file, indent=4)
        except FileNotFoundError:
            return []
        self.current = 0
        self.card_current["text"] = f"{self.current + 1}/{len(self.cards)}"
        self.cards_label["text"] = self.cards[self.current]["text"]


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400')
    root.title('Cardlet')

    app = Cardlet(master=root)
    app.mainloop()
