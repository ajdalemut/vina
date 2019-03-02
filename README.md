# Vina
## Projektna naloga za Programiranje 1 
Analizirala bom vsa vina (Red, White, Rose) količine 750ml (standardna velikost steklenice) iz spletne strani:
[winelibrary](https://winelibrary.com/search?color[]=Red&color[]=White&color[]=Rose&page=1&size[]=750ML)

**Za vsako vino bom zajela:**
* Id number (številko izdelka)
* Full name (celotno ime)
* Price (ceno)
* Country (državo)
* Region (regijo)
* Rating (oceno)
* Vintage (letnik)
* Color (barvo)
* ABV (alkohol)
* Closure (zaprtje)
* Taste (okus)
* Nose (vonj)

**Analiza:**
* Katera so najdraža in najcenejša vina?
* Katere države imajo najdrazja vina?
* Katera barva vina je najdrazja? (predvideno bodo najdrazja rdeca)
* Katero vino ima najvišjo vsebovanost alkohola?
* Katere države imajo vina z najvišjo vsebovanostjo alkohola?
* Ali je vsebovanost alkohola povezana s ceno? (predvidoma ne)
* Kako sta okus in vonj povezana z barvo in zaprtjem?
* Ali so letniki vin povezani z ceno vina? (v splošnem ja, vendar gre lahko za neopazno majhne razlike)
* Ali je cena povezana z oceno vina? 
* Ali je cena povezana z zaprtjem vina? (predvidevam, da bodo drazja vina z 'Cork' zaprtjem)

**Kaj vsebujejo datoteke?**
* datoteka *orodja.py* vsebuje nekaj pomožnih funkcij za shranjevanje podatkov iz urljev
* datoteka *zajem_podatkov.py* vsebuje vzorce podatkov in funkcije ki te podatke shranijo v html, csv in json obliki
* datoteka *vina.csv* vsebuje tabelo podatkov o številkah, imenih, cenah, drzavah, regijah, ocenah, letnikih, barvah, alkoholih in zaprtjih izdelkov
* datoteka *okusi.csv* vsebuje tabelo z stevilko vina in okusom vina
* datoteka *vonji.csv* vsebuje tabelo z stevilko vina in vonjem vina
Datoteke so dobljene z pogonom datoteke *zajem_podatkov.py* vendar so vse dobljene mape že vključene v repozitorij, saj lahko njihov zajem traja nekoliko dlje.
Zadnje tri datoteke so vsebovane v mapi obdelani-podatki.
