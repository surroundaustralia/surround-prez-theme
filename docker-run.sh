# for local testing

# (NOTE: for running triplestore in WSL2, run `ip addr`, use IP inet under eth0 for local SPARQL_ENDPOINT IP)

docker run --name <container_name> \
-v <abs_repo_path>/theme:/app/prez/theme \
-p 8000:8000 \
--env-file .env \
surroundaustralia/prez:0.1.0
