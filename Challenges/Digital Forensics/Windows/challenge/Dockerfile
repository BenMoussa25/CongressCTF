FROM alpine:latest
RUN apk update
RUN apk upgrade
RUN apk add socat

RUN adduser -h /home/somebody -s /bin/bash ctf -u 1001 | echo ctf | echo ctf

WORKDIR /home/ctf

COPY ./flag.txt /home/ctf/flag.txt
COPY ./asker /home/ctf/asker
COPY ./questions.txt /home/ctf/question.txt

RUN chmod +x ./asker /home/ctf/asker
USER ctf

CMD socat TCP-LISTEN:1339,reuseaddr,fork EXEC:"./asker "