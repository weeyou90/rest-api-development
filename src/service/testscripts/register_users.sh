echo "Clearing users"

curl localhost:8080/clear

echo "\n\nTrying to insert User 1 again"
curl localhost:8080/users/register -i -X POST -H "Content-Type: application/json" -d '{"username": "AzureDiamond", "password": "hunter2", "fullname": "Joey Pardella", "age": "15"}'

echo "\n\nInserting User 2"
curl localhost:8080/users/register -i -X POST -H "Content-Type: application/json" -d '{"username": "BloodDiamond", "password": "hunter2", "fullname": "Joey Pardella", "age": "15"}'

echo "\n\nTrying to insert User 1 again"
curl localhost:8080/users/register -i -X POST -H "Content-Type: application/json" -d '{"username": "AzureDiamond", "password": "hunter2", "fullname": "Joey Pardella", "age": "15"}'


echo "\n"
