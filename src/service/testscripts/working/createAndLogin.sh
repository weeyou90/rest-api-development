
curl localhost:8080/users/register --silent -X POST -H "Content-Type: application/json" -d '{"username": "AzureDiamond", "password": "hunter2", "fullname": "Joey Pardella", "age": "15"}' > /dev/null

curl localhost:8080/users/authenticate --silent -X POST -H "Content-Type: application/json" -d '{"username": "AzureDiamond", "password": "hunter2"}' | tail --silent -c38 | head -c36 > token.ini

echo "Created user and logged in! Use token.ini to access the rest of the site!"
