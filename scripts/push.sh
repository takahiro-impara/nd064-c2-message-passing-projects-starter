docker build --platform linux/amd64 . -t frkoichi/$1
docker image push frkoichi/$1:latest

