#!/bin/bash -x
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"width":100,"height":100,"file_format":"jpg","colour": true}' \
  http://localhost:5000/basic
