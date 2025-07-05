# ReAzure
Group 5  \
Project proposal: https://drive.google.com/file/d/1AcfpSmkxHPtAycWrDmN0ioSYhyqiX5Qr/view?usp=drive_link  \
Gantt chart: https://docs.google.com/spreadsheets/d/1ijYl5Bpg2EKnJSlfxoNBIK7D4_sALDX6/edit?usp=sharing&ouid=114568529811023043094&rtpof=true&sd=true  \


Pre-requisites

Step 1. git clone https://github.com/ivnjlsjnr/ReAzure  \
Step 2. cd ReAzure  \
Step 3. Create a virtual environment  \
Step 4. pip install "Requirements.txt"  \
Step 5. Run main.py




Troubleshooting Issues encountered:
"libmpv.so.1: cannot open shared object file: No such file or directory"
solution: 
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1
