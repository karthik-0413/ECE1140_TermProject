# Polar Express Train System Project

Welcome to Polar Express! Follow these instructions to clone the repository, download the required dependencies, and navigate to the correct directory to run the project.

## Getting Started

### Prerequisites
Make sure you have Git installed on your machine. You can download it from [Git's official website](https://git-scm.com/).

### Clone the Repository
1. Open your terminal (Command Prompt, Git Bash, or any terminal of your choice).
2. Run the following command to clone the repository:

    ```bash
    git clone https://github.com/karthik-0413/ECE1140_TermProject.git
    ```

### Install Dependencies
Navigate to the cloned repository directory in the MAIN branch:

```bash
cd ECE1140_TermProject
```

Install the necessary python packages using the requirements file and by running this command in your terminal:

```bash
pip install -r requirements.txt 
```

### Run the Project
Finally, to run the project, execute the appropriate command in your terminal.

```bash
python train_control_system.py
```

### Process of Initializing Modules
There are certain chronological steps that need to be taken in order to successfully launch the project.

1. First, upload the Track Layout to the Track Model by clicking the 'Upload Layout' button in the Train Model UI.

2. Second, upload the corresponding PLC programs to the Waysides by clicking the 'Upload' button in the Wayside Controller UI.

3. Finally, upload the Track Layout to the CTC by clicking the 'Upload Layout' button in the 'Block View' tab in the CTC UI.

4. Now, to dispatch a train, in the Train View of the CTC UI, you can select the Destination Station on the CTC UI and click "Dispatch Train."

5. Then, the corresponding Train Controller UI of the train dispatched will appear and a train has been successfully dispatched!

Now, the Train System is initialized in the proper manner in order for the simulation to function as intended.