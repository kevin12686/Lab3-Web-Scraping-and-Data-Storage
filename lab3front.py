import tkinter as tk
import sqlite3
import os


class MainWindows(tk.Frame):
    def __init__(self, master=None):
        try:
            super().__init__(master)
            self.master = master
            for i in range(3):
                tk.Grid.rowconfigure(master, i, weight=1)
            for i in range(2):
                tk.Grid.columnconfigure(master, i, weight=1)
            assert os.path.exists('data.db')
            self.conn = sqlite3.connect('data.db')
            self.init_window()
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))
            self.master.destroy()

    def init_window(self):
        self.master.title('Colleges')
        title_lab = tk.Label(self.master, text='Two-Year College Ranking', font=('Calibri', 20))
        title_lab.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        salary_btn = tk.Button(self.master, text='By Salary Potential', font=('Calibri', 14))
        salary_btn.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        salary_btn.bind('<Button-1>', lambda e: self.open_choices('NULL'))
        early_btn = tk.Button(self.master, text='By Early Career Pay', font=('Calibri', 14))
        early_btn.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        early_btn.bind('<Button-1>', lambda e: self.open_choices('starting_salary'))
        mid_btn = tk.Button(self.master, text='By Mid Career Pay', font=('Calibri', 14))
        mid_btn.grid(row=2, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        mid_btn.bind('<Button-1>', lambda e: self.open_choices('mid_career_salary'))
        stem_btn = tk.Button(self.master, text='By STEM Percentage', font=('Calibri', 14))
        stem_btn.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        stem_btn.bind('<Button-1>', lambda e: self.open_choices('STEM_degrees'))

    def open_choices(self, order_by):
        try:
            ChoicesWindows(order_by, self.conn.cursor(), self.master)
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def close_db_and_quit(self):
        self.conn.close()
        self.master.destroy()


class ChoicesWindows(tk.Toplevel):
    def __init__(self, order_by, cur, master=None):
        try:
            super().__init__(master)
            self.title('Colleges')
            self.grab_set()
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            title_lab = tk.Label(self, text='Choose type of colleges:', font=('Calibri', 14))
            title_lab.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NW)
            v = tk.StringVar(self, '')
            r = 1
            for _type in [d[0] for d in cur.execute('SELECT DISTINCT sector FROM colleges;').fetchall()] + ['Both']:
                tk.Radiobutton(self, text=_type, variable=v, value=_type, font=('Calibri', 14)).grid(row=r, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NW)
                tk.Grid.rowconfigure(self, r, weight=1)
                r += 1
            ok_btn = tk.Button(self, text='OK', font=('Calibri', 14))
            ok_btn.grid(row=r, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NW)
            ok_btn.bind('<Button-1>', lambda e: self.query(order_by, v.get(), cur))
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))
            self.destroy()

    def query(self, order_by, _type, cur):
        try:
            if _type:
                if _type == 'Both':
                    _type = '*'
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))


'''
class DisplayWindows(tk.Toplevel):
    def __init__(self, result, master=None):
        try:
            super().__init__(master)
            self.title('Dialog')
            self.grab_set()
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            lb = tk.Listbox(self, font=('Calibri', 14), selectmode=tk.MULTIPLE)
            for i in range(countries_list.size):
                lb.insert(i, countries_list[i])
            lb.grid(row=0, column=0, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            sc = tk.Scrollbar(self, orient='vertical')
            sc.grid(row=0, column=1, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            sc.config(command=lb.yview)
            lb.config(yscrollcommand=sc.set)
            cf_btn = tk.Button(self, text='Confirm', font=('Calibri', 14))
            cf_btn.grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            cf_btn.bind('<Button-1>', lambda event: self.fn_countries(list(lb.curselection()), figure_fn))
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))
            self.destroy()
'''

if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindows(master=root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_and_quit)
    app.mainloop()
