# Dice Roller
## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)

## Introduction

The Dice Roller is a Python-based application that allows users to roll a virtual dice, with the result displayed on a connected Busy Tag device. The app provides an interactive interface for users to roll a dice and watch the result both on the app window and on the Busy Tag device.

## Project Purpose

The main goal of this project is to:
	
- Provide a simple, fun, and interactive way to simulate rolling a dice.

- Display the rolled number on a Busy Tag device.

- Handle file transfers and Busy Tag device setup automatically within the app.

## Prerequisites

Before running the Dice Roller App, ensure you have the following installed:

- Python 3.6 or higher
- `PyQt5` for the graphical user interface
- A Busy Tag device connected to your computer

## Installation
 
  To get started with this Python script, follow these steps:

1. **Clone the repository:**
   First, clone the repository from GitHub to your local machine.
   ```
   git clone https://github.com/busy-tag/dice_roller.git
2. Navigate to the cloned repository:

	```
	cd dice_roller
	```
3. Install the required dependencies:
	Use `pip` to install the necessary packages.
	
	```
	pip install PyQt5
	```

4. Ensure all necessary asset files (e.g., roll.gif, dice_1.png, dice_2.png, etc.) are in the assets folder.


## Usage
1. **Execute the script:**
You can run the script from the command line:
```
python main.py
```
         
2. **Provide Drive Letter:**

	Enter the drive letter assigned to the Busy Tag device (e.g., D) when prompted.
	
3. **Roll the dice:**
	
	Click the "ROLL" button to roll the dice. The result will be displayed on the app window and transferred to the Busy Tag device.

### Example

After running the application and providing the drive letter, the app will set up the Busy Tag device and transfer the necessary files. When you click "ROLL," you should see output similar to this:

<img src="/assets/GUI_sample.PNG" alt="You rolled: 6" width="280" height="200"/>

The corresponding dice image (e.g., dice_6.png) will be displayed on the Busy Tag device.

Sample:

<img src="/assets/dice_roll_sample.png" alt="You rolled: 6" width="300" height="370"/>

### Troubleshooting

If you encounter any issues, ensure:

All required Python packages are installed correctly (PyQt5 and others).

The assets folder contains all necessary files (e.g., roll.gif, dice_1.png, etc.).

The drive letter is correct, and the Busy Tag device is properly connected.

You have the correct permissions to copy files to the Busy Tag device.

For any additional help, please open an issue in the repository or contact the maintainer.
