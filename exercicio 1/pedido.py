import asyncio
import aiohttp
import hashlib
import sqlite3
import logging


logging.basicConfig(level=logging.INFO)


conn = sqlite3.connect("base.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    pedidos_id TEXT PRIMARY KEY, 
    cliente TEXT
    produtos TEXT,
    total REAL, 
    hash TEXT, 
    nome TEXT,
    description TEXT)
    """)

conn.commit()


# valida o pedido
def validar_pedido(pedido):
    if "id" not in pedido or "cliente" not in pedido or "productos" not in pedido:
        raise Exception("pedido inválido")

# busca produto

async def buscar_produto(session, sku):
    url = f"https://fakestoreapi.com/products/{sku}" # sku codigo do produto
    # tentativas de receber uma resposta da api
    for tentativa in range(3):
        try:
            async with session.get(url) as resp:
                return await resp.json()
        except:
            # caso de erro, gravo o erro no logging do python para consultas
            logging.warning(f"Erro ao buscar produto {sku}, tentativa {tentativa+1}")
            # faz com que esta tarefa aguarde 1 segundo para tentar novamente neste laço
            await asyncio.sleep(1)
    return None

# processamento

async def processar_pedido(pedido, session):
    try:
        validar_pedido(pedido)

        total = 0

        for p in pedido["productos"]:
            produto_api = await buscar_produto(session, p["sku"])

            if produto_api:
                nome = produto_api.get("title")
                description = produto_api.get("description")
            else:
                nome = "Desconhecido"
                description = "N/A"

            preco = p['precio_unitario']
            quantidade = p["cantidad"]

            total += preco * quantidade

        # desconto

        if total > 500:
            total = total * 0.9

        # hash simples criando um id unico para os pedidos

        hash_pedido = hashlib.md5(str(pedido["id"]).encode()).hexdigest()

        # Salvar no banco de dados sem duplicar
        cursor.execute("SELECT 1 FROM pedidos  where pedidos_id = ?", (pedido["id"],))
        existe = cursor.fetchone()

        if existe:
            logging.warning(f"Pedido {pedido['id']} já foi processado")
            return
        cursor.execute("""
        INSERT OR IGNORE INTO pedidos (pedidos_id, cliente, total, hash, nome, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (pedido["id"], pedido["cliente"], total, hash_pedido, nome, description))

        conn.commit()
        # criar o log do processamento

        logging.info(f"Pedido {pedido['id']} processado")
    except Exception as e:
        logging.error(f"Erro no pedido {pedido.get('id')}: {e}")


# fila

async def worker(fila, session):
    while True:
        pedido = await fila.get()

        await processar_pedido(pedido, session)

        fila.task_done()

# main

async  def main():
    fila = asyncio.Queue()

    pedidos = [
        {
            "id": 1,
            "cliente": "ACME",
            "productos": [
                {"sku": 1, "cantidad":2, "precio_unitario": 600}
            ]
        },
        {
            "id": 2,
            "cliente": "XYZ",
            "productos": [
                {"sku": 2, "cantidad": 10, "precio_unitario": 60}
            ]
        }
    ]



    # adiciona na fila
    for p in pedidos:
        await fila.put(p)

    async with aiohttp.ClientSession() as session:
        # cria 2 workers
        tarefas = [
            asyncio.create_task(worker(fila, session)),
            asyncio.create_task(worker(fila, session))
        ]

        await fila.join()

        for t in tarefas:
            t.cancel()

asyncio.run(main())




# Resultado

"""
INFO:root:Pedido 2 processado
INFO:root:Pedido 1 processado

informações em banco de dados:
  [
  ('2', 
  'XYZ', 
   540.0, 
  'c81e728d9d4c2f636f067f89cc14862c', 
  'Mens Casual Premium Slim Fit T-Shirts ', 
  'Slim-fitting style, contrast raglan long sleeve, 
  three-button henley placket, light weight & soft fabric for breathable and comfortable wearing. 
  And Solid stitched shirts with round neck made for durability and a great fit for casual fashion 
  wear and diehard baseball fans. The Henley style round neckline includes a three-button placket.'), 
  
  ('1', 
   'ACME', 
    200.0, 
   'c4ca4238a0b923820dcc509a6f75849b', 
   'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops', 
   'Your perfect pack for everyday use and walks in the forest. 
    Stash your laptop (up to 15 inches) in the padded sleeve, your everyday')
    ]
"""

# Resultado rodando novamente o script:

"""
WARNING:root:Pedido 1 já foi processado
WARNING:root:Pedido 2 já foi processado
"""