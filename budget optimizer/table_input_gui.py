import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os


class TableInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Optimizer - Categories & Expenses")
        self.root.geometry("900x650")
        
        # Data storage
        self.data = []
        self.columns = ["Category", "Expense Amount", "Date", "Description"]
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title label
        title_label = ttk.Label(main_frame, text="Budget Categories & Expenses", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Total expenses label
        self.total_label = ttk.Label(main_frame, text="Total Expenses: $0.00", font=("Arial", 12, "bold"), foreground="darkgreen")
        self.total_label.grid(row=1, column=0, pady=(0, 10))
        
        # Create table (Treeview)
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview (table)
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings", 
                                yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configure columns
        column_widths = {"Category": 180, "Expense Amount": 150, "Date": 120, "Description": 250}
        column_anchors = {"Expense Amount": tk.E}  # Right-align amounts
        
        for col in self.columns:
            self.tree.heading(col, text=col)
            anchor = column_anchors.get(col, tk.W)
            self.tree.column(col, width=column_widths.get(col, 100), anchor=anchor)
        
        # Grid table and scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(10, 0))
        
        # Buttons
        ttk.Button(button_frame, text="Add Row", command=self.add_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Row", command=self.edit_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Row", command=self.delete_row).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load", command=self.load_data).pack(side=tk.LEFT, padx=5)
        
    def add_row(self):
        """Open dialog to add a new row"""
        dialog = InputDialog(self.root, "Add New Expense", self.columns)
        # Wait for dialog to close
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            values = dialog.result
            # Validate expense amount
            if not self.validate_expense(values[1]):
                return
            # Format expense amount
            try:
                amount = float(values[1])
                values[1] = f"${amount:,.2f}"
            except ValueError:
                pass
            item_id = self.tree.insert("", tk.END, values=values)
            self.data.append(values)
            self.update_total()
    
    def edit_row(self):
        """Edit selected row"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to edit.")
            return
        
        item = selected[0]
        current_values = list(self.tree.item(item, "values"))
        # Remove $ and formatting from expense amount for editing
        if len(current_values) > 1 and current_values[1].startswith("$"):
            current_values[1] = current_values[1].replace("$", "").replace(",", "")
        
        dialog = InputDialog(self.root, "Edit Expense", self.columns, current_values)
        # Wait for dialog to close
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            # Validate expense amount
            if not self.validate_expense(dialog.result[1]):
                return
            # Format expense amount
            try:
                amount = float(dialog.result[1])
                dialog.result[1] = f"${amount:,.2f}"
            except ValueError:
                pass
            self.tree.item(item, values=dialog.result)
            # Update data list
            index = self.tree.index(item)
            if 0 <= index < len(self.data):
                self.data[index] = dialog.result
            self.update_total()
    
    def delete_row(self):
        """Delete selected row"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected row?"):
            item = selected[0]
            index = self.tree.index(item)
            self.tree.delete(item)
            if 0 <= index < len(self.data):
                self.data.pop(index)
            self.update_total()
    
    def clear_all(self):
        """Clear all rows"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data?"):
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.data.clear()
            self.update_total()
    
    def on_double_click(self, event):
        """Handle double-click to edit"""
        self.edit_row()
    
    def validate_expense(self, amount_str):
        """Validate that expense amount is a valid number"""
        try:
            # Remove $ and commas if present
            clean_amount = amount_str.replace("$", "").replace(",", "").strip()
            amount = float(clean_amount)
            if amount < 0:
                messagebox.showerror("Invalid Amount", "Expense amount cannot be negative.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number for the expense amount.")
            return False
    
    def update_total(self):
        """Calculate and update the total expenses"""
        total = 0.0
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values and len(values) > 1:
                try:
                    # Extract numeric value from formatted string
                    amount_str = values[1].replace("$", "").replace(",", "").strip()
                    total += float(amount_str)
                except (ValueError, IndexError):
                    pass
        self.total_label.config(text=f"Total Expenses: ${total:,.2f}")
    
    def save_data(self):
        """Save data to JSON file"""
        # Collect all data from tree
        data_to_save = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            data_to_save.append(dict(zip(self.columns, values)))
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(data_to_save, f, indent=2)
                messagebox.showinfo("Success", f"Data saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_data(self):
        """Load data from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    loaded_data = json.load(f)
                
                # Clear existing data
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.data.clear()
                
                # Load new data
                for row in loaded_data:
                    values = [row.get(col, "") for col in self.columns]
                    # Format expense amount if it's a number
                    if values[1] and not values[1].startswith("$"):
                        try:
                            amount = float(values[1].replace("$", "").replace(",", ""))
                            values[1] = f"${amount:,.2f}"
                        except ValueError:
                            pass
                    self.tree.insert("", tk.END, values=values)
                    self.data.append(values)
                
                self.update_total()
                messagebox.showinfo("Success", f"Data loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")


class InputDialog:
    def __init__(self, parent, title, columns, initial_values=None):
        self.result = None
        self.columns = columns
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Common budget categories
        common_categories = ["Food", "Transportation", "Housing", "Utilities", "Entertainment", 
                           "Healthcare", "Shopping", "Education", "Insurance", "Other"]
        
        # Entry fields
        self.entries = {}
        for i, col in enumerate(columns):
            ttk.Label(main_frame, text=f"{col}:").grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if col == "Category":
                # Use Combobox for category with common options
                entry = ttk.Combobox(main_frame, width=37, values=common_categories)
                entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
                if initial_values and i < len(initial_values):
                    entry.set(str(initial_values[i]))
            elif col == "Expense Amount":
                # Entry for expense amount
                entry = ttk.Entry(main_frame, width=40)
                entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
                if initial_values and i < len(initial_values):
                    entry.insert(0, str(initial_values[i]))
                    entry.select_range(0, tk.END)
                else:
                    # Add placeholder text for new entries
                    entry.insert(0, "0.00")
                    entry.select_range(0, tk.END)
            elif col == "Date":
                # Entry for date with placeholder
                entry = ttk.Entry(main_frame, width=40)
                entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
                if initial_values and i < len(initial_values):
                    entry.insert(0, str(initial_values[i]))
                else:
                    from datetime import datetime
                    entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            else:
                # Regular entry for description
                entry = ttk.Entry(main_frame, width=40)
                entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
                if initial_values and i < len(initial_values):
                    entry.insert(0, str(initial_values[i]))
            
            self.entries[col] = entry
        
        main_frame.columnconfigure(1, weight=1)
        
        # Add hint label
        hint_label = ttk.Label(main_frame, text="Tip: Use common categories or create your own", 
                              font=("Arial", 8), foreground="gray")
        hint_label.grid(row=len(columns), column=0, columnspan=2, pady=(5, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(columns) + 1, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry
        if self.entries:
            first_entry = list(self.entries.values())[0]
            first_entry.focus()
            first_entry.bind("<Return>", lambda e: self.ok_clicked())
    
    def ok_clicked(self):
        """Collect values and close dialog"""
        self.result = [self.entries[col].get() for col in self.columns]
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Close dialog without saving"""
        self.dialog.destroy()


def main():
    root = tk.Tk()
    app = TableInputGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

