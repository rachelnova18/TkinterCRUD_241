import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

#   KONEKSI DATABASE
def koneksi():
    return sqlite3.connect("nilai_siswa.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    con.commit()
    con.close()

#   FUNGSI Create, Read, Update, Delete (CRUD)
def insert_siswa(nama, bio, fis, inggris, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, bio, fis, inggris, prediksi))
    con.commit()
    con.close()

def read_siswa():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT * FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

def update_siswa(id, nama, bio, fis, ing, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        UPDATE nilai_siswa
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
    """, (nama, bio, fis, ing, prediksi, id))
    con.commit()
    con.close()

def delete_siswa(id):
    con = koneksi()
    cur = con.cursor()
    cur.execute("DELETE FROM nilai_siswa WHERE id=?", (id,))
    con.commit()
    con.close()

#   GUI TKINTER
class AplikasiNilai(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Berdasarkan Nilai")
        self.geometry("750x550")
        self.selected_id = None

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

        # Tombol submit
        btn_submit = tk.Button(frame, text="Submit Nilai", bg="lightblue", command=self.proses_data)
        btn_submit.grid(row=4, column=1, pady=10, sticky="w")

        # Tombol refresh
        btn_refresh = tk.Button(frame, text="Refresh", bg="lightgreen", command=self.load_data)
        btn_refresh.grid(row=4, column=1, padx=120, pady=10)

        # Tombol update
        btn_update = tk.Button(frame, text="Update", bg="orange", command=self.update_data)
        btn_update.grid(row=5, column=1, pady=5, sticky="w")

        # Tombol delete
        btn_delete = tk.Button(frame, text="Delete", bg="red", command=self.delete_data)
        btn_delete.grid(row=5, column=1, padx=120, pady=5)

        # Tabel Treeview
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

        # Event klik baris tabel
        self.tree.bind("<<TreeviewSelect>>", self.get_selected)

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

        # Logika Prediksi Fakultas
        nilai_max = max(bio, fis, ing)

        if nilai_max == bio:
            prediksi = "Kedokteran"
        elif nilai_max == fis:
            prediksi = "Teknik"
        else:
            prediksi = "Bahasa"

        insert_siswa(nama, bio, fis, ing, prediksi)
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        self.load_data()
        self.clear_input()

    # LOAD DATA KE TABLE
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = read_siswa()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    # GET SELECTED ROW
    def get_selected(self, event):
        selected = self.tree.focus()
        data = self.tree.item(selected)["values"]

        if data:
            self.selected_id = data[0]
            self.ent_nama.delete(0, tk.END)
            self.ent_bio.delete(0, tk.END)
            self.ent_fis.delete(0, tk.END)
            self.ent_ing.delete(0, tk.END)

            self.ent_nama.insert(0, data[1])
            self.ent_bio.insert(0, data[2])
            self.ent_fis.insert(0, data[3])
            self.ent_ing.insert(0, data[4])

    # UPDATE DATA
    def update_data(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Pilih data dari tabel!")
            return

        try:
            nama = self.ent_nama.get()
            bio = int(self.ent_bio.get())
            fis = int(self.ent_fis.get())
            ing = int(self.ent_ing.get())
        except:
            messagebox.showerror("Error", "Nilai harus angka!")
            return

        nilai_max = max(bio, fis, ing)
        prediksi = "Kedokteran" if nilai_max == bio else "Teknik" if nilai_max == fis else "Bahasa"

        update_siswa(self.selected_id, nama, bio, fis, ing, prediksi)
        self.load_data()
        self.clear_input()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")

    # DELETE DATA
    def delete_data(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Pilih data yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            delete_siswa(self.selected_id)
            self.load_data()
            self.clear_input()
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")

    def clear_input(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_bio.delete(0, tk.END)
        self.ent_fis.delete(0, tk.END)
        self.ent_ing.delete(0, tk.END)
        self.selected_id = None

# MAIN APP
if __name__ == "__main__":
    create_table()
    app = AplikasiNilai()
    app.mainloop()