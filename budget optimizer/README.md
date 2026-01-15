# Budget Optimizer - Categories & Expenses

A Python GUI application for tracking budget categories and their expenses.

## Features

- **Budget Tracking Table**: Track expenses by category with amount, date, and description
- **Category Dropdown**: Pre-filled with common budget categories (Food, Transportation, Housing, etc.)
- **Expense Validation**: Validates that expense amounts are valid numbers
- **Total Calculator**: Automatically calculates and displays total expenses
- **Currency Formatting**: Expenses are displayed in currency format ($X,XXX.XX)
- **Double-click to Edit**: Double-click any row to edit it
- **Data Persistence**: Save and load budget data as JSON files
- **User-friendly Interface**: Clean and intuitive design

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Usage

Run the program:
```bash
python table_input_gui.py
```

### Operations

1. **Add Expense**: Click "Add Row" button to add a new expense entry
   - Select or type a category
   - Enter the expense amount (validated as a number)
   - Date defaults to today (YYYY-MM-DD format)
   - Add an optional description
2. **Edit Expense**: Select a row and click "Edit Row", or double-click the row
3. **Delete Expense**: Select a row and click "Delete Row"
4. **Clear All**: Remove all expenses from the table
5. **Save**: Save the current budget data to a JSON file
6. **Load**: Load budget data from a previously saved JSON file

## Table Columns

The table tracks the following information:
- **Category**: Budget category (dropdown with common options)
- **Expense Amount**: The amount spent (formatted as currency)
- **Date**: Date of the expense (defaults to today)
- **Description**: Optional description of the expense

## Common Categories

The application includes these pre-defined categories:
- Food
- Transportation
- Housing
- Utilities
- Entertainment
- Healthcare
- Shopping
- Education
- Insurance
- Other

You can also type in your own custom categories.

