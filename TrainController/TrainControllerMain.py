# main.py
import multiprocessing
import subprocess

def run_ui1():
    subprocess.run(["python", "TrainController/TrainControllerUI.py"])

def run_ui2():
    subprocess.run(["python", "TrainController/TrainControllerEngineer.py"])

def run_ui3():
    subprocess.run(["python", "TrainController.py"])

if __name__ == "__main__":
    # Create separate processes for each UI
    p1 = multiprocessing.Process(target=run_ui1)
    p2 = multiprocessing.Process(target=run_ui2)
    p3 = multiprocessing.Process(target=run_ui3)

    # Start all UIs simultaneously
    p1.start()
    p2.start()
    p3.start()

    # Wait for all processes to complete
    p1.join()
    p2.join()
    p3.join()
