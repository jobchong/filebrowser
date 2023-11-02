import os
import tkinter as tk
from tkinter import ttk

class DirectoryBrowser(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Directory Browser")
        self.geometry("600x400")

        self.tree = ttk.Treeview(self, columns=("Path",), show='tree')
        self.tree.heading('#1', text='Directory Structure')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.populate_tree()

        self.tree.bind('<<TreeviewOpen>>', self.on_open)

    def populate_tree(self, parent_item='', directory='.'):
        entries = list(os.scandir(directory))
        entries.sort(key=lambda entry: (not entry.is_dir(), entry.name.lower()))  # Sort directories first, then files
        for entry in entries:
            abs_path = os.path.abspath(entry.path)
            oid = self.tree.insert(parent_item, 'end', text=entry.name, values=[abs_path])
            if entry.is_dir():
                self.tree.insert(oid, 'end')

    def on_open(self, event):
        item = self.tree.focus()
        directory = self.tree.item(item, 'values')[0]
        if os.path.isdir(directory):
            self.tree.delete(*self.tree.get_children(item))
            self.populate_tree(item, directory)

if __name__ == "__main__":
    app = DirectoryBrowser()
    app.mainloop()
