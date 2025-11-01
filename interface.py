import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MemorySimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("VirtuMemSim")
        self.master.geometry("1100x700")
        self.create_widgets()

        self.load_callback = None
        self.start_callback = None
        self.step_callback = None
        self.pause_callback = None
        self.compare_callback = None
        self.reset_callback = None

    def create_widgets(self):
        control = tk.Frame(self.master, bg="#eee", height=60)
        control.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(control, text="▶ Start", width=12, command=self.on_start).pack(side=tk.LEFT, padx=5)
        tk.Button(control, text="⏩ Step", width=12, command=self.on_step).pack(side=tk.LEFT, padx=5)
        tk.Button(control, text="⏸ Pause", width=12, command=self.on_pause).pack(side=tk.LEFT, padx=5)
        tk.Button(control, text="📂 Load File", width=18, command=self.on_load).pack(side=tk.LEFT, padx=5)
        tk.Button(control, text="🔄 Reset", width=12, command=self.on_reset).pack(side=tk.LEFT, padx=5)

        self.algo_var = tk.StringVar()
        cb = ttk.Combobox(control, textvariable=self.algo_var, state='readonly', width=15)
        cb['values'] = ("FIFO", "LRU", "Optimal")
        cb.current(0)
        cb.pack(side=tk.LEFT, padx=5)

        tk.Button(control, text="📊 Compare Algorithms", width=20, command=self.on_compare).pack(side=tk.RIGHT, padx=5)

        tablef = tk.LabelFrame(self.master, text="Page Table")
        tablef.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.page_table = ttk.Treeview(tablef, columns=("Page", "Frame", "Valid"), show='headings', height=20)
        for c, w in zip(("Page", "Frame", "Valid"), (80, 80, 80)):
            self.page_table.heading(c, text=c)
            self.page_table.column(c, width=w)
        self.page_table.pack()

        memf = tk.LabelFrame(self.master, text="Physical Memory")
        memf.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(memf, bg="#cdf0ea")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        logf = tk.LabelFrame(self.master, text="Step Log")
        logf.pack(fill=tk.X, padx=10, pady=5)
        self.log_table = ttk.Treeview(logf, columns=("Step", "Page", "Frame", "Result"), show='headings', height=6)
        for c in ("Step", "Page", "Frame", "Result"):
            self.log_table.heading(c, text=c)
            self.log_table.column(c, width=100)
        self.log_table.pack()

    def on_start(self):
        if self.start_callback:
            self.start_callback()

    def on_step(self):
        if self.step_callback:
            self.step_callback()

    def on_pause(self):
        if self.pause_callback:
            self.pause_callback()

    def on_load(self):
        if self.load_callback:
            self.load_callback()

    def on_compare(self):
        if self.compare_callback:
            self.compare_callback()

    def on_reset(self):
        if self.reset_callback:
            self.reset_callback()

    def update_page_table(self, data):
        self.page_table.delete(*self.page_table.get_children())
        for row in data:
            self.page_table.insert('', 'end', values=row)

    def update_memory_blocks(self, frames):
        self.canvas.delete("all")
        h = 40
        w = 200
        m = 10
        for i, f in enumerate(frames):
            y = i * (h + m)
            self.canvas.create_rectangle(10, y, 10 + w, y + h, fill="#74b9ff")
            self.canvas.create_text(110, y + 20, text=f"Frame {i}: {f}", font=("Arial", 12))

    def log_step(self, step, page, frame, result):
        self.log_table.insert('', 'end', values=(step, page, frame, result))
