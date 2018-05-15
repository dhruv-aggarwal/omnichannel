# omnichannel
Omnichannel View for customer reviews, responses and tickets

# Local Setup
  1) Clone the repository:

  `git clone git@github.com:practo/holonet.git`

  2) Copy docker-compose.yml:

  `cp docker-compose.yml.sample docker-compose.yml`

  3) Build and run docker compose:

  `docker-compose up --build`

  4) Create database for first time:

  `docker exec -it omnichannel_mysql_1 bash`

  `bash-4.2# mysql`

  `mysql> create database omnichannel;`

  5) Check health status

  `curl localhost:1786/api/status`



