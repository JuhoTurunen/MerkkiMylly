# MerkkiMylly

MerkkiMylly is a university-themed, browser-based clicker game built as a full-stack web application.

The game runs on a Flask (Python) backend with a PostgreSQL database that stores all persistent game state, including players, scores, upgrades, and progression. Points are earned through user actions and automated upgrades, with all game logic handled server-side and reflected to the client via HTTP endpoints and AJAX requests.

The project includes a defined SQL schema and database dump used to model the game economy and initial data, as well as a simple frontend built with HTML, CSS, and JavaScript to provide real-time interaction. The application also supports player lookup and a global leaderboard based on stored score data.

MerkkiMylly was created as a university course project and is not under active development.

## Windows setup instructions

Clone this repository to your local machine and navigate to the project root directory.

Create a `.env` file in the root directory and define the following environment variables:

```
DATABASE_URL=postgresql+psycopg2://merkkimylly:merkkimylly@localhost/merkkimylly_db
SECRET_KEY=<your-secret-key>
```

Next, create and activate a virtual environment and install the required dependencies:

```
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Database setup

The command below creates a PostgreSQL database named `merkkimylly_db` and a user named `merkkimylly` using the provided `dump.sql` file.

The user is granted full permissions on the database.

The `dump.sql` file also inserts initial data into the upgrades table, which is required for the application to function.

> **Note:**
> If you already have a database named `merkkimylly_db` or a user named `merkkimylly`, do **not** run these commands as-is.

```
createdb -U <username> -h localhost merkkimylly_db
psql -U <username> -h localhost -d merkkimylly_db -f dump.sql
```

#### Alternative: schema-only setup

You may also use `schema.sql` if you only want to create the database table structure without users, permissions, or initial data.

If you use `schema.sql`, you must manually insert upgrade data into the `upgrades` table for the application to work.
The upgrade entries at the end of `dump.sql` can be used as a reference.

### Running the application

Once the setup is complete, start the application with:

```
flask run
```
