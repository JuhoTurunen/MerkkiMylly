# MerkkiMylly

MerkkiMylly on yksinkertainen, cookie clicker -tyylinen nettiselaimessa toimiva peli, yliopistoteemalla. 

Lyhyesti pelin päämäärä on kerätä pisteitä. Niitä saa joko klikkaamalla nappia tai ostamalla päivityksiä jotka tuo tietyn määrän pisteitä minuutissa. Päivityksiä ostetaan pisteillä ja paremmat päivitykset vaativat enemmän pisteitä. 

Ohjelmassa olisi hakutoiminto jolla voi hakea muita pelaajia ja nähdä heidän dataa sekä leaderboard eniten pisteitä omaaville pelaajille.

## Nykytilanne

Projektin tietokantapuoli on sekä pelitoiminnot toimivat.

Tavoitteenani lopulliselle palautukselle oli luoda profiilien haku, profiilien editointi ja AJAX päivitysten osto toiminnot sovellukseen. Aioin myös korjata CSRF heikkoudet ja varmistaa myös sovelluksen puolustus muita yleisiä tietoturva heikkouksia vastaan. Viimeiseksi halusin viimeisessä palautuksessa erottaa projektin SQL scheman dumpista sekä toteuttaa pienempiä UX päivityksiä mm. Rekisteröinnin virheilmoitusten erittelyä, ja CSS päivityksiä. 

Koen saaneeni jokaisen näistä tavoitteesta suoritettua, mukaan lukematta profiilien editointia. En kokenut tämän toiminnon tuovan mitään uutta projektiin oppimisen kannalta, sillä projekti muokkaa tietokantaa jo useaan kertaan, monimutkaisemmillakin keinoilla. Lisäksi aikarajoitteet tulivat vastaan. 

Sain palautteena myös suosituksen ottaa käyttöön aggregate SQL funktioita, mutta en valitettavasti löytänyt tälle järkeviä käyttötarpeita MerkkiMylly sovelluksessa. 

Kaikkiaan uskon projektin olevan hyvällä tasolla. Tavoitteeni projektissa liikkui huomattavasti sovelluksen alkuperäisestä suunnitelmasta, mutta koen näiden muutosten enimmäkseen parantaneen sovelluksen käyttökokemusta. 

## Projektin tulevaisuus 

Jos jatkaisin projektin kehitystä lisäisin siihen enemmän yhteisöä ja kilpailua kasvattavia toimintoja, kuten ainejärjestö kiltoja sekä niiden välisen leaderboardin joka näyttäisi minkä järjestön jäsenet ovat saaneet eniten pisteitä. Myös alkuperäisessä suunnitelmassa mukana olleen haalarimerkki konseptin voisi jalostaa mukaan nykyiseen projektiin, jotta peli olisi lähempänä yliopisto teemaa. 

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

Alla olevalla komennolla luot tietokannan ja uuden "merkkimylly" nimisen käyttäjän dump.sql tiedostosta. Tämä käyttäjä saa kaikki oikeudet uudelle tietokannalle "merkkimylly_db". dump.sql tiedosto luo myös tietokannan upgrades tauluun valmiita päivityksiä. Jos sinulla on jo tietokanta nimeltä merkkimylly_db taikka käyttäjä nimeltä merkkimylly, en suosittele komennon suorittamista sellaisenaan.

Voit käyttää myös pelkkää schema.sql tiedostoa, jos haluat luoda vain tietokannan taulukkorakenteen, ilman dataa, käyttäjiä tai oikeuksia. Jos käytät schema.sql tiedostoa sinun täytyy luoda omat päivitykset tietokantaan, jotta saat sovelluksen toimimaan. Voit käyttää mallina dump.sql tiedoston pohjalla olevaa upgrades taulukon data dumppia. 

```
createdb -U <käyttäjänimi> -h localhost merkkimylly_db
psql -U <käyttäjänimi> -h localhost -d merkkimylly_db -f dump.sql
```

Nyt voit käynnistää sovelluksen komennolla

```
flask run
```
