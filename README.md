# Faltômetro Bot

Bot para Telegram escrito em Python com o intuito de registrar faltas em matérias.

**Disponível em:** [http://t.me/faltometro_bot](http://t.me/faltometro_bot)

## Instalação e Configurações para Desenvolvimento

* Criar e ativar um [_virtualenv_](https://virtualenv.pypa.io/en/latest/) com Python 3.6.
* Instalar as dependências do projeto com ```pip install -r requirements.txt``` 
* Instalar o [SQLite](https://www.sqlite.org/index.html) e criar o banco de desenvolvimento local:
  * ```sqlite3 bot.db```
* Criar as tabelas (no momento só uma) no banco. Para isso, abrir uma _shell_ python e seguir os passsos:
  ```
    > from models.base import db
    > from models.class_model import ClassModel
    > db.create_tables([ClassModel])
  ```
 * Criar na raiz do projeto um arquivo .env e adicionar a variável ```BOT_API_TOKEN```, com o token gerado pelo Telegram para o bot.
 * Para rodar o projeto: ```python main.py```
