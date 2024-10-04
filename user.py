import os
import csv
import customtkinter
import tkinter.ttk as ttk
from tkinter import messagebox
from penggunaan import Button, CustomTreeviewStyle

class User(customtkinter.CTkFrame): 
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.file_path = "./data/user.csv"
        
        self.dialog = None

        self.grid_columnconfigure(0, weight=1)  # Biar label memenuhi horizontal
        self.grid_rowconfigure(1, weight=1) # Button frame tidak perlu melar

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_add_user = Button(self.button_frame, text="Tambah User", command=self.add_user) 
        self.b_delete_user = Button(self.button_frame, text="Hapus User", command=self.delete_user)
        self.b_edit_user = Button(self.button_frame, text="Edit User", command=self.edit_user)

        self.b_add_user.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_delete_user.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_user.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.user_table_frame = customtkinter.CTkFrame(self)
        self.user_table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Buat Treeview di dalam tabel_pengguna_frame
        self.table_wrapper = customtkinter.CTkFrame(self.user_table_frame)
        self.table_wrapper.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.user_table = ttk.Treeview(self.table_wrapper, style="Treeview", selectmode="browse")
        self.user_table['show'] = 'headings'
        self.user_table.pack(fill="both", expand=True)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = CustomTreeviewStyle()
        self.load_data()
        

    def hide(self):
        self.grid_remove()
        
    def load_data(self):
        self.user_table.delete(*self.user_table.get_children())
        
        try: 
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file) 
                file_columns = tuple(reader.fieldnames)
        
                self.user_table["columns"] = ("No.",) + tuple(reader.fieldnames)
                
                max_width = {"No.": len("No.")}
                max_width.update({col: len(col) for col in file_columns})
                
                rows = list(reader)
                for i, row in enumerate(rows, start=1): 
                    max_width["No."] = max(max_width["No."], len(str(i)))
                    for col in file_columns:
                        max_width[col] = max(max_width[col], len(str(row[col])))
                
                total_width = sum(max_width.values())
                all_columns = ("No.",) + file_columns
                for col in all_columns:
                    width_ratio = max_width[col] / total_width
                    
                    if col == 'No.':
                        self.user_table.column(col, width=50, stretch=False)
                    elif col == 'Status':
                        self.user_table.column(col, width=80, stretch=False)
                    else:
                        self.user_table.column(col, width=int(width_ratio * 800), stretch=True)
                    self.user_table.heading(col, text=col.title())
                
                for i, row in enumerate(rows, start=1):
                    self.user_table.insert("", "end", values=(i,) + tuple(row.values()))

        except FileNotFoundError:
            print(f"File {self.file_path} tidak ditemukan.")
    
    def add_user(self):
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = AddUserDialog(self)
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
            messagebox.showinfo("Sukses", "Data User berhasil ditambahkan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {str(e)}")
    
    def delete_user(self):
        selected_user = self.user_table.selection()
        if not selected_user:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus terlebih dahulu.")
            return
        
        confirm = messagebox.askyesno("Konfirmasi", "Hapus Data?")
        if confirm:
            user_values = self.user_table.item(selected_user)['values']
            self.delete_csv(user_values[1:])  # Skip the "No." column
    
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
                        print(f"data deleted false {row}")
                    else:
                        deleted = True
                        print(f"data deleted true {row}")
            
            os.replace(temp_file, self.file_path)
            
            if deleted:
                messagebox.showinfo("Sukses", "Data user berhasil dihapus.")
                self.load_data() 
            else:
                messagebox.showwarning("Peringatan", "Data tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def edit_user(self):
        selected_user = self.user_table.selection()
        if not selected_user:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diedit terlebih dahulu.")
            return
        
        user_values = self.user_table.item(selected_user)['values']
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = EditUserDialog(self, user_values[1:])  
            self.dialog.grab_set()
            self.wait_window(self.dialog)
        if self.dialog.result:
            self.update_csv(user_values[1:], self.dialog.result)
            self.load_data() 
        else:
            self.dialog.focus()
    
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
                messagebox.showinfo("Sukses", "Data user berhasil diperbarui.")
                self.load_data() 
            else:
                messagebox.showwarning("Peringatan", "Data tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
class AddUserDialog(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tambah User")
        self.geometry("500x480")
        self.result = None

        self.nama_label = customtkinter.CTkLabel(self, text="Nama:")
        self.nama_label.pack()
        self.nama_entry = customtkinter.CTkEntry(self)
        self.nama_entry.pack(pady=(0, 10))

        self.status_label = customtkinter.CTkLabel(self, text="Status:")
        self.status_label.pack()
        self.status_combobox = customtkinter.CTkComboBox(self, values=["Dosen", "Mahasiswa"])
        self.status_combobox.pack(pady=(0, 10))

        self.jabatan_label = customtkinter.CTkLabel(self, text="Jabatan:")
        self.jabatan_label.pack()
        self.jabatan_entry = customtkinter.CTkEntry(self)
        self.jabatan_entry.pack(pady=(0, 10))

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        # id = self.id_entry.get()
        nama = self.nama_entry.get()
        status = self.status_combobox.get()
        jabatan = self.jabatan_entry.get()

        if not all([nama, status, jabatan]):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        self.result = [nama, status, jabatan]
        self.destroy()

class EditUserDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("Edit Penggunaan")
        self.geometry("500x480")
        self.result = None

        self.nama_label = customtkinter.CTkLabel(self, text="Nama:")
        self.nama_label.pack(pady=(10, 0))
        self.nama_entry = customtkinter.CTkEntry(self)
        self.nama_entry.insert(0, data[0])
        self.nama_entry.pack(pady=(0, 10))

        self.status_label = customtkinter.CTkLabel(self, text="Status:")
        self.status_label.pack()
        self.status_combobox = customtkinter.CTkComboBox(self, values=["Dosen", "Mahasiswa"])
        self.status_combobox.set(data[1])
        self.status_combobox.pack(pady=(0, 10))

        self.jabatan_label = customtkinter.CTkLabel(self, text="Jabatan:")
        self.jabatan_label.pack()
        self.jabatan_entry = customtkinter.CTkEntry(self)
        self.jabatan_entry.insert(0, data[2])
        self.jabatan_entry.pack(pady=(0, 10))

        self.submit_button = customtkinter.CTkButton(self, text="Update", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        nama = self.nama_entry.get()
        status = self.status_combobox.get()
        jabatan = self.jabatan_entry.get()

        if not all([nama, status, jabatan]):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        self.result = [nama, status, jabatan]
        self.destroy()
                

