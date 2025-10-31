# Quick Start Guide for Windows

## 🚀 One-Click Execution (Recommended)

### For PowerShell Users (Windows):

```powershell
# Run everything in one command
.\run_all.ps1
```

### For Git Bash / WSL Users (Windows):

```bash
# Run everything in one command
bash run_all.sh
```

---

## 📋 Manual Execution Steps

### Option 1: PowerShell (Native Windows)

#### Project A - Faulty Implementation:
```powershell
cd Project_A_Faulty
.\setup_original.ps1
.\run_original.ps1
cd ..
```

#### Project B - Optimized Implementation:
```powershell
cd Project_B_Optimized
.\setup_optimized.ps1
.\run_optimized.ps1
cd ..
```

### Option 2: Git Bash / WSL

#### Project A - Faulty Implementation:
```bash
cd Project_A_Faulty
bash setup_original.sh
bash run_original.sh
cd ..
```

#### Project B - Optimized Implementation:
```bash
cd Project_B_Optimized
bash setup_optimized.sh
bash run_optimized.sh
cd ..
```

---

## ⚙️ Prerequisites

1. **Python 3.7+** installed and in PATH
   - Check: `python --version`
   - Download: https://www.python.org/downloads/

2. **PowerShell** (for .ps1 scripts) OR **Git Bash** (for .sh scripts)
   - PowerShell is included with Windows
   - Git Bash: https://git-scm.com/downloads

3. **Execution Policy** (PowerShell only):
   ```powershell
   # If you get execution policy errors, run:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

---

## 📊 Expected Output

### After running `run_all.ps1` or `bash run_all.sh`:

✅ **Project A (Faulty)**: 
- 2 regression test failures (Tests 2 and 5)
- 5 tests pass or fail as expected
- Exit code may be non-zero (indicates test failures)

✅ **Project B (Optimized)**: 
- All tests pass
- 100% success rate
- Exit code 0 (success)

✅ **Generated Files**:
- `Project_A_Faulty/log_original.txt` - Detailed test output
- `Project_A_Faulty/time_original.txt` - Performance metrics
- `Project_B_Optimized/log_optimized.txt` - Detailed test output
- `Project_B_Optimized/time_optimized.txt` - Performance metrics
- `compare_report.md` - Side-by-side comparison

---

## 🔍 Viewing Results

### PowerShell:
```powershell
# View comparison report
Get-Content compare_report.md

# View Project A logs
Get-Content Project_A_Faulty\log_original.txt

# View Project B logs
Get-Content Project_B_Optimized\log_optimized.txt
```

### Git Bash:
```bash
# View comparison report
cat compare_report.md

# View Project A logs
cat Project_A_Faulty/log_original.txt

# View Project B logs
cat Project_B_Optimized/log_optimized.txt
```

---

## 🐛 Troubleshooting

### "python: command not found"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal after installation

### "execution policy" error (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "pytest: command not found"
- Run the setup scripts first:
  ```powershell
  cd Project_A_Faulty
  .\setup_original.ps1
  ```

### Virtual environment activation fails
- Make sure you're in the correct project directory
- Try running the setup script again
- On PowerShell, you may need to enable script execution (see above)

---

## 📁 File Structure After Execution

```
chatWorkspace/
├── README.md
├── WINDOWS_QUICKSTART.md (this file)
├── test_data.json
├── compare_report.md (✨ generated)
├── run_all.ps1 (Windows PowerShell)
├── run_all.sh (Git Bash/WSL)
│
├── Project_A_Faulty/
│   ├── original_code.py
│   ├── test_original.py
│   ├── requirements_original.txt
│   ├── setup_original.ps1 (Windows)
│   ├── setup_original.sh (Git Bash)
│   ├── run_original.ps1 (Windows)
│   ├── run_original.sh (Git Bash)
│   ├── venv_original/ (✨ created by setup)
│   ├── log_original.txt (✨ generated)
│   ├── time_original.txt (✨ generated)
│   └── test_results_original.json (✨ generated)
│
└── Project_B_Optimized/
    ├── optimized_code.py
    ├── test_optimized.py
    ├── requirements_optimized.txt
    ├── setup_optimized.ps1 (Windows)
    ├── setup_optimized.sh (Git Bash)
    ├── run_optimized.ps1 (Windows)
    ├── run_optimized.sh (Git Bash)
    ├── venv_optimized/ (✨ created by setup)
    ├── log_optimized.txt (✨ generated)
    ├── time_optimized.txt (✨ generated)
    └── test_results_optimized.json (✨ generated)
```

---

## ⏱️ Estimated Execution Time

- **Setup** (each project): ~30-60 seconds
- **Tests** (each project): ~2-5 seconds
- **Total time**: ~2-3 minutes

---

## 🎯 Success Criteria

After running `run_all.ps1`, you should see:

✅ PowerShell output showing both projects executing  
✅ Project A: Some tests failing (regression detected)  
✅ Project B: All tests passing (regression fixed)  
✅ `compare_report.md` file created  
✅ Log files in both project directories  

If you see all of these, **the evaluation is complete!**

---

## 💡 Tips

1. **First time running?** Use the one-click execution:
   ```powershell
   .\run_all.ps1
   ```

2. **Want to re-run tests?** Just run the `run_*.ps1` scripts again (no need to setup again)

3. **Clean start?** Delete the `venv_*` folders and run setup again

4. **Compare outputs?** Check the `compare_report.md` file for detailed analysis

---

*For detailed information, see the main README.md file*
