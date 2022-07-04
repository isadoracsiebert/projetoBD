import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect, flash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sk'

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="dbProject",
        user='postgres',
        password='120616')
    return conn


@app.route('/')
def index():  # pagina inicial
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM jogo')
    jogo = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('index.html', jogos=jogo)

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

@app.route('/search/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()

        filtered_arg_list = filter(lambda item: item[1], request.form.items())

        print(filtered_arg_list)
        where_clause = ' AND '.join(map(
            lambda filter: f"{filter[0] if filter[1].isnumeric() else f'UPPER({filter[0]})'} = '{filter[1].upper()}'",
            filtered_arg_list))

        cur.execute(f"""
                     SELECT * FROM jogo
                     WHERE {where_clause}
                   """)

        print(where_clause)

        results = cur.fetchall()
        print(results)
        conn.commit()
        cur.close()
        conn.close()
        return render_template('result.html', games=results)

    return render_template('search.html')


@app.route('/insert/<string:game>', methods=('GET', 'POST'))
def insert(game):
    if request.method == 'POST':
        print(game)

        user = request.form['usuario']
        review = request.form['avaliacao']
        text = request.form['texto']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM jogo')

        jogos = cur.fetchall()
        game_id = None
        for jogo in jogos:
            print(jogo[0])
            print(jogo[2])
            print(jogo[2].strip() == game)
            if jogo[2].strip() == game:
                print('ok')
                game_id = jogo[0]
                break

        print(game_id)
        try:
            cur.execute('INSERT INTO review (usuario, jogo, datahora, avaliacao, texto)'
                        'VALUES (%s, %s, %s, %s, %s)',
                        (user, game_id, datetime.now(), review, text))
        except Exception as e:
            print(e)
            flash('Erro: ' + str(e))
            return redirect(url_for('insert', game=game))

        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('insert.html', game=game)


if __name__ == '__main__':
    app.run()
