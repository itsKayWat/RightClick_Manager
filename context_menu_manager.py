import winreg
import os
import sys
import ctypes
from tkinter import *
from tkinter import ttk, messagebox

class ContextMenuManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Context Menu Manager")
        self.root.geometry("800x600")
        
        # Configure dark theme
        self.root.configure(bg='#1e1e1e')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure(".", 
            background='#1e1e1e',
            foreground='white',
            fieldbackground='#333333')
        
        self.style.configure("Treeview",
            background='#333333',
            foreground='white',
            fieldbackground='#333333')
        
        self.style.map('Treeview',
            background=[('selected', '#007acc')])

        # Predefined menu items with categories
        self.preset_commands = {
            "File Management": {
                "Advanced Copy": {
                    "command": f"python \"{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts', 'adv_copy.py')}\" \"%1\"",
                    "extensions": ["*"]
                },
                "Copy Path": {
                    "command": "cmd /c echo %1|clip",
                    "extensions": ["*"]
                },
                "Open Command Here": {
                    "command": "cmd.exe /k cd /d \"%1\"",
                    "extensions": ["Directory"]
                }
            }
        }

        self.verify_scripts()
        self.create_gui()
        self.load_menu_items()

    def verify_scripts(self):
        """Verify that required script files exist"""
        scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
        
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)
            
        # Verify each script exists
        for category in self.preset_commands.values():
            for command_name, info in category.items():
                if 'scripts\\' in info['command']:
                    script_name = info['command'].split('scripts\\')[1].split('"')[0]
                    script_path = os.path.join(scripts_dir, script_name)
                    if not os.path.exists(script_path):
                        messagebox.showwarning("Missing Script", 
                            f"Script not found: {script_name}\n"
                            "Please ensure all required scripts are in the 'scripts' folder.")

    def create_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # Create tabs
        self.manage_tab = ttk.Frame(self.notebook)
        self.add_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.manage_tab, text='Manage Menu Items')
        self.notebook.add(self.add_tab, text='Add New Item')

        self.create_manage_tab()
        self.create_add_tab()

    def create_manage_tab(self):
        # Create treeview for existing items
        columns = ('Name', 'Command', 'Type')
        self.tree = ttk.Treeview(self.manage_tab, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.manage_tab)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text='Remove Selected', 
                  command=self.remove_menu_item).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='Refresh', 
                  command=self.load_menu_items).pack(side='left', padx=5)

    def create_add_tab(self):
        # Category selection
        ttk.Label(self.add_tab, text="Category:").pack(padx=5, pady=5)
        self.category_var = StringVar()
        category_combo = ttk.Combobox(self.add_tab, 
                                    textvariable=self.category_var,
                                    values=list(self.preset_commands.keys()))
        category_combo.pack(padx=5, pady=5)
        category_combo.bind('<<ComboboxSelected>>', self.update_presets)
        
        # Preset commands
        ttk.Label(self.add_tab, text="Available Commands:").pack(padx=5, pady=5)
        self.preset_listbox = Listbox(self.add_tab, bg='#333333', fg='white')
        self.preset_listbox.pack(padx=5, pady=5, fill='x')
        
        # Add preset button
        ttk.Button(self.add_tab, text='Add Selected Command', 
                  command=self.add_preset).pack(padx=5, pady=5)

    def update_presets(self, event=None):
        try:
            self.preset_listbox.delete(0, END)
            category = self.category_var.get()
            if category in self.preset_commands:
                for command in self.preset_commands[category].keys():
                    self.preset_listbox.insert(END, command)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update presets: {str(e)}")

    def add_preset(self):
        try:
            selection = self.preset_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a command to add")
                return
                
            category = self.category_var.get()
            command_name = self.preset_listbox.get(selection[0])
            command_info = self.preset_commands[category][command_name]
            
            self.add_menu_item(command_name, command_info['command'], command_info['extensions'])
            messagebox.showinfo("Success", f"Added {command_name} to context menu")
            self.load_menu_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add command: {str(e)}")

    def add_menu_item(self, name, command, extensions):
        try:
            for ext in extensions:
                if ext == "Directory":
                    key_path = r"Directory\shell\\" + name
                else:
                    key_path = f"Software\\Classes\\{ext}\\shell\\{name}"
                
                key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key_path)
                command_key = winreg.CreateKeyEx(key, "command")
                winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(key)
        except Exception as e:
            raise Exception(f"Failed to add menu item: {str(e)}")

    def remove_menu_item(self):
        try:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an item to remove")
                return
                
            item = self.tree.item(selected[0])
            name = item['values'][0]
            type_key = item['values'][2]
            
            if type_key == "Directory":
                key_path = f"Directory\\shell\\{name}"
            else:
                key_path = f"Software\\Classes\\{type_key}\\shell\\{name}"
            
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
            
            messagebox.showinfo("Success", f"Removed {name} from context menu")
            self.load_menu_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove item: {str(e)}")

    def load_menu_items(self):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Load items from registry
            self.load_type_items("*")
            self.load_type_items("Directory")
            
            # Load custom file type items
            for category in self.preset_commands.values():
                for command_info in category.values():
                    for ext in command_info['extensions']:
                        if ext not in ["*", "Directory"]:
                            self.load_type_items(ext)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load menu items: {str(e)}")

    def load_type_items(self, type_key):
        try:
            if type_key == "Directory":
                base_key = winreg.HKEY_CURRENT_USER
                key_path = "Directory\\shell"
            else:
                base_key = winreg.HKEY_CURRENT_USER
                key_path = f"Software\\Classes\\{type_key}\\shell"
            
            shell_key = winreg.OpenKey(base_key, key_path, 0, winreg.KEY_READ)
            
            index = 0
            while True:
                try:
                    name = winreg.EnumKey(shell_key, index)
                    command_key = winreg.OpenKey(shell_key, f"{name}\\command", 0, winreg.KEY_READ)
                    command = winreg.QueryValue(command_key, "")
                    self.tree.insert('', 'end', values=(name, command, type_key))
                    winreg.CloseKey(command_key)
                    index += 1
                except WindowsError:
                    break
            
            winreg.CloseKey(shell_key)
        except WindowsError:
            pass  # Ignore if key doesn't exist

def main():
    try:
        root = Tk()
        app = ContextMenuManager(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Critical Error", f"Application error: {str(e)}")
        
if __name__ == "__main__":
    main()