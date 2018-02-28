if [ $# -eq 1 ] 
then
	i=$1
else 
	i=1
fi

echo "Logging out random token"

curl localhost:8080/users/expire -i -X POST -H "Content-Type: application/json" -d '{"token": "6bf00d02-dffc-4849-a635-a21b08500d61"}'

echo "\n\n Logging out token in argument (if any)"
curl localhost:8080/users/expire -i -X POST -H "Content-Type: application/json" -d '{"token": "'$i'"}'


