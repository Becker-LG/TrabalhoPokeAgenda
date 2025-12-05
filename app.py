# =========================================================================================================
# ============================================== IMPORTAÇÕES ==============================================
# =========================================================================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import requests


# =====================================================================================================================
# =============================================== CRIAÇÃO BANCO DE DADOS ==============================================
# =====================================================================================================================

app = Flask(__name__)
app.secret_key = '17f5fe9813722ae4f396dc93f56b3125c7797b18e2af49a5c912de405956a009'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pokemon_db',
    'port': '3306'
}

# ===============================================================================================================
# =============================================== CRIAÇÃO DE ROTAS ==============================================
# ===============================================================================================================

# Rota de Cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        cpf = request.form['cpf']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM treinador WHERE nome = %s OR email = %s", (nome, email))
        if cursor.fetchone():
            flash("Nome de usuário ou email já cadastrado.", "erro")
            return redirect(url_for('cadastro'))

        cursor.execute("""INSERT INTO treinador (nome, email, cpf)
                          VALUES (%s, %s, %s)""", (nome, email, cpf))
        
        conn.commit()
        cursor.close()
        conn.close()

        flash("Cadastro realizado com sucesso! Você já pode fazer login.", "sucesso")
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM treinador WHERE nome = %s AND email = %s", (nome, email))
        treinador = cursor.fetchone()
        print(treinador)
        cursor.close()
        conn.close()

        if treinador:
            session['usuario_id'] = treinador['id']
            session['usuario_nome'] = treinador['nome']
            print(session['usuario_id'])
            return redirect(url_for('dashboard'))
        else:
            flash("Treinador ou senha inválidos.", "erro")
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota do Painel Principal (Dashboard) - VERSÃO CORRIGIDA
@app.route('/dashboard')
def dashboard():
    # Verifica se a chave 'usuario_id' existe na sessão.
    if 'usuario_id' not in session:
        # Se não estiver logado, envia uma mensagem e redireciona para a tela de login.
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM treinador")
    lista_treinadores = cursor.fetchall()

    return render_template('dashboard.html', treinadores=lista_treinadores)

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for('login'))

# Rota Principal (Raiz do site)
@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota para verificar se usuário ou email já existem
@app.route('/verificar_usuario_email', methods=['POST'])
def verificar_usuario_email():
    nome = request.form['nome']
    email = request.form['email']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM treinador WHERE nome = %s OR email = %s", (nome, email))
    existe = cursor.fetchone()
    cursor.close()
    conn.close()

    return 'existe' if existe else 'disponivel'

# ==============================================================================================================
# =============================================== ROTAS TREINADOR ==============================================
# ==============================================================================================================

# Rota para Editar uma Desenvolvedora
@app.route('/treinador', methods=['GET', 'POST'])
def treinador():
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cod = session['usuario_id']

    if request.method == 'POST':
        nome = request.form['nome'].strip()
        email = request.form['email'].strip()
        cpf = request.form['cpf'].strip()
        foto = request.form['foto'].strip()
        if foto == 'None':
            foto = ''
        cidade = request.form['cidade'].strip()
        if cidade == 'None':
            cidade = ''

        if not nome:
            flash("O nome do treinador é obrigatório.", "erro")
            return redirect(url_for('treinador'))
        if not email:
            flash("O email do treinador é obrigatório.", "erro")
            return redirect(url_for('treinador'))
        if not cpf:
            flash("O cpf do treinador é obrigatório.", "erro")
            return redirect(url_for('treinador'))

        # Verifica se o novo nome já existe em outro registro
        cursor.execute("SELECT id FROM treinador WHERE id != %s AND (nome = %s OR email = %s OR cpf = %s)", (cod, nome, email, cpf))
        if cursor.fetchone():
            flash("Já existe outro desenvolvedor ou com este nome, ou com este email, ou com este cpf.", "erro")
            cursor.close()
            conn.close()
            return redirect(url_for('treinador'))
        
        # Atualiza o registro
        cursor.execute("UPDATE treinador SET nome = %s, email = %s, cpf = %s, foto = %s, cidade = %s WHERE id = %s", (nome, email, cpf, foto, cidade, cod))
        conn.commit()
        
        cursor.close()
        conn.close()

        flash("Treinador atualizado com sucesso!", "sucesso")
        return redirect(url_for('treinador'))

    # GET: Busca o Treinador atual para preencher o formulário
    cursor.execute("SELECT * FROM treinador WHERE id = %s", (cod,))
    tre = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if not treinador:
        flash("Treinador não encontrado.", "erro")
        return redirect(url_for('dashboard'))

    return render_template('treinador.html', tre=tre)

# ================================================================================================================
# =============================================== PESQUISA POKÉMONS ==============================================
# ================================================================================================================

@app.route('/pokemons')
def pokemons():
    # Proteção de rota
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Lógica de pesquisa
    query = request.args.get('q')

    base_query = """
        SELECT
            p.id,
            p.nome,
            p.imagem_url,
            p.hp,
            p.attack,
            p.defense,
            p.special_attack,
            p.special_defense,
            p.speed,
            GROUP_CONCAT(DISTINCT t.nome ORDER BY t.nome SEPARATOR ', ') AS tipos,

            CASE 
                WHEN tp.local IS NOT NULL THEN tp.local
                ELSE 'nenhum'
            END AS local_pokemon

        FROM
            Pokemon p
        LEFT JOIN
            Pokemon_Tipo pt ON p.id = pt.pokemon_id
        LEFT JOIN
            Tipo t ON pt.tipo_id = t.id
        LEFT JOIN
            treinador_pokemon tp ON p.id = tp.pokemon_id
    """

    params = []

    # pesquisa apenas por nome
    if query:
        search_query = "%" + query + "%"
        base_query += " WHERE p.nome LIKE %s "
        params.append(search_query)

    base_query += """
        GROUP BY
            p.id, p.nome, p.imagem_url,
            p.hp, p.attack, p.defense,
            p.special_attack, p.special_defense, p.speed,
            local_pokemon
        ORDER BY
            p.nome ASC
    """

    cursor.execute(base_query, params if params else None)
    lista_pokemons = cursor.fetchall()

    for p in lista_pokemons:
        if p.get('tipos'):
            p['tipos'] = [t.strip() for t in p['tipos'].split(',') if t.strip()]
        else:
            p['tipos'] = []
    
    cursor.close()
    conn.close()

    return render_template('pokemons.html', pokemons=lista_pokemons, query=query)

# ==============================================================================================================

@app.route('/pokemons/adicionar/<int:pokemon_id>', methods=['POST'])
def adicionar_pokemon(pokemon_id):
    # Proteção de rota
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Lógica somente para POST
    local = 'time'
    cursor.execute("SELECT * FROM treinador_pokemon WHERE local = %s", (local,))
    registro = cursor.fetchall()
    print(registro)

    if len(registro) < 6:
        local = 'time'
    else:
        local = 'box'

    # Cadastra o pokémon novo
    treinador_id = session['usuario_id']

    cursor.execute("""
        INSERT INTO treinador_pokemon (treinador_id, pokemon_id, local)
        VALUES (%s, %s, %s)
    """, (treinador_id, pokemon_id, local))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('pokemons'))

# ================================================================================================================
# ==================================================== POKÉDEX ===================================================
# ================================================================================================================

@app.route('/pokedex')
def pokedex():
    # Proteção de rota
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Lógica de pesquisa
    treinador_id = session['usuario_id']

    
    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.imagem_url,
            p.hp,
            p.attack,
            p.defense,
            p.special_attack,
            p.special_defense,
            p.speed,
            tp.local,
            GROUP_CONCAT(DISTINCT t.nome ORDER BY t.nome SEPARATOR ', ') AS tipos
        FROM treinador_pokemon tp
        JOIN pokemon p ON tp.pokemon_id = p.id
        LEFT JOIN pokemon_tipo pt ON p.id = pt.pokemon_id
        LEFT JOIN tipo t ON t.id = pt.tipo_id
        WHERE tp.treinador_id = %s
        GROUP BY
            p.id, p.nome, p.imagem_url,
            p.hp, p.attack, p.defense,
            p.special_attack, p.special_defense, p.speed,
            tp.local
        ORDER BY p.nome ASC
    """, (treinador_id,))
    lista_pokemons = cursor.fetchall()
    
    for p in lista_pokemons:
        if p.get('tipos'):
            p['tipos'] = [t.strip() for t in p['tipos'].split(',') if t.strip()]
        else:
            p['tipos'] = []

    cursor.close()
    conn.close()

    return render_template('pokedex.html', pokemons=lista_pokemons)

# ==============================================================================================================

@app.route('/pokedex/retirarTime/<int:pokemon_id>', methods=['POST'])
def retirarTime_pokemon(pokemon_id):
    # Proteção de rota
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))
    
    treinador_id = session['usuario_id']
    local = 'box'

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("UPDATE treinador_pokemon SET local = %s WHERE (treinador_id = %s AND pokemon_id = %s)", (local, treinador_id, pokemon_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('pokedex'))

# ==============================================================================================================

@app.route('/pokedex/retirarBox/<int:pokemon_id>', methods=['POST'])
def retirarBox_pokemon(pokemon_id):
    # Proteção de rota
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    treinador_id = session['usuario_id']

    cursor.execute("DELETE FROM treinador_pokemon WHERE (treinador_id = %s AND pokemon_id = %s)", (treinador_id, pokemon_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('pokedex'))

@app.route('/pokedex/aumentarTime/<int:pokemon_id>', methods=['POST'])
def aumentarTime_pokemon(pokemon_id):
    if 'usuario_id' not in session:
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    treinador_id = session['usuario_id']
    local = 'time'

    cursor.execute("UPDATE treinador_pokemon SET local = %s WHERE (treinador_id = %s AND pokemon_id = %s)", (local, treinador_id, pokemon_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('pokedex'))

# Executa o app
if __name__ == '__main__':
    app.run(debug=True)

#Agora, eu necessito de um select da tabela treinador_pokemon, onde eu necessito de um 