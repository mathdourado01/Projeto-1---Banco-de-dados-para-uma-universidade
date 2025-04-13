from faker import Faker
import random
from supabase import create_client, Client

# ---------------------------
# Configurações do Supabase
# ---------------------------
url = "https://ckvrlploqcolcsehibre.supabase.co"  
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNrdnJscGxvcWNvbGNzZWhpYnJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyNTc5MTMsImV4cCI6MjA1OTgzMzkxM30._YRvMwADA_6Qaez4iKZAp_Jc-LNoQGVtGP3H_LseZXk"
supabase: Client = create_client(url, key)
fake = Faker("pt_BR")

# ---------------------------
# 1. Limpar as tabelas antes de inserir novos dados
# ---------------------------
# Importante: esses comandos apagam todos os registros existentes
supabase.table("disciplinas").delete().neq("id_disciplina", 0).execute()
supabase.table("professores").delete().neq("id_professor", 0).execute()
supabase.table("aluno").delete().neq("matricula_aluno", 0).execute()
supabase.table("tccs").delete().neq("id_tcc", 0).execute()
supabase.table("cursos").delete().neq("id_curso", 0).execute()
supabase.table("departamentos").delete().neq("id_departamento", 0).execute()
print("🧹 Tabelas limpas com sucesso!\n")

# ---------------------------
# 2. Inserir dados na tabela Departamentos
# ---------------------------
nomes_departamentos = [
    "Engenharia",
    "Ciências Exatas",
    "Administração"
]

departamentos = []
for i, nome in enumerate(nomes_departamentos, start=1):
    departamento = {
        "id_departamento": i,
        "nome_departamento": nome
    }
    departamentos.append(departamento)
    supabase.table("departamentos").insert(departamento).execute()
print("✅ Departamentos inseridos:")
print(departamentos)
print("\n")

# ---------------------------
# 3. Inserir dados na tabela Cursos
# ---------------------------
# Lista de cursos possíveis inspirados na FEI
cursos_possiveis = [
    {"nome": "Engenharia Elétrica", "duracao": 5, "id_departamento": 1},
    {"nome": "Engenharia Mecânica", "duracao": 5, "id_departamento": 1},
    {"nome": "Engenharia de Produção", "duracao": 5, "id_departamento": 1},
    {"nome": "Engenharia Civil", "duracao": 5, "id_departamento": 1},
    {"nome": "Engenharia de Automação e Controle", "duracao": 5, "id_departamento": 1},
    {"nome": "Engenharia Química", "duracao": 5, "id_departamento": 1},
    {"nome": "Ciência da Computação", "duracao": 4, "id_departamento": 2},
    {"nome": "Ciência de Dados e IA", "duracao": 5, "id_departamento": 2},
    {"nome": "Administração", "duracao": 4, "id_departamento": 3}
]

num_cursos = 5
cursos_originais = random.sample(cursos_possiveis, num_cursos)

# Converter e inserir os cursos com o formato desejado (chave "nome_curso")
cursos_inseridos = []
for i, c in enumerate(cursos_originais, start=1):
    curso = {
        "id_curso": i,
        "nome_curso": c["nome"],     # Converter a chave 'nome' para 'nome_curso'
        "duracao_curso": c["duracao"],
        "id_departamento": c["id_departamento"]
    }
    cursos_inseridos.append(curso)
    supabase.table("cursos").insert(curso).execute()

print("✅ Cursos inseridos:")
print(cursos_inseridos)
print("\n")

# ---------------------------
# 4. Inserir dados na tabela TCCs
# ---------------------------
num_tccs = 5
tccs = []
for i in range(1, num_tccs + 1):
    tcc = {
        "id_tcc": i,
        "titulo_tcc": f"TCC sobre {fake.bs()}",
        "nota_tcc": round(random.uniform(6.0, 10.0), 2),
        "id_curso": random.randint(1, len(cursos_inseridos))
    }
    tccs.append(tcc)
    supabase.table("tccs").insert(tcc).execute()
print("✅ TCCs inseridos:")
print(tccs)
print("\n")

# ---------------------------
# 5. Inserir dados na tabela Aluno
# ---------------------------
num_alunos = 10
alunos = []
for i in range(1, num_alunos + 1):
    aluno = {
        "matricula_aluno": f"2024{i:04}",
        "nome_aluno": fake.name(),
        "email_aluno": fake.email(),
        "id_curso": random.randint(1, len(cursos_inseridos)),
        "id_tcc": random.randint(1, num_tccs)
    }
    alunos.append(aluno)
    supabase.table("aluno").insert(aluno).execute()
print("✅ Alunos inseridos:")
print(alunos)
print("\n")

# ---------------------------
# 6. Inserir dados na tabela Professores
# ---------------------------
num_professores = 5
professores = []
for i in range(1, num_professores + 1):
    professor = {
        "id_professor": i,
        "nome_professor": fake.name(),
        "email_professor": fake.email(),
        "id_tcc": random.randint(1, num_tccs)
    }
    professores.append(professor)
    supabase.table("professores").insert(professor).execute()
print("✅ Professores inseridos:")
print(professores)
print("\n")

# ---------------------------
# 7. Inserir disciplinas usando a tabela disciplina (sem FK direta com cursos) 
#    e depois criar a associação na tabela disciplina_curso.
# ---------------------------

# Primeiro, vamos inserir as disciplinas básicas sem o campo 'id_curso'
# (Assumindo que a tabela 'disciplinas' possui os campos: id_disciplina, nome_disciplina, media_disciplina, situacao_disciplina)
disciplinas = []
id_disciplina = 1

# Vamos iterar sobre os cursos inseridos e para cada curso procurar suas disciplinas no dicionário realista
disciplinas_por_curso = {
    "Engenharia Elétrica": [
        "Circuitos Elétricos",
        "Eletromagnetismo",
        "Sistemas de Controle",
        "Eletrônica Analógica"
    ],
    "Engenharia Mecânica": [
        "Mecânica dos Sólidos",
        "Termodinâmica",
        "Dinâmica",
        "Resistência dos Materiais"
    ],
    "Engenharia de Produção": [
        "Logística",
        "Gestão da Qualidade",
        "Planejamento da Produção",
        "Pesquisa Operacional"
    ],
    "Engenharia Civil": [
        "Estruturas de Concreto",
        "Geotecnia",
        "Hidráulica",
        "Construção Civil"
    ],
    "Engenharia de Automação e Controle": [
        "Controle de Processos",
        "Instrumentação",
        "Automação Industrial",
        "Redes Industriais"
    ],
    "Engenharia Química": [
        "Operações Unitárias",
        "Fenômenos de Transporte",
        "Reatores Químicos",
        "Química Orgânica"
    ],
    "Ciência da Computação": [
        "Algoritmos e Estruturas de Dados",
        "Sistemas Operacionais",
        "Compiladores",
        "Inteligência Artificial"
    ],
    "Ciência de Dados e IA": [
        "Aprendizado de Máquina",
        "Estatística para Dados",
        "Processamento de Linguagem Natural",
        "Deep Learning"
    ],
    "Administração": [
        "Marketing",
        "Contabilidade",
        "Gestão Financeira",
        "Gestão de Pessoas"
    ]
}

# Inserir as disciplinas básicas na tabela "disciplinas"
for curso in cursos_inseridos:
    nome_curso = curso["nome_curso"]
    # Se houver disciplinas definidas para esse curso, insere todas elas
    if nome_curso in disciplinas_por_curso:
        for nome_disciplina in disciplinas_por_curso[nome_curso]:
            media = round(random.uniform(0, 10), 2)
            situacao = "Aprovado" if media >= 5.0 else "Reprovado"
            disciplina = {
                "id_disciplina": id_disciplina,
                "nome_disciplina": nome_disciplina,
                "media_disciplina": media,
                "situacao_disciplina": situacao
                # Note que NÃO inserimos o campo 'id_curso' aqui, pois usaremos a tabela associativa
            }
            supabase.table("disciplinas").insert(disciplina).execute()
            disciplinas.append(disciplina)
            id_disciplina += 1

print("✅ Disciplinas inseridas (sem associação direta com curso):")
print(disciplinas)
print("\n")

# Agora, insere as associações na tabela "disciplina_curso"
# A tabela associativa "disciplina_curso" deve ter ao menos os campos: id_disciplina e id_curso
associations = []
for curso in cursos_inseridos:
    nome_curso = curso["nome_curso"]
    id_curso = curso["id_curso"]
    # Se o curso possui disciplinas cadastradas no dicionário realista, pegue seus nomes
    if nome_curso in disciplinas_por_curso:
        disciplinas_do_curso = disciplinas_por_curso[nome_curso]
        # Para cada disciplina cadastrada para esse curso, encontre o id correspondente
        for nome_disciplina in disciplinas_do_curso:
            # Procura na lista de disciplinas inseridas por aquele nome
            for disc in disciplinas:
                if disc["nome_disciplina"] == nome_disciplina:
                    association = {
                        "id_disciplina": disc["id_disciplina"],
                        "id_curso": id_curso
                    }
                    supabase.table("disciplina_curso").insert(association).execute()
                    associations.append(association)
                    break

print("✅ Associações inseridas na tabela 'disciplina_curso':")
print(associations)
