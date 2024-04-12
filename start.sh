# Function to handle the interrupt signal (Ctrl+C)
cleanup() {
    echo "Caught Signal ... cleaning up."
    # Send SIGTERM to all processes in the current process group
    kill -- -$PGID
    echo "Done cleanup ... quitting."
    exit 1
}

# Trap the SIGINT signal (Ctrl+C) and call the cleanup function
trap 'cleanup' SIGINT

# Store the process group ID
PGID=$$
echo "Process Group ID: $PGID"

# Start the Flask backend
cd environment
echo "Starting Python server..."
python app.py &

# Start the Next.js frontend
cd frontend
echo "Starting NPM server..."
npm run dev &

# Wait for both processes to exit
wait