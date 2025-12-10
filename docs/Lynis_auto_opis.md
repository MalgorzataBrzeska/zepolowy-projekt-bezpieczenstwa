## Cel projektu

Celem było zautomatyzowanie testów Lynis, który wykonywaliśmy wcześniej.
Poprzednio audyt wykonywany był ręcznie poleceniem sudo lynis audit system, wyniki musiały być analizowane ręczenie.
Aktualnie proces ten został zautomatyzowany za pomocą skryptu w Pythonie.

## Co wykonuje skrypt
1. uruchamia Lynis automatycznie
2. mierzy czas audytu
3. zapisuje pełny raport TXT
4. generuje podsumowanie w CSV
5. pobiera liczbę ostrzeżeń z /var/log/lynis-report.dat
6. zapisuje wszystko w katalogu Wyniki_Lynis_auto/
7. tworzy unikalne nazwy raportów z datą i godziną

## Wyniki czasowe

Aktualnie cały proces trwa max 3 min i generowany jest cały raport bez udziału człowieka. Gdy robiliśmy to ręcznie czas znacznie się wydłużał przez to ze wyniki musieliśmy analizować sami.