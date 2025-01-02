
FROM ubuntu:20.04


RUN apt-get update && apt-get install -y bash

COPY worker.sh /app/worker.sh


WORKDIR /app


RUN chmod +x worker.sh


CMD ["./worker.sh"]
