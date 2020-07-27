import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


import tkinter as tk
from tkinter import filedialog, Text

root = tk.Tk()


root.mainloop()