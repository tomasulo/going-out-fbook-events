#!/bin/sh

docker build . -t going-out/fbook-events

docker tag going-out/fbook-events:latest 845599215609.dkr.ecr.eu-central-1.amazonaws.com/going-out/fbook-events:latest

docker push 845599215609.dkr.ecr.eu-central-1.amazonaws.com/going-out/fbook-events:latest