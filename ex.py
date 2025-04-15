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

# =====================================================
# 1. Limpeza das Tabelas (ordem de deleção)
# =====================================================
supabase.table("disciplina_aluno").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_professor").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_historicoescolar").delete().neq("id_historicoescolar", -1).execute()
supabase.table("historicodisciplina_professor").delete().neq("id_professor", -1).execute()
supabase.table("disciplinas_lecionadasprofessor").delete().neq("id_disciplina", -1).execute()  # Se ainda existir
supabase.table("departamento_professor").delete().neq("id_professor", -1).execute()
supabase.table("disciplina_curso").delete().neq("id_curso", -1).execute()
supabase.table("historico_escolar").delete().neq("id_historicoescolar", -1).execute()
supabase.table("disciplinas").delete().neq("id_disciplina", -1).execute()
supabase.table("professores").delete().neq("id_professor", -1).execute()
supabase.table("aluno").delete().neq("matricula_aluno", "").execute()
supabase.table("tccs").delete().neq("id_tcc", -1).execute()
supabase.table("cursos").delete().neq("id_curso", -1).execute()
supabase.table("departamentos").delete().neq("id_departamento", -1).execute()

print("🧹 Tabelas limpas com sucesso!\n")

# =====================================================
# 2. Inserção de Departamentos
# =====================================================
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

# =====================================================
# 3. Inserção de Cursos
# =====================================================
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

# =====================================================
# 4. Inserção de TCCs
# =====================================================
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

# =====================================================
# 5. Inserção de Alunos
# =====================================================
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

# =====================================================
# 6. Inserção de Professores (AGORA usando TCCs válidos)
# =====================================================
num_professores = 5
professores = []

# Se quiser atribuir 'cargo' (ex: 'Chefe', 'Coordenador', 'Nenhum'), defina:
cargos_possiveis = ["Chefe", "Coordenador", "Nenhum"]

for i in range(1, num_professores + 1):
    professor = {
        "id_professor": i,
        "nome_professor": fake.name(),
        "email_professor": fake.email(),
        # Agora usando id_tcc válido
        "id_tcc": random.choice([t["id_tcc"] for t in tccs]),
        # Se quiser cargo no professor
        "cargo": random.choice(cargos_possiveis)
    }
    professores.append(professor)
    supabase.table("professores").insert(professor).execute()

print("✅ Professores inseridos:")
print(professores)
print("\n")

# =====================================================
# 7. Disciplinas (dados básicos)
# =====================================================
disciplinas = []
id_disciplina = 1

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
            }
            supabase.table("disciplinas").insert(disciplina).execute()
            disciplinas.append(disciplina)
            id_disciplina += 1

print("✅ Disciplinas inseridas (sem associação direta):")
print(disciplinas)
print("\n")

# =====================================================
# 8. Associar disciplinas a cursos (disciplina_curso)
# =====================================================
associations_curso = []
for curso in cursos_inseridos:
    nome_curso = curso["nome_curso"]
    id_curso = curso["id_curso"]
    if nome_curso in disciplinas_por_curso:
        for nome_disciplina in disciplinas_por_curso[nome_curso]:
            # Procura disciplina na lista
            for disc in disciplinas:
                if disc["nome_disciplina"] == nome_disciplina:
                    association = {
                        "id_disciplina": disc["id_disciplina"],
                        "id_curso": id_curso
                    }
                    supabase.table("disciplina_curso").insert(association).execute()
                    associations_curso.append(association)
                    break

print("✅ Associações na tabela 'disciplina_curso':")
print(associations_curso)
print("\n")

# =====================================================
# 9. Inserir registros em Historico_Escolar
# =====================================================
historicos = []
id_historico = 1
for aluno in alunos:
    media_geral = round(random.uniform(0, 10), 2)
    situacao = "Aprovado" if media_geral >= 5.0 else "Reprovado"
    hist = {
        "id_historicoescolar": id_historico,
        "matricula_aluno": aluno["matricula_aluno"],
        "media_escolar": media_geral,
        "situacao_escolar": situacao
    }
    supabase.table("historico_escolar").insert(hist).execute()
    historicos.append(hist)
    id_historico += 1

print("✅ Historicos escolares inseridos:")
print(historicos)
print("\n")

# =====================================================
# 10. Associar disciplinas ao histórico (disciplina_historicoescolar)
# =====================================================
associations_disc_hist = []
for hist in historicos:
    qtd = random.randint(1, min(3, len(disciplinas)))
    discs_sel = random.sample(disciplinas, qtd)
    for disc in discs_sel:
        assoc = {
            "id_historicoescolar": hist["id_historicoescolar"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("disciplina_historicoescolar").insert(assoc).execute()
        associations_disc_hist.append(assoc)

print("✅ Associações em disciplina_historicoescolar:")
print(associations_disc_hist)
print("\n")

# =====================================================
# 11. Ligação departamento_professor
# =====================================================
# em vez de rodar o for _ in range(num_depts):
# e random.randint(1, 3), faça assim:

associations_dept_prof = []
for professor in professores:
    # Lista de IDs possíveis
    possible_depts = [1, 2, 3]
    
    # Escolhe de 1 a 2 departamentos únicos
    num_depts = random.randint(1, 2)
    dept_selecionados = random.sample(possible_depts, num_depts)

    for dept_id in dept_selecionados:
        assoc = {
            "id_professor": professor["id_professor"],
            "id_departamento": dept_id
        }
        supabase.table("departamento_professor").insert(assoc).execute()
        associations_dept_prof.append(assoc)

print("✅ Associações em departamento_professor:")
print(associations_dept_prof)
print("\n")


# =====================================================
# 12. Tabela historicodisciplina_professor
# =====================================================
associations_hist_disc_prof = []
for professor in professores:
    qtd = random.randint(1, 2)
    discs_sel = random.sample(disciplinas, qtd)
    for disc in discs_sel:
        assoc = {
            "id_professor": professor["id_professor"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("historicodisciplina_professor").insert(assoc).execute()
        associations_hist_disc_prof.append(assoc)

print("✅ Associações em historicodisciplina_professor:")
print(associations_hist_disc_prof)

# =====================================================
# Associação disciplina_aluno
# =====================================================
associations_aluno = []
for aluno in alunos:
    qtd = random.randint(1, min(3, len(disciplinas)))
    discs_sel = random.sample(disciplinas, qtd)
    for disc in discs_sel:
        assoc = {
            "matricula_aluno": aluno["matricula_aluno"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("disciplina_aluno").insert(assoc).execute()
        associations_aluno.append(assoc)

print("✅ Associações em disciplina_aluno:")
print(associations_aluno)
print("\n")

# =====================================================
# Associação disciplina_professor
# =====================================================
associations_prof = []
for professor in professores:
    qtd = random.randint(1, min(3, len(disciplinas)))
    discs_sel = random.sample(disciplinas, qtd)
    for disc in discs_sel:
        assoc = {
            "id_professor": professor["id_professor"],
            "id_disciplina": disc["id_disciplina"]
        }
        supabase.table("disciplina_professor").insert(assoc).execute()
        associations_prof.append(assoc)

print("✅ Associações em disciplina_professor:")
print(associations_prof)
print("\n")

print("✅ Script concluído com sucesso!")
