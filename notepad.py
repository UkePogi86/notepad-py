import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

class Notepad:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notepad")
        self.root.geometry("500x500")
        self.text = tk.Text(self.root)
        self.text.insert('1.0', 'Enter text here...')
        self.text.bind("<FocusIn>", self.clear_placeholder)
        self.text.bind("<FocusOut>", self.add_placeholder)
        self.text.pack()
        self.file_name = None

        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="New Window", command=self.create_new_window)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_command(label="Exit", command=self.on_closing)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def new_file(self):
        if self.changes_made():
            result = self.confirm_save()
            if result == 'yes':
                self.save_file()
            elif result == 'cancel':
                return
        self.file_name = None
        self.text.delete('1.0', 'end')
        self.text.edit_modified(False)
        
    def clear_placeholder(self, evt):
        if self.text.get('1.0', 'end') == 'Enter text here...\n':
            self.text.delete('1.0', 'end')
            self.text.config(fg='black')
            
    def add_placeholder(self, evt):
        if self.text.get('1.0', 'end') == 'Enter text here...\n':
            self.text.insert('1.0', 'end')
            self.text.config(fg='gray')

    def open_file(self):
        if self.changes_made():
            result = self.confirm_save()
            if result == 'yes':
                self.save_file()
            elif result == 'cancel':
                return
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"),
                                                                                   ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as f:
                self.text.delete('1.0', 'end')
                self.text.insert('1.0', f.read())
            self.file_name = file_path
            self.text.edit_modified(False)

    def save_file(self):
        if not self.file_name:
            self.save_as_file()
        else:
            with open(self.file_name, 'w') as f:
                f.write(self.text.get('1.0', 'end'))
            self.text.edit_modified(False)

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"),
                                                                                     ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text.get('1.0', 'end'))
            self.file_name = file_path
            self.text.edit_modified(False)
            self.root.title(f"Notepad - {file_path}")

    def changes_made(self):
        return self.text.edit_modified()

    def confirm_save(self):
        result = tkinter.messagebox.askyesnocancel(title="Confirm", message="Do you want to save changes?")
        if result == None:
            return 'cancel'
        return 'yes' if result else 'no'
    
    def create_new_window(self):
        Notepad()

    def on_closing(self):
        if self.changes_made():
            result = self.confirm_save()
            if result == 'yes':
                self.save_file()
            elif result == 'cancel':
                return
        self.root.destroy()

if __name__ == '__main__':
    Notepad()