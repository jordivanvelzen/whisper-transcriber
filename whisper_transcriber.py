import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import warnings
import time
import psutil

# Suppress warnings and macOS Tk deprecation message
os.environ["TK_SILENCE_DEPRECATION"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

def select_file():
    print("📂 Please select an audio or video file...")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an audio or video file")
    if not file_path:
        print("❌ No file selected. Exiting.")
        exit()
    print(f"✅ File Selected: {file_path}")
    return file_path

def convert_to_wav(input_file):
    output_file = os.path.splitext(input_file)[0] + "_16khz.wav"
    
    print(f"🎵 Converting {input_file} to 16kHz WAV format...")
    
    convert_cmd = [
        "ffmpeg", "-y",  # `-y` forces overwrite of existing files
        "-i", input_file,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_file
    ]
    
    subprocess.run(convert_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Conversion complete.")
    
    return output_file

def transcribe(file_path, language):
    output_transcript = os.path.splitext(file_path)[0] + "_transcription.txt"
    print(f"📝 Transcribing {file_path} in {language}...")

    # Get all existing whisper-cli PIDs BEFORE starting a new process
    existing_pids = get_whisper_pids()

    # Corrected osascript command with proper escaping
    whisper_cmd = f'osascript -e \'tell application "Terminal" to do script "whisper-cli -m ~/.whisper/medium.bin -l {language} -t 8 \\"{file_path}\\" | tee \\"{output_transcript}\\""\''

    # Start transcription in a new Terminal window
    subprocess.Popen(whisper_cmd, shell=True)

    # Wait a bit to allow the new process to start
    time.sleep(2)

    # Get new whisper-cli PIDs AFTER starting process
    new_pids = get_whisper_pids()

    # Determine the new Whisper process PID
    whisper_pid = list(set(new_pids) - set(existing_pids))
    
    if whisper_pid:
        whisper_pid = whisper_pid[0]  # Extract single PID
        print(f"🔄 Monitoring whisper process (PID: {whisper_pid})...")
    else:
        print("⚠️ Could not determine whisper process ID. Waiting based on output file.")

    # Monitor the Whisper process
    print("⏳ Transcription in progress...", end="", flush=True)
    
    while whisper_pid and is_process_running(whisper_pid):
        print(".", end="", flush=True)
        time.sleep(3)

    print("\n✅ Transcription finished.")
    return output_transcript

def get_whisper_pids():
    """Return a list of all running whisper-cli process PIDs."""
    return [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if "whisper-cli" in p.info['name']]

def is_process_running(pid):
    """Check if a process with a given PID is still running."""
    return psutil.pid_exists(pid)

def highlight_finder(file_path):
    print("📂 Highlighting transcript in Finder...")
    subprocess.run(["open", "-R", file_path])

def main():
    print("🚀 Whisper Transcriber Started...")
    root = tk.Tk()
    root.withdraw()
    
    lang_choice = messagebox.askquestion("Language Selection", "Do you want the transcript in English? Click 'No' for Dutch.")
    language = "en" if lang_choice == "yes" else "nl"
    print(f"✅ Selected Language: {language}")
    
    file_path = select_file()
    
    print("🎵 Converting file to 16kHz WAV format... Please wait.")
    wav_file = convert_to_wav(file_path)
    
    print("📝 Starting transcription....")
    transcript_file = transcribe(wav_file, language)
    
    print("🔍 Transcription done! Opening Finder...")
    highlight_finder(transcript_file)
    print("🎉 Process complete! Transcription is ready.")

if __name__ == "__main__":
    main()
