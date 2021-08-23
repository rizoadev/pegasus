#!/bin/bash

img='registry.gitlab.com/viavallen/kentang-goreng/fastnclean:latest'

docker login registry.gitlab.com -u viavallen -p d8pGJNRMpM6JekEQ6taT

docker build -t $img .
docker push $img

echo "crod"