# KoeSovellus
Verkkosovellus, jossa voi luoda kokeita, suorittaa kokeita ja tarkistaa kokeita.

## Toteutetut toiminnot:
### Keskeiset toiminnot
- Opettaja ja Oppilas käyttäjien luominen Eli user ja admin käyttäjä


Olen jäänyt jälkeen tämän projektion kanssa, mutta toivon, että seuraavilla parilla viikolla minulla on paljon aikaa tehdä projekti loppuun

## Tekemättömät toiminnot:
### Keskeiset toiminnot
- Kokeen luominen
- Kokeen tekeminen
- Kokeen arviointi
- Arvioinnin lukeminen

## Mahdollisia ominaisuuksia
- Kokeen alkamisen ajoittaminen
- Automaattisia tarkistuksia yksinkertaisille tehtäville
- Automaattinen pisteiden yhteen laskenta
- 

## Sovelluksen kokeileminen
Sovellus on kirjoitettu Python 3.11.4 ja PostgreSQL 16. Sinulla tulee olla asennettuna ne. Jotkin muut versiot saattavat toimia myös.

asennus:
- lataa sovellus
- navigoi terminaalissa juuri kansioon
- Luo venv
```
.\root\> python -m venv venv
```
- Aktivoi venv
Linux
```
.\root\> ./.venv/bin/activate
```
Windows
```
.\root\>./.venv/Scripts/activate
```
- asenna vaadittavat kirjastot
```
.\root\>pip install requirements.txt
```
Luo ohjelman juureen .env tiedosto ja lisää sinne
```
DATABASE_URL=<tietokannan-paikallinen-osoite> (esim. DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<user>)
SECRET_KEY=<salainen-avain> (esim. SECRET_KEY="BAD_SECRET_KEY")
```

Varmista, että sinulla on tyhjä public Schema

```
.\root\>psql -U <user> # Missä <user> on joko postgres tai muu luomasi psql käyttäjä
user=#DROP SCHEMA public CASCADE;
user=#CREATE SCHEMA public;
```
- Poistu psql painamalla Ctrl+C
- Aseta schema ohjelman mukaiseksi
```
.\root\>psql -U <user> -d <user> -f schema.sql# Missä <user> on joko postgres tai muu luomasi psql käyttäjä
```
- Navigoi source kansioon
```
.\root\>cd .\source\
```
- käynnistä sovellus
```
.\root\source\>flask run
```

Sovelluksessa on automaattisesti admin käyttäjä, jonka nimi on admin ja salasana on admin.