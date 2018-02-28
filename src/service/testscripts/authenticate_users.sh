echo "logging in with wrong combi"

curl localhost:8080/users/authenticate -i -X POST -H "Content-Type: application/json" -d '{"username": "AzureDiamond", "password": "hunter1"}'

echo "\n\nlogging in with right combi"

curl localhost:8080/users/authenticate -i -X POST -H "Content-Type: application/json" -d '{"username": "AzureDiamond", "password": "hunter2"}'

echo "\n"
