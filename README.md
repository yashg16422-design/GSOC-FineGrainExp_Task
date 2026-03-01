# GSOC-FineGrainExp_Task

# Storage I/O Benchmark — Fine Grain Experiment

Benchmarking three file storage strategies across 100,000 records (1–2 KB each) 
measuring write, sequential read, and random read performance.

## Strategies Tested
- Single Large File — all records in one file with offset+size index
- Chunked Files — 1,000 records per file with chunk+offset index  
- Individual Files — one file per record with deterministic naming
- 
## Getting Started

### 1. Clone the Repository
```
git clone https://github.com/yashg16422-design/GSOC-FineGrainExp_Task.git
cd GSOC-FineGrainExp_Task
```

### 2. Create and Activate Virtual Environment
```
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```
## Requirements
Python 3.8+ and one third party dependency:
```
pip install -r requirements.txt
```

## Task 1 — Reproducing Benchmark Results

Run the main benchmarking script from your project directory:
```
python benchmarkingIO.py
```
A prompt will appear asking for your preferred run mode:
- `write` — only runs write phase
- `read` — only runs read phase (requires existing data)
- `both` — runs write then read
- `full` — runs all strategies end to end without prompts

Results may vary slightly across devices due to hardware and OS differences 
but relative performance ranges will remain consistent.

## Task 2 — Extended Metrics

### System Call Analysis
> WSL or Linux only — strace is not available on Windows

Copy the project to your WSL or Linux home directory and run from there.
Important: run from `~/...` and NOT from `/mnt/c/...`
```
strace -c -e trace=read,write,openat,close,lseek python3 benchmarkingIO.py
```
This will output a syscall summary table with counts and time per call.

### CPU and I/O Statistics
The output of Task 1 itself includes a comprehensive resource utilization 
report covering Wall Time, User CPU, System CPU, Disk Read, and Disk Write 
— no additional steps required.

### Disk Utilization Logging
From your project directory in PowerShell:
```
./run_benchmark.ps1
```
This generates `disk_utilization_log.csv` with per-timestamp read/write MB/s 
and cumulative totals. Refer to page 3 of the report for interpretation steps.

## Notes
- Data directories (single/, chunked/, individual/) are git-ignored — 
  run write mode first before attempting read mode
- All random operations use fixed seeds for full reproducibility
- For accurate syscall counts always use WSL/Linux — Windows strace 
  alternatives do not provide equivalent kernel-level visibility
