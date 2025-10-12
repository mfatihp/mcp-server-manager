FROM golang:tip-alpine3.22 AS builder

WORKDIR /app

COPY . .

RUN go build -o db_syncer db_syncer.go



FROM scratch

COPY  --from=builder /app/db_syncer /db_syncer
COPY .env .

CMD ["/db_syncer"]