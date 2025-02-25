import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import warnings
import time
import psutil
import re

# Suppress warnings and macOS Tk deprecation message
os.environ["TK_SILENCE_DEPRECATION"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)

CHUNK_DURATION = 1800  # 30 minutes in seconds

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
    """ Converts the input file to a single 16kHz WAV file. """
    output_file = os.path.splitext(input_file)[0] + "_16khz.wav"
    
    convert_cmd = [
        "ffmpeg", "-y",  # `-y` forces overwrite of existing files
        "-i", input_file,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_file
    ]
    
    subprocess.run(convert_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return output_file

def get_audio_duration(file_path):
    """ Returns the duration of the audio file in seconds. """
    result = subprocess.run(
        ["ffmpeg", "-i", file_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    lines = result.stderr.split("\n")
    for line in lines:
        if "Duration" in line:
            time_str = line.split(",")[0].split("Duration:")[1].strip()
            h, m, s = map(float, time_str.replace(":", " ").split())
            return int(h * 3600 + m * 60 + s)
    return 0

def split_audio(input_wav):
    """ Splits a long WAV file into 30-minute chunks if necessary. """
    duration = get_audio_duration(input_wav)
    
    if duration <= CHUNK_DURATION:
        return [input_wav]  # Return original file in a list

    output_files = []
    base_name = os.path.splitext(input_wav)[0]
    
    for i, start_time in enumerate(range(0, duration, CHUNK_DURATION)):
        chunk_file = f"{base_name}_part{i+1}_16khz.wav"
        output_files.append(chunk_file)
        
        split_cmd = [
            "ffmpeg", "-y", "-i", input_wav, "-ss", str(start_time),
            "-t", str(CHUNK_DURATION), "-c", "copy", chunk_file
        ]
        subprocess.run(split_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"✅ Split complete: {len(output_files)} parts created.")
    
    # Remove the original 16kHz file
    os.remove(input_wav)

    return output_files

def transcribe(file_path, language, part_num, total_parts):
    """ Runs whisper-cli on a given file and returns the transcript path. """
    output_transcript = os.path.splitext(file_path)[0] + "_transcription.txt"
    print(f"\n📝 Transcribing part {part_num} of {total_parts} in {language}...")

    # Get existing whisper-cli PIDs
    existing_pids = get_whisper_pids()

    whisper_cmd = f'osascript -e \'tell application "Terminal" to do script "whisper-cli -m ~/.whisper/medium.bin -l {language} -t 8 \\"{file_path}\\" | tee \\"{output_transcript}\\"; exit"\''
    
    # Start transcription in a new Terminal window and close it after completion
    subprocess.Popen(whisper_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2)  # Allow time for the process to start

    # Get new Whisper process PID
    new_pids = get_whisper_pids()
    whisper_pid = list(set(new_pids) - set(existing_pids))

    if whisper_pid:
        whisper_pid = whisper_pid[0]
    else:
        print(f"⚠️ Could not determine Whisper process ID for part {part_num}. Waiting based on output file.")

    # Monitor the Whisper process
    print("⏳ Transcription in progress...", end="", flush=True)
    
    while whisper_pid and is_process_running(whisper_pid):
        print(".", end="", flush=True)
        time.sleep(3)

    print(f"\n✅ Transcription for part {part_num} finished.")

    # Close the terminal window if the process completed
    os.system(f"osascript -e 'tell application \"Terminal\" to close front window'")

    return output_transcript

def get_whisper_pids():
    """ Returns a list of all running whisper-cli process PIDs. """
    return [p.info['pid'] for p in psutil.process_iter(attrs=['pid', 'name']) if "whisper-cli" in p.info['name']]

def is_process_running(pid):
    """ Checks if a process with a given PID is still running. """
    return psutil.pid_exists(pid)

def shift_timestamp(timestamp, offset_seconds):
    """ Shift a timestamp by a given offset in seconds. """
    h, m, s_ms = timestamp.split(":")
    if "," in s_ms:
        s, ms = map(float, s_ms.split(","))
    elif "." in s_ms:
        s, ms = map(float, s_ms.split("."))
    else:
        s, ms = float(s_ms), 0

    total_seconds = int(h) * 3600 + int(m) * 60 + s + offset_seconds

    new_h = int(total_seconds // 3600)
    new_m = int((total_seconds % 3600) // 60)
    new_s = int(total_seconds % 60)
    new_ms = round(ms)

    return f"{new_h:02}:{new_m:02}:{new_s:02},{new_ms:03}"  # Keep correct format

def adjust_transcript_timestamps(transcript_file):
    """ Adjust timestamps in the transcript file based on detected resets. """
    adjusted_lines = []
    timestamp_pattern = re.compile(r"(\d{2}:\d{2}:\d{2}[,.]\d{3})")  # Matches timestamps like 00:01:15,123 or 00:01:15.123
    offset_seconds = 0
    last_timestamp = 0  # Track last timestamp in seconds

    with open(transcript_file, "r") as file:
        lines = file.readlines()

    for line in lines:
        matches = timestamp_pattern.findall(line)
        for match in matches:
            h, m, s_ms = match.split(":")
            if "," in s_ms:
                s, ms = map(float, s_ms.split(","))
            elif "." in s_ms:
                s, ms = map(float, s_ms.split("."))
            else:
                s, ms = float(s_ms), 0

            current_seconds = int(h) * 3600 + int(m) * 60 + s

            # Check if timestamp reset (indicating a new part)
            if current_seconds < last_timestamp:
                offset_seconds += last_timestamp  # Increase offset

            adjusted_time = shift_timestamp(match, offset_seconds)

            line = line.replace(match, adjusted_time)
            last_timestamp = current_seconds  # Update last timestamp

        adjusted_lines.append(line)

    return adjusted_lines

def merge_transcripts(transcript_files, final_output):
    """ Merges transcript files without modifying timestamps initially. """

    with open(final_output, "w") as outfile:
        for transcript in sorted(transcript_files):
            with open(transcript, "r") as infile:
                outfile.writelines(infile.readlines() + ["\n"])

    # Clean up temporary transcript files
    for transcript in transcript_files:
        os.remove(transcript)

    adjusted_transcript = adjust_transcript_timestamps(final_output)
    with open(final_output, "w") as f:
        f.writelines(adjusted_transcript)


def highlight_finder(file_path):
    """ Opens the Finder and highlights the specified file. """
    subprocess.run(["open", "-R", file_path])

def main():
    print("🚀 Whisper Transcriber Started...")
    root = tk.Tk()
    root.withdraw()
    
    lang_choice = messagebox.askquestion("Language Selection", "Do you want the transcript in English? Click 'No' for Dutch.")
    language = "en" if lang_choice == "yes" else "nl"
    print(f"✅ Selected Language: {language}")
    
    file_path = select_file()
    
    wav_file = convert_to_wav(file_path)
    
    # Split if needed
    wav_files = split_audio(wav_file)
    
    transcript_files = []
    
    for idx, wav in enumerate(wav_files):
        transcript_files.append(transcribe(wav, language, idx + 1, len(wav_files)))
        os.remove(wav)  # Cleanup each WAV file after processing

    # Merge all transcript parts
    final_transcript = os.path.splitext(file_path)[0] + "_transcription.txt"
    merge_transcripts(transcript_files, final_transcript)
    
    print("🔍 Transcription done! Highlighting transcript in Finder...")
    highlight_finder(final_transcript)
    
    print("🎉 Process complete! Final transcription is ready.")

if __name__ == "__main__":
    main()
