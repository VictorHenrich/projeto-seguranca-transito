call init_app.bat

echo "...Executando Serviço do RabbitMQ..."

python src/main.py amqp -r

