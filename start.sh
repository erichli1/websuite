# Function to handle the interrupt signal (Ctrl+C)
cleanup() {
    echo "Caught Signal ... cleaning up."
    kill $PID_PYTHON
    kill $PID_NPM
    echo "Done cleanup ... quitting."
    exit 1
}

# Trap the SIGINT signal (Ctrl+C) and call the cleanup function
trap 'cleanup' SIGINT

# Start the Flask backend in the background and get its PID
python app.py &
PID_PYTHON=$!

# Change to the frontend directory, start the Next frontend in the background, and get its PID
cd frontend && npm run dev &
PID_NPM=$!

# Wait for both processes to exit
wait $PID_PYTHON
wait $PID_NPM