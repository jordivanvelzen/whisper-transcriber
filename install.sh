#!/bin/bash

echo "🚀 Checking environment for Whisper Transcriber setup..."
set -e  # Exit immediately on error (explicit checks control flow)

check_or_exit() {
    local cmd="$1"
    local tip="$2"
    if ! command -v "$cmd" &>/dev/null; then
        echo "❌ '$cmd' is not installed."
        echo "💡 Tip: $tip"
        exit 1
    else
        echo "✅ '$cmd' is installed."
    fi
}

# 1. Homebrew
check_or_exit brew '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'

# 2. ffmpeg
check_or_exit ffmpeg "brew install ffmpeg"

# 3. pipx
check_or_exit pipx "brew install pipx && pipx ensurepath && source ~/.zshrc"

# 4. whisper-cli (via whisper.cpp)
check_or_exit whisper-cli "brew install whisper-cpp"

# 5. Check model file
MODEL_PATH="$HOME/.whisper/medium.bin"
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Whisper model not found at $MODEL_PATH"
    echo "💡 Tip: Download the model with:"
    echo "mkdir -p ~/.whisper"
    echo "curl -L -o ~/.whisper/medium.bin https://ggml.ggerganov.com/ggml-model-whisper-medium-q5_0.bin"
    echo "💡 Or check latest models: https://ggml.ggerganov.com/"
    exit 1
else
    echo "✅ Whisper model found: $MODEL_PATH"
fi

# 6. Check Python
PYTHON_PATH=$(which python3)
echo "✅ Python found at: $PYTHON_PATH"
PYTHON_VERSION=$($PYTHON_PATH --version)
echo "✅ Python version: $PYTHON_VERSION"

#7. Optional: Check psutil (comment out or remove if not needed)
if ! $PYTHON_PATH -c "import psutil" &>/dev/null; then
    echo "❌ Python package 'psutil' not found."
    echo "💡 Tip: Install it using:"
    echo "brew install psutils"
    exit 1
else
    echo "✅ Python package 'psutil' is installed."
fi

# ✅ Only reached if ALL above passed
echo "📌 Setting up 'run-transcriber'..."
sudo rm -f /usr/local/bin/run-transcriber
echo "#!/bin/bash" | sudo tee /usr/local/bin/run-transcriber > /dev/null
echo "$PYTHON_PATH $(pwd)/whisper_transcriber.py \"\$@\"" | sudo tee -a /usr/local/bin/run-transcriber > /dev/null
sudo chmod +x /usr/local/bin/run-transcriber

echo "✅ Setup complete! You can now run the transcriber using:"
echo "   run-transcriber"
