# AutoBookz v1.0

Autobooks is a Python-based tool designed to automate tasks within Zybooks, mainly solving the boring participation problems within Zybooks cources. This tool interacts with the Zybooks API to streamline your study workflow and complete these automatically.

## Features
- Automatically solves participation & challenge activities.
- Logs errors and skips unsupported problem types.
- Works on Windows, macOS, and Linux.
## Prerequisites
- Python 3.7 or later
- pip package installer
- Internet connection
## Installation

    1. Clone the Repository
    Open your terminal and run the following command to clone the repository:

```bash
git clone https://github.com/BryceMcLeod24/autobooks.git
cd autobooks
```

    2. Install Dependencies
    After navigating to the project directory, install the required Python packages:

```bash
pip install -r requirements.txt
```

    3. Set Up Environment Variables (Optional)
    If you want to set up environment variables for authentication or other configuration, create a '.env' file in the project root:

```bash
touch .env
```

Add the following lines to your '.env' file:

```bash
EMAIL=your-email@example.com
PASSWORD=your-password
```
Note: It's recommended to keep your credentials secure and not include them in the .env file if possible. The program will prompt for credentials at runtime if not provided.

## Running the Program
You can run the `autobooks` program directly from the terminal. Here's how to do it on different platforms:

### Windows

1. **Open Command Prompt:**
   - Press `Win + R`, type `cmd`, and hit Enter.

2. **Navigate to the Project Directory:**

   ```cmd
   cd path\to\autobooks
   
3. **Run the Program**
    ```cmd
    python main.py

### macOS

1.**Open Terminal:**
- Press Cmd + Space, type Terminal, and hit Enter.

2.**Navigate to the Project Directory:**
```bash
cd /path/to/autobooks
```

3.**Run the Program:**
```bash
python3 main.py
```

### Linux
1. **Open Terminal:**
    - Press Ctrl + Alt + T to open the terminal.

2. **Navigate to the Project Directory:**
```bash
cd /path/to/autobooks
```

3. **Run the Program:**
```bash
python3 main.py
```

## Logging in and Running
When you run the program, you will be prompted to enter your Zybooks login credentials (email and password). The program will then start processing the books, chapters, and problems.

Input email: your-email@example.com
Input password: ********

The program will output logs to the terminal, showing progress and any errors encountered.  
