import tkinter as tk
import sqlite3
import os
import webbrowser
from tkinter import messagebox


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
            self._type = ''
            self.init_window()
        except Exception as e:
            messagebox.showerror('Error', str(e))
            self.master.destroy()

    def init_window(self):
        self.master.title('Colleges')
        title_lab = tk.Label(self.master, text='Two-Year College Ranking', font=('Calibri', 20))
        title_lab.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        salary_btn = tk.Button(self.master, text='By Salary Potential', font=('Calibri', 14))
        salary_btn.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        salary_btn.bind('<Button-1>', lambda e: self.do_next('NULL'))
        early_btn = tk.Button(self.master, text='By Early Career Pay', font=('Calibri', 14))
        early_btn.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        early_btn.bind('<Button-1>', lambda e: self.do_next('starting_salary'))
        mid_btn = tk.Button(self.master, text='By Mid Career Pay', font=('Calibri', 14))
        mid_btn.grid(row=2, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        mid_btn.bind('<Button-1>', lambda e: self.do_next('mid_career_salary'))
        stem_btn = tk.Button(self.master, text='By STEM Percentage', font=('Calibri', 14))
        stem_btn.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        stem_btn.bind('<Button-1>', lambda e: self.do_next('STEM_degrees'))

    def set_type(self, _type):
        self._type = _type

    def do_next(self, order_by):
        try:
            if self._type:
                if order_by == 'starting_salary':
                    data = self.conn.cursor().execute('SELECT name, url, starting_salary FROM colleges WHERE sector LIKE ? ORDER BY starting_salary DESC;', (self._type,)).fetchall()
                    data = [(f'{each[0]}: ${each[2]:,}', each[1], each[0]) for each in data]
                    lable = 'College Ranking by Early Career Pay'
                elif order_by == 'mid_career_salary':
                    data = self.conn.cursor().execute('SELECT name, url, mid_career_salary FROM colleges WHERE sector LIKE ? ORDER BY mid_career_salary DESC;', (self._type,)).fetchall()
                    data = [(f'{each[0]}: ${each[2]:,}', each[1], each[0]) for each in data]
                    lable = 'College Ranking by Mid Career Pay'
                elif order_by == 'STEM_degrees':
                    data = self.conn.cursor().execute('SELECT name, url, STEM_degrees FROM colleges WHERE sector LIKE ? ORDER BY STEM_degrees DESC;', (self._type,)).fetchall()
                    data = [(f'{each[0]}: {each[2]}%', each[1], each[0]) for each in data]
                    lable = 'College Ranking by % STEM Degrees'
                else:
                    data = self.conn.cursor().execute('SELECT name, url FROM colleges WHERE sector LIKE ?;', (self._type,)).fetchall()
                    data = [(f'{each[0]}', each[1], each[0]) for each in data]
                    lable = 'College Ranking by Salary Potential'
                DisplayWindows(lable, data)
            else:
                ChoicesWindows(self.set_type, self.master)
        except ArithmeticError as e:
            messagebox.showerror('Error', str(e))

    def close_db_and_quit(self):
        self.conn.close()
        self.master.destroy()


class ChoicesWindows(tk.Toplevel):
    def __init__(self, set_type, master=None):
        try:
            super().__init__(master)
            self.title('Colleges')
            self.wait_visibility()
            self.grab_set()
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            title_lab = tk.Label(self, text='Choose type of colleges:', font=('Calibri', 14))
            title_lab.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NW)
            v = tk.StringVar(self, '')
            r = 1
            for _type in ['Private', 'Public', 'Both']:
                tk.Radiobutton(self, text=_type, variable=v, value=_type, font=('Calibri', 14)).grid(row=r, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NW)
                tk.Grid.rowconfigure(self, r, weight=1)
                r += 1
            ok_btn = tk.Button(self, text='OK', font=('Calibri', 14))
            ok_btn.grid(row=r, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NW)
            ok_btn.bind('<Button-1>', lambda e: self.lock_choice(set_type, v.get()))
        except Exception as e:
            messagebox.showerror('Error', str(e))
            self.destroy()

    def lock_choice(self, set_type, _type):
        try:
            assert _type, 'Please choose a option.'
            if _type == 'Both':
                set_type('%%')
            else:
                set_type('%s%%' % _type)
            self.destroy()
        except Exception as e:
            messagebox.showerror('Error', str(e))


class DisplayWindows(tk.Toplevel):
    def __init__(self, label, data, master=None):
        try:
            super().__init__(master)
            self.data = data
            self.title('Colleges')
            for i in range(3):
                tk.Grid.rowconfigure(self, i, weight=1)
            for i in range(1):
                tk.Grid.columnconfigure(self, i, weight=1)
            title_lab = tk.Label(self, text=label, font=('Calibri', 14))
            title_lab.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            lb = tk.Listbox(self, font=('Calibri', 14), height=10, selectmode=tk.SINGLE)
            lb.bind('<<ListboxSelect>>', lambda e: self.browse(lb.curselection()))
            for i in range(len(self.data)):
                lb.insert(i, '%d. %s' % (i + 1, self.data[i][0]))
            lb.grid(row=1, column=0, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            sc = tk.Scrollbar(self, orient='vertical')
            sc.grid(row=1, column=1, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            sc.config(command=lb.yview)
            lb.config(yscrollcommand=sc.set)
            label = tk.Label(self, text='Click on a colleges to go to the website', font=('Calibri', 14))
            label.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        except Exception as e:
            messagebox.showerror('Error', str(e))
            self.destroy()

    def browse(self, selection):
        if self.data[selection[0]][1]:
            webbrowser.open(self.data[selection[0]][1])
        else:
            messagebox.askokcancel('No data', 'No web page for %s' % self.data[selection[0]][2])


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindows(master=root)
    root.protocol("WM_DELETE_WINDOW", app.close_db_and_quit)
    app.mainloop()
