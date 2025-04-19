# nexus-archive
App for answering the question of what Star Trek episode should you watch.

Built with Python, FastApi, PostgresSQL, and Docker.


## local development

Start the server and db
* `docker compose up --build`
Run the server in the background
* `docker compose up --build -d`
Enable automatic local file reload
* `docker compose watch`


## TODO
* add remaining models, (ie categories/themes)  
* add initial data 
* add tests
* add migrations (tables are currently added via SQLModel)
* add frontend
