#!/bin/bash

echo "========================================="
echo "Running Project B - Optimized Implementation"
echo "========================================="
echo ""

# Activate virtual environment
if [ -f "venv_optimized/Scripts/activate" ]; then
    source venv_optimized/Scripts/activate
else
    source venv_optimized/bin/activate
fi

# Clear previous logs
rm -f log_optimized.txt time_optimized.txt

# Start timing
start_time=$(date +%s)

echo "Running tests with pytest..."
echo ""

# Run tests and capture output
pytest test_optimized.py -v --tb=short --json-report --json-report-file=test_results_optimized.json 2>&1 | tee log_optimized.txt

# End timing
end_time=$(date +%s)
execution_time=$((end_time - start_time))

# Generate timing report
echo "=========================================" > time_optimized.txt
echo "Project B - Performance Report" >> time_optimized.txt
echo "=========================================" >> time_optimized.txt
echo "" >> time_optimized.txt
echo "Execution Time: ${execution_time} seconds" >> time_optimized.txt
echo "Timestamp: $(date)" >> time_optimized.txt
echo "" >> time_optimized.txt
echo "Test Results Summary:" >> time_optimized.txt
echo "See log_optimized.txt for detailed output" >> time_optimized.txt
echo "See test_results_optimized.json for structured results" >> time_optimized.txt
echo "" >> time_optimized.txt

# Display summary
echo ""
echo "========================================="
echo "Execution Complete!"
echo "========================================="
echo "Total execution time: ${execution_time} seconds"
echo "Results saved to:"
echo "  - log_optimized.txt"
echo "  - time_optimized.txt"
echo "  - test_results_optimized.json"
echo "========================================="
