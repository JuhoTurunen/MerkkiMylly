# MerkkiMylly

MerkkiMylly on yksinkertainen, cookie clicker -tyylinen nettiselaimessa toimiva peli, yliopistoteemalla. 

Lyhyesti pelin päämäärä on kerätä pisteitä. Niitä saa joko klikkaamalla nappia tai ostamalla päivityksiä jotka tuo tietyn määrän pisteitä minuutissa. Päivityksiä ostetaan pisteillä ja paremmat päivitykset vaativat enemmän pisteitä. 

Ohjelmassa olisi hakutoiminto jolla voi hakea muita pelaajia ja nähdä heidän dataa sekä leaderboard eniten pisteitä omaaville pelaajille.  

Tietyn ajan välein pelaaja saa mahdollisuuden tienata randomisoitu haalarimerkki. Haalarimerkkien esiintyvyyttä voi kasvattaa ostamalla niihin liittyviä päivityksiä.

Kun pelaaja poistuu tallentaa tietokanta poistumis ajan ja kun hän palaa uudelleen peliin, laskee saapumisajan perusteella offline tilassa tienatut pisteet. 

Tässä on esimerkki siitä millaiselta projektin tietokanta voisi näyttää taulujen kannalta:

- Päivitykset: Taulu, joka sisältää ostettavat päivitykset, jotka nopeuttavat pisteiden kertymistä.
- Käyttäjät: Käyttäjätilien hallintaa varten, esimerkiksi kirjautumistietoja varten.
- Haalarimerkit: Taulu keräiltäville haalarimerkeille, jotka ovat palkkioita käytetystä ajasta ja joiden yleisyyttä voi kasvattaa maksamalla pisteitä.
- Kerätyt päivitykset: Käyttäjäkohtainen tieto ostetuista päivityksistä.
- CPM (Clicks per Minute) ja score-data: Käyttäjän napsautusten määrän ja pisteiden seurantaan.


Pelin kehityksen hankaluuden mukaan aion dynaamisesti vähentää tai kasvattaa pelin toimintojen määrää, jotta kerkeän aikarajoitteisiin. 


schema.sql tiedostossa on tietokannan rakenne sekä muutama päivitystä valmiiksi asetettuna. Voit muunnella päivityksiä tietokannassa, mutta "passive_power" on tällä hetkellä vain kosmeettinen.

## Ohjeet:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL=postgresql+psycopg2://merkkimylly:merkkimylly@localhost/merkkimylly_db
SECRET_KEY=<salainen-avain>
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

Windows CMD ohjeet:

```
$ py -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

Määritä vielä tietokannan skeema komennolla

```
$ createdb -U <käyttäjänimi> -h localhost merkkimylly_db
$ psql -U <käyttäjänimi> -h localhost -d merkkimylly_db -f schema.sql
```

Nyt voit käynnistää sovelluksen komennolla

```
$ flask run
```

## TODO:
- Email verification
- Protection against SQL injections, XSS, and CSRF
- Passive click upgrades
- Upgrade price scaling with each purchase
- Impove UI
- Add profile page with account settings
- Add a leaderboard
