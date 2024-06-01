#!/bin/bash

# Assign positional arguments to variables
BINARY_FILE=$1
RESULT_DIR=$2

# Ensure that the binary file exists
if [ ! -f "$BINARY_FILE" ]; then
    echo "Error: The specified binary file '$BINARY_FILE' does not exist." >&2
    exit 1
fi

# Ensure that the specified directory exists
if [ ! -d "$RESULT_DIR" ]; then
    echo "Error: The specified directory '$RESULT_DIR' does not exist." >&2
    exit 1
fi

# Get the path to the testing suite directory
TEST_SUITE_DIR="$(dirname "$(realpath "$0")")/../testing_suites"

# Create input file to be read in by the NIST testing suite
input_file="$RESULT_DIR/nist_inputs.txt"
cat <<EOL > "$input_file"
0
$BINARY_FILE
1
0
100
1
EOL

# copy experiments folder to present working directory of user for NIST to be able to store the results
cp -r "$TEST_SUITE_DIR/sts-2.1.2/experiments" "."

# Function to clean up the temporary directory
cleanup() {
    rm -rf "./experiments"
}

# Set up a trap to call the cleanup function on exit
trap cleanup EXIT

# Run the NIST test suite
{ time "$TEST_SUITE_DIR/sts-2.1.2/assess" 10000 < "$input_file"; } 2> "$RESULT_DIR/time_nist"

# Log the timing results
echo "NIST" >> "$RESULT_DIR/time"
cat "$RESULT_DIR/time_nist" >> "$RESULT_DIR/time"
rm "$RESULT_DIR/time_nist"

# Copy the final analysis report to the result directory
cp "$TEST_SUITE_DIR/experiments/AlgorithmTesting/finalAnalysisReport.txt" "$RESULT_DIR/test_nist.log"

echo "NIST test completed."

