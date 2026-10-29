
# Tema 4: Consultas Avançadas, Filtros e Otimização de Performance

## Integrantes e contribuições

- **Joyce Wellen:** pesquisa do conteúdo e preparação dos slides.
- **Ranielly Brito:** levantamento dos conceitos e organização da apresentação.
- **Thalis Emanuel:** implementação do programa Python e configuração do banco de dados.
- **Lílian Vitória:** produção da documentação em Markdown e organização do repositório no GitHub.
- **Kauan Jhonatas:** colaboração na pesquisa e revisão dos conteúdos do trabalho.

---

## Introdução

O objetivo deste trabalho é compreender como realizar consultas mais eficientes em bancos de dados utilizando o Peewee ORM.

Um ORM permite trabalhar com as informações do banco por meio de classes e objetos, facilitando a escrita das consultas em Python. Além de recuperar registros, também podemos aplicar condições, organizar resultados, realizar cálculos e melhorar a maneira como os dados são acessados.

Ao longo da atividade, exploramos esses recursos por meio de exemplos práticos e de uma comparação entre diferentes formas de consultar informações relacionadas.

## Tecnologias utilizadas

- **Python:** desenvolvimento da aplicação.
- **Peewee ORM:** criação dos modelos e execução das consultas.
- **SQLite:** armazenamento dos registros utilizados na prática.

##  Conceitos abordados

### 1. Consultas condicionais e pesquisas textuais

Em algumas situações, não precisamos consultar todos os registros de uma tabela. Podemos definir condições para retornar apenas as informações desejadas.

No Peewee, o método `where()` permite estabelecer essas condições. Os operadores lógicos também podem ser utilizados para combinar ou inverter expressões.

| Operador | Função |
|---|---|
| `&` | Combina condições usando AND. |
| `|` | Combina condições usando OR. |
| `~` | Inverte uma condição usando NOT. |

Para pesquisas de texto, podemos utilizar:

- `contains()`: encontra textos que contenham determinado trecho.
- `startswith()`: encontra textos que comecem com uma sequência específica.

Por exemplo, em um sistema empresarial, podemos procurar funcionários com salário acima de determinado valor ou localizar nomes que comecem com uma letra específica.

Essas operações tornam as consultas mais flexíveis e permitem recuperar informações de acordo com as necessidades da aplicação.

### 2. Ordenação, paginação e escolha de campos

Depois de consultar os registros, podemos organizar a apresentação dos resultados e evitar o carregamento de informações desnecessárias.

Os principais métodos estudados são:

- `order_by()`: ordena os registros por um ou mais campos.
- `paginate()`: apresenta os resultados em páginas.
- `select()`: especifica os campos que serão consultados.

Em um cadastro de funcionários, por exemplo, podemos ordenar os salários do menor para o maior, mostrar apenas alguns funcionários por página ou consultar somente os nomes.

Esses recursos ajudam a tornar as consultas mais organizadas e adequadas ao que o usuário precisa visualizar.

### 3. Agrupamento e operações de agregação

O agrupamento permite reunir registros que possuem alguma característica em comum. Já as funções de agregação realizam cálculos sobre esses registros.

| Recurso | Descrição |
|---|---|
| `group_by()` | Agrupa registros por um campo. |
| `having()` | Define condições para os grupos formados. |
| `fn.COUNT()` | Conta a quantidade de registros. |
| `fn.SUM()` | Soma os valores de um campo numérico. |

Essas funcionalidades podem ser usadas para descobrir quantos funcionários existem em cada departamento, identificar departamentos com mais de um funcionário e calcular a soma dos salários de cada setor.

Dessa maneira, o banco de dados também pode ser utilizado para produzir informações úteis para análises e relatórios.

### 4. O problema N+1 Queries

O problema N+1 acontece quando uma consulta inicial é seguida por várias consultas adicionais para recuperar dados relacionados.

Imagine que o sistema carregue oito funcionários e, depois, consulte separadamente o departamento de cada um. Caso cada acesso gere uma nova consulta, serão realizadas nove consultas SQL: uma para os funcionários e outras oito para os departamentos.

Esse comportamento pode aumentar o tempo de execução, principalmente quando a quantidade de registros cresce.

Para reduzir esse problema, o Peewee oferece duas alternativas importantes:

- `join()`: utiliza uma junção SQL para consultar dados de tabelas relacionadas.
- `prefetch()`: busca antecipadamente os registros relacionados, evitando consultas individuais durante o acesso aos objetos.

Embora ambas as técnicas possam reduzir consultas repetidas, a escolha depende da estrutura dos dados e do resultado que precisamos obter.

### 5. Seleção de campos e uso eficiente dos dados

Carregar todas as informações disponíveis nem sempre é necessário. Quando uma consulta precisa apenas do nome e do salário de um funcionário, por exemplo, os outros campos podem ser dispensáveis.

O Peewee permite definir os campos desejados com `select()`. Outros ORMs, como o Django, disponibilizam recursos como `only()` para controlar quais campos serão carregados.

Essa abordagem pode diminuir a quantidade de dados processados e transferidos. É importante, porém, selecionar os campos considerando as informações que serão realmente utilizadas pelo programa.

---

##  Desenvolvimento da prática

Para aplicar os conteúdos, foi proposta uma aplicação de cadastro de funcionários organizada em duas tabelas relacionadas.

### Estrutura do banco de dados

**Tabela `Departamento`**

Armazena os setores de uma empresa.

Campos principais:
- `id`: identificador do departamento.
- `nome`: nome do setor.

**Tabela `Funcionario`**

Registra os funcionários vinculados aos departamentos.

Campos principais:
- `id`: identificador do funcionário.
- `nome`: nome do funcionário.
- `idade`: idade do funcionário.
- `salario`: salário cadastrado.
- `departamento`: referência ao departamento ao qual pertence.

A relação entre as tabelas é feita por uma chave estrangeira. Assim, vários funcionários podem pertencer ao mesmo departamento.

### Dados utilizados nos testes

A prática pode começar com três departamentos:

- Tecnologia
- Financeiro
- Recursos Humanos

Também serão cadastrados oito funcionários distribuídos entre esses setores.

Os registros servem de base para testar os métodos do Peewee, permitindo consultar funcionários por idade, pesquisar nomes, ordenar salários, contar funcionários por departamento e somar os salários de cada setor.

Para evitar duplicações, o programa pode verificar se os dados iniciais já existem antes de inseri-los.

### Consultas realizadas

A aplicação deverá demonstrar as seguintes operações:

1. Buscar funcionários que atendam a condições específicas.
2. Pesquisar nomes utilizando `contains()` e `startswith()`.
3. Ordenar funcionários por nome, idade ou salário.
4. Dividir os registros em páginas com `paginate()`.
5. Selecionar apenas os campos necessários.
6. Contar os funcionários de cada departamento.
7. Somar os salários agrupados por departamento.
8. Comparar o acesso aos departamentos usando diferentes estratégias de consulta.

### Comparação das estratégias

Para analisar o problema N+1, serão executados três testes:

**Teste 1 — Consulta sem otimização**

Os funcionários são carregados inicialmente e seus departamentos são acessados individualmente. Isso pode gerar consultas extras ao banco de dados.

**Teste 2 — Consulta com `join()`**

Os funcionários e seus departamentos são recuperados por meio de uma junção SQL, permitindo acessar as informações relacionadas sem uma consulta adicional para cada funcionário.

**Teste 3 — Consulta com `prefetch()`**

Os dados dos funcionários e dos departamentos são carregados antecipadamente, reduzindo a necessidade de consultas individuais.

O tempo de cada teste pode ser medido com `time.perf_counter()`. Para contar as consultas, podemos utilizar um contador próprio que acompanhe a execução de comandos SQL.

---

##  Como executar o projeto

### 1. Instalar a biblioteca

Abra o terminal do VS Code e execute:

```bash
pip install peewee
```

### 2. Executar o programa

Se o arquivo principal estiver nomeado como `pratica.py`, utilize:

```bash
python pratica.py
```

O programa deverá criar o banco SQLite automaticamente, cadastrar os dados iniciais quando necessário e executar as consultas demonstrativas.

O nome do arquivo do banco poderá ser `empresa.db`, separando essa prática da atividade anterior.

---

## 📊 Avaliação do desempenho

O objetivo da comparação é verificar como a quantidade de consultas SQL e o tempo de execução se comportam nas três estratégias.

| Estratégia | Consultas SQL | Tempo de execução |
|---|---:|---:|
| Sem otimização | A medir | A medir |
| Com `join()` | A medir | A medir |
| Com `prefetch()` | A medir | A medir |

Os resultados devem ser preenchidos após executar o programa com os dados cadastrados.

### Como interpretar os resultados

Na consulta sem otimização, a quantidade de consultas pode aumentar conforme o número de funcionários, caso o acesso a cada departamento provoque uma nova busca.

Com `join()`, os dados relacionados podem ser obtidos em uma única consulta SQL, quando a consulta é estruturada dessa forma.

Com `prefetch()`, normalmente são realizadas consultas separadas para carregar os funcionários e os departamentos relacionados. Mesmo assim, os acessos individuais podem ser evitados.

A comparação permite observar que diminuir a quantidade de consultas é uma forma de otimizar o acesso ao banco. Entretanto, o tempo de execução também depende da estrutura da consulta, do volume de dados e das condições do computador.

**Importante:** os valores de tempo e de quantidade de consultas precisam ser obtidos na execução real do programa. Não é adequado utilizar números de uma prática diferente como se fossem resultados deste banco de dados.

---

##  Conclusão

A atividade permitiu estudar diferentes recursos oferecidos pelo Peewee para consultar e organizar informações armazenadas em um banco de dados.

Com os filtros, aprendemos a localizar registros de acordo com condições específicas. A ordenação e a paginação ajudam a organizar os resultados, enquanto os agrupamentos e as funções de agregação permitem produzir informações resumidas.

Outro ponto importante foi compreender como o problema N+1 pode gerar consultas desnecessárias. As técnicas `join()` e `prefetch()` oferecem alternativas para diminuir esse tipo de operação e tornar o acesso aos dados mais eficiente.

Por fim, a prática com departamentos e funcionários demonstra como esses conceitos podem ser aplicados em um cenário diferente, reforçando a importância de desenvolver consultas que atendam às necessidades do sistema sem desperdiçar recursos.

---

**Tema:** Consultas Avançadas, Filtros e Otimização de Performance

**Bibliotecas principais:** Python, Peewee e SQLite.
