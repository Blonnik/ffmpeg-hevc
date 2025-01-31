import tkinter as tk
from tkinter import filedialog
import ffmpeg
import os

def select_input_file():
    file_path = filedialog.askopenfilename(title="Wybierz plik HEVC")
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(title="Wybierz lokalizację zapisu", defaultextension=".mp4", filetypes=[("Pliki MP4", "*.mp4")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def validate_output_file(output_file):
    if not output_file.lower().endswith(".mp4"):
        output_file += ".mp4"
    return output_file

def start_conversion():
    input_file = input_entry.get()
    output_file = output_entry.get()
    if not input_file or not output_file:
        result_label.config(text="Proszę wybrać pliki wejściowe i wyjściowe!")
        return

    output_file = validate_output_file(output_file)

    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vcodec='libx264', acodec='aac', preset='fast', crf=23)
            .run(overwrite_output=True)
        )
        result_label.config(text=f"Sukces! Plik zapisano jako: {output_file}")
    except ffmpeg.Error as e:
        result_label.config(text=f"Błąd: {e}")

root = tk.Tk()
root.title("Konwerter HEVC na H.264")

frame = tk.Frame(root)
frame.pack(pady=10)

input_label = tk.Label(frame, text="Plik wejściowy HEVC:")
input_label.grid(row=0, column=0, padx=5, pady=5)
input_entry = tk.Entry(frame, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
input_button = tk.Button(frame, text="Wybierz", command=select_input_file)
input_button.grid(row=0, column=2, padx=5, pady=5)

output_label = tk.Label(frame, text="Plik wyjściowy H.264:")
output_label.grid(row=1, column=0, padx=5, pady=5)
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
output_button = tk.Button(frame, text="Wybierz", command=select_output_file)
output_button.grid(row=1, column=2, padx=5, pady=5)

convert_button = tk.Button(root, text="Konwertuj", command=start_conversion)
convert_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
