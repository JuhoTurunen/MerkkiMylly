# MerkkiMylly

MerkkiMylly on yksinkertainen, cookie clicker -tyylinen nettiselaimessa toimiva peli, yliopistoteemalla. 

Lyhyesti pelin päämäärä on kerätä pisteitä. Niitä saa joko klikkaamalla nappia tai ostamalla päivityksiä jotka tuo tietyn määrän pisteitä minuutissa. Päivityksiä ostetaan pisteillä ja paremmat päivitykset vaativat enemmän pisteitä. 

Ohjelmassa olisi hakutoiminto jolla voi hakea muita pelaajia ja nähdä heidän dataa sekä leaderboard eniten pisteitä omaaville pelaajille.

## Nykytilanne

Projektin tietokantapuoli on sekä yleiset pelitoiminnot toimivat, mutta profiilien haku ja editointi puuttuu.

Tavoitteenani oli saada kolmanteen välipalautukseen mennessä valmiiksi CPS-päivitykset, profiilien editoinnin, leaderboadin sekä offline-klikkejen kerryttämisen. Sain suoritettua kaikki nämä paitsi profiilien editoinnin. Profiili sivu on jo olemassa, mutta toimintoa muokata omia tietoja ei ole vielä. 

Sain näiden tavoitteiden lisäksi siirryttyä suorien SQL-komentojen käyttöön ORM:n sijaan. Lisäsin peliin monia pienempiä toimintoja ja parannuksia kuten massa osto mahdollisuuden päivityksiin, päivitysten hinnan kasvun toistuvilla ostoksilla sekä päivityksiä pelin ulkonäköön. Tavoitteena lopulliseen palautukseen olisi saada viimeisetkin alla olevan TO-DO-listan osat valmiiksi.

## Windows ohjeet:

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

```
DATABASE_URL=postgresql+psycopg2://merkkimylly:merkkimylly@localhost/merkkimylly_db
SECRET_KEY=<salainen-avain>
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla

```
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Seuraavalla komennolla luot tietokannan ja uuden käyttäjän nimeltä "merkkimylly" schema.sql tiedostosta. Tämä käyttäjä saa kaikki oikeudet uudelle tietokannalle "merkkimylly_db". schema.sql tiedosto luo myös tietokannan "upgrades" tauluun valmiita päivityksiä. Jos sinulla on jo tietokanta nimeltä "merkkimylly_db" taikka käyttäjä nimeltä "merkkimylly" en suosittele komennon käyttämistä sellaisenaan.

```
createdb -U <käyttäjänimi> -h localhost merkkimylly_db
psql -U <käyttäjänimi> -h localhost -d merkkimylly_db -f schema.sql
```

Nyt voit käynnistää sovelluksen komennolla

```
flask run
```

## TODO:
- Remake schema.sql
- Try to find use cases for aggregate functions
- Add AJAX handling to upgrades to avoid refresh
- Add profile bio editing
- UI improvements
