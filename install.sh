#!/bin/bash

echo "🚀 Setting up Whisper Transcriber..."

# Check if Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "🍺 Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "🍺 Homebrew is already installed. Updating..."
    brew update
fi

# Install required dependencies
echo "🔧 Installing dependencies..."
brew install python3 ffmpeg whisper-cli

# Set Python to macOS system Python
SYSTEM_PYTHON="/Library/Developer/CommandLineTools/usr/bin/python3"

# Install Python dependencies
echo "🐍 Installing required Python packages..."
$SYSTEM_PYTHON -m pip install --upgrade pip
$SYSTEM_PYTHON -m pip install psutil

# Create or update the global shortcut command 'run-transcriber'
echo "📌 Setting up 'run-transcriber'..."
sudo rm -f /usr/local/bin/run-transcriber  # Remove existing one if needed
echo "#!/bin/bash" | sudo tee /usr/local/bin/run-transcriber > /dev/null
echo "$SYSTEM_PYTHON $(pwd)/whisper_transcriber.py" | sudo tee -a /usr/local/bin/run-transcriber > /dev/null
sudo chmod +x /usr/local/bin/run-transcriber

# Ensure the system recognizes the new command
source ~/.zshrc

echo "✅ Installation complete! You can now run the transcriber using:"
echo "   run-transcriber"
