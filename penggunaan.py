import os
import traceback
import csv
from datetime import datetime
import customtkinter
import tkinter.ttk as ttk
from tkinter import messagebox
from crud import CRUD


class Penggunaan(customtkinter.CTkFrame, CRUD):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.file_path = "./data/penggunaan_lab.csv"
        
        self.dialog = None       
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_add_usage = Button(self.button_frame, text="Tambah Penggunaan", command=self.add_data) 
        self.b_delete_usage = Button(self.button_frame, text="Hapus Penggunaan", command=self.delete_data)
        self.b_edit_usage = Button(self.button_frame, text="Edit Penggunaan", command=self.edit_data)

        self.b_add_usage.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_delete_usage.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_usage.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.usage_table_frame = customtkinter.CTkFrame(self)
        self.usage_table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.table_wrapper = customtkinter.CTkFrame(self.usage_table_frame)
        self.table_wrapper.pack(fill="both", expand=True, padx=20, pady=20)

        self.table = ttk.Treeview(self.table_wrapper, style="Treeview", selectmode="browse")
        self.table['show'] = 'headings'
        self.table.pack(fill="both", expand=True)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = CustomTreeviewStyle()        
        self.load_data()


    def hide(self):
        self.grid_remove()
        
    def load_data(self):
        self.table.delete(*self.table.get_children())

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                file_columns = tuple(reader.fieldnames)

                self.table["columns"] = ("No.",) + tuple(reader.fieldnames)

                max_width = {"No.": len("No.")}
                max_width.update({col: len(col) for col in file_columns})
                
                rows = list(reader)
                for i, row in enumerate(rows, start=1):
                    max_width["No."] = max(max_width["No."], len(str(i)))
                    for col in reader.fieldnames:
                        if col == 'Tanggal':
                            tanggal_str = datetime.strptime(row['Tanggal'], '%Y-%m-%d').strftime('%d-%m-%Y')
                            max_width[col] = max(max_width[col], len(str(row[col])))
                        else:
                            max_width[col] = max(max_width[col], len(str(row[col])))
                            
                total_width = sum(max_width.values())
                all_columns = ("No.",) + file_columns
                for col in all_columns:
                    width_ratio = max_width[col] / total_width
                    if col == 'No':
                        self.table.column(col, width=50, stretch=False)
                    elif col == 'Tanggal':
                        self.table.column(col, width=100, stretch=False)
                    elif col in ['Kelas', 'Dosen', 'Penanggung Jawab']:
                        self.table.column(col, width=max(150, int(width_ratio * 800)), stretch=True)
                    else:
                        self.table.column(col, width=int(width_ratio * 800), stretch=True)
                    self.table.heading(col, text=col.title())

                for i, row in enumerate(rows, start=1):
                    tanggal = datetime.strptime(row['Tanggal'], '%Y-%m-%d').strftime('%d-%m-%Y')
                    values = list(row.values())
                    values[1] = tanggal
                    self.table.insert("", "end", values=(i,) + tuple(row.values()))

                    
        except FileNotFoundError:
            print(f"File {self.file_path} tidak ditemukan.")
    
    def add_data(self):
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = TambahPenggunaanDialog(self)
            self.dialog.grab_set()
            self.wait_window(self.dialog)
        if self.dialog.result:
            self.add_csv(self.dialog.result)
            self.load_data()  
        else:
            self.dialog.focus()  
    
    def add_csv(self, data):
        try:
            with open(self.file_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
            messagebox.showinfo("Sukses", "Data penggunaan berhasil ditambahkan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {str(e)}")
    
    def delete_data(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus terlebih dahulu.")
            return
        
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if confirm:
            item_values = self.table.item(selected_item)['values']
            self.delete_csv(item_values[1:]) 
    
    def delete_csv(self, row_data):
        temp_file = self.file_path + '.tmp'
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file, \
                open(temp_file, 'w', newline='', encoding='utf-8') as temp:
                reader = csv.reader(file)
                writer = csv.writer(temp)
                header = next(reader)
                writer.writerow(header)
                deleted = False
                for row in reader:
                    if row != row_data:
                        writer.writerow(row)
                    else:
                        deleted = True
            
            os.replace(temp_file, self.file_path)
            
            if deleted:
                messagebox.showinfo("Sukses", "Data penggunaan berhasil dihapus.")
                self.load_data() 
            else:
                messagebox.showwarning("Peringatan", "Data tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def edit_data(self):
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diedit terlebih dahulu.")
            return

        item_values = self.table.item(selected_item)['values']
        self.edit_dialog(item_values[1:]) 

    def edit_dialog(self, data):
        try:
            dialog = EditPenggunaanDialog(self, data)
            dialog.wait_visibility()
            dialog.grab_set()  
            self.wait_window(dialog)  
            if dialog.result:
                self.update_csv(data, dialog.result)
                self.load_data() 
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    
    def update_csv(self, old_data, new_data):
        temp_file = self.file_path + '.tmp'
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file, \
                 open(temp_file, 'w', newline='', encoding='utf-8') as temp:
                reader = csv.reader(file)
                writer = csv.writer(temp)
                header = next(reader)
                writer.writerow(header)
                updated = False
                for row in reader:
                    if row == old_data:
                        writer.writerow(new_data)
                        updated = True
                    else:
                        writer.writerow(row)
            
            os.replace(temp_file, self.file_path)
            
            if updated:
                messagebox.showinfo("Sukses", "Data penggunaan berhasil diperbarui.")
                self.load_data() 
            else:
                messagebox.showwarning("Peringatan", "Data tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)

class TambahPenggunaanDialog(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tambah Penggunaan")
        self.geometry("500x480")
        self.result = None

        self.tanggal_label = customtkinter.CTkLabel(self, text="Tanggal (YYYY-MM-DD):")
        self.tanggal_label.pack(pady=(10, 0))
        self.tanggal_entry = customtkinter.CTkEntry(self)
        self.tanggal_entry.pack(pady=(0, 10))

        self.kelas_label = customtkinter.CTkLabel(self, text="Kelas:")
        self.kelas_label.pack()
        self.kelas_entry = customtkinter.CTkEntry(self)
        self.kelas_entry.pack(pady=(0, 10))

        self.dosen_label = customtkinter.CTkLabel(self, text="Dosen:")
        self.dosen_label.pack()
        self.dosen_entry = customtkinter.CTkEntry(self)
        self.dosen_entry.pack(pady=(0, 10))

        self.penanggung_jawab_label = customtkinter.CTkLabel(self, text="Penanggung Jawab:")
        self.penanggung_jawab_label.pack()
        self.penanggung_jawab_entry = customtkinter.CTkEntry(self)
        self.penanggung_jawab_entry.pack(pady=(0, 10))

        self.deskripsi_label = customtkinter.CTkLabel(self, text="Deskripsi:")
        self.deskripsi_label.pack()
        self.deskripsi_entry = customtkinter.CTkEntry(self)
        self.deskripsi_entry.pack(pady=(0, 10))

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        tanggal = self.tanggal_entry.get()
        kelas = self.kelas_entry.get()
        dosen = self.dosen_entry.get()
        penanggung_jawab = self.penanggung_jawab_entry.get()
        deskripsi = self.deskripsi_entry.get()

        if not all([tanggal, kelas, dosen, penanggung_jawab, deskripsi]):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        try:
            datetime.strptime(tanggal, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD.")
            return

        self.result = [tanggal, kelas, dosen, penanggung_jawab, deskripsi]
        self.destroy()

class EditPenggunaanDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("Edit Penggunaan")
        self.geometry("500x480")
        self.result = None

        self.tanggal_label = customtkinter.CTkLabel(self, text="Tanggal (YYYY-MM-DD):")
        self.tanggal_label.pack(pady=(10, 0))
        self.tanggal_entry = customtkinter.CTkEntry(self)
        self.tanggal_entry.insert(0, data[0])
        self.tanggal_entry.pack(pady=(0, 10))

        self.kelas_label = customtkinter.CTkLabel(self, text="Kelas:")
        self.kelas_label.pack()
        self.kelas_entry = customtkinter.CTkEntry(self)
        self.kelas_entry.insert(0, data[1])
        self.kelas_entry.pack(pady=(0, 10))

        self.dosen_label = customtkinter.CTkLabel(self, text="Dosen:")
        self.dosen_label.pack()
        self.dosen_entry = customtkinter.CTkEntry(self)
        self.dosen_entry.insert(0, data[2])
        self.dosen_entry.pack(pady=(0, 10))

        self.penanggung_jawab_label = customtkinter.CTkLabel(self, text="Penanggung Jawab:")
        self.penanggung_jawab_label.pack()
        self.penanggung_jawab_entry = customtkinter.CTkEntry(self)
        self.penanggung_jawab_entry.insert(0, data[3])
        self.penanggung_jawab_entry.pack(pady=(0, 10))

        self.deskripsi_label = customtkinter.CTkLabel(self, text="Deskripsi:")
        self.deskripsi_label.pack()
        self.deskripsi_entry = customtkinter.CTkEntry(self)
        self.deskripsi_entry.insert(0, data[4])
        self.deskripsi_entry.pack(pady=(0, 10))

        self.submit_button = customtkinter.CTkButton(self, text="Update", command=self.submit)
        self.submit_button.pack(pady=10)

        self.after(100, self.grab_set)

    def submit(self):
        tanggal = self.tanggal_entry.get()
        kelas = self.kelas_entry.get()
        dosen = self.dosen_entry.get()
        penanggung_jawab = self.penanggung_jawab_entry.get()
        deskripsi = self.deskripsi_entry.get()

        if not all([tanggal, kelas, dosen, penanggung_jawab, deskripsi]):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        try:
            datetime.strptime(tanggal, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD.")
            return

        self.result = [tanggal, kelas, dosen, penanggung_jawab, deskripsi]
        self.destroy()
                
        
class CustomTreeviewStyle:
    def __init__(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.configure_treeview()

    def configure_treeview(self):
        self.style.configure("Treeview",
                            background=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            foreground=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"][1],
                            fieldbackground=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][1],
                            bordercolor=customtkinter.ThemeManager.theme["CTkFrame"]["border_color"][1],
                            borderwidth=0)

        self.style.configure("Treeview.Heading",
                            background=customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"][1],
                            foreground=customtkinter.ThemeManager.theme["CTkLabel"]["text_color"][1],
                            relief="flat")

        self.style.map("Treeview.Heading",
                      relief=[('active', 'groove'), ('pressed', 'sunken')])

        self.style.map("Treeview",
                      background=[('selected', customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][1])],
                      foreground=[('selected', customtkinter.ThemeManager.theme["CTkButton"]["text_color"][1])])
        

class Button(customtkinter.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, font=customtkinter.CTkFont(size=15), **kwargs)
        




    

