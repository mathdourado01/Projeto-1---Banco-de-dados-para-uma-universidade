from faker import Faker
import random
from supabase import create_client, Client

# ============================
# Configurações do Supabase
# ============================
url = "https://ckvrlploqcolcsehibre.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNrdnJscGxvcWNvbGNzZWhpYnJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyNTc5MTMsImV4cCI6MjA1OTgzMzkxM30._YRvMwADA_6Qaez4iKZAp_Jc-LNoQGVtGP3H_LseZXk"
supabase: Client = create_client(url, key)
fake = Faker("pt_BR")

# ============================
# 1. Limpeza das Tabelas
# ============================
# Para evitar violação de constraints, a ordem é importante:
# Deletar dependentes primeiro (associações e históricos), depois entidades principais
supabase.table("disciplina_aluno").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_professor").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_historicoescolar").delete().neq("id_historicoescolar", -1).execute()
supabase.table("historicodisciplina_professor").delete().neq("id_professor", -1).execute()
supabase.table("departamento_professor").delete().neq("id_professor", -1).execute()
supabase.table("disciplina_aluno").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_professor").delete().neq("id_professor", -1).execute()
supabase.table("disciplina_curso").delete().neq("id_curso", -1).execute()
supabase.table("historico_escolar").delete().neq("id_historicoescolar", -1).execute()  # <-- Adiciona isso antes de aluno
supabase.table("disciplinas").delete().neq("id_disciplina", -1).execute()
supabase.table("professores").delete().neq("id_professor", -1).execute()
supabase.table("aluno").delete().neq("matricula_aluno", "").execute()
supabase.table("tccs").delete().neq("id_tcc", -1).execute()
supabase.table("cursos").delete().neq("id_curso", -1).execute()
supabase.table("departamentos").delete().neq("id_departamento", -1).execute()



print("🧹 Tabelas limpas com sucesso!\n")

# ============================
# 2. Inserção dos Departamentos
# ============================
nomes_departamentos = [
    "Engenharia",
    "Ciências Exatas",
    "Administração"
]

departamentos = []
for i, nome in enumerate(nomes_departamentos, start=1):
    dept = {
        "id_departamento": i,
        "nome_departamento": nome
    }
    departamentos.append(dept)
    supabase.table("departamentos").insert(dept).execute()

print("✅ Departamentos inseridos:")
print(departamentos)
print("\n")

# ============================
# 3. Inserção dos Cursos
# ============================
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

# Converter para o formato desejado: a chave 'nome' vira 'nome_curso'
cursos_inseridos = []
for i, c in enumerate(cursos_originais, start=1):
    curso = {
        "id_curso": i,
        "nome_curso": c["nome"],
        "duracao_curso": c["duracao"],
        "id_departamento": c["id_departamento"]
    }
    cursos_inseridos.append(curso)
    supabase.table("cursos").insert(curso).execute()

print("✅ Cursos inseridos:")
print(cursos_inseridos)
print("\n")

# ============================
# 4. Inserção dos TCCs
# ============================
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

# ============================
# 5. Inserção dos Alunos
# ============================
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

# ============================
# 6. Inserção dos Professores
# ============================
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

# ============================
# 7. Inserção das Disciplinas (dados básicos sem FK direta com cursos)
# ============================
disciplinas = []
id_disciplina = 1

# Dicionário realista de disciplinas por curso
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

# Para cada curso inserido, se houver disciplinas definidas para ele, inserir as disciplinas básicas
for curso in cursos_inseridos:
    nome_curso = curso["nome_curso"]
    if nome_curso in disciplinas_por_curso:
        for nome_disciplina in disciplinas_por_curso[nome_curso]:
            media = 5.0
            situacao = "Aprovado" if media >= 5.0 else "Reprovado"
            disciplina = {
                "id_disciplina": id_disciplina,
                "nome_disciplina": nome_disciplina,
                "media_disciplina": media,
                "situacao_disciplina": situacao
                # Não inserimos id_curso aqui, pois usaremos a tabela associativa "disciplina_curso"
            }
            supabase.table("disciplinas").insert(disciplina).execute()
            disciplinas.append(disciplina)
            id_disciplina += 1

print("✅ Disciplinas inseridas (sem associação direta):")
print(disciplinas)
print("\n")

# ============================
# 8. Inserção das associações na tabela "disciplina_curso"
# ============================
associations_curso = []
for curso in cursos_inseridos:
    nome_curso = curso["nome_curso"]
    id_curso = curso["id_curso"]
    if nome_curso in disciplinas_por_curso:
        for nome_disciplina in disciplinas_por_curso[nome_curso]:
            # Procura na lista de disciplinas inseridas para encontrar o id correspondente
            for disc in disciplinas:
                if disc["nome_disciplina"] == nome_disciplina:
                    association = {
                        "id_disciplina": disc["id_disciplina"],
                        "id_curso": id_curso
                    }
                    supabase.table("disciplina_curso").insert(association).execute()
                    associations_curso.append(association)
                    break

print("✅ Associações inseridas na tabela 'disciplina_curso':")
print(associations_curso)
print("\n")

# ============================
# 9. Inserção dos registros na tabela Historico_Escolar
# ============================
historicos = []
id_historico = 1
for aluno in alunos:
    media_geral = round(random.uniform(0, 10), 2)
    situacao = "Aprovado" if media_geral >= 5.0 else "Reprovado"
    historico = {
        "id_historicoescolar": id_historico,
        "matricula_aluno": aluno["matricula_aluno"],
        "media_escolar": media_geral,
        "situacao_escolar": situacao
    }
    supabase.table("historico_escolar").insert(historico).execute()
    historicos.append(historico)
    id_historico += 1

print("✅ Historicos escolares inseridos:")
print(historicos)
print("\n")

# ============================
# 10. Inserção das associações na tabela "disciplina_historicoescolar"
# ============================
associations_disc_hist = []
for hist in historicos:
    num_disc = random.randint(1, min(3, len(disciplinas)))
    disciplinas_selecionadas = random.sample(disciplinas, num_disc)
    for disc in disciplinas_selecionadas:
        assoc = {
            "id_historicoescolar": hist["id_historicoescolar"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("disciplina_historicoescolar").insert(assoc).execute()
        associations_disc_hist.append(assoc)

print("✅ Associações inseridas em disciplina_historicoescolar:")
print(associations_disc_hist)
print("\n")

# ============================
# 11. Inserção das associações na tabela "departamento_professor"
# ============================
associations_dept_prof = []
for professor in professores:
    num_depts = random.randint(1, min(2, len(departamentos)))
    depts_selecionados = random.sample(departamentos, num_depts)
    for dept in depts_selecionados:
        association = {
            "id_professor": professor["id_professor"],
            "id_departamento": dept["id_departamento"]
        }
        supabase.table("departamento_professor").insert(association).execute()
        associations_dept_prof.append(association)

print("✅ Associações inseridas em departamento_professor:")
print(associations_dept_prof)
print("\n")

# ============================
# 12. Inserção das associações na tabela "historicodisciplina_professor"
# ============================
associations_hist_disc_prof = []
for professor in professores:
    num_assoc = random.randint(1, min(2, len(disciplinas)))
    disciplinas_selecionadas = random.sample(disciplinas, num_assoc)
    for disc in disciplinas_selecionadas:
        assoc = {
            "id_professor": professor["id_professor"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("historicodisciplina_professor").insert(assoc).execute()
        associations_hist_disc_prof.append(assoc)

print("✅ Associações inseridas em historicodisciplina_professor:")
print(associations_hist_disc_prof)

# Inserir associações na tabela disciplina_aluno
associations_aluno = []
for aluno in alunos:
    num_assoc = random.randint(1, min(3, len(disciplinas)))
    disciplinas_selecionadas = random.sample(disciplinas, num_assoc)
    for disc in disciplinas_selecionadas:
        association = {
            "matricula_aluno": aluno["matricula_aluno"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("disciplina_aluno").insert(association).execute()
        associations_aluno.append(association)
print("✅ Associações em disciplina_aluno inseridas:")
print(associations_aluno)
print("\n")

# Inserir associações na tabela disciplina_professor
associations_prof = []
for professor in professores:
    num_assoc = random.randint(1, min(3, len(disciplinas)))
    disciplinas_selecionadas = random.sample(disciplinas, num_assoc)
    for disc in disciplinas_selecionadas:
        association = {
            "id_professor": professor["id_professor"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("disciplina_professor").insert(association).execute()
        associations_prof.append(association)
print("✅ Associações em disciplina_professor inseridas:")
print(associations_prof)
print("\n")
