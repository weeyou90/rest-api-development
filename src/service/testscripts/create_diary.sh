echo "Unable to retireve all entries belonging to an authenticated user due to invalid post inputs:"

curl localhost:8080/diary/create -X POST -H "Content-Type: application/json" -d '{"token":"2"}'

echo "\n\n Retrieve all entries belonging to an authenticated user with correct post inputs:"

curl localhost:8080/diary/create -X POST -H "Content-Type: application/json" -d '{"token":"6bf00d02-dffc-4849-a635-a21b08500d61", "title":"No One Can See This Post", "public": false, "text": "It is very secret!"}'

echo "\n"
