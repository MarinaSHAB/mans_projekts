import tkinter as tk
from tkinter import messagebox
import random
class TrisRinda:
    def __init__(self):
        self.logs = tk.Tk()
        self.logs.title("Trīs rindā")
        self.logs.geometry("400x500")
        self.logs.configure(bg="#f4f4f4")
        self.logs.resizable(False, False)

        self.patreizejais_speletajs = "X"
        self.laukums = [["" for _ in range(3)] for _ in range(3)]
        self.pogas = [[None for _ in range(3)] for _ in range(3)]
        self.rezultats = 0
        self.jautajuma_skaits = 1
        self.spele_beigusies = False

        self.jautajumu_skaititajs = tk.Label(
            self.logs, text=f"Gājiens: {self.jautajuma_skaits} no 10", font=("Arial", 14, "bold"), bg="#f4f4f4"
        )
        self.jautajumu_skaititajs.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.rezultatu_skaititajs = tk.Label(
            self.logs, text=f"Punkti: {self.rezultats}", font=("Arial", 14, "bold"), bg="#f4f4f4"
        )
        self.rezultatu_skaititajs.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        self.izveidot_pogas()
        self.logs.mainloop()

    def izveidot_pogas(self):
        """Create the game buttons."""
        for rinda in range(3):
            for kolonna in range(3):
                poga = tk.Button(
                    self.logs,
                    text="",
                    font=("Arial", 28, "bold"),
                    width=4,
                    height=2,
                    bg="#ffffff",
                    activebackground="#e8e8e8",
                    command=lambda r=rinda, c=kolonna: self.nospied_pogu(r, c),
                )
                poga.grid(row=rinda + 1, column=kolonna, sticky="nsew", padx=5, pady=5)
                self.logs.grid_rowconfigure(rinda + 1, weight=1)
                self.logs.grid_columnconfigure(kolonna, weight=1)
                self.pogas[rinda][kolonna] = poga

    def nospied_pogu(self, rinda, kolonna):
        if not self.spele_beigusies and self.laukums[rinda][kolonna] == "" and self.patreizejais_speletajs == "X":
            self.veikt_gajienu(rinda, kolonna, "X")

            if self.parbaudit_uzvaretaju():
                self.rezultats += 1
                self.spele_beigusies = True
                self.atjaunot_rezultatu()
                messagebox.showinfo("Spēle beigusies", "Tu uzvarēji!")
                self.reset_spele()
                return
            elif self.vai_neizskirts():
                self.spele_beigusies = True
                messagebox.showinfo("Spēle beigusies", "Neizšķirts!")
                self.reset_spele()
                return

            self.patreizejais_speletajs = "O"
            self.logs.after(1000, self.bota_gajiens)

    def veikt_gajienu(self, rinda, kolonna, speletajs):
        self.laukums[rinda][kolonna] = speletajs
        self.pogas[rinda][kolonna].config(text=speletajs, fg="red" if speletajs == "X" else "blue")

    def bota_gajiens(self):
        if self.spele_beigusies:
            return
        tukšie_lauki = [(r, c) for r in range(3) for c in range(3) if self.laukums[r][c] == ""]
        if tukšie_lauki:
            rinda, kolonna = random.choice(tukšie_lauki)
            self.veikt_gajienu(rinda, kolonna, "O")

            if self.parbaudit_uzvaretaju():
                if not self.spele_beigusies:
                    self.rezultats = max(self.rezultats - 1, 0)
                self.spele_beigusies = True
                self.atjaunot_rezultatu()
                messagebox.showinfo("Spēle beigusies", "Bots uzvarēja!")
                self.reset_spele()
                return
            elif self.vai_neizskirts():
                self.spele_beigusies = True
                messagebox.showinfo("Spēle beigusies", "Neizšķirts!")
                self.reset_spele()
                return

            self.patreizejais_speletajs = "X"

    def parbaudit_uzvaretaju(self):
        for i in range(3):
            if self.laukums[i][0] == self.laukums[i][1] == self.laukums[i][2] != "":
                return True
            if self.laukums[0][i] == self.laukums[1][i] == self.laukums[2][i] != "":
                return True

        if self.laukums[0][0] == self.laukums[1][1] == self.laukums[2][2] != "":
            return True
        if self.laukums[0][2] == self.laukums[1][1] == self.laukums[2][0] != "":
            return True

        return False

    def vai_neizskirts(self):
        return all(cell for row in self.laukums for cell in row)

    def reset_spele(self):
        if self.jautajuma_skaits >= 10:
            self.spele_beigusies_pilniba()
            return

        self.spele_beigusies = False
        self.jautajuma_skaits += 1
        self.patreizejais_speletajs = "X"
        self.laukums = [["" for _ in range(3)] for _ in range(3)]
        for rinda in range(3):
            for kolonna in range(3):
                self.pogas[rinda][kolonna].config(text="", bg="#ffffff")
        self.atjaunot_rezultatu()

    def spele_beigusies_pilniba(self):
        if self.rezultats == 10:
            itog = "Tu esi īsts meistars! Apsveicam!"
        elif self.rezultats >= 6:
            itog = "Labs rezultāts! Bet ir vēl, kur augt."
        else:
            itog = "Pamēģini uzlabot savas prasmes!"

        messagebox.showinfo("Spēle beigusies", f"Tavs rezultāts: {self.rezultats}. {itog}")
        self.logs.destroy()

    def atjaunot_rezultatu(self):
        self.jautajumu_skaititajs.config(text=f"Gājiens: {self.jautajuma_skaits} no 10")
        self.rezultatu_skaititajs.config(text=f"Punkti: {self.rezultats}")


if __name__ == "__main__":
    TrisRinda()
