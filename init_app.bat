if not exist "venv-app-win" (
    echo "...Criando pasta venv-app-win..."

    python -m venv venv-app-win

    echo "...Pasta venv-app-win foi criada com sucesso..."

    call venv-app-win/Scripts/activate

    echo "...Instalando bibliotecas..."

    pip install -r requirements.txt

    playwright install

    echo "...Bibliotecas instaladas com sucesso..."

) else (
    echo "...Acessando pasta venv-app-win..."

    call venv-app-win/Scripts/activate
)