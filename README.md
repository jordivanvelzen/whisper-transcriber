# Whisper Transcriber

Whisper Transcriber is a simple tool that allows you to transcribe audio and video files using OpenAI's Whisper model (via **Whisper-CLI / whisper.cpp**) on macOS. This script simplifies running the transcription process and organizing your results.

## 🚀 Features

- Supports **English** and **Dutch** transcription
- Automatically splits long files into chunks and merges transcripts with correct timestamps
- Converts video/audio files to **16kHz WAV** format automatically
- Runs **Whisper-CLI** in a new terminal window
- Highlights the transcript in Finder for easy access
- Simplified console output for a cleaner user experience
- Sets up the **`run-transcriber`** command for easy execution

---

## 🛠 Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/jordivanvelzen/whisper-transcriber.git
cd whisper-transcriber
```

### 2️⃣ Install Required Tools **Manually**

The installer **checks** for dependencies but **does not install** them automatically. You must install the following:

#### ✅ Homebrew (if missing)
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### ✅ FFmpeg
```sh
brew install ffmpeg
```

#### ✅ pipx
```sh
brew install pipx
pipx ensurepath
source ~/.zshrc
```

#### ✅ Whisper-CLI (`whisper.cpp`)
```sh
brew install whisper-cpp
```

#### ✅ Python `psutil` library
Make sure your `python3` can import `psutil`:
```sh
python3 -m pip install psutil
```

#### ✅ Download the Whisper model file (ggml format)
```sh
mkdir -p ~/.whisper
curl -L -o ~/.whisper/medium.bin https://ggml.ggerganov.com/ggml-model-whisper-medium-q5_0.bin
```
📥 Or get the latest model here: [https://ggml.ggerganov.com/](https://ggml.ggerganov.com/)

---

### 3️⃣ Run the Installer Check
```sh
./install.sh
```
✅ This will:
- Check all dependencies
- Set up the `run-transcriber` command if everything is ready
- Exit and guide you if anything is missing

---

## 🎯 Usage
1. Run `run-transcriber`
2. Choose a **language** (English/Dutch)
3. Select an **audio or video file**
4. The script:
   - Converts the file to 16kHz WAV
   - Splits long files
   - Runs transcription with **Whisper-CLI**
   - Saves the result next to the original file
   - Highlights the transcript in Finder

---

## 📂 File Structure

```
whisper-transcriber/
│── install.sh              # Dependency check + run-transcriber setup
│── whisper_transcriber.py  # Main Python script
│── README.md               # Documentation
```

---

## 🛠 Troubleshooting
- If `run-transcriber` isn’t recognized, restart your terminal or run:
  ```sh
  source ~/.zshrc
  ```
- If `tkinter` is missing, ensure you’re using macOS system Python:
  ```sh
  /Library/Developer/CommandLineTools/usr/bin/python3 -m tkinter
  ```
  Although I don't think this is needed anymore with the current install method, it may be good to keep this info here for now

## 📜 License
This project is licensed under the **MIT License**.

---

## 🙌 Contributions
Feel free to **fork**, submit **issues**, or make **pull requests**!

---

🎉 **Enjoy transcribing effortlessly!**
