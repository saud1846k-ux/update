from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox

from .codec import decode_base64, encode_base64

AUTHOR_NAME = "MYERS502"
APP_TITLE = f"{AUTHOR_NAME} - Base64 Codec Tool"


class Myers502CodecApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("780x580")
        self.minsize(650, 480)
        self.configure(bg="#111317")

        self.mode_var = tk.StringVar(value="auto")
        self.status_var = tk.StringVar(value=f"Ready  |  Created by {AUTHOR_NAME}")

        self._build_ui()
        self._bind_shortcuts()

    def _build_ui(self) -> None:
        top_banner = tk.Frame(self, bg="#181c24", pady=12, padx=16)
        top_banner.pack(fill="x")

        tk.Label(
            top_banner,
            text=AUTHOR_NAME,
            font=("Segoe UI", 24, "bold"),
            fg="#38bdf8",
            bg="#181c24",
        ).pack(side="left")

        tk.Label(
            top_banner,
            text="Base64 Encoder & Decoder\nUTF-8  /  PowerShell UTF-16LE",
            font=("Segoe UI", 10, "bold"),
            fg="#e5e7eb",
            bg="#181c24",
            justify="right",
        ).pack(side="right")

        controls = tk.Frame(self, bg="#111317", padx=16, pady=8)
        controls.pack(fill="x")

        tk.Label(
            controls,
            text="Mode:",
            font=("Segoe UI", 10, "bold"),
            fg="#d1d5db",
            bg="#111317",
        ).pack(side="left", padx=(0, 8))

        for label, val in [
            ("Auto (Decode)", "auto"),
            ("UTF-8", "utf8"),
            ("PowerShell (UTF-16LE)", "ps"),
        ]:
            tk.Radiobutton(
                controls,
                text=label,
                variable=self.mode_var,
                value=val,
                font=("Segoe UI", 9),
                fg="#f3f4f6",
                bg="#111317",
                selectcolor="#1f2937",
                activebackground="#111317",
                activeforeground="#ffffff",
            ).pack(side="left", padx=6)

        tk.Label(
            self,
            text=f"Input ({AUTHOR_NAME}):",
            font=("Segoe UI", 10, "bold"),
            fg="#e5e7eb",
            bg="#111317",
            anchor="w",
        ).pack(fill="x", padx=16, pady=(4, 2))

        self.input_box = tk.Text(
            self,
            height=8,
            font=("Consolas", 10),
            bg="#1b2029",
            fg="#f9fafb",
            insertbackground="#ffffff",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.input_box.pack(fill="both", expand=True, padx=16)

        btn_bar = tk.Frame(self, bg="#111317", padx=16, pady=10)
        btn_bar.pack(fill="x")

        btn_style = {
            "font": ("Segoe UI", 9, "bold"),
            "relief": "flat",
            "padx": 12,
            "pady": 6,
            "cursor": "hand2",
        }

        tk.Button(
            btn_bar, text="Decode", bg="#2563eb", fg="white", command=self.on_decode, **btn_style
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            btn_bar, text="Encode UTF-8", bg="#059669", fg="white", command=self.on_encode_utf8, **btn_style
        ).pack(side="left", padx=6)

        tk.Button(
            btn_bar, text="Encode PowerShell", bg="#7c3aed", fg="white", command=self.on_encode_ps, **btn_style
        ).pack(side="left", padx=6)

        tk.Button(
            btn_bar, text="Copy", bg="#374151", fg="white", command=self.on_copy, **btn_style
        ).pack(side="right", padx=(6, 0))

        tk.Button(
            btn_bar, text="Save", bg="#374151", fg="white", command=self.on_save, **btn_style
        ).pack(side="right", padx=6)

        tk.Button(
            btn_bar, text="Clear", bg="#991b1b", fg="white", command=self.on_clear, **btn_style
        ).pack(side="right", padx=6)

        tk.Label(
            self,
            text=f"Output ({AUTHOR_NAME}):",
            font=("Segoe UI", 10, "bold"),
            fg="#e5e7eb",
            bg="#111317",
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 2))

        self.output_box = tk.Text(
            self,
            height=8,
            font=("Consolas", 10),
            bg="#1b2029",
            fg="#34d399",
            insertbackground="#ffffff",
            relief="flat",
            padx=8,
            pady=8,
        )
        self.output_box.pack(fill="both", expand=True, padx=16)

        footer = tk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 9, "bold"),
            fg="#9ca3af",
            bg="#181c24",
            anchor="w",
            padx=16,
            pady=6,
        )
        footer.pack(fill="x", pady=(10, 0))

    def _bind_shortcuts(self) -> None:
        for widget in (self.input_box, self.output_box):
            menu = tk.Menu(widget, tearoff=0, bg="#1f2937", fg="#f9fafb")
            menu.add_command(label="Paste", command=lambda w=widget: self._paste_into_widget(w))
            menu.add_command(label="Copy", command=lambda w=widget: w.event_generate("<<Copy>>"))
            menu.add_command(label="Select All", command=lambda w=widget: w.tag_add("sel", "1.0", "end"))
            widget.bind("<Button-3>", lambda e, m=menu: m.tk_popup(e.x_root, e.y_root))

        self.input_box.bind("<Control-v>", lambda e: self._paste_into_widget(self.input_box))
        self.input_box.bind("<Control-V>", lambda e: self._paste_into_widget(self.input_box))
        self.input_box.bind("<Shift-Insert>", lambda e: self._paste_into_widget(self.input_box))

    def _paste_into_widget(self, widget: tk.Text) -> str:
        try:
            clip_text = self.clipboard_get()
            if clip_text:
                widget.insert(tk.INSERT, clip_text)
        except tk.TclError:
            pass
        return "break"

    def _set_output(self, text: str, status: str) -> None:
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert("1.0", text)
        self.status_var.set(f"{status}  |  {AUTHOR_NAME}")

    def on_decode(self) -> None:
        raw = self.input_box.get("1.0", tk.END).strip()
        if not raw:
            return
        try:
            res = decode_base64(raw, mode=self.mode_var.get())
            self._set_output(res, f"Decoded ({self.mode_var.get()})")
        except Exception as exc:
            messagebox.showerror("Decode Error", str(exc))

    def on_encode_utf8(self) -> None:
        raw = self.input_box.get("1.0", tk.END).rstrip("\r\n")
        if not raw:
            return
        res = encode_base64(raw, mode="utf8")
        self._set_output(res, "Encoded (UTF-8)")

    def on_encode_ps(self) -> None:
        raw = self.input_box.get("1.0", tk.END).rstrip("\r\n")
        if not raw:
            return
        res = encode_base64(raw, mode="ps")
        self._set_output(res, "Encoded (PowerShell UTF-16LE)")

    def on_copy(self) -> None:
        out = self.output_box.get("1.0", tk.END).rstrip("\r\n")
        if not out:
            return
        self.clipboard_clear()
        self.clipboard_append(out)
        self.status_var.set(f"Copied to clipboard  |  {AUTHOR_NAME}")

    def on_save(self) -> None:
        out = self.output_box.get("1.0", tk.END).rstrip("\r\n")
        if not out:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="myers502_output.txt",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(out)
            self.status_var.set(f"Saved: {path}  |  {AUTHOR_NAME}")

    def on_clear(self) -> None:
        self.input_box.delete("1.0", tk.END)
        self.output_box.delete("1.0", tk.END)
        self.status_var.set(f"Cleared  |  {AUTHOR_NAME}")