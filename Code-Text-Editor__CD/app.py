import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
import ast

# Implement lexical analyzer
def lexical_analyzer(text):
    print(text)
    lexer = get_lexer_by_name("python", stripall=True)
    # The above line means that we are using the python lexer. The stripall=True means that we are removing all the whitespaces.
    tokens = lexer.get_tokens(text)
    # The above line means that we are getting the tokens from the lexer.
    
    # create a table
    table = ttk.Treeview(root, height=50)
    table['columns'] = ('Token', 'Value')
    table.column('#0', width=0, stretch=tk.NO)
    table.column('Token', anchor=tk.W, width=200)
    table.column('Value', anchor=tk.CENTER, width=250)
    table.heading('#0', text='', anchor=tk.W)
    table.heading('Token', text='Token', anchor=tk.W)
    table.heading('Value', text='Value', anchor=tk.CENTER)
    table.pack()

    # add data
    i=0
    for token in tokens:
        print(str(token[0]))
        table.insert(parent='', index=i, iid=i, text='', values=(str(token[0]), str(token[1])))
        i+=1

# Implement syntax analyser
def syntax_check(text):
    print(text)
    try:
        # Parse the code into an abstract syntax tree
        ast.parse(text)
        # If parsing succeeds, return None (no errors)
        return None
    except SyntaxError as e:
        # If parsing fails, return the error message and location
        return str(e), e.lineno, e.offset

# Render the result of the syntax check in the same window
def render_syntax_check_result(result):
    if result:
        messagebox.showerror("Error", result[0])
    else:
        messagebox.showinfo("Success", "No syntax errors found.")

# summarize the code with AI
def summarize_code():
    # open the file dialog
    file = filedialog.askopenfilename(initialdir="/", title="Select a file", filetypes=(("Python files", "*.py"), ("All files", "*.*")))
    # read the file
    with open(file, "r") as f:
        code = f.read()
    # summarize the code
    summary = summarize(code)
    # display the summary
    messagebox.showinfo("Summary", summary)

root = tk.Tk()
root.title("Lexical Analyzer")

# create a menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create a text area
textarea = tk.Text(root)
textarea.pack(fill=tk.BOTH, expand=True)

# create a button to implement the lexical analyzer
b1 = tk.Button(root, text="Get tokens", command=lambda: lexical_analyzer(textarea.get("1.0", tk.END)))
# set padding for the button
b1.pack(pady=30, padx=30)
b1.pack(side=tk.BOTTOM)

# create a button to implement the syntax analyzer
b2 = tk.Button(root, text="Check for Errors", command=lambda: render_syntax_check_result(syntax_check(textarea.get("1.0", tk.END))))
# set padding for the button
b2.pack(pady=30, padx=30)
b2.pack(side=tk.BOTTOM)

# configure the window
root.config(menu=menubar)

# set the window size to full screen
root.state("zoomed")

root.mainloop()
