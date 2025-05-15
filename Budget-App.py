import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

from bokeh.layouts import column

from models import Expense, Income
from storage import load_data, save_data, load_categories, save_categories

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')

DATA_FILES = {
    'expenses': 'expenses.json',
    'incomes': 'incomes.json',
    'exp_cats': 'expense_categories.json',
    'inc_cats': 'income_categories.json'
}

class BudgetApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Budget Manager')
        self.geometry('1000x600')
        self.current_month = datetime.now().replace(day=1)
        self.expenses = load_data(DATA_FILES['expenses'], Expense)
        self.incomes = load_data(DATA_FILES['incomes'], Income)
        self.exp_cats = load_categories(['exp_cats'])
        self.inc_cats = load_categories(['inc_cats'])
        self.selected_exp = None
        self.selected_inc = None
        self.month_label = None
        self.tabview = None
        self.exp_frame = None
        self.exp_list = None
        self.exp_controls = None
        self.inc_frame = None
        self.inc_list = None
        self.inc_controls = None
        self.create_widgets()
        self.refresh_lists()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky='nsew')
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
        header.grid_columnconfigure(3, weight=0)

        self.month_label = ctk.CTkLabel(header, text = self.current_month.strftime('%B %Y'), font=('Helvetica', 18))
        self.month_label.grid(row=0, column=0, sticky='ew')

        ctk.CTkButton(header, text='←', width=40, command=self.prev_month).grid(row=0, column=1, sticky='ew')
        ctk.CTkButton(header, text='→', width=40, command =self.next_month).grid(row=0, column=2, sticky='ew')

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky='nsew')
        self.tabview.add('Expenses')
        self.tabview.add('Incomes')

        # Expenses Tab
        self.exp_frame = ctk.CTkFrame(self.tabview.tab('Expenses'))
        self.exp_frame.grid_columnconfigure(0, weight=1)
        self.exp_frame.grid_columnconfigure(1, weight=0)
        self.exp_frame.grid_rowconfigure(0, weight=1)

        self.exp_list = ctk.CTkScrollableFrame(self.exp_frame)
        self.exp_list.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.exp_controls = ctk.CTkFrame(self.exp_frame)
        self.exp_controls.grid(row=0, column=1, sticky='ns', padx=10, pady=10)
        self.show_expense_controls()

        # Incomes Tab
        self.inc_frame = ctk.CTkFrame(self.tabview.tab('Incomes'))
        self.inc_frame.grid_columnconfigure(0, weight=1)
        self.inc_frame.grid_columnconfigure(1, weight=0)
        self.inc_frame.grid_rowconfigure(0, weight=1)

        self.inc_list = ctk.CTkScrollableFrame(self.inc_frame)
        self.inc_list.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.inc_controls = ctk.CTkFrame(self.inc_frame)
        self.inc_controls.grid(row=0, column=1, sticky = 'ns', padx=10, pady=10)
        self.show_income_controls()

    def prev_month(self):
        self.current_month = (self.current_month - timedelta(days=1)).replace(day=1)
        self.update_month_view()

    def next_month(self):
        year = self.current_month.year + (self.current_month.month // 12)
        month = self.current_month.month % 12 + 1
        self.current_month = datetime(year,month, 1)
        self.update_month_view()

    def update_month_view(self):
        self.month_label.configure(text=self.current_month.strftime('%B %Y'))
        self.refresh_lists()

    def show_expense_controls(self):
        for widget in self.exp_controls.winfo_children():
            widget.destroy()
        ctk.CTkButton(self.exp_controls, text='Add expense', command=self.show_expense_form).grid(row=0, column=0, sticky='ew', pady=5)
        ctk.CTkButton(self.exp_controls, text='Delete selected expense', command=self.remove_selected_expense).grid(row=1, column=0, sticky='ew', pady=5)
        ctk.CTkButton(self.exp_controls, text='Manage categories', command=self.manage_expense_categories).grid(row=2, column=0, sticky='ew', pady=5)

    def show_income_controls(self):
        for widget in self.inc_controls.winfo_children():
            widget.destroy()
        ctk.CTkButton(self.exp_controls, text='Add expense', command=self.show_income_form).grid(row=0, column=0,
                                                                                                  sticky='ew', pady=5)
        ctk.CTkButton(self.exp_controls, text='Delete selected expense', command=self.remove_selected_income).grid(row=1, column=0, sticky='ew', pady=5)
        ctk.CTkButton(self.exp_controls, text='Manage categories', command=self.manage_income_categories).grid(row=2, column=0, sticky='ew', pady=5)

    def show_expense_form(self):
        for widget in self.exp_controls.winfo_children():
            widget.destroy()
        name = ctk.CTkEntry(self.exp_controls, placeholder_text='Name')
        name.grid(row=0, column=0, sticky='ew', pady=2)
        category = ctk.CTkOptionMenu(self.exp_controls, values=self.exp_cats)
        category.grid(row=1, column=0, sticky='ew', pady=2)
        amount = ctk.CTkEntry(self.exp_controls, placeholder_text='Amount')
        amount.grid(row=2, column=0, sticky='ew', pady=2)
        essentiality = ctk.CTkOptionMenu(self.exp_controls, values=['Essential', 'Important', 'Non-essential'])
        essentiality.grid(row=3, column=0, sticky='ew', pady=2)
        ctk.CTkButton(self.exp_controls, text='Save', command=lambda: self.save_expense(name.get(), category.get(), amount.get(), essentiality.get())).grid(row=4, column=0, sticky='ew', pady=2)
        ctk.CTkButton(self.exp_controls, text='Cancel', command=self.show_expense_controls).grid(row=5, column=0, sticky='ew', pady=2)

    def show_income_form(self):
        for widget in self.inc_controls.winfo_children():
            widget.destroy()
        name = ctk.CTkEntry(self.inc_controls, placeholder_text='Name')
        name.grid(row=0, column=0, sticky='ew', pady=2)
        category = ctk.CTkOptionMenu(self.inc_controls, values=self.inc_cats)
        category.grid(row=1, column=0, sticky='ew', pady=2)
        amount = ctk.CTkEntry(self.inc_controls, placeholder_text='Amount')
        amount.grid(row=2, column=0, sticky='ew', pady=2)
        essentiality = ctk.CTkOptionMenu(self.inc_controls, values=['Essential', 'Important', 'Non-essential'])
        essentiality.grid(row=3, column=0, sticky='ew', pady=2)
        ctk.CTkButton(self.exp_controls, text='Save',command=lambda: self.save_expense(name.get(), category.get(), amount.get(),essentiality.get())).grid(row=4, column=0, sticky='ew', pady=2)
        ctk.CTkButton(self.exp_controls, text='Cancel', command=self.show_expense_controls).grid(row=5, column=0, sticky='ew', pady=2)

    def manage_expense_categories(self):
        self.manage_categories_panel(self.exp_controls, self.exp_cats, DATA_FILES['exp_cats'], self.show_expense_controls)

    def manage_income_categories(self):
        self.manage_categories_panel(self.inc_controls, self.inc_cats, DATA_FILES['inc_cats'], self.show_income_controls)

    def manage_categories_panel(self, frame, cat_list, filename, back_callback):
        for widget in frame.winfo_children():
            widget.destroy()
        listbox = ctk.CTkScrollableFrame(frame)
        listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        selected = {'index': None}

        def refresh():
            for widget in listbox.winfo_children():
                widget.destroy()
            for idx, c in enumerate(cat_list):
                btn = ctk.CTkButton(listbox, text=c, anchor='w', command=lambda i=idx: selected.update({'index': i}))
                btn.pack(fill='x', pady=2)

        entry = ctk.CTkEntry(frame, placeholder_text='Category name')
        entry.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        btns = ctk.CTkFrame(frame)
        ctk.CTkButton(btns, text="Add", command=lambda: self.add_category(entry.get(), cat_list, filename, refresh)).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btns, text="Remove selected", command=lambda: self.remove_category(selected['index'], cat_list, filename, refresh)).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame, text="Back", command=back_callback).grid(row=3, column=0, pady=5)
        refresh()

    def add_category(self, new_cat, cat_list, filename, refresh_callback):
        new = new_cat.strip()
        if new and new not in cat_list:
            cat_list.append(new)
            save_categories(filename, cat_list)
            refresh_callback()
        else:
            messagebox.showerror('Error', 'Invalid category name or already exists')

    def remove_category(self, index, cat_list, filename, refresh_callback):
        if index is None:
            messagebox.showerror('Error', 'No category selected')
            return
        cat_list.pop(index)
        save_categories(filename, cat_list)
        refresh_callback()