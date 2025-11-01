import tkinter as tk
import csv
from tkinter import filedialog, messagebox
from core.memory_simulator import MemorySimulator
from core.page_replacement import ReplacementPolicy
from core.analytics import PerformanceLogger
from gui.interface import MemorySimulatorGUI

class Controller:
    def __init__(self, root):
        self.gui = MemorySimulatorGUI(root)
        self.sim = None
        self.logger = None
        self.original_access_list = []

        self.gui.load_callback = self.load_file
        self.gui.start_callback = self.step
        self.gui.step_callback = self.step
        self.gui.pause_callback = self.pause_simulation
        self.gui.compare_callback = self.compare
        self.gui.reset_callback = self.reset

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return

        access_list = []
        try:
            with open(path) as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    val = int(row[2], 16) if 'x' in row[2] else int(row[2])
                    access_list.append(val)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid file format: {e}")
            return

        self.original_access_list = access_list.copy()
        self.reset()

        algo_name = self.gui.algo_var.get()
        policy = getattr(ReplacementPolicy, algo_name)

        self.sim = MemorySimulator(policy=policy)
        self.sim.load_access_file(access_list)
        self.logger = PerformanceLogger()

        self.gui.update_page_table(self.sim.page_table)
        self.gui.update_memory_blocks(self.sim.frames)
        self.gui.log_table.delete(*self.gui.log_table.get_children())

        messagebox.showinfo("File Loaded", f"Loaded {len(access_list)} memory accesses.")

    def step(self):
        if not self.sim:
            messagebox.showerror("Error", "Please load an input file first.")
            return

        result = self.sim.step()
        if result:
            step_num = len(self.logger.faults) + 1
            self.logger.log(result["faults"])
            self.gui.update_page_table(result["table"])
            self.gui.update_memory_blocks(result["frames"])
            result_type = "Hit" if result["hit"] else "Page Fault"
            self.gui.log_step(step_num, result["page"], result["frame"], result_type)
        else:
            messagebox.showinfo("Simulation Complete", f"Total Page Faults: {self.logger.faults[-1]}")
            self.logger.plot()
            self.logger.export_csv()
            self.logger.export_pdf()

    def reset(self):
        self.sim = None
        self.logger = None
        self.gui.canvas.delete("all")
        self.gui.update_page_table([[i, -1, 0] for i in range(8)])
        self.gui.update_memory_blocks([-1] * 4)
        self.gui.log_table.delete(*self.gui.log_table.get_children())
        messagebox.showinfo("Reset", "Simulation reset successfully.")

    def compare(self):
        if not self.original_access_list:
            messagebox.showerror("Error", "Please load input file first.")
            return

        import matplotlib.pyplot as plt
        algorithms = ["FIFO", "LRU", "Optimal"]
        total_faults = {}

        for alg in algorithms:
            sim = MemorySimulator(policy=getattr(ReplacementPolicy, alg))
            sim.load_access_file(self.original_access_list.copy())
            faults = 0
            while True:
                res = sim.step()
                if not res:
                    break
                faults = res["faults"]
            total_faults[alg] = faults

        best = min(total_faults, key=total_faults.get)
        plt.figure(figsize=(8, 5))
        bars = plt.bar(total_faults.keys(), total_faults.values(), color=['#3498db', '#2ecc71', '#e74c3c'])
        for bar, alg in zip(bars, total_faults.keys()):
            if alg == best:
                bar.set_color('#f39c12')
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     str(total_faults[alg]), ha='center', va='bottom', fontsize=10)
        plt.title("Page Faults Comparison — Best: " + best)
        plt.xlabel("Algorithm")
        plt.ylabel("Total Page Faults")
        plt.tight_layout()
        plt.show()

    def pause_simulation(self):
        messagebox.showinfo("Paused", "Pause functionality is reserved for future threading integration.")

if __name__ == "__main__":
    root = tk.Tk()
    Controller(root)
    root.mainloop()