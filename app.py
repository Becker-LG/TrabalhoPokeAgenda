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

        #Verifica se já foi cadastrado um email ou usuário igual, se não, cadastra e encaminha para o login
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

        #seleciona o treinador
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM treinador WHERE nome = %s AND email = %s", (nome, email))
        treinador = cursor.fetchone()
        print(treinador)
        cursor.close()
        conn.close()

        #confere se existe. Se sim, realiza o login, e se não, redireciona para a página de login novamente
        if treinador:
            session['usuario_id'] = treinador['id']
            session['usuario_nome'] = treinador['nome']
            print(session['usuario_id'])
            return redirect(url_for('treinador'))
        else:
            flash("Treinador ou senha inválidos.", "erro")
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota Principal (Raiz do site, direciona para o login)
@app.route('/')
def index():
    return redirect(url_for('login'))

# Rota para verificar se usuário ou email já existem no momento do cadastro
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

# Rota do Painel Principal (Dashboard)
@app.route('/treinador')
def treinador():
    # Verifica se a chave 'usuario_id' existe na sessão.
    if 'usuario_id' not in session:
        # Se não estiver logado, envia uma mensagem e redireciona para a tela de login.
        flash("Você precisa fazer login para acessar esta página.", "erro")
        return redirect(url_for('login'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    treinador_id = session['usuario_id']

    cursor.execute("SELECT * FROM treinador WHERE id = %s", (treinador_id,))
    treinador = cursor.fetchone()

    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.imagem_url,
            p.altura,
            p.peso,
            p.hp,
            p.attack,
            p.defense,
            p.special_attack,
            p.special_defense,
            p.speed,
            p.evolucao,
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

    return render_template('treinador.html', treinador=treinador, pokemons=lista_pokemons)

# Rota para Editar um Treinador
@app.route('/treinador/editar', methods=['GET', 'POST'])
def editar_treinador():
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
            return redirect(url_for('editar_treinador'))
        if not email:
            flash("O email do treinador é obrigatório.", "erro")
            return redirect(url_for('editar_treinador'))
        if not cpf:
            flash("O cpf do treinador é obrigatório.", "erro")
            return redirect(url_for('editar_treinador'))

        # Verifica se o novo nome já existe em outro registro
        cursor.execute("SELECT id FROM treinador WHERE id != %s AND (nome = %s OR email = %s OR cpf = %s)", (cod, nome, email, cpf))
        if cursor.fetchone():
            flash("Já existe outro desenvolvedor ou com este nome, ou com este email, ou com este cpf.", "erro")
            cursor.close()
            conn.close()
            return redirect(url_for('editar_treinador'))
        
        # Atualiza o registro
        cursor.execute("UPDATE treinador SET nome = %s, email = %s, cpf = %s, foto = %s, cidade = %s WHERE id = %s", (nome, email, cpf, foto, cidade, cod))
        conn.commit()
        
        cursor.close()
        conn.close()

        flash("Treinador atualizado com sucesso!", "sucesso")
        return redirect(url_for('editar_treinador'))

    # GET: Busca o Treinador atual para preencher o formulário
    cursor.execute("SELECT * FROM treinador WHERE id = %s", (cod,))
    treinador = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if not treinador:
        flash("Treinador não encontrado.", "erro")
        return redirect(url_for('treinador'))

    return render_template('editar_treinador.html', treinador=treinador)

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
    treinador_id = session['usuario_id']
    query = request.args.get('q')

    base_query = """
        SELECT
            p.id,
            p.nome,
            p.imagem_url,
            p.altura,
            p.peso,
            p.hp,
            p.attack,
            p.defense,
            p.special_attack,
            p.special_defense,
            p.speed,
            p.evolucao,
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

        -- 🔥 AQUI está a mudança principal 🔥
        -- Só retorna local se o registro pertencer ao treinador_id
        LEFT JOIN
            treinador_pokemon tp 
            ON p.id = tp.pokemon_id 
            AND tp.treinador_id = %s
    """

    params = [treinador_id]

    # pesquisa por nome OU id
    if query:
        search_query = "%" + query + "%"
        base_query += " WHERE p.nome LIKE %s OR p.id = %s "
        params.append(search_query)
        params.append(query)

    base_query += """
        GROUP BY
            p.id, p.nome, p.imagem_url,
            p.hp, p.attack, p.defense,
            p.special_attack, p.special_defense, p.speed,
            local_pokemon
        ORDER BY
            p.nome ASC
    """

    cursor.execute(base_query, params)
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

    treinador_id = session['usuario_id']

    # Lógica somente para POST
    local = 'time'
    cursor.execute("SELECT * FROM treinador_pokemon WHERE local = %s AND treinador_id = %s", (local, treinador_id))
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
            p.altura,
            p.peso,
            p.hp,
            p.attack,
            p.defense,
            p.special_attack,
            p.special_defense,
            p.speed,
            p.evolucao,
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

# ==============================================================================================================

@app.route('/pokedex/retirarPokedex/<int:pokemon_id>', methods=['POST'])
def retirarPokedex_pokemon(pokemon_id):
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

# ==============================================================================================================

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