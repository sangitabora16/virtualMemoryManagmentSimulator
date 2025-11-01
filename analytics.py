import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

class PerformanceLogger:
    def __init__(self):
        self.faults = []

    def log(self, faults):
        self.faults.append(faults)

    def export_csv(self):
        with open("output/simulation_log.csv", "w") as f:
            f.write("Step,Page Faults\n")
            for i, val in enumerate(self.faults):
                f.write(f"{i+1},{val}\n")

    def export_pdf(self):
        c = canvas.Canvas("output/report.pdf")
        c.setFont("Helvetica", 14)
        c.drawString(100, 800, "Virtual Memory Simulation Report")
        c.setFont("Helvetica", 12)
        y = 770
        for i, val in enumerate(self.faults):
            c.drawString(100, y, f"Step {i+1}: {val} page faults")
            y -= 20
        c.save()

    def plot(self):
        plt.plot(range(1, len(self.faults) + 1), self.faults, marker='o', linestyle='-')
        plt.title("Page Faults Over Time")
        plt.xlabel("Step")
        plt.ylabel("Page Faults")
        plt.grid(True)
        plt.savefig("output/page_fault_graph.png")
        plt.show()
