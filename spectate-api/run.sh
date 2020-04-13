docker build -t mindreader/spectate .
docker run --rm -v /home/anders/Code/cold-start-framework/results:/results -p 8888:5000 mindreader/spectate