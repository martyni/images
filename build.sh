NAME=$(cat run/NAME)
VERSION=$(cat run/VERSION)
docker build -t $NAME:$VERSION .
echo docker run $NAME:$VERSION
