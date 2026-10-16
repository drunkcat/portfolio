# Wyszukiwarka odpowiedzi o ubezpieczeniu domu i mieszkania

## Krok 1. Zakres pierwszej wersji

### Cel

Użytkownik wpisuje pytanie po polsku, a aplikacja wyszukuje najbardziej pasujące fragmenty w publicznych materiałach edukacyjnych. Wynik pokazuje fragment odpowiedzi wraz z tytułem źródła, linkiem i — w przypadku PDF — numerem strony.

Pierwsza wersja będzie wyszukiwarką fragmentów, bez generowania odpowiedzi przez model językowy. Jeśli nie znajdzie dobrego dopasowania, powinna jasno powiedzieć, że nie znalazła odpowiedzi w zebranych materiałach.

### Tematy objęte zakresem

- suma ubezpieczenia oraz niedoubezpieczenie i nadubezpieczenie;
- elementy domu lub mieszkania, które można ubezpieczyć;
- zakres ochrony, w tym powódź, zalanie i typowe wyłączenia;
- pierwsze działania po szkodzie w domu, np. dokumentacja uszkodzeń;
- postępowanie, gdy proponowana kwota odszkodowania wydaje się za niska.

### Tematy poza zakresem

- wyliczanie składki i porównywanie ofert konkretnych ubezpieczycieli;
- interpretacja indywidualnej polisy lub OWU;
- rekomendowanie produktu ubezpieczeniowego;
- rozstrzyganie sporów prawnych oraz podawanie terminów jako aktualnej porady prawnej;
- ubezpieczenia komunikacyjne, na życie, zdrowotne i podróżne.

### Pytania do sprawdzenia wyszukiwarki

1. Co oznacza suma ubezpieczenia?
2. Czym różni się niedoubezpieczenie od nadubezpieczenia?
3. Jakie elementy mieszkania lub domu można objąć ubezpieczeniem?
4. Czy powódź zawsze jest objęta polisą mieszkaniową?
5. Czym różni się powódź od zalania w kontekście polisy?
6. Jaką sumę ubezpieczenia ustalić dla ruchomości domowych?
7. Co zrobić bezpośrednio po szkodzie spowodowanej wichurą?
8. Czy trzeba czekać z naprawą do przyjazdu rzeczoznawcy?
9. Co zrobić, jeśli odszkodowanie wydaje się za niskie?
10. Czy wyszukiwarka potrafi wyliczyć składkę dla mojego mieszkania? — pytanie poza zakresem; oczekiwany wynik to informacja o braku takich danych.

## Krok 2. Źródła materiałów

Wybrane zostały krótkie, publiczne materiały Rzecznika Finansowego. Oba dotyczą ubezpieczeń mieszkaniowych, a pierwszy jest poradnikiem w układzie pytań i odpowiedzi. Do prototypu należy pobrać lub odczytać wyłącznie potrzebną treść i zachować metadane źródła. Nie kopiować do repozytorium elementów strony, takich jak menu, banery ani treści niezwiązanych z poradnikiem.

| ID | Źródło | Zakres przydatny w projekcie | Format i uwagi |
|---|---|---|---|
| RF-HOME-2026 | [Ubezpieczenia mieszkaniowe. Jak się dobrze ubezpieczyć?](https://rf.gov.pl/wp-content/uploads/2026/01/Poradnik_Ubezpieczenia-mieszkaniowe-1.pdf) | Suma ubezpieczenia, niedoubezpieczenie, wartość mienia, zakres ochrony i typowe wyłączenia. | PDF, 21 stron, styczeń 2026. Tekst jest możliwy do odczytania i zachowuje numerację stron. Główne źródło prototypu. |
| RF-STORM-2022 | [Odszkodowania po wichurach w pytaniach i odpowiedziach](https://rf.gov.pl/odszkodowania-po-wichurach-w-pytaniach-i-odpowiedziach/) | Zabezpieczenie mienia, dokumentowanie szkody, kontakt z ubezpieczycielem, wycena i kwestionowanie odszkodowania. | Strona HTML, 22 lutego 2022. Q&A łatwo podzielić według pytań. Informacje o terminach trzeba traktować jako potencjalnie nieaktualne i nie używać ich jako porady prawnej. |

### Ewidencja źródeł

Przy każdym wczytanym dokumencie zachować co najmniej:

- `source_id` — identyfikator z tabeli;
- tytuł, instytucję i oryginalny URL;
- datę publikacji (jeśli jest podana) oraz datę pobrania;
- numer strony PDF lub nagłówek/pytanie źródłowe dla strony HTML;
- tekst fragmentu wykorzystanego przez wyszukiwarkę.

Treść źródeł może się zmienić lub zostać przeniesiona. W prototypie należy pokazywać link do oryginału, a wyniki opisywać jako wyszukane informacje edukacyjne, nie indywidualną poradę ubezpieczeniową lub prawną.
