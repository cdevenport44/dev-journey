

import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox
from PIL import Image, ImageTk
import segno
import os

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")
        self.qr_image = None

        # Default values
        self.scale = tk.IntVar(value=5)
        self.border = tk.IntVar(value=2)
        self.dark_color = "#000000"
        self.light_color = "#ffffff"
        self.output_format = tk.StringVar(value="png")

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Input Text or URL:").pack(pady=5)
        self.text_entry = tk.Entry(self.root, width=50)
        self.text_entry.pack(pady=5)

        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Scale:").grid(row=0, column=0)
        tk.Entry(settings_frame, textvariable=self.scale, width=5).grid(row=0, column=1)

        tk.Label(settings_frame, text="Border:").grid(row=0, column=2)
        tk.Entry(settings_frame, textvariable=self.border, width=5).grid(row=0, column=3)

        tk.Label(settings_frame, text="Format:").grid(row=0, column=4)
        ttk.Combobox(settings_frame, textvariable=self.output_format, values=["png", "svg", "pdf"], width=5).grid(row=0, column=5)

        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=5)

        tk.Button(color_frame, text="Dark Color", command=self.choose_dark_color).pack(side="left", padx=10)
        tk.Button(color_frame, text="Light Color", command=self.choose_light_color).pack(side="left", padx=10)

        tk.Button(self.root, text="Generate QR Code", command=self.generate_qr).pack(pady=10)
        tk.Button(self.root, text="Save QR Code", command=self.save_qr).pack(pady=5)

        self.qr_preview = tk.Label(self.root, text="QR Preview will appear here", padx=10, pady=10)
        self.qr_preview.pack(pady=20)

    def choose_dark_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.dark_color = color

    def choose_light_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.light_color = color

    def generate_qr(self):
        data = self.text_entry.get().strip()
        if not data:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        try:
            qr = segno.make(data, error='h')
            qr.save("temp_preview.png",
                    scale=self.scale.get(),
                    border=self.border.get(),
                    dark=self.dark_color,
                    light=self.light_color,
                    kind='png')

            img = Image.open("temp_preview.png")
            img = img.resize((250, 250))
            self.qr_image = ImageTk.PhotoImage(img)
            self.qr_preview.configure(image=self.qr_image, text="")

        except Exception as e:
            messagebox.showerror("QR Error", str(e))

    def save_qr(self):
        data = self.text_entry.get().strip()
        if not data:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        file = filedialog.asksaveasfilename(defaultextension=f".{self.output_format.get()}",
                                            filetypes=[("Image", f"*.{self.output_format.get()}")])
        if not file:
            return

        try:
            qr = segno.make(data, error='h')
            qr.save(file,
                    scale=self.scale.get(),
                    border=self.border.get(),
                    dark=self.dark_color,
                    light=self.light_color,
                    kind=self.output_format.get())
            messagebox.showinfo("Saved", f"QR code saved to {file}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()


