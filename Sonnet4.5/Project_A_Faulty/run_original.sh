#!/bin/bash

echo "========================================="
echo "Running Project A - Faulty Implementation"
echo "========================================="
echo ""

# Activate virtual environment
if [ -f "venv_original/Scripts/activate" ]; then
    source venv_original/Scripts/activate
else
    source venv_original/bin/activate
fi

# Clear previous logs
rm -f log_original.txt time_original.txt

# Start timing
start_time=$(date +%s)

echo "Running tests with pytest..."
echo ""

# Run tests and capture output
pytest test_original.py -v --tb=short --json-report --json-report-file=test_results_original.json 2>&1 | tee log_original.txt

# End timing
end_time=$(date +%s)
execution_time=$((end_time - start_time))

# Generate timing report
echo "=========================================" > time_original.txt
echo "Project A - Performance Report" >> time_original.txt
echo "=========================================" >> time_original.txt
echo "" >> time_original.txt
echo "Execution Time: ${execution_time} seconds" >> time_original.txt
echo "Timestamp: $(date)" >> time_original.txt
echo "" >> time_original.txt
echo "Test Results Summary:" >> time_original.txt
echo "See log_original.txt for detailed output" >> time_original.txt
echo "See test_results_original.json for structured results" >> time_original.txt
echo "" >> time_original.txt

# Display summary
echo ""
echo "========================================="
echo "Execution Complete!"
echo "========================================="
echo "Total execution time: ${execution_time} seconds"
echo "Results saved to:"
echo "  - log_original.txt"
echo "  - time_original.txt"
echo "  - test_results_original.json"
echo "========================================="
