# ReAzure
Group 5  \
- 📌 **Proposal**: [View on Google Drive](https://drive.google.com/file/d/1AcfpSmkxHPtAycWrDmN0ioSYhyqiX5Qr/view?usp=drive_link)
- 📅 **Gantt Chart**: [View Progress Plan](https://docs.google.com/spreadsheets/d/1ijYl5Bpg2EKnJSlfxoNBIK7D4_sALDX6/edit?usp=sharing&ouid=114568529811023043094&rtpof=true&sd=true)


Pre-requisites
Ensure you have:
- Python **3.10 or higher**
 
# Step 1: Clone the repository
git clone https://github.com/ivnjlsjnr/ReAzure
cd ReAzure

# Step 2: Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the app
python main.py




Troubleshooting Issues encountered:  \
"libmpv.so.1: cannot open shared object file: No such file or directory"  \
solution:   \
sudo apt update  \
sudo apt install libmpv-dev libmpv2  \
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1  \
