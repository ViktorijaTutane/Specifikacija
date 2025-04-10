from tkinter import *
from PIL import ImageTk, Image
import random
import os
import time

class MatSpele:
    def __init__(self, window):
        #Sākumekrāna atvēršana
        self.window = window
        self.window.geometry("708x502")
        self.window.title("Ātrā matemātika")
        self.window.resizable(False, False)
        self.window.configure(bg='#355DB1')
        # Līmeņu kopīgs noformējums noformējums
        self.bg_color = '#355DB1'
        self.btn_color = "#92D6F9"
        self.btn_text_color = "#0D096C"
        self.text_color = 'white'
        # Spēles rezultātu apkopošana
        self.punkti = 0
        self.kop_uzd = 0
        self.tagadejs_timers = None
        self.tagad_atbilde = None
        self.tagad_limenis = None
        self.uzd_label = None
        self.start_time = 0  
        self.total_score = 0  
        self.difficulty_multipliers = {  # Punktu skaits dažādiem līmeņiem
            "add": 1,
            "subtract": 1,
            "multiply": 2,
            "divide": 2
        }
        self.sakumaekrans()
        
    def sakumaekrans(self):
        self.clear_window()
        self.window.title("Ātrā matemātika")
        # Atiestatīt punktu skaitu
        self.punkti = 0
        self.kop_uzd = 0
        self.total_score = 0
        # Sākumekrāna fona uzstādīšana
        try:
            if os.path.exists('sakumaekrans.png'):
                img = ImageTk.PhotoImage(Image.open('sakumaekrans.png'))
                img_label = Label(self.window, image=img, bg=self.bg_color)
                img_label.image = img 
                img_label.pack()
        except Exception as e:
            print(f"Attēls nelādējas: {e}")
            Label(self.window, text="Ātrā matemātika", font=("Arial Black", 36), bg=self.bg_color, fg='white').pack(fill=BOTH, expand=True)
        # Līmeņu atbilstošas pogas, jo radās problēmaas ar logu generēšanu
        limenu_pogas = [
            ("Saskaitīšana", "add", 40, 250),
            ("Atņemšana", "subtract", 380, 250),
            ("Reizināšana", "multiply", 40, 400),
            ("Dalīšana", "divide", 380, 400) ]
        for text, op, x, y in limenu_pogas:
            Button(self.window, text=text, font=("Arial Black", 20, "bold"), bg=self.btn_color, fg=self.btn_text_color, width=15,command=lambda o=op: self.limenu_logs(o)).place(x=x, y=y)
            
    def limenu_logs(self, operation):
        self.clear_window()
        self.tagad_limenis = operation
        op_nosaukumi = {
            "add": "Saskaitīšana", 
            "subtract": "Atņemšana",
            "multiply": "Reizināšana", 
            "divide": "Dalīšana"
        }
        self.window.title(op_nosaukumi.get(operation, "Ātrā matemātika"))
        # Generē katra līmeņa uzdevumu noformējumu
        uzdevums, self.tagad_atbilde = self.uzdevumu_gen(operation) 
        self.rezultatu_label = Label(self.window, text=f"Pareizās atbildes: {self.punkti}/{self.kop_uzd}",font=("Arial", 16), bg=self.bg_color, fg='white')
        self.rezultatu_label.pack(pady=5)
        self.score_label = Label(self.window, text=f"Kopējais rezultāts: {self.total_score}", font=("Arial", 16), bg=self.bg_color, fg='white')
        self.score_label.pack(pady=5)
        self.timer_label = Label(self.window, text="Atlicis laiks: 20s",font=("Arial", 24), bg=self.bg_color, fg='white')
        self.timer_label.pack(pady=10)
        self.uzd_label = Label(self.window, text=uzdevums, font=("Arial", 36),bg=self.bg_color, fg='white')
        self.uzd_label.pack(pady=20)
        self.atbildes_ievad = Entry(self.window, font=("Arial", 24),justify='center', bg='white')
        self.atbildes_ievad.pack(pady=10)
        self.atbildes_ievad.focus()
        self.atsauksme_label = Label(self.window, text="", font=("Arial", 16),bg=self.bg_color, fg='white')
        self.atsauksme_label.pack()
        Button(self.window, text="Iesniegt", font=("Arial", 18),bg=self.btn_color, fg=self.btn_text_color,command=self.atb_parbaude).pack(pady=20)
        self.window.bind('<Return>', lambda e: self.atb_parbaude())
        self.start_time = time.time()  # Sāk laiku priekš ši uzdevuma
        self.tameris()
#Uzdevuma generēšana
    def uzdevumu_gen(self, operation):
        if operation == "add":
            a, b = random.randint(1, 100), random.randint(1, 100)
            return f"{a} + {b} = ?", a + b
        elif operation == "subtract":
            a, b = random.randint(1, 100), random.randint(1, 100)
            return f"{a} - {b} = ?", a - b
        elif operation == "multiply":
            a, b = random.randint(1, 20), random.randint(1, 20)
            return f"{a} × {b} = ?", a * b
        elif operation == "divide":
            b = random.randint(1, 20)
            a = b * random.randint(1, 20) 
            return f"{a} ÷ {b} = ?", a // b

    def atb_parbaude(self):
        lietotaja_atb = self.atbildes_ievad.get().strip()
        if not lietotaja_atb:
            self.atsauksme_label.config(text="Lūdzu ievadiet atbildi!", fg='red')
            return    
        
        self.kop_uzd += 1
        try:
            # Skaita laiku cik ilgi lietotājam aizņēma atbildēt pareizi
            time_taken = time.time() - self.start_time
            base_score = max(1, int(20 - time_taken))  
            multiplier = self.difficulty_multipliers.get(self.tagad_limenis, 1)
            question_score = int(base_score * multiplier)
            
            if float(lietotaja_atb) == self.tagad_atbilde:
                self.punkti += 1
                self.total_score += question_score
                self.atsauksme_label.config(text=f"Pareizi! +{question_score} punkti", fg='green')
                self.rezultatu_label.config(text=f"Pareizās atbildes: {self.punkti}/{self.kop_uzd}")
                self.score_label.config(text=f"Kopējais rezultāts: {self.total_score}")
                self.jauns_uzd()
            else:
                self.atsauksme_label.config(text=f"Nepareizi! Mēģini vēlreiz!", fg='red')
                self.rezultatu_label.config(text=f"Pareizās atbildes: {self.punkti}/{self.kop_uzd}")
                self.score_label.config(text=f"Kopējais rezultāts: {self.total_score}")
                self.atbildes_ievad.delete(0, END)
        except ValueError:
            self.atsauksme_label.config(text="Lūdzu ievadiet skaitli!", fg='red')

    def jauns_uzd(self):
        if self.tagadejs_timers:
            self.window.after_cancel(self.tagadejs_timers)   
        uzdevums, self.tagad_atbilde = self.uzdevumu_gen(self.tagad_limenis)
        self.uzd_label.config(text=uzdevums)
        self.atbildes_ievad.delete(0, END)
        self.atsauksme_label.config(text="")
        self.start_time = time.time()  # Restartē taimeri jaunam uzdevumam
        self.tameris()

    def tameris(self, remaining=20):
        self.timer_label.config(text=f"Atlicis laiks: {remaining}s")
        if remaining > 0:
            self.tagadejs_timers = self.window.after(1000, self.tameris, remaining-1)
        else:
            self.timer_label.config(text="Laiks beidzies!")
            self.tagadejs_timers = self.window.after(2000, self.rezultati)

    def rezultati(self):
        self.clear_window()
        self.window.title("Rezultāti")
        Label(self.window, text="Spēle Pabeigta!", font=("Arial", 24), bg=self.bg_color, fg='white').pack(pady=20)
        Label(self.window, text=f"Pareizās atbildes: {self.punkti}", font=("Arial", 18), bg=self.bg_color, fg='white').pack()
        Label(self.window, text=f"Izpildītie uzdevumi: {self.kop_uzd}", font=("Arial", 18), bg=self.bg_color, fg='white').pack()
        Label(self.window, text=f"Kopējais rezultāts: {self.total_score}", font=("Arial", 18), bg=self.bg_color, fg='white').pack()
        
        # Calculate grade based on total score
        grade = "Nepietiekami"
        if self.total_score >= 300:
            grade = "Izcili!"
        elif self.total_score >= 200:
            grade = "Labi"
        elif self.total_score >= 100:
            grade = "Viduvēji"
        elif self.total_score > 0:
            grade = "Vāji! Trenējies vēl vairāk!"
            
        Label(self.window, text=f"Vērtējums: {grade}", font=("Arial", 18, "bold"), bg=self.bg_color, fg='white').pack(pady=10)
        
        # Parādas procenti attiecībā uz pareizi izpildīto uzdevumu skaitu
        if self.kop_uzd > 0:
            procenti = (self.punkti / self.kop_uzd) * 100
            color = 'white'
            Label(self.window, text=f"Precizitāte: {procenti:.1f}%", font=("Arial", 18), bg=self.bg_color, fg=color).pack(pady=10)
        Button(self.window, text="Spēlēt vēlreiz", font=("Arial", 16), bg=self.btn_color, fg=self.btn_text_color,command=self.sakumaekrans).pack(pady=20)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        if hasattr(self, 'tagadejs_timers') and self.tagadejs_timers:
            self.window.after_cancel(self.tagadejs_timers)
            self.tagadejs_timers = None
        self.window.configure(bg=self.bg_color)

if __name__ == "__main__":
    window = Tk()
    game = MatSpele(window)
    window.mainloop()
