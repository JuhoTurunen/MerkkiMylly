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

TODO:
- Email verification
- Protection against SQL injections, XSS, and CSRF
- Passive click upgrades
- Upgrade price scaling with each purchase
