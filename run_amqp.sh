if [ ! -d "venv-app" ]; then
    echo "Pasta venv-app nao foi criada ainda"

    python3 -m venv venv-app

    echo "...Pasta venv-app foi criada com sucesso..."

    source venv-app/bin/activate

    echo "...Instalando bibliotecas..."

    pip install -r requirements.txt

    echo "...Bibliotecas instaladas com sucesso..."

else
    echo "...Acessando pasta venv-app..."

    source venv-app/bin/activate

fi


python3 src/main.py amqp -r

