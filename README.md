# Whisper Transcriber

Whisper Transcriber is a simple tool that allows you to transcribe audio and video files using OpenAI's Whisper model on macOS. This script automates the conversion process and provides an easy-to-use interface.

## 🚀 Features
- Supports **English** and **Dutch** transcription
- Converts video/audio files to **16kHz WAV** format automatically
- Runs **Whisper-CLI** in a new terminal window
- Highlights the transcript in Finder for easy access
- One-command setup via `install.sh`

## 🛠 Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR-USERNAME/whisper-transcriber.git
cd whisper-transcriber
```

### 2️⃣ Run the Installer
```sh
./install.sh
```
This will:
- Install **Python**, **FFmpeg**, and **Whisper-CLI** (if missing)
- Set up the **`run-transcriber`** command for easy execution
- Ensure all dependencies are installed

### 3️⃣ Run the Transcriber
After installation, simply type:
```sh
run-transcriber
```
This will:
- Ask you to select an **audio or video file**
- Convert it to **16kHz WAV** if necessary
- Start **Whisper-CLI** in a new terminal window
- Save the transcription next to the original file
- Highlight the transcript in Finder

## 🎯 Usage
1. Run `run-transcriber`
2. Choose a **language** (English/Dutch)
3. Select an **audio or video file**
4. Let the script process and transcribe it
5. Open the transcript file from Finder

## 📂 File Structure
```
whisper-transcriber/
│── install.sh            # Installation script
│── whisper_transcriber.py # Main Python script
│── README.md             # Documentation
│── resources/            # (Optional) Extra help files
│── scripts/              # (Optional) Additional utilities
```

## 🛠 Troubleshooting
- If `run-transcriber` isn't recognized, restart your terminal or run:
  ```sh
  source ~/.zshrc
  ```
- If `tkinter` is missing, ensure you’re using macOS system Python by running:
  ```sh
  /Library/Developer/CommandLineTools/usr/bin/python3 -m tkinter
  ```

## 📜 License
This project is licensed under the **MIT License**.

## 🙌 Contributions
Feel free to **fork**, submit **issues**, or make **pull requests**!

## 📧 Contact
For questions or suggestions, reach out via GitHub Issues.

---
🎉 **Enjoy transcribing effortlessly!**
