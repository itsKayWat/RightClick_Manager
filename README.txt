# RightClick Manager

![Dark Themed Screenshot](screenshot.png)

## Table of Contents
- [Introduction](#introduction)
- [Purpose](#purpose)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Example Use Case](#example-use-case)
- [Contributing](#contributing)
- [License](#license)

## Introduction

RightClick Manager is a Python-based graphical user interface (GUI) tool designed to help Windows users manage their context menu items effortlessly. Whether you want to add new functionalities or clean up unused commands, RightClick Manager provides an intuitive interface to customize your right-click experience.

## Purpose

The tool was created to simplify the process of managing Windows context menu items. Manually editing the Windows Registry can be daunting and risky for many users. RightClick Manager offers a safe and user-friendly alternative to customize context menus without delving into complex system settings.

## Features

- **Add Custom Commands:** Easily add new context menu items with custom commands.
- **Remove Existing Items:** Remove unwanted or unused context menu entries.
- **Manage Categories:** Organize commands into categories for better management.
- **Dark Theme:** Enjoy a sleek dark mode interface that reduces eye strain.
- **Script Verification:** Ensures necessary scripts are present before adding commands.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/RightClick-Manager.git
   ```
2. **Navigate to the Directory:**
   ```bash
   cd RightClick-Manager
   ```
3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application:**
   ```bash
   python context_menu_manager.py
   ```
2. **Manage Menu Items:**
   - Navigate to the "Manage Menu Items" tab to view, remove, or refresh context menu entries.
3. **Add New Items:**
   - Go to the "Add New Item" tab.
   - Select a category from the dropdown.
   - Choose a preset command and add it to the context menu.

## Requirements

- **Python 3.x**
  - [Download Python](https://www.python.org/downloads/)
- **Required Python Packages:**
  ```bash
  pip install tkinter
  pip install pillow
  pip install winreg
  ```
  
## Example Use Case

**Customer Situation:**

Sarah frequently works with large directories and needs to copy file paths or open command prompts directly from the context menu. Instead of manually performing these actions, she uses RightClick Manager to add "Copy Path" and "Open Command Here" options. This customization streamlines her workflow, saving time and enhancing productivity.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).