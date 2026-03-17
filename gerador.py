import sqlite3
import random
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from tqdm import tqdm


LIMITE_MAXIMO_TRANSACOES = 1_000_000


def obter_caminho_db() -> Path:
    home = Path.home()
    pasta = home / "Documentos" / "walleto"
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta / "walleto.db"


DB_PATH = obter_caminho_db()

categorias = {
    "Alimentação": ["Supermercado", "Padaria", "iFood", "Restaurante"],
    "Transporte": ["Uber", "Posto de Gasolina"],
    "Moradia": ["Aluguel", "Conta de Luz", "Conta de Água", "Internet"],
    "Saúde": ["Farmácia", "Plano de Saúde"],
    "Lazer": ["Cinema", "Streaming", "Bar"],
    "Compras": ["Amazon", "Mercado Livre", "Shopee"],
}

faixa_valores = {
    "Alimentação": (20, 300),
    "Transporte": (15, 200),
    "Moradia": (100, 1500),
    "Saúde": (30, 500),
    "Lazer": (20, 250),
    "Compras": (50, 1200),
}

descricoes = [
    "Pagamento do mês",
    "Compra do dia",
    "Despesa recorrente",
    "Gasto inesperado",
    "Compra planejada",
]


def criar_banco() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        valor TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'saida')),
        data TEXT NOT NULL,
        descricao TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES usuarios(id),
        FOREIGN KEY(categoria_id) REFERENCES categorias(id)
    )
    """)

    conn.commit()
    conn.close()


def popular_categorias() -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for categoria in categorias.keys():
        cursor.execute(
            "INSERT OR IGNORE INTO categorias (nome) VALUES (?)",
            (categoria,)
        )

    conn.commit()
    conn.close()


def obter_ou_criar_usuario(nome: str = "Diego") -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (nome,))
    usuario = cursor.fetchone()

    if usuario is not None:
        conn.close()
        return usuario[0]

    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    user_id = cursor.lastrowid

    conn.commit()
    conn.close()
    return user_id


def obter_mapa_categorias() -> dict[str, int]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM categorias")
    resultados = cursor.fetchall()

    conn.close()

    return {nome: categoria_id for categoria_id, nome in resultados}


def gerar_data() -> str:
    inicio = datetime(2024, 1, 1)
    fim = datetime(2025, 12, 31)
    delta = fim - inicio
    dias = random.randint(0, delta.days)
    return (inicio + timedelta(days=dias)).strftime("%d/%m/%Y")


def gerar_transacao(user_id: int, mapa_categorias: dict[str, int]) -> tuple:
    categoria = random.choice(list(categorias.keys()))
    nome = random.choice(categorias[categoria])

    valor_min, valor_max = faixa_valores[categoria]
    valor = Decimal(str(random.uniform(valor_min, valor_max))).quantize(Decimal("0.01"))

    tipo = "saida"

    if random.random() < 0.1:
        tipo = "entrada"
        nome = "Salário"
        valor = Decimal(str(random.uniform(1500, 5000))).quantize(Decimal("0.01"))

    descricao = random.choice(descricoes)
    categoria_id = mapa_categorias[categoria]

    return (
        user_id,
        categoria_id,
        nome,
        str(valor),
        tipo,
        gerar_data(),
        descricao
    )


def inserir_transacoes(qtd: int, user_id: int) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    mapa_categorias = obter_mapa_categorias()

    print("\nGerando transações...")

    with tqdm(total=qtd, desc="Inserindo", unit="transação") as barra:
        for _ in range(qtd):
            cursor.execute("""
            INSERT INTO transacoes (
                user_id, categoria_id, nome, valor, tipo, data, descricao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, gerar_transacao(user_id, mapa_categorias))
            barra.update(1)

    conn.commit()
    conn.close()


def pedir_quantidade() -> int | None:
    entrada = input("Quantas transações deseja gerar? ").strip()

    if not entrada.isdigit():
        print("Digite apenas números inteiros positivos.")
        return None

    qtd = int(entrada)

    if qtd <= 0:
        print("A quantidade precisa ser maior que zero.")
        return None

    if qtd > LIMITE_MAXIMO_TRANSACOES:
        print(
            f"Quantidade muito alta. "
            f"O limite permitido é {LIMITE_MAXIMO_TRANSACOES:,} transações."
            .replace(",", ".")
        )
        return None

    return qtd


def main() -> None:
    print("=" * 40)
    print("GERADOR PROFISSIONAL - WALLETO")
    print("=" * 40)

    criar_banco()
    popular_categorias()
    user_id = obter_ou_criar_usuario("Diego")

    qtd = pedir_quantidade()
    if qtd is None:
        return

    inserir_transacoes(qtd, user_id)

    print("\nFinalizado com sucesso.")
    print(f"Banco salvo em: {DB_PATH.resolve()}")


if __name__ == "__main__":
    main()