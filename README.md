
# ☁️ ReAzure

A **Mental Health Mood Tracker** platform designed to support emotional well-being through self-reflection, mood tracking, and community-based resources. By integrating journaling features and mood analytics, ReAzure encourages individuals to actively engage with their mental health.


### 📌 Proposal

[View Full Proposal on Google Drive](https://drive.google.com/file/d/1AcfpSmkxHPtAycWrDmN0ioSYhyqiX5Qr/view?usp=drive_link)  \
[View Project Documentation](https://drive.google.com/file/d/19nmpCg2kTsBvvyUbvxEVvmFAipfEPnOP/view?usp=sharing) 

### 🗕️ Gantt Chart

[View Progress Plan](https://docs.google.com/spreadsheets/d/1mWkYS2yBVCVVsYYMnSqV1aa-3epj6grH/edit?usp=sharing&ouid=107369633571634366071&rtpof=true&sd=true)


## 🔧 Pre-requisites

It is suggested that to have Python **3.11**>=  installed.
To check your version:
```bash
python --version
````

If it does **not** show Python 3.11 >=, download it from [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/)  \
Use pyenv to easily manage python version. Instructions here:[Pyenv](https://github.com/pyenv/pyenv#installation)  

## 🚀 Setup & Run Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/ivnjlsjnr/ReAzure
```
```bash
cd ReAzure
```
### Step 2: Create and activate a virtual environment

```bash
python -m venv venv
```
```bash
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

#### 4.2: Run FastAPI backend  - On a new terminal and still inside the virtual environment (make sure you are inside ReAzure directory)

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
-----

-----

## App Main views
<img width="1255" height="690" alt="Image" src="https://github.com/user-attachments/assets/7032684a-30e1-4a30-8459-edcc27f3fd9b" />
<img width="1918" height="1031" alt="Image" src="https://github.com/user-attachments/assets/4353b956-7207-4d61-bfc5-06e228c5757a" />
<img width="1919" height="570" alt="Image" src="https://github.com/user-attachments/assets/b3a71ef5-93df-4520-b8df-6c4e9b737855" />
<img width="1916" height="1030" alt="Image" src="https://github.com/user-attachments/assets/281e589a-9624-4f27-b302-1e8c381edb60" /><!-- end list -->

```
```
