from peewee import *
from datetime import date
import time
import logging

logger = logging.getLogger('peewee')
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



db.connect()
db.create_tables([Autor, Livro, Emprestimo])

Autor.delete().execute()
Livro.delete().execute()


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


#SEM OTIMIZAÇÃO
contador = ContadorSQL()
logger.addHandler(contador)

print("\nSEM OTIMIZAÇÃO")
inicio = time.perf_counter()
livros = Livro.select()

for livro in livros:
    print(livro.titulo, livro.autor.nome)

fim = time.perf_counter()

print("Consultas:", contador.quantidade)
print("Tempo:", fim - inicio, "segundos")

logger.removeHandler(contador)


# TESTE COM PREFETCH()
contador = ContadorSQL()
logger.addHandler(contador)

print("\nCOM PREFETCH")
inicio = time.perf_counter()

livros = prefetch(
    Livro.select(),
    Autor.select()
)

for livro in livros:
    print(livro.titulo, livro.autor.nome)

fim = time.perf_counter()

print("Consultas:", contador.quantidade)
print("Tempo:", fim - inicio, "segundos")

logger.removeHandler(contador)


# TESTE COM JOIN()
contador = ContadorSQL()
logger.addHandler(contador)
print("\nCOM JOIN")
inicio = time.perf_counter()
livros = (
    Livro
    .select(Livro, Autor)
    .join(Autor)
)

for livro in livros:
    print(livro.titulo, livro.autor.nome)

fim = time.perf_counter()

print("Consultas:", contador.quantidade)
print("Tempo:", fim - inicio, "segundos")

logger.removeHandler(contador)