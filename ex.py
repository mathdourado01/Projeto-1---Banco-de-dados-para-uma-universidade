from faker import Faker
import itertools
from supabase import create_client, Client

# ============================
# Configurações do Supabase
# ============================
url = "https://ckvrlploqcolcsehibre.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNrdnJscGxvcWNvbGNzZWhpYnJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyNTc5MTMsImV4cCI6MjA1OTgzMzkxM30._YRvMwADA_6Qaez4iKZAp_Jc-LNoQGVtGP3H_LseZXk"
supabase: Client = create_client(url, key)
fake = Faker("pt_BR")

# =====================================================
<<<<<<< HEAD
# 1. Limpeza das Tabelas (em ordem para respeitar FKs)
# =====================================================
# Para cada tabela, use a coluna que existe como chave para garantir a deleção
supabase.table("disciplina_aluno").delete().neq("matricula_aluno", "").execute()
=======
# 1. Limpeza das Tabelas (ordem de deleção)
# =====================================================
supabase.table("disciplina_aluno").delete().neq("id_disciplina", -1).execute()
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
supabase.table("disciplina_professor").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_historicoescolar").delete().neq("id_disciplina", -1).execute()
supabase.table("historicodisciplina_professor").delete().neq("id_professor", -1).execute()
<<<<<<< HEAD
supabase.table("disciplinas_lecionadasprofessor").delete().neq("id_disciplinalecionadas", -1).execute()
=======
supabase.table("disciplinas_lecionadasprofessor").delete().neq("id_disciplina", -1).execute()  # Se ainda existir
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
supabase.table("departamento_professor").delete().neq("id_professor", -1).execute()
supabase.table("disciplina_curso").delete().neq("id_curso", -1).execute()
supabase.table("historico_escolar").delete().neq("id_historicoescolar", -1).execute()
supabase.table("disciplinas").delete().neq("id_disciplina", -1).execute()
supabase.table("professores").delete().neq("id_professor", -1).execute()
supabase.table("aluno").delete().neq("matricula_aluno", "").execute()
supabase.table("tccs").delete().neq("id_tcc", -1).execute()
supabase.table("cursos").delete().neq("id_curso", -1).execute()
supabase.table("departamentos").delete().neq("id_departamento", -1).execute()
<<<<<<< HEAD
 # valor fictício para deletar TODOS
=======
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9

print("🧹 Tabelas limpas com sucesso!\n")

# =====================================================
<<<<<<< HEAD
# 2. Inserção de Departamentos (fixos)
# =====================================================
departamentos = [
    {"id_departamento": 1, "nome_departamento": "Engenharia"},
    {"id_departamento": 2, "nome_departamento": "Ciências Exatas"},
    {"id_departamento": 3, "nome_departamento": "Administração"}
=======
# 2. Inserção de Departamentos
# =====================================================
nomes_departamentos = [
    "Engenharia",
    "Ciências Exatas",
    "Administração"
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
]
for dept in departamentos:
    supabase.table("departamentos").insert(dept).execute()

print("✅ Departamentos inseridos:")
print(departamentos, "\n")

# =====================================================
<<<<<<< HEAD
# 3. Inserção de Cursos (fixos)
# =====================================================
# Mapeamento: curso -> {duracao, id_departamento}
cursos_fixos = {
    "Engenharia Elétrica": {"duracao_curso": 5, "id_departamento": 1},
    "Engenharia Mecânica": {"duracao_curso": 5, "id_departamento": 1},
    "Engenharia de Produção": {"duracao_curso": 5, "id_departamento": 1},
    "Engenharia Civil": {"duracao_curso": 5, "id_departamento": 1},
    "Engenharia de Automação e Controle": {"duracao_curso": 5, "id_departamento": 1},
    "Engenharia Química": {"duracao_curso": 5, "id_departamento": 1},
    "Ciência da Computação": {"duracao_curso": 4, "id_departamento": 2},
    "Ciência de Dados e IA": {"duracao_curso": 5, "id_departamento": 2},
    "Administração": {"duracao_curso": 4, "id_departamento": 3}
}

cursos = []
curso_id = 1
for nome, info in cursos_fixos.items():
=======
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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
    curso = {
        "id_curso": curso_id,
        "nome_curso": nome,
        "duracao_curso": info["duracao_curso"],
        "id_departamento": info["id_departamento"]
    }
    cursos.append(curso)
    supabase.table("cursos").insert(curso).execute()
    curso_id += 1

print("✅ Cursos inseridos:")
for c in cursos:
    print(c)
print("")

# =====================================================
<<<<<<< HEAD
# 4. Inserção de TCCs (um por curso, em ordem)
# =====================================================
=======
# 4. Inserção de TCCs
# =====================================================
num_tccs = 5
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
tccs = []
tcc_id = 1
for curso in cursos:
    tcc = {
        "id_tcc": tcc_id,
        "titulo_tcc": f"TCC do curso {curso['nome_curso']} - Projeto {tcc_id}",
        "nota_tcc": 8.0 + tcc_id * 0.1,  # valores fixos
        "id_curso": curso["id_curso"]
    }
    tccs.append(tcc)
    supabase.table("tccs").insert(tcc).execute()
<<<<<<< HEAD
    tcc_id += 1

print("✅ TCCs inseridos:")
for t in tccs:
    print(t)
print("")

# =====================================================
# 5. Inserção de Alunos (fixos, 10 alunos, distribuição round-robin pelos cursos)
# =====================================================
=======

print("✅ TCCs inseridos:")
print(tccs)
print("\n")

# =====================================================
# 5. Inserção de Alunos
# =====================================================
num_alunos = 10
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
alunos = []
matriculas = [f"2024{i:04}" for i in range(1, 11)]
curso_ids = [c["id_curso"] for c in cursos]  # lista de cursos
# Distribui alunos sequencialmente pelos cursos (round-robin)
for i, mat in enumerate(matriculas, start=1):
    aluno = {
        "matricula_aluno": mat,
        "nome_aluno": fake.name(),
        "email_aluno": fake.email(),
        # pega o curso na ordem (ciclo)
        "id_curso": curso_ids[(i - 1) % len(curso_ids)],
        # atribui TCC: pega o TCC do curso do aluno (supondo que exista)
        "id_tcc": tccs[(i - 1) % len(tccs)]["id_tcc"]
    }
    alunos.append(aluno)
    supabase.table("aluno").insert(aluno).execute()
<<<<<<< HEAD

print("✅ Alunos inseridos:")
for a in alunos:
    print(a)
print("")

# =====================================================
# 6. Inserção de Professores (fixos)
# Sempre cria 1 Chefe e 1 Coordenador; os demais serão definidos fixamente.
professores = []

# Professor Chefe (obrigatório)
prof_chefe = {
    "id_professor": 1,
    "nome_professor": fake.name(),
    "email_professor": fake.email(),
    # Para TCC, pegue o primeiro TCC
    "id_tcc": tccs[0]["id_tcc"],
    "cargo": "Chefe"
}
professores.append(prof_chefe)
supabase.table("professores").insert(prof_chefe).execute()

# Professor Coordenador (obrigatório)
prof_coordenador = {
    "id_professor": 2,
    "nome_professor": fake.name(),
    "email_professor": fake.email(),
    "id_tcc": tccs[1]["id_tcc"],
    "cargo": "Coordenador"
}
professores.append(prof_coordenador)
supabase.table("professores").insert(prof_coordenador).execute()

# Outros 3 professores, definidos fixamente
outros = [
    {"id_professor": 3, "cargo": "Nenhum"},
    {"id_professor": 4, "cargo": "Nenhum"},
    {"id_professor": 5, "cargo": "Nenhum"}
]
for p in outros:
    prof = {
        "id_professor": p["id_professor"],
        "nome_professor": fake.name(),
        "email_professor": fake.email(),
        "id_tcc": tccs[p["id_professor"] % len(tccs)]["id_tcc"],
        "cargo": p["cargo"]
    }
    professores.append(prof)
    supabase.table("professores").insert(prof).execute()
=======

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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9

print("✅ Professores inseridos:")
for p in professores:
    print(p)
print("")

# =====================================================
<<<<<<< HEAD
# 7. Inserção de Disciplinas (utilizando o dicionário disciplinas_por_curso)
# Certifique-se de que "Ciência da Computação" e "Ciência de Dados e IA" contenham uma disciplina em comum ("Programação").
# Cada disciplina terá: nome, média fixa (5.0) e semestre definido pelo índice (i+1) na lista (se já existir, mantém o menor semestre)
=======
# 7. Disciplinas (dados básicos)
# =====================================================
disciplinas = []
id_disciplina = 1

>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
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
        "Inteligência Artificial",
        "Programação"
    ],
    "Ciência de Dados e IA": [
        "Aprendizado de Máquina",
        "Estatística para Dados",
        "Processamento de Linguagem Natural",
        "Deep Learning",
        "Programação"
    ],
    "Administração": [
        "Marketing",
        "Contabilidade",
        "Gestão Financeira",
        "Gestão de Pessoas"
    ]
}

<<<<<<< HEAD
disciplinas_global = {}  # chave: nome, valor: registro (com id, nome, media, semestre)
id_disciplina = 1

# Para cada curso, percorre as disciplinas e insere se ainda não existir
for curso_nome, lista_disc in disciplinas_por_curso.items():
    for idx, disc_nome in enumerate(lista_disc, start=1):
        # Se já existe, atualiza o semestre para o menor valor (caso apareça em outro curso)
        if disc_nome in disciplinas_global:
            disciplinas_global[disc_nome]["semestre_disciplina"] = min(disciplinas_global[disc_nome]["semestre_disciplina"], idx)
        else:
            novo = {
                "id_disciplina": id_disciplina,
                "nome_disciplina": disc_nome,
                "media_disciplina": 5.00,
                "semestre_disciplina": idx,
                "sigla_disciplina": "".join(word[0] for word in disc_nome.split()).upper() + str(idx)
=======
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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
            }
            disciplinas_global[disc_nome] = novo
            supabase.table("disciplinas").insert(novo).execute()
            id_disciplina += 1

disciplinas = list(disciplinas_global.values())
print("✅ Disciplinas inseridas (com sigla):")
for d in disciplinas:
    print(f"{d['nome_disciplina']} -> Sigla: {d['sigla_disciplina']} (Semestre {d['semestre_disciplina']})")
print("")

# =====================================================
<<<<<<< HEAD
# 8. Associar Disciplinas aos Cursos (tabela disciplina_curso)
# Para cada curso, associa as disciplinas referentes (usando o dicionário)
associations_curso = []
# Primeiro, cria um mapeamento curso_nome -> id_curso (usando nossos cursos fixos)
curso_nome_para_id = {c["nome_curso"]: c["id_curso"] for c in cursos}
for curso_nome, lista_disc in disciplinas_por_curso.items():
    curso_id = curso_nome_para_id.get(curso_nome)
    if curso_id:
        for disc_nome in lista_disc:
            # Associa usando o id da disciplina no disciplinas_global
            assoc = {
                "id_disciplina": disciplinas_global[disc_nome]["id_disciplina"],
                "id_curso": curso_id
            }
            supabase.table("disciplina_curso").insert(assoc).execute()
            associations_curso.append(assoc)
=======
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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9

print("✅ Associações na tabela 'disciplina_curso':")
print(associations_curso)
print("")

# =====================================================
<<<<<<< HEAD
# 9. Inserção de Histórico Escolar (fixo: 1 registro por aluno por semestre do curso)
# Para cada aluno, obtém a duração do curso e cria um histórico para cada semestre.
=======
# 9. Inserir registros em Historico_Escolar
# =====================================================
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
historicos = []
hist_id = 1
# Mapeamento curso_id -> duracao
curso_duracao = {c["id_curso"]: c["duracao_curso"] for c in cursos}

# Para cada aluno, para cada semestre de 1 até a duração, cria um registro:
for aluno in alunos:
<<<<<<< HEAD
    duracao = curso_duracao[aluno["id_curso"]]
    # Para exemplo: se semestre == 2 -> Reprovado (media 4.0), se == 3 -> Aprovado (media 6.0), senão Aprovado (media 7.0)
    for sem in range(1, duracao + 1):
        if sem == 2:
            media = 4.0
            situacao = "Reprovado"
        elif sem == 3:
            media = 6.0
            situacao = "Aprovado"
        else:
            media = 7.0
            situacao = "Aprovado"
        hist = {
            "id_historicoescolar": hist_id,
            "matricula_aluno": aluno["matricula_aluno"],
            "media_escolar": media,
            "situacao_escolar": situacao,
            "semestre_historico": sem
            }
        supabase.table("historico_escolar").insert(hist).execute()
        historicos.append(hist)
        hist_id += 1
=======
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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9

print("✅ Histórico escolar inserido:")
for h in historicos:
    print(h)
print("")

# =====================================================
<<<<<<< HEAD
# 10. Associar Disciplinas ao Histórico (tabela disciplina_historicoescolar)
# Para cada aluno, para cada histórico (semestre), associa as disciplinas do curso daquele aluno que são ofertadas no mesmo semestre.
associations_disc_hist = []
for aluno in alunos:
    # Obtenha o id do curso do aluno
    curso_id = aluno["id_curso"]
    # Pegue as associações de disciplinas para esse curso (da tabela disciplina_curso que criamos)
    disc_assoc = [assoc for assoc in associations_curso if assoc["id_curso"] == curso_id]
    # Para cada histórico do aluno:
    for hist in [h for h in historicos if h["matricula_aluno"] == aluno["matricula_aluno"]]:
        for assoc in disc_assoc:
            # Busque o registro da disciplina para saber o semestre em que ela é ofertada
            disc = next((d for d in disciplinas if d["id_disciplina"] == assoc["id_disciplina"]), None)
            if disc and disc["semestre_disciplina"] == hist["semestre_historico"]:

                rec = {
                    "id_historicoescolar": hist["id_historicoescolar"],
                    "id_disciplina": disc["id_disciplina"],
                    "semestre": disc["semestre_disciplina"]
                }
                supabase.table("disciplina_historicoescolar").insert(rec).execute()
                associations_disc_hist.append(rec)

=======
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

>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
print("✅ Associações em disciplina_historicoescolar:")
print(associations_disc_hist)
print("")

# =====================================================
<<<<<<< HEAD
# 11. Associação Disciplina-Aluno
# Cada aluno cursa todas as disciplinas do seu curso
associations_aluno = []
for aluno in alunos:
    curso_id = aluno["id_curso"]
    disc_assoc = [assoc for assoc in associations_curso if assoc["id_curso"] == curso_id]
    for assoc in disc_assoc:
        rec = {
=======
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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9
            "matricula_aluno": aluno["matricula_aluno"],
            "id_disciplina": assoc["id_disciplina"]
        }
<<<<<<< HEAD
        supabase.table("disciplina_aluno").insert(rec).execute()
        associations_aluno.append(rec)

print("✅ Associações em disciplina_aluno:")
print(associations_aluno)
print("")

# =====================================================
# 12. Associação Disciplina-Professor
# Para este exemplo, vamos associar cada disciplina a um professor fixo:
# Se o id da disciplina for par, associa ao professor 1; se ímpar, ao professor 2.
associations_prof = []
for d in disciplinas:
    prof_id = 1 if d["id_disciplina"] % 2 == 0 else 2
    rec = {
        "id_professor": prof_id,
        "id_disciplina": d["id_disciplina"]
    }
    supabase.table("disciplina_professor").insert(rec).execute()
    associations_prof.append(rec)

print("✅ Associações em disciplina_professor:")
print(associations_prof)
print("")

# =====================================================
# 13. Disciplinas Lecionadas (tabela disciplinas_lecionadasprofessor)
# Marcaremos como lecionada aquelas disciplinas cujo id seja divisível por 3.
disciplinas_lec = []
id_lec = 1
for d in disciplinas:
    if d["id_disciplina"] % 3 == 0:
        rec = {
            "id_disciplinalecionadas": id_lec,
            "nome_disciplinalecionadas": d["nome_disciplina"] + " (Lec)",
            "id_disciplina": d["id_disciplina"]
        }
        supabase.table("disciplinas_lecionadasprofessor").insert(rec).execute()
        disciplinas_lec.append(rec)
        id_lec += 1

print("✅ Registros inseridos em 'disciplinas_lecionadasprofessor':")
print(disciplinas_lec)
print("")

# =====================================================
# 14. Associação Professor - Disciplinas Lecionadas (historicodisciplina_professor)
# Para simplicidade, associamos todas as disciplinas lecionadas ao professor 1.
associations_hist_disc_prof = []
for lec in disciplinas_lec:
    rec = {
        "id_professor": 1,
        "id_disciplinalecionadas": lec["id_disciplinalecionadas"]
    }
    supabase.table("historicodisciplina_professor").insert(rec).execute()
    associations_hist_disc_prof.append(rec)

print("✅ Associações em historicodisciplina_professor (com disciplinas lecionadas):")
print(associations_hist_disc_prof)
print("")

# =====================================================
# 15. Associação Departamento-Professor
# Para fixar, atribuímos os seguintes departamentos:
# Professor 1 e 2 -> Departamento 1; Professor 3 -> Departamento 1; Professor 4 e 5 -> Departamento 2.
associations_dept_prof = []
dept_as = [
    {"id_professor": 1, "id_departamento": 1},
    {"id_professor": 2, "id_departamento": 1},
    {"id_professor": 3, "id_departamento": 1},
    {"id_professor": 4, "id_departamento": 2},
    {"id_professor": 5, "id_departamento": 2}
]
for assoc in dept_as:
    supabase.table("departamento_professor").insert(assoc).execute()
    associations_dept_prof.append(assoc)

print("✅ Associações em departamento_professor:")
print(associations_dept_prof)
print("")
=======
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
>>>>>>> da7e2c024296d8419e42c7bb16b174a8762944a9

print("✅ Script concluído com sucesso!")
