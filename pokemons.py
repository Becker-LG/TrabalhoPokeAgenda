import requests

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = '17f5fe9813722ae4f396dc93f56b3125c7797b18e2af49a5c912de405956a009'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pokemon_db',
    'port': '3306'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

def get_tipos_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f"Erro ao buscar {nome}")
        return []

    data = resp.json()

    tipos = [t["type"]["name"] for t in data["types"]]

    return tipos

def get_pokemon(nome):
    url = f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}"
    resp = requests.get(url)

    if resp.status_code != 200:
        print("Pokémon não encontrado")
        return None

    data = resp.json()

    # --- Dados básicos ---
    pokemon_id = data["id"]
    pokemon_nome = data["name"]
    sprite = data["sprites"]["front_default"]

    # Status (HP, ATT, DEF, SP.ATT, SP.DEF, SPEED)
    status = [s["base_stat"] for s in data["stats"]]

    altura = data["height"]
    peso = data["weight"]

    # --- Agora vamos buscar a evolução ---
    # 1. Pega o endpoint species
    species_url = data["species"]["url"]
    species_data = requests.get(species_url).json()

    # 2. Pega a URL da cadeia evolutiva
    evo_chain_url = species_data["evolution_chain"]["url"]
    evo_chain = requests.get(evo_chain_url).json()

    # Função para percorrer a cadeia e encontrar evolução
    def encontrar_evolucao(chain, alvo):
        atual = chain["species"]["name"]

        # Achou o Pokémon atual
        if atual == alvo:
            if chain["evolves_to"]:
                return chain["evolves_to"][0]["species"]["name"]
            return None

        # Se não for, procura nos próximos
        for evo in chain["evolves_to"]:
            resultado = encontrar_evolucao(evo, alvo)
            if resultado:
                return resultado
        return None

    proxima_evolucao = encontrar_evolucao(evo_chain["chain"], pokemon_nome)

    return {
        "id": pokemon_id,
        "nome": pokemon_nome,
        "sprite": sprite,
        "status": status,
        "altura": altura,
        "peso": peso,
        "evolucao": proxima_evolucao  # pode ser None
    }

def cadastrar_pokemon(pokemons):
    for pokemon in pokemons:
        print(pokemon)
        p = get_pokemon(pokemon)

        id = p['id']
        nome = p['nome']
        imagem_url = p['sprite']
        hp, attack, defense, special_attack, special_defense, speed = p['status']
        altura = p['altura']
        peso = p['peso']
        evolucao = p['evolucao']  # NOVO

        print(id, nome, imagem_url, hp, attack, defense, special_attack, special_defense, speed, altura, peso, evolucao)
        print('')

        cursor.execute("""
            INSERT INTO pokemon
            (id, nome, imagem_url, hp, attack, defense, special_attack, special_defense, speed, altura, peso, evolucao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, nome, imagem_url, hp, attack, defense, special_attack, special_defense, speed, altura, peso, evolucao))
        
        conn.commit()

def obter_tipos_pokemon():
    url = "https://pokeapi.co/api/v2/type"
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro ao acessar a PokéAPI")
        return []

    data = response.json()

    # A PokéAPI retorna também categorias como "shadow" e "unknown"
    # Se quiser, você pode filtrá-las.
    tipos = [tipo["name"] for tipo in data["results"]]

    return tipos

lista_tipos = obter_tipos_pokemon()
print(lista_tipos)

def cadastrar_tipos(lista):
    for tipo in lista:
        print(tipo)

        cursor.execute("""INSERT INTO tipo (nome)
                          VALUES (%s)""", (tipo,))
        conn.commit()


def linkar_TiposPokemons():
    pokemons = ['Pikachu', 'Charizard', 'Eevee', 'Greninja', 'Lucario', 'Gengar', 'Umbreon', 'Rayquaza', 'Gardevoir', 'Bulbasaur', 'Squirtle', 'Charmander', 'Jigglypuff', 'Snorlax', 'Dragonite', 'Blastoise', 'Mewtwo', 'Arcanine', 'Sylveon', 'Lapras', 'Garchomp', 'Vaporeon', 'Espeon', 'Jolteon', 'Blaziken', 'Magikarp', 'Togepi', 'Mew']
    for pokemon in pokemons:
        p = get_pokemon(pokemon)
        pokemon_id = int(p['id'])

        tipo = get_tipos_pokemon(p['nome'])
        

        if len(tipo) == 1:
            tipo = tipo[0]

            cursor.execute("SELECT * FROM tipo WHERE nome = %s", (tipo,))
            registro = cursor.fetchone()
            tipo_id = registro[0]

            cursor.execute("""INSERT INTO pokemon_tipo (pokemon_id, tipo_id)
                              VALUES (%s, %s)""", (pokemon_id, tipo_id))
            conn.commit()

            print('Um')
        elif len(tipo) == 2:
            tipo1 = tipo[0]
            tipo2 = tipo[1]

            #TIPO UM ====================================================================
            cursor.execute("SELECT * FROM tipo WHERE nome = %s", (tipo1,))
            registro = cursor.fetchone()
            tipo_id1 = registro[0]

            cursor.execute("""INSERT INTO pokemon_tipo (pokemon_id, tipo_id)
                              VALUES (%s, %s)""", (pokemon_id, tipo_id1))
            conn.commit()

            #TIPO DOIS ==================================================================
            cursor.execute("SELECT * FROM tipo WHERE nome = %s", (tipo2,))
            registro = cursor.fetchone()
            tipo_id2 = registro[0]

            cursor.execute("""INSERT INTO pokemon_tipo (pokemon_id, tipo_id)
                              VALUES (%s, %s)""", (pokemon_id, tipo_id2))
            conn.commit()

            print('Dois')
        

pokemons = ['Pikachu', 'Charizard', 'Eevee', 'Greninja', 'Lucario', 'Gengar', 'Umbreon', 'Rayquaza', 'Gardevoir', 'Bulbasaur', 'Squirtle', 'Charmander', 'Jigglypuff', 'Snorlax', 'Dragonite', 'Blastoise', 'Mewtwo', 'Arcanine', 'Sylveon', 'Lapras', 'Garchomp', 'Vaporeon', 'Espeon', 'Jolteon', 'Blaziken', 'Magikarp', 'Togepi', 'Mew']

cursor.execute("SELECT * FROM treinador")
lista_treinadores = cursor.fetchall()
print(lista_treinadores[0]['id'])

cursor.close()
conn.close()