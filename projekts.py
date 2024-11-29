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

        self.laukums = [["" for _ in range(3)] for _ in range(3)]
        self.pogas = [[None for _ in range(3)] for _ in range(3)]
        self.rezultats = 0
        self.jautajuma_skaits = 1
        self.spele_beigusies = False

        self.sakuma_ekrans = tk.Frame(self.logs, bg="#f4f4f4")
        tk.Label(
            self.sakuma_ekrans,
            text="Trīs rindā",
            font=("Arial", 32, "bold"),
            bg="#f4f4f4",
            fg="#800000",
        ).pack(pady=100)
        tk.Button(
            self.sakuma_ekrans,
            text="Sākt spēli",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            activebackground="#e8e8e8",
            command=self.paradit_spele,
        ).pack(pady=20)
        self.sakuma_ekrans.pack(fill="both", expand=True)

        self.spele_ekrans = tk.Frame(self.logs, bg="#f4f4f4")

        self.jautajumu_skaititajs = tk.Label(
            self.spele_ekrans,
            text=f"Gājiens: {self.jautajuma_skaits} no 10",
            font=("Arial", 14, "bold"),
            bg="#f4f4f4",
        )
        self.jautajumu_skaititajs.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.rezultatu_skaititajs = tk.Label(
            self.spele_ekrans,
            text=f"Punkti: {self.rezultats}",
            font=("Arial", 14, "bold"),
            bg="#f4f4f4",
        )
        self.rezultatu_skaititajs.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        self.izveidot_pogas()

        self.galapunkts_ekrans = tk.Frame(self.logs, bg="#f4f4f4")
        self.rezultatu_uzraksts = tk.Label(
            self.galapunkts_ekrans, text="", font=("Arial", 18, "bold"), bg="#f4f4f4"
        )
        self.rezultatu_uzraksts.pack(pady=50)
        tk.Button(
            self.galapunkts_ekrans,
            text="Iziet",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            activebackground="#e8e8e8",
            command=self.logs.destroy,
        ).pack(pady=20)

        self.logs.mainloop()

    def izveidot_pogas(self):
        """Izveido spēles pogas."""
        for rinda in range(3):
            for kolonna in range(3):
                poga = tk.Button(
                    self.spele_ekrans,
                    text="",
                    font=("Arial", 28, "bold"),
                    width=4,
                    height=2,
                    bg="#ffffff",
                    activebackground="#e8e8e8",
                    command=lambda r=rinda, c=kolonna: self.nospied_pogu(r, c),
                )
                poga.grid(row=rinda + 1, column=kolonna, sticky="nsew", padx=5, pady=5)
                self.spele_ekrans.grid_rowconfigure(rinda + 1, weight=1)
                self.spele_ekrans.grid_columnconfigure(kolonna, weight=1)
                self.pogas[rinda][kolonna] = poga

    def nospied_pogu(self, rinda, kolonna):
        """Apstrādā spēlētāja gājienu."""
        if not self.spele_beigusies and self.laukums[rinda][kolonna] == "":
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

            self.logs.after(500, self.bota_gajiens)  

    def veikt_gajienu(self, rinda, kolonna, speletajs):
        """Veic gājienu."""
        self.laukums[rinda][kolonna] = speletajs
        self.pogas[rinda][kolonna].config(text=speletajs, fg="red" if speletajs == "X" else "blue")

    def bota_gajiens(self):
        """Bota gājiens."""
        if self.spele_beigusies:
            return
        tukšie_lauki = [(r, c) for r in range(3) for c in range(3) if self.laukums[r][c] == ""]
        if tukšie_lauki:
            rinda, kolonna = random.choice(tukšie_lauki)
            self.veikt_gajienu(rinda, kolonna, "O")

            if self.parbaudit_uzvaretaju():
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

    def parbaudit_uzvaretaju(self):
        """Pārbauda uzvarētāju."""
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
        """Pārbauda neizšķirtu."""
        return all(cell for row in self.laukums for cell in row)

    def paradit_spele(self):
        """Pārslēdz uz spēles ekrānu."""
        self.sakuma_ekrans.pack_forget()
        self.spele_ekrans.pack(fill="both", expand=True)

    def paradit_galapunktu(self):
        """Pārslēdz uz beigu ekrānu."""
        self.spele_ekrans.pack_forget()
        if self.rezultats == 10:
            itog = "Tu esi īsts meistars! Apsveicam!"
        elif self.rezultats >= 6:
            itog = "Labs rezultāts! Bet ir vēl, kur augt."
        else:
            itog = "Pamēģini uzlabot savas prasmes!"
        self.rezultatu_uzraksts.config(text=f"Tavs rezultāts: {self.rezultats}.\n{itog}")
        self.galapunkts_ekrans.pack(fill="both", expand=True)

    def reset_spele(self):
        """Restartē spēli."""
        if self.jautajuma_skaits >= 10:
            self.paradit_galapunktu()
            return

        self.spele_beigusies = False
        self.jautajuma_skaits += 1
        self.laukums = [["" for _ in range(3)] for _ in range(3)]
        for rinda in range(3):
            for kolonna in range(3):
                self.pogas[rinda][kolonna].config(text="", bg="#ffffff")
        self.atjaunot_rezultatu()

    def atjaunot_rezultatu(self):
        """Atjauno spēles statistiku."""
        self.jautajumu_skaititajs.config(text=f"Gājiens: {self.jautajuma_skaits} no 10")
        self.rezultatu_skaititajs.config(text=f"Punkti: {self.rezultats}")


if __name__ == "__main__":
    TrisRinda()
