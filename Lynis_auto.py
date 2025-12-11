import subprocess
import datetime
import os
import csv
import time
import re

# ─────────────────────────────────────────────
# Usunięcie kodów kolorów ANSI z Lynis
# ─────────────────────────────────────────────
def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# ─────────────────────────────────────────────
# Folder wyników
# ─────────────────────────────────────────────
BASE_DIR = "Wyniki_Lynis_auto"
os.makedirs(BASE_DIR, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
REPORT_DIR = f"{BASE_DIR}/{timestamp}"
os.makedirs(REPORT_DIR, exist_ok=True)

WYNIK_RAPORTU = f"{REPORT_DIR}/WYNIK_RAPORTU.txt"
PODSUMOWANIE = f"{REPORT_DIR}/PODSUMOWANIE.csv"

# ─────────────────────────────────────────────
# weryfikacja czy lynis jest dostępny
# ─────────────────────────────────────────────
def check_lynis():
    try:
        subprocess.run(["lynis", "--version"], check=True, stdout=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("[ERROR] Lynis nie jest zainstalowany!")
        print("Zainstaluj: sudo apt install lynis -y")
        return False

# ─────────────────────────────────────────────
# Audyt systemu z pomiarem czasu
# ─────────────────────────────────────────────
def run_audit():
    print("[INFO] Uruchamiam audyt Lynis...")

    start = time.time()

    result = subprocess.run(
        ["sudo", "lynis", "audit", "system"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    end = time.time()

    duration_seconds = end - start
    minutes = int(duration_seconds // 60)
    seconds = round(duration_seconds % 60, 2)
    duration = f"{minutes} min {seconds} sek"

    clean_output = clean_ansi(result.stdout)

    with open(WYNIK_RAPORTU, "w") as f:
        f.write(clean_output)

    print(f"[INFO] Zapisano pełny raport: {WYNIK_RAPORTU}")
    print(f"[INFO] Audyt trwał: {duration}")

    return clean_output, duration

# ─────────────────────────────────────────────
# Pobranie liczby ostrzeżeń
# ─────────────────────────────────────────────
def get_real_warnings():
    report_path = "/var/log/lynis-report.dat"
    warnings_count = 0

    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            for line in f:
                if line.startswith("warning="):
                    try:
                        warnings_count = int(line.split("=")[1].strip())
                    except:
                        pass
    return warnings_count

# ─────────────────────────────────────────────
# Wyciągnięcie najważniejszych danych
# ─────────────────────────────────────────────
def parse_summary(audit_output):
    summary = {}

    for line in audit_output.splitlines():

        if "Hardening index" in line:
            num = re.findall(r'\d+', line)
            if num:
                summary["Wskaźnik utwardzenia systemu"] = num[0]

        if "Tests performed" in line:
            num = re.findall(r'\d+', line)
            if num:
                summary["Liczba wykonanych testów"] = num[0]

        if "Suggestions" in line:
            num = re.findall(r'\d+', line)
            summary["Sugestie"] = num[0] if num else "0"

    summary["Ostrzeżenia"] = str(get_real_warnings())
    return summary

# ─────────────────────────────────────────────
# Zapis CSV
# ─────────────────────────────────────────────
def save_csv(summary, duration):
    with open(PODSUMOWANIE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nazwa parametru", "Wartość parametru"])

        for key, value in summary.items():
            writer.writerow([key, value])

        writer.writerow(["Czas wykonania audytu", duration])

    print(f"[INFO] Zapisano podsumowanie do CSV: {PODSUMOWANIE}")

# ─────────────────────────────────────────────
# Główna część programu
# ─────────────────────────────────────────────
if __name__ == "__main__":
    if not check_lynis():
        exit(1)

    audit_output, duration = run_audit()
    summary = parse_summary(audit_output)
    save_csv(summary, duration)

    print("[DONE] Automatyczny audyt Lynis zakończony.")
