# 📊 PROJECT ARCHITECTURE VISUALIZATION

## 🏗️ Project Structure Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    REGRESSION TESTING FRAMEWORK                  │
│                  Bug Detection & Mitigation System               │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
        ┌───────▼────────┐            ┌────────▼────────┐
        │   PROJECT A    │            │   PROJECT B     │
        │    (FAULTY)    │            │  (OPTIMIZED)    │
        │  Regression ❌  │            │  Fixed ✅        │
        └───────┬────────┘            └────────┬────────┘
                │                              │
    ┌───────────┼──────────────┐   ┌──────────┼──────────────┐
    │           │              │   │          │              │
┌───▼───┐  ┌───▼───┐  ┌──────▼┐ ┌─▼────┐ ┌──▼────┐  ┌──────▼┐
│ CODE  │  │ TESTS │  │ SETUP │ │ CODE │ │ TESTS │  │ SETUP │
│ .py   │  │ .py   │  │ .ps1  │ │ .py  │ │ .py   │  │ .ps1  │
│       │  │       │  │ .sh   │ │      │ │       │  │ .sh   │
└───────┘  └───────┘  └───────┘ └──────┘ └───────┘  └───────┘
    │           │          │        │         │          │
    └───────────┼──────────┘        └─────────┼──────────┘
                │                             │
                └──────────┬──────────────────┘
                           │
                    ┌──────▼──────┐
                    │   RUN ALL   │
                    │ Master Script│
                    │  .ps1 / .sh │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼─────┐  ┌────▼────┐  ┌─────▼─────┐
      │  LOGS &   │  │  TEST   │  │ COMPARISON│
      │  TIMING   │  │  DATA   │  │  REPORT   │
      └───────────┘  └─────────┘  └───────────┘
```

---

## 🔄 Execution Flow

```
START
  │
  ├─> [1] Load Test Data (test_data.json)
  │         │
  │         └─> 7 Test Cases (normal, edge, boundary, invalid, security)
  │
  ├─> [2] Setup Project A (Faulty)
  │         │
  │         ├─> Create virtual environment
  │         ├─> Install dependencies (pytest)
  │         └─> Ready to test
  │
  ├─> [3] Run Project A Tests
  │         │
  │         ├─> Execute 7 test cases
  │         ├─> EXPECTED: 2 failures (regression bugs)
  │         ├─> Generate logs
  │         └─> Record timing
  │
  ├─> [4] Setup Project B (Optimized)
  │         │
  │         ├─> Create virtual environment
  │         ├─> Install dependencies (pytest)
  │         └─> Ready to test
  │
  ├─> [5] Run Project B Tests
  │         │
  │         ├─> Execute 7 test cases
  │         ├─> EXPECTED: All pass ✅
  │         ├─> Generate logs
  │         └─> Record timing
  │
  ├─> [6] Generate Comparison Report
  │         │
  │         ├─> Compare test results
  │         ├─> Analyze performance
  │         ├─> Document fixes
  │         └─> Create recommendations
  │
  └─> [7] COMPLETE ✅
            │
            └─> View compare_report.md
```

---

## 🧪 Test Data Flow

```
test_data.json (7 Test Cases)
        │
        ├─────────────────────────────────────────┐
        │                                         │
    Project A                                 Project B
        │                                         │
        ▼                                         ▼
┌───────────────────┐                   ┌───────────────────┐
│ Test 1: Normal    │ ✅ PASS           │ Test 1: Normal    │ ✅ PASS
├───────────────────┤                   ├───────────────────┤
│ Test 2: Strings   │ ❌ FAIL           │ Test 2: Strings   │ ✅ PASS (FIXED)
├───────────────────┤                   ├───────────────────┤
│ Test 3: Boundary  │ ✅ PASS           │ Test 3: Boundary  │ ✅ PASS
├───────────────────┤                   ├───────────────────┤
│ Test 4: Missing   │ ✅ FAIL (expected)│ Test 4: Missing   │ ✅ FAIL (expected)
├───────────────────┤                   ├───────────────────┤
│ Test 5: Mixed     │ ❌ FAIL           │ Test 5: Mixed     │ ✅ PASS (FIXED)
├───────────────────┤                   ├───────────────────┤
│ Test 6: Email     │ ✅ FAIL (expected)│ Test 6: Email     │ ✅ FAIL (expected)
├───────────────────┤                   ├───────────────────┤
│ Test 7: SQL Inject│ ✅ FAIL (expected)│ Test 7: SQL Inject│ ✅ FAIL (expected)
└───────────────────┘                   └───────────────────┘
        │                                         │
        └──────────────┬──────────────────────────┘
                       ▼
            ┌──────────────────────┐
            │  Comparison Report   │
            │  - Side-by-side      │
            │  - Performance       │
            │  - Recommendations   │
            └──────────────────────┘
```

---

## 🎯 Regression Detection Mechanism

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT DATA VALIDATION                         │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │                               │
┌───────────▼──────────┐        ┌──────────▼───────────┐
│   PROJECT A (FAULTY) │        │ PROJECT B (OPTIMIZED)│
│                      │        │                      │
│ Strict Type Checking │        │ Flexible Conversion  │
└───────────┬──────────┘        └──────────┬───────────┘
            │                              │
    ┌───────┴───────┐              ┌──────┴──────┐
    │               │              │             │
┌───▼───┐      ┌───▼───┐      ┌───▼───┐    ┌───▼───┐
│ int   │ ✅   │ "123" │ ❌   │ int   │ ✅ │ "123" │ ✅
└───────┘      └───────┘      └───────┘    └───────┘
│ float │ ✅   │  123  │ ❌   │ float │ ✅ │  123  │ ✅
└───────┘      └───────┘      └───────┘    └───────┘
│ bool  │ ✅   │   1   │ ❌   │ bool  │ ✅ │   1   │ ✅
└───────┘      └───────┘      └───────┘    └───────┘
    │               │              │             │
    └───────┬───────┘              └──────┬──────┘
            │                             │
            ▼                             ▼
      REGRESSION                      ALL PASS
      DETECTED ⚠️                       ✅
```

---

## 📁 File Dependency Map

```
run_all.ps1 / run_all.sh (Master Script)
    │
    ├─> test_data.json (Shared Test Cases)
    │
    ├─> Project_A_Faulty/
    │     │
    │     ├─> setup_original.ps1 / .sh
    │     │     └─> requirements_original.txt
    │     │           └─> Creates: venv_original/
    │     │
    │     ├─> run_original.ps1 / .sh
    │     │     │
    │     │     ├─> test_original.py
    │     │     │     └─> original_code.py
    │     │     │           └─> DataValidator (Faulty)
    │     │     │
    │     │     └─> Generates:
    │     │           ├─> log_original.txt
    │     │           ├─> time_original.txt
    │     │           └─> test_results_original.json
    │     │
    │     └─> Files: 9 total
    │
    ├─> Project_B_Optimized/
    │     │
    │     ├─> setup_optimized.ps1 / .sh
    │     │     └─> requirements_optimized.txt
    │     │           └─> Creates: venv_optimized/
    │     │
    │     ├─> run_optimized.ps1 / .sh
    │     │     │
    │     │     ├─> test_optimized.py
    │     │     │     └─> optimized_code.py
    │     │     │           └─> DataValidator (Fixed)
    │     │     │
    │     │     └─> Generates:
    │     │           ├─> log_optimized.txt
    │     │           ├─> time_optimized.txt
    │     │           └─> test_results_optimized.json
    │     │
    │     └─> Files: 9 total
    │
    └─> Generates: compare_report.md (Final Report)
```

---

## 🔍 Code Architecture Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                  PROJECT A - FAULTY VERSION                      │
└─────────────────────────────────────────────────────────────────┘

DataValidator.validate_and_normalize()
    │
    ├─> Check required fields
    │
    ├─> Validate user_id
    │     └─> isinstance(data['user_id'], int) ❌ STRICT
    │           └─> Rejects: "12345", "ABC123"
    │
    ├─> Validate age
    │     └─> isinstance(data['age'], int) ❌ STRICT
    │           └─> Rejects: "25", 25.0
    │
    ├─> Validate balance
    │     └─> isinstance(data['balance'], float) ❌ STRICT
    │           └─> Rejects: 1000, "1500.50"
    │
    └─> Validate is_active
          └─> isinstance(data['is_active'], bool) ❌ STRICT
                └─> Rejects: 1, "true"

┌─────────────────────────────────────────────────────────────────┐
│                 PROJECT B - OPTIMIZED VERSION                    │
└─────────────────────────────────────────────────────────────────┘

DataValidator.validate_and_normalize()
    │
    ├─> Check required fields
    │
    ├─> Validate user_id
    │     └─> _validate_and_convert_user_id() ✅ FLEXIBLE
    │           └─> Accepts: int, str → converts to str
    │
    ├─> Validate age
    │     └─> _validate_and_convert_age() ✅ FLEXIBLE
    │           └─> Accepts: int, float, numeric str → validates & converts
    │
    ├─> Validate balance
    │     └─> _validate_and_convert_balance() ✅ FLEXIBLE
    │           └─> Accepts: int, float, numeric str → validates & converts
    │
    └─> Validate is_active
          └─> _validate_and_convert_is_active() ✅ FLEXIBLE
                └─> Accepts: bool, int (0/1), str ("true"/"false") → converts
```

---

## 📊 Expected Results Matrix

```
┌─────────┬──────────────────────┬──────────────┬──────────────┐
│ Test ID │ Test Name            │ Project A    │ Project B    │
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    1    │ Normal valid data    │   ✅ PASS    │   ✅ PASS    │
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    2    │ Numeric strings      │   ❌ FAIL    │   ✅ PASS    │ ⚠️ REGRESSION
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    3    │ Zero/negative        │   ✅ PASS    │   ✅ PASS    │
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    4    │ Missing fields       │   ✅ FAIL*   │   ✅ FAIL*   │ *Expected
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    5    │ Mixed types          │   ❌ FAIL    │   ✅ PASS    │ ⚠️ REGRESSION
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    6    │ Invalid email        │   ✅ FAIL*   │   ✅ FAIL*   │ *Expected
├─────────┼──────────────────────┼──────────────┼──────────────┤
│    7    │ SQL injection        │   ✅ FAIL*   │   ✅ FAIL*   │ *Expected
└─────────┴──────────────────────┴──────────────┴──────────────┘

Legend:
  ✅ PASS = Test passes as expected
  ❌ FAIL = Unexpected failure (regression bug)
  ✅ FAIL* = Expected failure (validation working correctly)
  ⚠️ = Regression issue (fixed in Project B)
```

---

## 🚀 Quick Start Commands

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION OPTIONS                             │
└─────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════╗
║              OPTION 1: ONE-CLICK EXECUTION                     ║
╠═══════════════════════════════════════════════════════════════╣
║  Windows PowerShell:                                           ║
║    .\run_all.ps1                                              ║
║                                                                ║
║  Git Bash / Linux / macOS:                                    ║
║    bash run_all.sh                                            ║
╚═══════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════╗
║              OPTION 2: MANUAL STEP-BY-STEP                    ║
╠═══════════════════════════════════════════════════════════════╣
║  Step 1: Setup Project A                                      ║
║    cd Project_A_Faulty                                        ║
║    .\setup_original.ps1  (or bash setup_original.sh)         ║
║                                                                ║
║  Step 2: Run Project A Tests                                  ║
║    .\run_original.ps1  (or bash run_original.sh)             ║
║    cd ..                                                      ║
║                                                                ║
║  Step 3: Setup Project B                                      ║
║    cd Project_B_Optimized                                     ║
║    .\setup_optimized.ps1  (or bash setup_optimized.sh)       ║
║                                                                ║
║  Step 4: Run Project B Tests                                  ║
║    .\run_optimized.ps1  (or bash run_optimized.sh)           ║
║    cd ..                                                      ║
║                                                                ║
║  Step 5: View Results                                         ║
║    Get-Content compare_report.md  (or cat compare_report.md) ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📈 Performance Metrics Flow

```
Execution → Timing → Logging → Reporting

Project A:
  Start Time ────┐
                 │
  Run Tests ─────┤
                 │
  End Time ──────┘
                 │
                 ├─> Calculate Duration
                 │
                 ├─> time_original.txt
                 ├─> log_original.txt
                 └─> test_results_original.json

Project B:
  Start Time ────┐
                 │
  Run Tests ─────┤
                 │
  End Time ──────┘
                 │
                 ├─> Calculate Duration
                 │
                 ├─> time_optimized.txt
                 ├─> log_optimized.txt
                 └─> test_results_optimized.json

Both Results ────┐
                 │
                 └─> compare_report.md
                       │
                       ├─> Test comparison
                       ├─> Performance comparison
                       ├─> Code analysis
                       └─> Recommendations
```

---

## 🎓 Learning Path

```
1. Read Documentation
   └─> README.md
   └─> WINDOWS_QUICKSTART.md

2. Understand the Regression
   └─> Compare original_code.py vs optimized_code.py
   └─> Review test_data.json

3. Run the Tests
   └─> Execute run_all.ps1 or run_all.sh

4. Analyze Results
   └─> Review compare_report.md
   └─> Check log files

5. Understand the Fix
   └─> Study flexible type handling
   └─> Compare test results

6. Apply Learning
   └─> Recognize similar patterns
   └─> Implement best practices
```

---

*Visual guide for the Regression Detection & Mitigation Framework*  
*Version 1.0 - October 31, 2025*
