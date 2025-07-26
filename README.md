
# ☁️ ReAzure

A **Mental Health Tracker** platform designed to support emotional well-being through self-reflection, mood tracking, and community-based resources. By integrating journaling features and mood analytics, ReAzure encourages individuals to actively engage with their mental health.


### 📌 Proposal

[View Full Proposal on Google Drive](https://drive.google.com/file/d/1AcfpSmkxHPtAycWrDmN0ioSYhyqiX5Qr/view?usp=drive_link)

### 🗕️ Gantt Chart

[View Progress Plan](https://docs.google.com/spreadsheets/d/1ijYl5Bpg2EKnJSlfxpNOBIK7D4_sALDX6/edit?usp=sharing&ouid=114568529811023043094&rtpof=true&sd=true)


## 🔧 Pre-requisites

It is suggested that to have Python **3.11** installed.
To check your version:
```bash
python --version
````

If it does **not** show Python 3.11, download it from [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)

-----

## 🚀 Setup & Run Instructions

### Step 1: Clone the repository

```bash
git clone [https://github.com/ivnjlsjnr/ReAzure](https://github.com/ivnjlsjnr/ReAzure)
cd ReAzure
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv venv
python3 -m venv venv (linux)
```

#### To activate:

  * **Windows**:

    ```bash
    venv\Scripts\activate
    ```

  * **Mac/Linux**:

    ```bash
    source venv/bin/activate
    ```

### Step 3: Install dependencies

```bash
pip install -r Requirements.txt
```

### Step 4: Run the App -

#### 4.1: Run Flet app (main UI)

```bash
python main.py
```

#### 4.2: Run FastAPI backend  - On a new terminal and still inside the virtual environment

```bash
uvicorn api.main:app --reload
```

## 📋 Features

| Feature                   | Description                                         |
| :------------------------ | :-------------------------------------------------- |
| 🧠 Mood Tracking         | Select your mood using emojis and log your thoughts |
| 🗕️ Mood History           | View previous moods and journals by date            |
| 📘 Journal Viewer         | See detailed entries per mood log               |
| ☁️ Azure Wall             | Display motivational quotes based on mood          |
| 🔄 "More" Quotes          | Fetch new quotes based on keywords                  |
| 📈 Mood Analytics         | View bar chart of mood frequency using Matplotlib   |
| 👤 User Accounts          | Login and Resigter new user  |
| 🚀 FastAPI                 | Backend API for user authentication and application data             |
| 🧠 Coping Strategy      | Suggest strategies based on mood logs              |
| 🌐 Mental Health APIs | Integration with real mental health content APIs   |

-----
## App flow

  * Register an user
  * Log In using the registered user
  * Click the plus/add button to log mood
  * Add a journal entry
  * View quotes and other information fund on Azure Wall
  * Check the mood analytics
  * Recheck logged mood on the mood history
  * Click the mood emoji on mood history to delete or view journal
  * Logout after logging a mood

-----
## 🛠 Tech Stack

  * **Python 3.11**
  * [Flet](https://flet.dev/)
  * [FastAPI](https://fastapi.tiangolo.com/)
  * SQLite
  * Matplotlib
  * Pandas
  * Requests

-----

## 🐧 Linux Troubleshooting

### ❗ Error: `libmpv.so.1: cannot open shared object file: No such file or directory`

### ✅ Solution:

```bash
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
```

-----

## 👥 Team Role

  * **Juanier, Julius Ivan M.** - Lead

<!-- end list -->

```
```
