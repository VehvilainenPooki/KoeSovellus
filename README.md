# KoeSovellus 2.0
Tämä on versio 2.0 aloittamastani kurssin TiKaWe projektista. Alkuperäinen projekti löytyy haarasta version1.
Verkkosovellus, jossa voi luoda kokeita, suorittaa kokeita ja tarkistaa kokeita.

## Sovelluksen kokeileminen WIP
Sovellus on kirjoitettu Python 3.11 ja SQlite 3.51. Sinulla tulee olla asennettuna ne. Jotkin muut versiot saattavat toimia myös.

asennus:
- lataa sovellus
- navigoi terminaalissa juuri kansioon
- asenna Flask
```
\> pip install Flask
```
- Alusta tietokanta
```
\> sqlite3 database.db < schema.sql
```
- Navigoi source kansioon
```
\> cd .\source\
```
- käynnistä sovellus
```
\source\> flask run
```

Sovelluksessa on automaattisesti admin käyttäjä, jonka nimi on admin ja salasana on admin.

Juuri kansiossa on myös test_data.sql, jossa on 15 perus käyttäjää ja 3 admin käyttäjää. Nämä käyttäjät voi lisätä tietokantaan samalla komennolla kuin skeman:
```
\> sqlite3 database.db < test_data.sql
```
