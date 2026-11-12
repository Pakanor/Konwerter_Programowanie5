# Uniwersalny Konwerter Plików

Projekt aplikacji desktopowej do konwersji plików między różnymi formatami, zrealizowany w ramach przedmiotu Programowanie V (Laboratoria 2-5).

## Cel

Aplikacja pozwala wybrać plik wejściowy, pokazuje wyłącznie dostępne dla niego formaty docelowe, wykonuje konwersję i zapisuje wynik we wskazanym katalogu. Interfejs graficzny zbudowany w Pythonie z biblioteką Tkinter/ttk.

## Wymagania

- Python 3.10+
- Biblioteki Python (z pliku `requirements.txt`):
  - `python-docx` — obsługa plików DOCX
  - `lxml` — zależność python-docx
  - `typing_extensions` — wsparcie typowania
- Narzędzie systemowe (nie jest to paczka Python):
  - `libreoffice` lub `soffice` — wymagane dla konwersji DOCX/ODT do PDF i ODT do TXT (tryb headless)

## Instalacja

1. Sklonuj repozytorium:
   ```
   git clone https://github.com/Pakanor/Konwerter_Programowanie5
   cd ProgramowanieV
   ```

2. Utwórz i aktywuj środowisko wirtualne:
   ```
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. Zainstaluj zależności Pythona:
   ```
   pip install -r requirements.txt
   ```

4. Zainstaluj LibreOffice (wymagane dla konwersji grupy C):
   - Debian/Ubuntu: `sudo apt-get install libreoffice`
   - Fedora: `sudo dnf install libreoffice`
   - Windows/macOS: pobierz z https://www.libreoffice.org/

## Uruchomienie

Uruchom aplikację z głównego katalogu projektu:

```
python main.py
```

Lub bezpośrednio moduł GUI:

```
python gui/main.py
```

Po uruchomieniu:
1. Kliknij „Wybierz plik…” i wskaż plik wejściowy.
2. Kliknij „Wybierz katalog…” i wskaż katalog docelowy.
3. Z rozwijanej listy wybierz format docelowy (dostępne opcje zależą od rozszerzenia pliku źródłowego).
4. Kliknij „Konwertuj”.
5. Wynik pojawi się w katalogu docelowym; o sukcesie lub błędzie poinformuje komunikat oraz pasek statusu.

## Obsługiwane funkcje

- Wybór pliku wejściowego i katalogu docelowego przez natywne okna dialogowe.
- Dynamiczna lista formatów docelowych zależna od rozszerzenia pliku źródłowego.
- Konwersja w tle (wątek roboczy) — okno nie zamraża się podczas dłuższej operacji.
- Blokada niedozwolonych par formatów (niedostępne opcje są ukryte w liście i dodatkowo walidowane).
- Potwierdzenie nadpisania istniejącego pliku docelowego.
- Komunikaty błędów i sukcesu w języku polskim.
- Obsługa polskich znaków (UTF-8).

## Macierz wspieranych par formatów

| Grupa | Źródło | Cel | Uwagi |
|-------|--------|-----|-------|
| A – dane strukturalne | `.csv` | `.json` | JSON jako tablica obiektów, UTF-8 |
| A – dane strukturalne | `.json` | `.csv` | Wymaga niepustej listy obiektów; nagłówki z kluczy pierwszego obiektu |
| B – tekst/dokument | `.txt` | `.docx` | Polskie znaki UTF-8, akapity |
| B – tekst/dokument | `.docx` | `.txt` | Ekstrakcja tekstu akapitów |
| C – dokument/PDF | `.docx` | `.pdf` | Wymaga LibreOffice (headless) |
| C – dokument/PDF | `.odt` | `.pdf` | Wymaga LibreOffice (headless) |
| C – dokument/PDF | `.odt` | `.txt` | Wymaga LibreOffice (headless, filtr Text) |

Łącznie: **7 kierunków konwersji** w 3 grupach.

## Zależności i źródła

- Python 3 + Tkinter (biblioteka standardowa)
- python-docx: https://python-docx.readthedocs.io/
- LibreOffice (headless): https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html
- Moduł subprocess: https://docs.python.org/3/library/subprocess.html

Kod został opracowany z wykorzystaniem asystenta AI (Kilo). Wykorzystany kod został zrozumiany i zweryfikowany; źródło narzędzia AI ujawnione zgodnie z wymaganiami projektu.


