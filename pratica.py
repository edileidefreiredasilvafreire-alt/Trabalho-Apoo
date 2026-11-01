from peewee import *
from datetime import date
import time
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

db = SqliteDatabase('biblioteca.db')

class ContadorSQL(logging.Handler):

    def __init__(self):
        super().__init__()
        self.quantidade = 0

    def emit(self, record):
        mensagem = record.getMessage().upper()

        if 'SELECT' in mensagem or 'WITH' in mensagem:
            self.quantidade += 1

class BaseModel(Model):
    class Meta:
        database = db

class Autor(BaseModel):
    nome = CharField()

class Livro(BaseModel):
    titulo = CharField()

    autor = ForeignKeyField(
        Autor,
        backref='livros'
    )

class Emprestimo(BaseModel):
    leitor = CharField()

    livro = ForeignKeyField(
        Livro,
        backref='emprestimos'
    )

    data = DateField()
    devolvido = BooleanField(default=False)

db.connect()
db.create_tables([Autor, Livro, Emprestimo])

Autor.delete().execute()
Livro.delete().execute()
Emprestimo.delete().execute()

# autores
fernando = Autor.create(
    nome='Fernando Pessoa'
)

clarice = Autor.create(
    nome='Clarice Lispector'
)

neal = Autor.create(
    nome='Neal Shusterman'
)

# livros
livro1 = Livro.create(
    titulo='mensagem',
    autor=fernando
)

livro2 = Livro.create(
    titulo='a nuvem',
    autor=neal
)

livro3 = Livro.create(
    titulo='A Hora da Estrela',
    autor=clarice
)

livro4 = Livro.create(
    titulo='o ceifador',
    autor=neal
)

#emprestimo

Emprestimo.create(
    leitor='João',
    livro=livro1,
    data=date(2026, 10, 10)
)

Emprestimo.create(
    leitor='Maria',
    livro=livro3,
    data=date(2026, 10, 12)
)

Emprestimo.create(
    leitor='Pedro',
    livro=livro2,
    data=date(2026, 10, 15)
)


#SEM OTIMIZAÇÃO
contador = ContadorSQL()
logger.addHandler(contador)

inicio = time.perf_counter()
livros = Livro.select()

for livro in livros:
    print(livro.titulo, livro.autor.nome)

fim = time.perf_counter()

print("\nSEM OTIMIZAÇÃO")
print("Consultas:", contador.quantidade)
print("Tempo:", fim - inicio, "segundos")

logger.removeHandler(contador)


# TESTE COM PREFETCH()
contador = ContadorSQL()
logger.addHandler(contador)

inicio = time.perf_counter()

livros = prefetch(
    Livro.select(),
    Autor.select()
)

for livro in livros:
    print(livro.titulo, livro.autor.nome)

fim = time.perf_counter()

print("\nCOM PREFETCH")
print("Consultas:", contador.quantidade)
print("Tempo:", fim - inicio, "segundos")

logger.removeHandler(contador)


# TESTE COM JOIN()
contador = ContadorSQL()
logger.addHandler(contador)
inicio = time.perf_counter()
livros = (
    Livro
    .select(Livro, Autor)
    .join(Autor)
)

for livro in livros:
    print(livro.titulo, livro.autor.nome)

fim = time.perf_counter()

print("\nCOM JOIN")
print("Consultas:", contador.quantidade)
print("Tempo:", fim - inicio, "segundos")

logger.removeHandler(contador)