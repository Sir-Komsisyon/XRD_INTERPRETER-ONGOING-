import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from digitizer import digitize_image
from matcher import load_reference_patterns, match_pattern


class XRDMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XRD Pattern Matcher")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")

        self.input_two_theta = None
        self.input_intensity = None
        self.reference_patterns = load_reference_patterns("database")

        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="XRD Pattern Matcher",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        title.pack(pady=15)

        # Upload button
        upload_btn = tk.Button(
            self.root,
            text="Upload XRD Image",
            command=self.upload_image,
            font=("Helvetica", 12),
            bg="#89b4fa",
            fg="#1e1e2e",
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        upload_btn.pack(pady=5)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="No image loaded",
            font=("Helvetica", 10),
            bg="#1e1e2e",
            fg="#6c7086"
        )
        self.status_label.pack(pady=5)

        # Axis range inputs
        range_frame = tk.Frame(self.root, bg="#1e1e2e")
        range_frame.pack(pady=5)

        tk.Label(range_frame, text="2θ Min:", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        self.x_min_entry = tk.Entry(range_frame, width=6,
                                    font=("Helvetica", 10))
        self.x_min_entry.insert(0, "10")
        self.x_min_entry.grid(row=0, column=1, padx=5)

        tk.Label(range_frame, text="2θ Max:", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Helvetica", 10)).grid(row=0, column=2, padx=5)
        self.x_max_entry = tk.Entry(range_frame, width=6,
                                    font=("Helvetica", 10))
        self.x_max_entry.insert(0, "80")
        self.x_max_entry.grid(row=0, column=3, padx=5)

        # Match button
        match_btn = tk.Button(
            self.root,
            text="Find Matches",
            command=self.run_matching,
            font=("Helvetica", 12),
            bg="#a6e3a1",
            fg="#1e1e2e",
            padx=20,
            pady=8,
            relief="flat",
            cursor="hand2"
        )
        match_btn.pack(pady=10)

        # Plot area
        self.figure, self.ax = plt.subplots(figsize=(8, 3))
        self.figure.patch.set_facecolor("#1e1e2e")
        self.ax.set_facecolor("#313244")
        self.ax.tick_params(colors="#cdd6f4")
        self.ax.spines["bottom"].set_color("#6c7086")
        self.ax.spines["left"].set_color("#6c7086")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.set_xlabel("2θ (degrees)", color="#cdd6f4")
        self.ax.set_ylabel("Intensity", color="#cdd6f4")
        self.ax.set_title("XRD Pattern", color="#cdd6f4")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(pady=5, fill="x", padx=20)

        # Results box
        results_label = tk.Label(
            self.root,
            text="Top Matches:",
            font=("Helvetica", 11, "bold"),
            bg="#1e1e2e",
            fg="#cdd6f4"
        )
        results_label.pack(pady=(10, 2))

        self.results_text = tk.Text(
            self.root,
            height=6,
            font=("Courier", 10),
            bg="#313244",
            fg="#cdd6f4",
            relief="flat",
            padx=10,
            pady=5
        )
        self.results_text.pack(fill="x", padx=20, pady=5)

    def upload_image(self):
        filepath = filedialog.askopenfilename(
            title="Select XRD Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )

        if not filepath:
            return

        try:
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())

            self.input_two_theta, self.input_intensity = digitize_image(
                filepath, x_min=x_min, x_max=x_max
            )

            # Plot the extracted curve
            self.ax.clear()
            self.ax.set_facecolor("#313244")
            self.ax.plot(self.input_two_theta, self.input_intensity,
                         color="#89b4fa", linewidth=1.2)
            self.ax.set_xlabel("2θ (degrees)", color="#cdd6f4")
            self.ax.set_ylabel("Intensity", color="#cdd6f4")
            self.ax.set_title("Extracted XRD Pattern", color="#cdd6f4")
            self.ax.tick_params(colors="#cdd6f4")
            self.canvas.draw()

            self.status_label.config(
                text=f"Loaded: {filepath.split('/')[-1]}",
                fg="#a6e3a1"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def run_matching(self):
        if self.input_two_theta is None:
            messagebox.showwarning("No Image", "Please upload an XRD image first.")
            return

        if not self.reference_patterns:
            messagebox.showwarning("No Database",
                                   "No reference patterns found in database/ folder.")
            return

        matches = match_pattern(
            self.input_two_theta,
            self.input_intensity,
            self.reference_patterns,
            top_n=5
        )

        # Display results
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, f"{'Rank':<6}{'Phase Name':<40}{'Score'}\n")
        self.results_text.insert(tk.END, "-" * 55 + "\n")

        for i, match in enumerate(matches, 1):
            line = f"{i:<6}{match['name']:<40}{match['score']:.4f}\n"
            self.results_text.insert(tk.END, line)


if __name__ == "__main__":
    root = tk.Tk()
    app = XRDMatcherApp(root)
    root.mainloop()
