FROM golang:tip-alpine3.22 AS builder

WORKDIR /app

COPY . .

RUN go build -o log_fetch_service log_fetch_service.go



FROM scratch

COPY  --from=builder /app/log_fetch_service /log_fetch_service
COPY .env .

CMD ["/log_fetch_service"]