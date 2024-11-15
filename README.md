# Hand Recognition Script

This project uses MediaPipe and OpenCV for real-time hand recognition via a webcam. Follow the instructions below to set up the environment and run the script on [macOS](#macos-installation) or [Windows](#windows-installation).

---

## macOS Installation

### Prerequisites
- Python (preferably installed via Miniconda or Anaconda)
- Rosetta (for x86 compatibility on M1/M2 Macs)

### Introduction to Rosetta
Rosetta is an emulation layer provided by Apple to run x86 applications on ARM-based Macs (M1/M2). Some dependencies for this script require an x86 environment, which is why Rosetta is necessary.

### Steps to Install and Run:

1. **Enable Terminal for Rosetta:**
   - Right-click on the Terminal app in Finder.
   - Select **"Get Info"**.
   - Check the box labeled **"Open using Rosetta"**.

2. **Create the Environment:**
   Open a terminal (running under Rosetta) and run the following commands:

   ```bash
   CONDA_SUBDIR=osx-64 conda create --name mediapipe_x86 python=3.8
   conda activate mediapipe_x86 
   ```

3.	**Install Dependencies:**
   Use pip to install the required Python packages:
   ```bash
   pip install -r requirements.txt 
   ```
4.	**Run the Script:**
   Ensure the hand_recognition.py file is in the same directory. Then run:
   ```bash
   python hand_recognition.py
   ```

---

## Windows Installation

### Prerequisites
- Python (preferably installed via Miniconda or Anaconda)
- A webcam (internal or external)

### Steps to Install and Run:

1. **Create the Environment:**
   Open Command Prompt or PowerShell and run:
   ```bash
   conda create --name mediapipe_env python=3.8
   conda activate mediapipe_env
   ```

2. **Install Dependencies:**
   Use pip to install the required Python packages:
   ```bash
   pip install -r requirements.txt 
   ```
   
3.	**Run the Script:**
   Ensure the hand_recognition.py file is in the same directory. Then run:
   ```bash
   python hand_recognition.py
   ```
---

## Notes

- **Stopping the Script**: Press `q` in the script window to quit.
- **Webcam Setup**: Ensure your webcam is connected and accessible by your system.
- **Rosetta Tip**: Always run the terminal using Rosetta for macOS M1/M2 users when working with x86 environments.

If you encounter issues, feel free to open an issue in the repository.

This version includes explicit commands and steps for both macOS and Windows, ensuring users can follow along easily.
