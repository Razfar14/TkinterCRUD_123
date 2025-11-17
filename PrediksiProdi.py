import sqlite3
import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk


def koneksi():
    con = sqlite3.connect("PrediksiProdi.db")
    return con

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Calaon_Mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            NBa INTEGER,
            NF INTEGER,
            NBi INTEGER,
            Prediksi_Prodi TEXT
        )
    """)
    ##NBa = Nilai Nilai Bahasa Indonesia
    ##NF = Nilai Nilai Fisika
    ##NBi = Nilai Nilai Biologi
    con.commit()
    con.close()

def insertsiswa(name: str, NBa: int, NF: int, NBi: int, Prediksi: str ) -> int:
    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO Calaon_Mahasiswa (name, NBa, NF, NBi, Prediksi_Prodi ) VALUES (?, ?, ?, ?, ?)", (name, NBa, NF, NBi, Prediksi))
    con.commit()
    rowid = cur.lastrowid
    con.close()
    return rowid

def readsiswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT id, name, NBa, NF, NBi, Prediksi_Prodi FROM Calaon_Mahasiswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows


create_table()

class Mahasiswa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insert dan Read Data Calaon_Mahasiswa")
        self.geometry("600x420")
        self.configure(bg="#f0f2f5")

        frm = tk.Frame(self, bg="#ffffff", padx=12, pady=12)
        frm.pack(padx=16, pady=12, fill="x")

        tk.Label(frm, text="Nama:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_name = tk.Entry(frm, width=30)
        self.ent_name.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Bahasa Inggris:", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_NBa = tk.Entry(frm, width=30)
        self.ent_NBa.grid(row=1, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Fisika:", bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.ent_NF = tk.Entry(frm, width=30)
        self.ent_NF.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        tk.Label(frm, text="Nilai Biologi:", bg="#ffffff").grid(row=3, column=0, sticky="w")
        self.ent_NBi = tk.Entry(frm, width=30)
        self.ent_NBi.grid(row=3, column=1, sticky="w", padx=6, pady=6)

        btn_frame = tk.Frame(frm, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(6,0))

        self.btn_add = tk.Button(btn_frame, text="Tambah", width=10, command=self.insertdata)
        self.btn_add.pack(side="left", padx=6)
        self.btn_refresh = tk.Button(btn_frame, text="Refresh", width=10, command=self.read_data)
        self.btn_refresh.pack(side="left", padx=6)

        cols = ("id", "name", "NBa", "NF", "NBi","Prediksi Prodi")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        self.tree.heading("name", text="Nama")
        self.tree.column("name", width=350)
        self.tree.heading("NBa", text="Nilai Bahasa Inggris")
        self.tree.column("NBa", width=80, anchor="center")
        self.tree.heading("NF", text="Nilai Fisika")
        self.tree.column("NF", width=80, anchor="center")
        self.tree.heading("NBi", text="Nilai Biologi")
        self.tree.column("NBi", width=80, anchor="center")
        self.tree.heading("Prediksi Prodi", text="Prediksi Prodi")
        self.tree.column("Prediksi Prodi", width=150, anchor="center")
        self.tree.pack(padx=16, pady=(0,12), fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.read_data()

    def clear_inputs(self):
        self.ent_name.delete(0, tk.END)
        self.ent_NBa.delete(0, tk.END)
        self.ent_NF.delete(0, tk.END)
        self.ent_NBi.delete(0, tk.END)

    def validate_inputs(self):
        name = self.ent_name.get().strip()
        NBa_str = self.ent_NBa.get().strip()
        NF_str = self.ent_NF.get().strip()
        NBi_str = self.ent_NBi.get().strip()
        prediksi = self.prediks_prodi(int(NBa_str), int(NF_str), int(NBi_str))
        if not name or not NBa_str and not NF_str and not NBi_str:
            msg.showwarning("Peringatan", "Nama dan Nilai tidak boleh kosong.")
            return None
        try:
            NBa = int(NBa_str)
            NF = int(NF_str)
            NBi = int(NBi_str)
        
            if NBa and NF and NBi  < 0:
                raise ValueError
             
        except ValueError:
            msg.showerror("Salah", "Nilai tidak boleh kurang dari 0 dan harus bilangan bulat.")
            return None
        return name, NBa, NF, NBi, prediksi

    def insertdata(self):
        val = self.validate_inputs()
        if not val:
            return
        name, NBa, NF, NBi, Prediksi = val
        try:
            new_id = insertsiswa(name, NBa, NF, NBi,Prediksi) 
            msg.showinfo("Sukses", f"Data disimpan (id={new_id})\n" f"Prediksi Prodi: {self.prediks_prodi(NBa, NF, NBi)}")
            self.read_data()
            self.clear_inputs()
        except Exception as e:
            msg.showerror("DB Error", str(e))

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        _, name, NBa, NF, NBi = item["values"]
        self.ent_name.insert(0, name)
        self.ent_NBa(0, str(NBa))
        self.ent_NF(0, str(NF))
        self.ent_NBi(0, str(NBi))

    def read_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            rows = readsiswa()
            for r in rows:
                self.tree.insert("", tk.END, values=r)
        except Exception as e:
            msg.showerror("DB Error", str(e))
    
    def prediks_prodi(self, NBa, NF, NBi):
        if NBa >= NF and NBa >= NBi:
            return "Bahasa"
        elif NF >= NBa and NF >= NBi:
            return "Teknik"
        elif NBi >= NBa and NBi >= NF:
            return "Kedokteran"
        else:
            return "Masuk Kemana Saja"  

if __name__ == "__main__":
    app = Mahasiswa()
    app.mainloop()
