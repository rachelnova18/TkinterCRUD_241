import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# KONEKSI DATABASE & TABLE
def koneksi():
    return sqlite3.connect("nilai_siswa.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()

# FUNGSI INSERT DAN READ
def insert_siswa(nama, bio, fis, inggris, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, inggris, prediksi))
    con.commit()
    con.close()

def read_siswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT * FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

# GUI TKINTER
class AplikasiNilai(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Berdasarkan Nilai")
        self.geometry("700x500")

        # ---------------- Frame Input ----------------
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Nama Siswa").grid(row=0, column=0, sticky="w")
        tk.Label(frame, text="Nilai Biologi").grid(row=1, column=0, sticky="w")
        tk.Label(frame, text="Nilai Fisika").grid(row=2, column=0, sticky="w")
        tk.Label(frame, text="Nilai Inggris").grid(row=3, column=0, sticky="w")

        self.ent_nama = tk.Entry(frame, width=30)
        self.ent_bio = tk.Entry(frame, width=30)
        self.ent_fis = tk.Entry(frame, width=30)
        self.ent_ing = tk.Entry(frame, width=30)

        self.ent_nama.grid(row=0, column=1, pady=5)
        self.ent_bio.grid(row=1, column=1, pady=5)
        self.ent_fis.grid(row=2, column=1, pady=5)
        self.ent_ing.grid(row=3, column=1, pady=5)

        btn_submit = tk.Button(frame, text="Submit Nilai", command=self.proses_data)
        btn_submit.grid(row=4, column=1, pady=10, sticky="w")

        btn_refresh = tk.Button(frame, text="Refresh", command=self.load_data)
        btn_refresh.grid(row=4, column=1, padx=120, pady=10)

        # ---------------- Tabel Treeview ----------------
        columns = ("id", "nama", "bio", "fis", "ing", "prediksi")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("bio", text="Biologi")
        self.tree.heading("fis", text="Fisika")
        self.tree.heading("ing", text="Inggris")
        self.tree.heading("prediksi", text="Prediksi Fakultas")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nama", width=150)
        self.tree.column("bio", width=80, anchor="center")
        self.tree.column("fis", width=80, anchor="center")
        self.tree.column("ing", width=80, anchor="center")
        self.tree.column("prediksi", width=140, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_data()

    # PROSES INPUT → HITUNG → SIMPAN
    def proses_data(self):
        try:
            nama = self.ent_nama.get()
            bio = int(self.ent_bio.get())
            fis = int(self.ent_fis.get())
            ing = int(self.ent_ing.get())
        except:
            messagebox.showerror("Error", "Harap masukkan nilai berupa angka!")
            return

        # ---- Logika Prediksi Fakultas ----
        nilai_max = max(bio, fis, ing)

        if nilai_max == bio:
            prediksi = "Kedokteran"
        elif nilai_max == fis:
            prediksi = "Teknik"
        else:
            prediksi = "Bahasa"

        # ---- Simpan ke DB ----
        insert_siswa(nama, bio, fis, ing, prediksi)
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")

        self.load_data()

        # Clear input
        self.ent_nama.delete(0, tk.END)
        self.ent_bio.delete(0, tk.END)
        self.ent_fis.delete(0, tk.END)
        self.ent_ing.delete(0, tk.END)

    # LOAD DATA KE TABEL
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = read_siswa()
        for row in rows:
            self.tree.insert("", tk.END, values=row)


# MAIN RUN
if __name__ == "__main__":
    create_table()
    app = AplikasiNilai()
    app.mainloop()