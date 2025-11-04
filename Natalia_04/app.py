from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respostas_detalhadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT,
            resposta_text TEXT,
            data_evento DATE,
            local_evento TEXT,
            data_resposta DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ✅ Importante para funcionar no Render
with app.app_context():
    init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        form = request.form
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        processed = set()
        for key in form.keys():
            if key in processed:
                continue

            if key.endswith('_date'):
                base = key[:-5]
                date_val = form.get(f'{base}_date')
                local_val = form.get(f'{base}_local', '')
                pergunta_label = form.get(f'{base}_label', base)

                cursor.execute('''
                    INSERT INTO respostas_detalhadas (pergunta, resposta_text, data_evento, local_evento)
                    VALUES (?, ?, ?, ?)
                ''', (pergunta_label, '', date_val if date_val else None, local_val))
                processed.add(key)
                processed.add(f'{base}_local')
                processed.add(f'{base}_label')

            else:
                if f'{key}_date' in form:
                    continue

                pergunta_label = form.get(f'{key}_label', key)
                resposta_text = form.get(key)
                cursor.execute('''
                    INSERT INTO respostas_detalhadas (pergunta, resposta_text, data_evento, local_evento)
                    VALUES (?, ?, ?, ?)
                ''', (pergunta_label, resposta_text, None, None))
                processed.add(key)
                processed.add(f'{key}_label')

        conn.commit()
        conn.close()
        return redirect('/surpresa')

    return render_template('quiz.html')

@app.route('/surpresa')
def surpresa():
    return render_template('surpresa.html')

@app.route('/respostas')
def ver_respostas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, pergunta, resposta_text, data_evento, local_evento, data_resposta FROM respostas_detalhadas ORDER BY id')
    dados = cursor.fetchall()
    conn.close()
    return render_template('respostas.html', respostas=dados)

if __name__ == '__main__':
    app.run(debug=True)
