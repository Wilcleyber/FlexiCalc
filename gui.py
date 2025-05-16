import tkinter as tk
from tkinter import ttk, messagebox
from arithmetic import evaluate_expression, convert_percentage_expressions, square, square_root, percentage
from temperature import convert_temperature
from geometry import (
    area_rectangle, area_square, area_triangle,
    area_circle, area_trapezoid
)

dark_bg = '#2e2e2e'
dark_fg = '#ffffff'
btn_bg = '#3e3e3e'
btn_fg = '#ffffff'

def apply_dark_theme(root: tk.Tk):
    root.configure(bg=dark_bg)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TNotebook', background=dark_bg)
    style.configure('TNotebook.Tab', background=btn_bg, foreground=btn_fg)
    style.map('TNotebook.Tab', background=[('selected', '#505050')])
    style.configure('TFrame', background=dark_bg)
    style.configure('TLabel', background=dark_bg, foreground=dark_fg)
    style.configure('TButton', background=btn_bg, foreground=btn_fg)
    style.configure('TEntry', background=dark_bg, foreground=dark_fg)

def create_arithmetic_tab(notebook, display_var):
    frame = ttk.Frame(notebook)
    
    display = ttk.Label(frame, textvariable=display_var, anchor='e', font=('Arial', 24))
    display.pack(fill='x', padx=10, pady=10)
    buttons = [
        ['7','8','9','÷','×'],
        ['4','5','6','√','x²'],
        ['1','2','3','%','CE'],
        ['0','.','+','-','=']
    ]
    btn_frame = ttk.Frame(frame)
    btn_frame.pack()
    for r, row in enumerate(buttons):
        for c, char in enumerate(row):
            btn = tk.Button(btn_frame, text=char, width=5, height=2,
                            bg=btn_bg, fg=btn_fg,
                            command=lambda ch=char: on_arith_button(ch, display_var))
            btn.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
    return frame

def on_arith_button(ch, display_var):
    expr = display_var.get().strip()  
    try:
        if ch == 'CE':   
            display_var.set('')
        elif ch == '=':   
            if not expr or not any(c.isdigit() for c in expr):
                raise ValueError("Invalid expression")
    
            expr = expr.replace('×', '*').replace('÷', '/')
            result = evaluate_expression(expr)
            display_var.set(str(result))
        elif ch == 'x²':
            val = float(expr)
            display_var.set(str(square(val)))
        elif ch == '√':
            val = float(expr)
            display_var.set(str(square_root(val)))
        elif ch == '%':
            display_var.set(expr + '%')
        else:
            display_var.set(expr + ch)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_temperature_tab(notebook, display_var):
    frame = ttk.Frame(notebook)
    display = ttk.Label(frame, textvariable=display_var, anchor='e', font=('Arial', 18))
    display.pack(fill='x', padx=10, pady=10)

    content = ttk.Frame(frame)
    content.pack(pady=20)
    
    tk.Label(content, text="Value:", bg=dark_bg, fg=dark_fg).grid(row=0, column=0, sticky='nsew')
    value_entry = tk.Entry(content)
    value_entry.grid(row=0, column=1, sticky='nsew')
    
    units = ['Celsius','Fahrenheit','Kelvin']
    from_cb = ttk.Combobox(content, values=units, state='readonly')
    from_cb.current(0)
    from_cb.grid(row=1, column=0, pady=5, sticky='nsew')
    to_cb = ttk.Combobox(content, values=units, state='readonly')
    to_cb.current(1)
    to_cb.grid(row=1, column=1, pady=5, sticky='nsew')
    
    btn = tk.Button(frame, text="Convert", bg=btn_bg, fg=btn_fg,
                    command=lambda: on_convert_temp(value_entry, from_cb, to_cb, display_var))
    btn.pack(pady=10)
    return frame

def on_convert_temp(val_entry, from_cb, to_cb, display_var):
    try:
        v = float(val_entry.get())
        out = convert_temperature(v, from_cb.get(), to_cb.get())
        unit = to_cb.get()[0]  
        display_var.set(f"{out:.2f} {unit}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_geometry_tab(notebook, display_var):
    frame = ttk.Frame(notebook)
    display = ttk.Label(frame, textvariable=display_var, anchor='e', font=('Arial', 18))
    display.pack(fill='x', padx=10, pady=10)

    content = ttk.Frame(frame)
    content.pack(pady=20)
    
    shapes = ['Rectangle', 'Square', 'Triangle', 'Circle', 'Trapezoid']
    tk.Label(content, text="Shape:", bg=dark_bg, fg=dark_fg).grid(row=0, column=0, sticky='nsew')
    shape_cb = ttk.Combobox(content, values=shapes, state='readonly')
    shape_cb.current(0)
    shape_cb.grid(row=0, column=1, sticky='nsew')
    
    params_frame = ttk.Frame(content)
    params_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')

    def update_fields(event=None):
        
        for w in params_frame.winfo_children():
            w.destroy()
        s = shape_cb.get()
        fields = []
        if s == 'Rectangle': fields = [('Base',0), ('Height',1)]
        elif s == 'Square': fields = [('Side',0)]
        elif s == 'Triangle': fields = [('Base',0), ('Height',1)]
        elif s == 'Circle': fields = [('Radius',0)]
        elif s == 'Trapezoid': fields = [('Top Base',0), ('Bottom Base',1), ('Height',2)]
        for label, col in fields:
            tk.Label(params_frame, text=f"{label}:", bg=dark_bg, fg=dark_fg).grid(row=col, column=0, sticky='nsew')
            e = tk.Entry(params_frame)
            e.grid(row=col, column=1, sticky='nsew')
        params_frame.entries = params_frame.winfo_children()[1::2]

    shape_cb.bind('<<ComboboxSelected>>', update_fields)
    update_fields()

    btn = tk.Button(frame, text="Calculate Area", bg=btn_bg, fg=btn_fg,
                    command=lambda: on_calc_area(shape_cb, params_frame.entries, display_var))
    btn.pack(pady=10)
    return frame

def on_calc_area(shape_cb, entries, display_var):
    try:
        vals = [float(e.get()) for e in entries]
        s = shape_cb.get()
        if s == 'Rectangle': res = area_rectangle(*vals)
        elif s == 'Square': res = area_square(*vals)
        elif s == 'Triangle': res = area_triangle(*vals)
        elif s == 'Circle': res = area_circle(*vals)
        elif s == 'Trapezoid': res = area_trapezoid(*vals)
        else: raise ValueError("Unknown shape")
        display_var.set(f"{res:.2f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_key_press(event, display_var, notebook):
    if notebook.index(notebook.select()) != 0:
        return  

    char = event.char

    if char in '0123456789+-*/=.':
        display_var.set(display_var.get() + char)
    elif char == '\r':  
        on_arith_button('=', display_var)
    elif char == '\x08':  
        display_var.set(display_var.get()[:-1])
          

def main():
    root = tk.Tk()
    root.title("FlexiCalc")
    apply_dark_theme(root)

    notebook = ttk.Notebook(root)
    display_var = tk.StringVar()  

    tab1 = create_arithmetic_tab(notebook, display_var)
    tab2 = create_temperature_tab(notebook, display_var)
    tab3 = create_geometry_tab(notebook, display_var)

    notebook.add(tab1, text='Arithmetic')
    notebook.add(tab2, text='Temperature')
    notebook.add(tab3, text='Geometry')
    notebook.pack(expand=True, fill='both')
    notebook.bind("<<NotebookTabChanged>>", lambda e: on_tab_change(e, display_var))

    root.bind('<Key>', lambda event: on_key_press(event, display_var, notebook))

    root.mainloop()

def on_tab_change(event, display_var):
    display_var.set('')  
    
if __name__ == '__main__':
    main()
