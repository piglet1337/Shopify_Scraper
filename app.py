import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import excel
import os
import sys


class RedirectText:
    """Redirect print statements to Tkinter Text widget."""
    def __init__(self, text_widget):
        self.output_widget = text_widget

    def write(self, message):
        self.output_widget.insert(tk.END, message)
        self.output_widget.see(tk.END)  # Auto-scroll
        self.output_widget.update_idletasks()  # Force UI update

    def flush(self):
        pass  # Needed for compatibility with sys.stdout

def process_excel(input_path):
    try:
        df = excel.read_excel(input_path)
        output_path = input_path.replace(".xlsx", "_processed.xlsx")
        dataframes = excel.get_new_pd_dataframes(df)
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            dataframes[0].to_excel(writer, sheet_name='bucket7')
            dataframes[1].to_excel(writer, sheet_name='notBucket7')
            dataframes[2].to_excel(writer, sheet_name='failed')
        # df.to_excel(output_path, sheet_name='bucket7')
        return output_path

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")
        return None

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        output_path = process_excel(file_path)
        if output_path:
            messagebox.showinfo("Success", f"File processed successfully!\nSaved as: {output_path}")
            download_button.config(state=tk.NORMAL)  # Enable the download button
            global processed_file
            processed_file = output_path  # Store the processed file path

def download_file():
    if processed_file:
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if save_path:
            os.rename(processed_file, save_path)
            messagebox.showinfo("Download Complete", f"File saved as: {save_path}")

# Initialize Tkinter Window
root = tk.Tk()
root.title("Shopify Processor")
root.geometry("400x250")

# UI Elements
label = tk.Label(root, text="Upload an Excel file to process with a list of Domains", font=("Arial", 12))
label.pack(pady=10)

upload_button = tk.Button(root, text="Upload File", command=upload_file, font=("Arial", 12))
upload_button.pack(pady=10)

download_button = tk.Button(root, text="Download Processed File", command=download_file, font=("Arial", 12), state=tk.DISABLED)
download_button.pack(pady=10)

# Output Log Box
log_label = tk.Label(root, text="Process Output:", font=("Arial", 10))
log_label.pack(pady=5)

log_text = tk.Text(root, height=10, width=60)
log_text.pack(pady=5)
log_text.config(state=tk.NORMAL)  # Allow writing

# Redirect print output to the text widget
sys.stdout = RedirectText(log_text)

# Run the application
processed_file = None  # Store the processed file path
root.mainloop()