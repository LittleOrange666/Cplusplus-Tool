#!/bin/bash

docker build -t cplusplus_tool .

docker rm -f cplusplus_tool 2>/dev/null
docker run -d -p 5555:5555 --name cplusplus_tool --restart=always cplusplus_tool