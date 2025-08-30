from pytubefix import YouTube
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def download_video(url, dir, quality, only_audio=False, progress_callback=None):
    yt = YouTube(url, on_progress_callback=progress_callback)
    if only_audio:
        stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not stream:
            stream = yt.streams.filter(only_audio=True).first()
    else:
        if quality == "full":
            stream = yt.streams.get_highest_resolution()
        elif quality == "half":
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().filter(resolution="480p").first()
            if stream is None:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().filter(resolution="360p").first()
        elif quality == "low":
            stream = yt.streams.get_lowest_resolution()
        else:
            raise ValueError("Invalid quality. Choose 'full', 'half', or 'low'.")

    if stream:
        stream.download(output_path=dir)
    else:
        raise Exception(f"No stream found for the selected option.")

def start_gui():
    def browse_directory():
        dir_selected = filedialog.askdirectory()
        if dir_selected:
            dir_var.set(dir_selected)

    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent = int(bytes_downloaded / total_size * 100)
        progress_var.set(percent)
        progress_bar.update()

    def run_download():
        url = url_var.get().strip()
        directory = dir_var.get().strip()
        quality = quality_var.get().strip().lower()
        only_audio = audio_var.get()
        try:
            download_video(url, directory, quality, only_audio, progress_callback=on_progress)
            messagebox.showinfo("Success", f"Downloaded {'audio' if only_audio else 'video'} to {directory}")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")
        finally:
            progress_var.set(0)
            progress_bar.update()
            download_btn.config(state="normal")

    def on_download():
        url = url_var.get().strip()
        directory = dir_var.get().strip()
        quality = quality_var.get().strip().lower()
        only_audio = audio_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        if not directory:
            messagebox.showerror("Error", "Please select a download directory.")
            return
        download_btn.config(state="disabled")
        threading.Thread(target=run_download, daemon=True).start()

    root = tk.Tk()
    root.title("YouTube Video Downloader")

    tk.Label(root, text="YouTube URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    url_var = tk.StringVar()
    tk.Entry(root, textvariable=url_var, width=40).grid(row=0, column=1, padx=5, pady=5, columnspan=2)

    tk.Label(root, text="Download Directory:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    dir_var = tk.StringVar()
    tk.Entry(root, textvariable=dir_var, width=30).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=browse_directory).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(root, text="Quality:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    quality_var = tk.StringVar(value="full")
    quality_menu = ttk.Combobox(root, textvariable=quality_var, values=["full", "half", "low"], state="readonly", width=10)
    quality_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    audio_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Download audio only", variable=audio_var).grid(row=2, column=2, padx=5, pady=5, sticky="w")

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)
    progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    download_btn = tk.Button(root, text="Download", command=on_download, width=20)
    download_btn.grid(row=4, column=0, columnspan=3, pady=15)

    root.mainloop()

if __name__ == "__main__":
    start_gui()






