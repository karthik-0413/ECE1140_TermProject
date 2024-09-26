class TrainEngineer:
    def __init__(self):
        self._kp = 0.0
        self._ki = 0.0
        
    def set_kp(self, kp):
        self._kp = kp
        print(f"Kp set to {self._kp}")
        
    def set_ki(self, ki):
        self._ki = ki
        print(f"Kp set to {self._ki}")
        
    def get_kp(self):
        return self._kp
    
    def get_ki(self):
        return self._ki
    
if __name__ == "__main__":
    engineer = TrainEngineer()
    engineer.set_kp(0.5)
    engineer.set_ki(0.1)
    print(engineer.get_kp())
    print(engineer.get_ki())