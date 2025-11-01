import threading, time
class SimulatorThread(threading.Thread):
    def __init__(self,sim,ctrl,delay=1):
        super().__init__(); self.sim, self.ctrl = sim, ctrl; self.delay=delay; self.running=True
    def run(self):
        while self.running:
            r=self.sim.step()
            if not r: break
            self.ctrl.after_step(r)
            time.sleep(self.delay)
    def stop(self): self.running=False
