FROM golang:tip-alpine3.22 AS builder

WORKDIR /app

COPY . .

RUN go build -o syncer syncer.go



FROM scratch

COPY  --from=builder /app/syncer /syncer

CMD ["/syncer"]