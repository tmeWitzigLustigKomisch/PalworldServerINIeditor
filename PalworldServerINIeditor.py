import configparser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class SettingsEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Palworld Server INI Einstellungseditor")
        self.master.geometry("600x800")  # Größere Standardstartgröße

        self.entries = {}

        # Rahmen für die Einstellungen erstellen
        settings_frame = ttk.Frame(master)
        settings_frame.pack(fill=tk.BOTH, expand=True)

        # Leinwand mit einer Scrollleiste erstellen
        self.canvas = tk.Canvas(settings_frame)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Rahmen innerhalb der Leinwand erstellen
        self.settings_frame = ttk.Frame(self.canvas)
        self.settings_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.settings_frame, anchor="nw")

        # Button zum Laden der INI-Datei
        load_button = tk.Button(master, text="INI-Datei laden", command=self.load_ini_file)
        load_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Button zum Speichern der Einstellungen
        save_button = tk.Button(master, text="Speichern", command=self.save_settings)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Mausradevent an die Leinwand binden
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Info-Button hinzufügen
        info_button = tk.Button(master, text="Info", command=self.show_info)
        info_button.pack(side=tk.LEFT, padx=5, pady=5)

    def load_ini_file(self):
        # Dateibrowser öffnen, um die INI-Datei auszuwählen
        file_path = filedialog.askopenfilename(initialfile="PalWorldSettings.ini", filetypes=[("INI-Dateien", "*.ini")])
        if file_path:
            self.load_ini_settings(file_path)

    def load_ini_settings(self, file_path):
        # Konfigurationsdatei einlesen
        self.config = configparser.ConfigParser()
        self.config.read(file_path)
        self.settings = self.config['/Script/Pal.PalGameWorldSettings']

        # Einstellungen zum Rahmen hinzufügen
        self.add_settings_to_frame()

    def add_settings_to_frame(self):
        # Optionseinstellungen aus der Konfiguration extrahieren
        option_settings = self.settings["OptionSettings"]
        options_list = option_settings.strip()[1:-1].split(",")
        for i, option in enumerate(options_list):
            setting, value = option.strip().split("=")
            label = ttk.Label(self.settings_frame, text=setting)
            label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(self.settings_frame)
            entry.insert(0, str(value))
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="we")
            self.entries[setting] = entry

    def save_settings(self):
        # Aktualisierte Einstellungen sammeln und in die Konfiguration schreiben
        option_settings = []
        for setting, entry in self.entries.items():
            value = entry.get()
            option_settings.append(f"{setting}={value}")

        self.settings["OptionSettings"] = "(" + ",".join(option_settings) + ")"

        # Konfigurationsdatei speichern
        with open("PalWorldSettings.ini", 'w') as configfile:
            self.config.write(configfile)

    def on_mousewheel(self, event):
        # Scrollen der Leinwand bei Mausradevent
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def show_info(self):
        # Info über den Entwickler und das Programm anzeigen
        info = "Entwickler: FleXcon\n\nTelegram: t.me/WitzigLustigKomisch\n\nDieses Programm ermöglicht das einfache bearbeiten von Palworld Server INI-Einstellungen."
        messagebox.showinfo("Info", info)


def main():
    # Hauptfenster erstellen und Anwendung starten
    root = tk.Tk()
    app = SettingsEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

