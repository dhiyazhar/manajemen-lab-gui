import os
import traceback
import csv
import tkinter.ttk as ttk
from tkinter import messagebox
import customtkinter
from penggunaan import Button, CustomTreeviewStyle

class Peralatan(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.file_path = "./data/peralatan_lab.csv"
        
        self.dialog = None
        
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(1, weight=1)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 0)) 
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="kolom") 

        self.b_add_inventory = Button(self.button_frame, text="Tambah Inventori Peralatan", command=self.add_inventory) 
        self.b_delete_inventory = Button(self.button_frame, text="Hapus Inventori Peralatan", command=self.delete_inventory)
        self.b_edit_inventory = Button(self.button_frame, text="Edit Inventori Peralatan", command=self.edit_inventory)

        self.b_add_inventory.grid(row=0, column=0, padx=5, pady=5, sticky="nsew") 
        self.b_delete_inventory.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") 
        self.b_edit_inventory.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.inventory_table_frame = customtkinter.CTkFrame(self)
        self.inventory_table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.table_wrapper = customtkinter.CTkFrame(self.inventory_table_frame)
        self.table_wrapper.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.inventory_table = ttk.Treeview(self.table_wrapper, style="Treeview", selectmode="browse")
        self.inventory_table['show'] = 'headings'
        self.inventory_table.pack(fill="both", expand=True)


    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        
        style = CustomTreeviewStyle()        
        self.load_data()
        

    def hide(self):
        self.grid_remove()
        
    def load_data(self):
        self.inventory_table.delete(*self.inventory_table.get_children())

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                file_columns = tuple(reader.fieldnames)
                
                self.inventory_table["columns"] = ("No.",) + file_columns

                max_width = {"No.": len("No.")}
                max_width.update({col: len(col) for col in file_columns})
                
                rows = list(reader)
                for i, row in enumerate(rows, start=1):
                    max_width["No."] = max(max_width["No."], len(str(i)))
                    for col in file_columns:
                        max_width[col] = max(max_width[col], len(str(row[col])))

                # Atur heading dan width kolom
                total_width = sum(max_width.values())
                all_columns = ("No.",) + file_columns
                for col in all_columns:
                    width_ratio = max_width[col] / total_width
                    if col == 'No.':
                        self.inventory_table.column(col, width=50, stretch=False)
                    # elif col == 'ID':
                    #     self.inventory_table.column(col, width=80, stretch=False)
                    else:
                        self.inventory_table.column(col, width=int(width_ratio * 800), stretch=True)
                    self.inventory_table.heading(col, text=col.title())

                for i, row in enumerate(rows, start=1):
                    self.inventory_table.insert("", "end", values=(i,) + tuple(row.values()))

        except FileNotFoundError:
            print(f"File {self.file_path} tidak ditemukan.")   
            
    def add_inventory(self):
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = TambahPeralatanDialog(self)
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
            messagebox.showinfo("Sukses", "Data inventori peralatan berhasil ditambahkan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan data: {str(e)}")
    
    def delete_inventory(self):
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus terlebih dahulu.")
            return
        
        confirm = messagebox.askyesno("Konfirmasi", "Hapus Data?")
        if confirm:
            item_values = self.inventory_table.item(selected_item)['values']
            self.delete_csv(item_values[1:])  # Skip the "No." column
    
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
                messagebox.showinfo("Sukses", "Data peralatan berhasil dihapus.")
                self.load_data()  # Refresh the table
            else:
                messagebox.showwarning("Peringatan", "Data tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def edit_inventory(self):
        selected_item = self.inventory_table.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diedit terlebih dahulu.")
            return
        
        item_values = self.inventory_table.item(selected_item)['values']
        self.open_edit_dialog(item_values[1:])  # Skip the "No." column

    def open_edit_dialog(self, data):
        try:
            dialog = EditPeralatanDialog(self, data)
            dialog.wait_visibility()  # Wait for the dialog to be visible
            dialog.grab_set()  # Set the grab
            self.wait_window(dialog)  # Wait for the dialog to be closed
            if dialog.result:
                self.update_csv(data, dialog.result)
                self.load_data()  # Refresh the table after editing data
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
                messagebox.showinfo("Sukses", "Data peralatan berhasil diperbarui.")
                self.load_data() 
            else:
                messagebox.showwarning("Peringatan", "Data tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {str(e)}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
class TambahPeralatanDialog(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tambah Peralatan")
        self.geometry("500x480")
        self.result = None

        self.nama_label = customtkinter.CTkLabel(self, text="Nama:")
        self.nama_label.pack()
        self.nama_entry = customtkinter.CTkEntry(self)
        self.nama_entry.pack(pady=(0, 10))

        self.status_label = customtkinter.CTkLabel(self, text="Status:")
        self.status_label.pack()
        self.status_combobox = customtkinter.CTkComboBox(self, values=["Baik", "Rusak Ringan", "Rusak Berat"])
        self.status_combobox.pack(pady=(0, 10))

        self.jumlah_label = customtkinter.CTkLabel(self, text="Jumlah:")
        self.jumlah_label.pack()
        self.jumlah_entry = customtkinter.CTkEntry(self)
        self.jumlah_entry.pack(pady=(0, 10))

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        nama = self.nama_entry.get()
        status = self.status_combobox.get()

        if not all([nama, status]):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return
        
        self.result = [nama, status]
        self.destroy()

class EditPeralatanDialog(customtkinter.CTkToplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("Edit Peralatan")
        self.geometry("500x480")
        self.result = None

        self.nama_label = customtkinter.CTkLabel(self, text="Nama:")
        self.nama_label.pack(pady=(10, 0))
        self.nama_entry = customtkinter.CTkEntry(self)
        self.nama_entry.insert(0, data[0])
        self.nama_entry.pack(pady=(0, 10))

        self.status_label = customtkinter.CTkLabel(self, text="Status:")
        self.status_label.pack()
        self.status_combobox = customtkinter.CTkComboBox(self, values=["Baik", "Rusak Ringan", "Rusak Berat"])
        self.status_combobox.set(data[1])
        self.status_combobox.pack(pady=(0, 10))

        self.submit_button = customtkinter.CTkButton(self, text="Update", command=self.submit)
        self.submit_button.pack(pady=10)

    def submit(self):
        nama = self.nama_entry.get()
        status = self.status_combobox.get()

        if not all([nama, status]):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        self.result = [nama, status]
        self.destroy()
            
        
        
                        