from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.registry import ConversionRequest, execute, available_targets, REGISTRY
import converters  

class ConverterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Konwerter plikow")
        self.root.resizable(False, False)

        self.source_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.target_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        # Plik zrodlowy
        ttk.Label(frame, text="Plik zrodlowy:").grid(row=0, column=0, sticky="w", pady=(0, 4))
        ttk.Entry(frame, textvariable=self.source_var, width=52).grid(row=1, column=0, sticky="we", pady=(0, 8))
        ttk.Button(frame, text="Wybierz plik...", command=self._choose_source).grid(row=1, column=1, padx=(8, 0), pady=(0, 8))

        # Katalog docelowy
        ttk.Label(frame, text="Katalog docelowy:").grid(row=2, column=0, sticky="w", pady=(0, 4))
        ttk.Entry(frame, textvariable=self.output_dir_var, width=52).grid(row=3, column=0, sticky="we", pady=(0, 8))
        ttk.Button(frame, text="Wybierz katalog...", command=self._choose_output_dir).grid(row=3, column=1, padx=(8, 0), pady=(0, 8))

        # Format docelowy
        ttk.Label(frame, text="Format docelowy:").grid(row=4, column=0, sticky="w", pady=(0, 4))
        self.target_combo = ttk.Combobox(
            frame,
            textvariable=self.target_var,
            width=50,
            state="readonly",
        )
        self.target_combo.grid(row=5, column=0, columnspan=2, sticky="we", pady=(0, 12))
        self.target_combo.bind("<<ComboboxSelected>>", lambda _e: self._update_convert_state())

        # Przycisk konwersji
        self.convert_btn = ttk.Button(frame, text="Konwertuj", command=self._convert)
        self.convert_btn.grid(row=6, column=0, columnspan=2, pady=(0, 8))
        self._update_convert_state()

        # Status
        self.status_var = tk.StringVar(value="Gotowy.")
        status = ttk.Label(frame, textvariable=self.status_var, foreground="#555555")
        status.grid(row=7, column=0, columnspan=2, sticky="w")

        frame.columnconfigure(0, weight=1)

    def _choose_source(self) -> None:
        path = filedialog.askopenfilename(
            title="Wybierz plik do konwersji",
            filetypes=[("Wszystkie pliki", "*.*")],
        )
        if not path:
            return
        self.source_var.set(path)
        self._refresh_targets(Path(path))

    def _choose_output_dir(self) -> None:
        path = filedialog.askdirectory(title="Wybierz katalog docelowy")
        if path:
            self.output_dir_var.set(path)
        self._update_convert_state()

    def _refresh_targets(self, source: Path) -> None:
        targets = available_targets(source)
        self.target_combo["values"] = targets
        if targets:
            self.target_var.set(targets[0])
        else:
            self.target_var.set("")
        self._update_convert_state()
        if not targets:
            self.status_var.set(f"Brak obslugiwanych formatow docelowych dla {source.suffix or '(brak rozszerzenia)'}.")
        else:
            self.status_var.set(f"Dostępne cele: {', '.join(targets)}")

    def _update_convert_state(self) -> None:
        source = Path(self.source_var.get()) if self.source_var.get() else None
        output_dir = Path(self.output_dir_var.get()) if self.output_dir_var.get() else None
        target = self.target_var.get().strip()
        enabled = bool(source and source.is_file() and output_dir and output_dir.is_dir() and target)
        self.convert_btn.state(["!disabled"] if enabled else ["disabled"])

    def _convert(self) -> None:
        source = Path(self.source_var.get())
        output_dir = Path(self.output_dir_var.get())
        target_format = self.target_var.get().strip().lower()

        if not source.is_file():
            messagebox.showerror("Blad", "Wybierz poprawny plik zrodlowy.")
            return
        if not output_dir.is_dir():
            messagebox.showerror("Blad", "Wybierz poprawny katalog docelowy.")
            return
        if not target_format:
            messagebox.showerror("Blad", "Wybierz format docelowy.")
            return

        key = (source.suffix.lower(), target_format)
        if key not in REGISTRY:
            messagebox.showerror(
                "Niedozwolona para",
                f"Konwersja {source.suffix.lower()} -> {target_format} nie jest obslugiwana.",
            )
            return

        target_path = output_dir / f"{source.stem}{target_format}"
        if target_path.exists():
            answer = messagebox.askyesno(
                "Plik juz istnieje",
                f"Plik {target_path.name} juz istnieje w katalogu docelowym.\n"
                "Nadpisac go?",
                icon=messagebox.WARNING,
            )
            if not answer:
                self.status_var.set("Anulowano - plik nie zostal nadpisany.")
                return

        try:
            request = ConversionRequest(source, target_format, output_dir)
            result = execute(request)
            self.status_var.set(f"Sukces: zapisano {result.name}")
            messagebox.showinfo("Sukces", f"Plik zostal zapisany:\n{result}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Blad konwersji", str(exc))
            self.status_var.set(f"Blad: {exc}")


def main() -> None:
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
