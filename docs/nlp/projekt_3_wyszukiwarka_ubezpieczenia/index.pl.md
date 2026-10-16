# Wyszukiwarka odpowiedzi o ubezpieczeniu

Prosta aplikacja Streamlit wyszukująca informacje w dwóch publicznych materiałach Rzecznika Finansowego o ubezpieczeniu domu i szkodach po wichurach. TF-IDF szereguje pasujące fragmenty tekstu; dla poradnika PDF aplikacja pokazuje również numer strony.

Aplikacja nie generuje odpowiedzi ani nie udziela indywidualnej porady ubezpieczeniowej lub prawnej.

## Wersja online

[Otwórz aplikację w Streamlit](https://gmarkowski-nlpwyszukiwarkaodpowiedzi.streamlit.app/).

## Uruchomienie lokalne

W tym folderze zainstaluj zależności i uruchom Streamlit:

    python -m pip install -r requirements.txt
    streamlit run app.py

Dwa pliki źródłowe muszą pozostać w tym folderze obok `app.py`.
