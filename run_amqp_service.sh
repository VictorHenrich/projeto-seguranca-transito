source init_app.sh

echo "...Executando Serviço do RabbitMQ..."

python3 src/main.py amqp -r

