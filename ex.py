from faker import Faker
import itertools
from supabase import create_client, Client
import random

# ============================
# Configurações do Supabase
# ============================
url = "https://ckvrlploqcolcsehibre.supabase.co"
key = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
       "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNrdnJscGxvcWNvbGNzZWhpYnJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQyNTc5MTMsImV4cCI6MjA1OTgzMzkxM30._YRvMwADA_6Qaez4iKZAp_Jc-LNoQGVtGP3H_LseZXk")
supabase: Client = create_client(url, key)
fake = Faker("pt_BR")

# =====================================================
# 1. Limpeza das Tabelas (respeitando FK)
# =====================================================
supabase.table("disciplina_aluno").delete().neq("matricula_aluno", "").execute()
supabase.table("disciplina_professor").delete().neq("id_disciplina", -1).execute()
supabase.table("disciplina_historicoescolar").delete().neq("id_disciplina", -1).execute()
supabase.table("historicodisciplina_professor").delete().neq("id_professor", -1).execute()
supabase.table("disciplinas_lecionadasprofessor").delete().neq("id_disciplinalecionadas", -1).execute()
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
# 2. Inserção de Departamentos (fixos)
# =====================================================
departamentos = [
    {"id_departamento": 1, "nome_departamento": "Engenharia"},
    {"id_departamento": 2, "nome_departamento": "Ciências Exatas"},
    {"id_departamento": 3, "nome_departamento": "Administração"}
]
for dept in departamentos:
    supabase.table("departamentos").insert(dept).execute()

print("✅ Departamentos inseridos:")
print(departamentos, "\n")

# =====================================================
# 3. Inserção de Cursos (fixos)
# =====================================================
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

# Mapeamento: id_curso → nome (para uso posterior)
curso_id_para_nome = {c["id_curso"]: c["nome_curso"] for c in cursos}

# =====================================================
# 4. Inserção de TCCs (um por curso, em ordem)
# =====================================================
tccs = []
tcc_id = 1
for curso in cursos:
    tcc = {
        "id_tcc": tcc_id,
        "titulo_tcc": f"TCC do curso {curso['nome_curso']} - Projeto {tcc_id}",
        "nota_tcc": 8.0 + tcc_id * 0.1,
        "id_curso": curso["id_curso"]
    }
    tccs.append(tcc)
    supabase.table("tccs").insert(tcc).execute()
    tcc_id += 1
print("✅ TCCs inseridos:")
for t in tccs:
    print(t)
print("")

# =====================================================
# 5. Inserção de Alunos (100 alunos)
# Distribuição: os 60 primeiros alunos serão atribuídos ao curso "Ciência da Computação" (id 7)
# e os demais serão distribuídos entre os outros cursos.
alunos = []
numero_alunos = 100
matriculas = [f"2024{i:04}" for i in range(1, numero_alunos + 1)]
tcc_ids = [tc["id_tcc"] for tc in tccs]
curso_ids = [c["id_curso"] for c in cursos]
# Lista de cursos disponíveis, exceto o curso 7 (Ciência da Computação)
outros_cursos = [cid for cid in curso_ids if cid != 7]

for i, mat in enumerate(matriculas, start=1):
    if i <= 60:
        # Os 60 primeiros alunos vão para "Ciência da Computação" (id 7)
        id_curso_escolhido = 7
    else:
        # Os demais distribuídos entre os outros cursos em round-robin
        id_curso_escolhido = outros_cursos[(i - 61) % len(outros_cursos)]
    # Para TCC, também usamos round-robin entre todos os TCCs
    id_tcc_escolhido = tcc_ids[(i - 1) % len(tcc_ids)]
    aluno = {
        "matricula_aluno": mat,
        "nome_aluno": fake.name(),
        "email_aluno": fake.email(),
        "id_curso": id_curso_escolhido,
        "id_tcc": id_tcc_escolhido
    }
    alunos.append(aluno)
    supabase.table("aluno").insert(aluno).execute()
print("✅ Alunos inseridos (100):")
for a in alunos:
    print(a)
print("")

# =====================================================
# 6. Inserção de Professores (20 professores)
# Garantir: cada departamento tem 1 Chefe e cada curso tem 1 Coordenador.
professores = []
next_prof_id = 1

# Professores Chefe: 1 para cada departamento (3 no total)
for dept in departamentos:
    prof = {
        "id_professor": next_prof_id,
        "nome_professor": fake.name(),
        "email_professor": fake.email(),
        "id_tcc": random.choice(tcc_ids),
        "cargo": "Chefe"
    }
    professores.append(prof)
    supabase.table("professores").insert(prof).execute()
    next_prof_id += 1

# Professores Coordenador: 1 para cada curso (9 no total)
for curso in cursos:
    prof = {
        "id_professor": next_prof_id,
        "nome_professor": fake.name(),
        "email_professor": fake.email(),
        "id_tcc": tccs[curso["id_curso"] - 1]["id_tcc"],
        "cargo": "Coordenador"
    }
    professores.append(prof)
    supabase.table("professores").insert(prof).execute()
    next_prof_id += 1

# Professores adicionais (cargo "Nenhum") para completar 20
while next_prof_id <= 20:
    prof = {
        "id_professor": next_prof_id,
        "nome_professor": fake.name(),
        "email_professor": fake.email(),
        "id_tcc": random.choice(tcc_ids),
        "cargo": "Nenhum"
    }
    professores.append(prof)
    supabase.table("professores").insert(prof).execute()
    next_prof_id += 1

print("✅ Professores inseridos (20):")
for p in professores:
    print(p)
print("")

# =====================================================
# 7. Inserção de Disciplinas (10 por curso)
# Cada curso terá 10 disciplinas com nomes fixos.
disciplinas_por_curso = {
    "Engenharia Elétrica": [
        "Circuitos Elétricos","Eletromagnetismo","Sistemas de Controle","Eletrônica Analógica","Máquinas Elétricas",
        "Potência e Máquinas","Eletrônica de Potência","Conversão de Energia","Telemetria Elétrica","Instrumentação Elétrica"
    ],
    "Engenharia Mecânica": [
        "Mecânica dos Sólidos","Termodinâmica","Dinâmica","Resistência dos Materiais","Materiais de Engenharia",
        "Mecânica dos Fluidos","Controle de Processos Mecânicos","Projeto Mecânico","Fabricação Mecânica","Desenho Técnico"
    ],
    "Engenharia de Produção": [
        "Logística","Gestão da Qualidade","Planejamento da Produção","Pesquisa Operacional","Engenharia de Métodos",
        "Estatística Aplicada","Simulação de Processos","Gerenciamento de Projetos","Gestão de Custos","Inovação e Empreendedorismo"
    ],
    "Engenharia Civil": [
        "Estruturas de Concreto","Geotecnia","Hidráulica","Construção Civil","Pavimentação",
        "Mecânica dos Solos","Saneamento Ambiental","Projeto Estrutural","Resistência dos Materiais","Topografia"
    ],
    "Engenharia de Automação e Controle": [
        "Controle de Processos","Instrumentação","Automação Industrial","Redes Industriais","Sistemas de Supervisão",
        "Robótica Industrial","Sinais e Sistemas","Eletrônica Digital","Modelagem e Simulação","Integração de Sistemas"
    ],
    "Engenharia Química": [
        "Operações Unitárias","Fenômenos de Transporte","Reatores Químicos","Química Orgânica","Processos Químicos",
        "Termodinâmica Química","Equilíbrio Químico","Processos de Separação","Controle de Processos","Tecnologia dos Polímeros"
    ],
    "Ciência da Computação": [
        "Algoritmos e Estruturas de Dados","Sistemas Operacionais","Compiladores","Inteligência Artificial","Programação",
        "Banco de Dados","Redes de Computadores","Arquitetura de Computadores","Engenharia de Software","Computação Gráfica"
    ],
    "Ciência de Dados e IA": [
        "Aprendizado de Máquina","Estatística para Dados","Processamento de Linguagem Natural","Deep Learning","Programação",
        "Mineração de Dados","Visualização de Dados","Big Data","Inteligência Computacional","Modelos Preditivos"
    ],
    "Administração": [
        "Marketing","Contabilidade","Gestão Financeira","Gestão de Pessoas","Economia Empresarial",
        "Estratégia e Planejamento","Comportamento Organizacional","Gestão de Operações","Recursos Humanos","Gestão de Projetos"
    ]
}

disciplinas_global = {}  # mapeia: nome_disciplina → registro
id_disciplina = 1
for curso_nome, lista_disc in disciplinas_por_curso.items():
    for idx, disc_nome in enumerate(lista_disc, start=1):
        if disc_nome in disciplinas_global:
            disciplinas_global[disc_nome]["semestre_disciplina"] = min(disciplinas_global[disc_nome]["semestre_disciplina"], idx)
        else:
            novo = {
                "id_disciplina": id_disciplina,
                "nome_disciplina": disc_nome,
                "media_disciplina": 5.00,
                "semestre_disciplina": idx,
                "sigla_disciplina": "".join(word[0] for word in disc_nome.split()).upper() + str(idx)
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
# 8. Associação Disciplina-Curso (tabela disciplina_curso)
# =====================================================
associations_curso = []
curso_nome_para_id = {c["nome_curso"]: c["id_curso"] for c in cursos}
for curso_nome, lista_disc in disciplinas_por_curso.items():
    cid = curso_nome_para_id[curso_nome]
    for disc_nome in lista_disc:
        assoc = {
            "id_disciplina": disciplinas_global[disc_nome]["id_disciplina"],
            "id_curso": cid
        }
        supabase.table("disciplina_curso").insert(assoc).execute()
        associations_curso.append(assoc)
print("✅ Associações na tabela 'disciplina_curso':")
print(associations_curso)
print("")

# =====================================================
# 9. Histórico Escolar (com notas aleatórias)
# Cada curso tem duração (em anos); cada ano tem 2 semestres.
historicos = []
hist_id = 1
curso_duracao_semestres = {c["id_curso"]: c["duracao_curso"] * 2 for c in cursos}
for aluno in alunos:
    total_semestres = curso_duracao_semestres[aluno["id_curso"]]
    if total_semestres >= 2:
        falha_semestre = random.randint(1, total_semestres - 1)
    else:
        falha_semestre = None
    for sem in range(1, total_semestres + 1):
        if falha_semestre is not None and sem == falha_semestre:
            media = round(random.uniform(0, 4.99), 2)
            situacao = "Reprovado"
        elif falha_semestre is not None and sem == falha_semestre + 1:
            media = round(random.uniform(5, 10), 2)
            situacao = "Aprovado"
        else:
            media = round(random.uniform(5, 10), 2)
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
print("✅ Histórico escolar inserido:")
for h in historicos:
    print(h)
print("")

# =====================================================
# 10. Associação Disciplina-Historico (tabela disciplina_historicoescolar)
# Para cada aluno, associamos as disciplinas ofertadas de forma cíclica.
associations_disc_hist = []
curso_id_para_nome = {c["id_curso"]: c["nome_curso"] for c in cursos}
for aluno in alunos:
    cid = aluno["id_curso"]
    curso_nome = curso_id_para_nome[cid]
    total_discip = len(disciplinas_por_curso[curso_nome])
    disc_assoc = [assoc for assoc in associations_curso if assoc["id_curso"] == cid]
    for hist in [h for h in historicos if h["matricula_aluno"] == aluno["matricula_aluno"]]:
        oferta = ((hist["semestre_historico"] - 1) % total_discip) + 1
        for assoc in disc_assoc:
            disc_id = assoc["id_disciplina"]
            disc = next((d for d in disciplinas if d["id_disciplina"] == disc_id), None)
            if disc and disc["semestre_disciplina"] == oferta:
                rec = {
                    "id_historicoescolar": hist["id_historicoescolar"],
                    "id_disciplina": disc["id_disciplina"],
                    "semestre": oferta
                }
                supabase.table("disciplina_historicoescolar").insert(rec).execute()
                associations_disc_hist.append(rec)
print("✅ Associações em disciplina_historicoescolar:")
print(associations_disc_hist)
print("")

# =====================================================
# 11. Associação Disciplina-Aluno (cada aluno cursa todas as disciplinas do seu curso)
# =====================================================
associations_aluno = []
for aluno in alunos:
    cid = aluno["id_curso"]
    disc_assoc = [assoc for assoc in associations_curso if assoc["id_curso"] == cid]
    for assoc in disc_assoc:
        rec = {
            "matricula_aluno": aluno["matricula_aluno"],
            "id_disciplina": assoc["id_disciplina"]
        }
        supabase.table("disciplina_aluno").insert(rec).execute()
        associations_aluno.append(rec)
print("✅ Associações em disciplina_aluno:")
print(associations_aluno)
print("")

# =====================================================
# 12. Associação Disciplina-Professor
# Agora associamos cada disciplina a um professor aleatório (entre os 20).
associations_prof = []
prof_ids = [p["id_professor"] for p in professores]
for d in disciplinas:
    pid = random.choice(prof_ids)
    rec = {
        "id_professor": pid,
        "id_disciplina": d["id_disciplina"]
    }
    supabase.table("disciplina_professor").insert(rec).execute()
    associations_prof.append(rec)
print("✅ Associações em disciplina_professor (professor aleatório):")
print(associations_prof)
print("")

# =====================================================
# 13. Disciplinas Lecionadas (tabela disciplinas_lecionadasprofessor)
# Marcamos como lecionada as disciplinas cujo id seja divisível por 3.
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
print("✅ Disciplinas lecionadas (id % 3 == 0):")
print(disciplinas_lec)
print("")

# =====================================================
# 14. Associação Professor - Disciplinas Lecionadas (historicodisciplina_professor)
# Para cada disciplina lecionada, associamos a um professor aleatório (entre os 20).
associations_hist_disc_prof = []
for lec in disciplinas_lec:
    pid = random.choice(prof_ids)
    rec = {
        "id_professor": pid,
        "id_disciplinalecionadas": lec["id_disciplinalecionadas"]
    }
    supabase.table("historicodisciplina_professor").insert(rec).execute()
    associations_hist_disc_prof.append(rec)
print("✅ Associações em historicodisciplina_professor:")
print(associations_hist_disc_prof)
print("")

# =====================================================
# 15. Associação Departamento-Professor
# Cada departamento terá um Chefe (já criados) e cada curso terá um Coordenador (já criados);
# os demais professores com cargo "Nenhum" serão associados aleatoriamente.
associations_dept_prof = []
for prof in professores:
    if prof["cargo"] == "Chefe":
        # Atribui o Chefe ao departamento correspondente (para os 3 Chefe, associamos com dept 1, 2 e 3, respectivamente)
        dpt_id = {1:1, 2:2, 3:3}.get(prof["id_professor"], 1)
        rec = {
            "id_professor": prof["id_professor"],
            "id_departamento": dpt_id
        }
        supabase.table("departamento_professor").insert(rec).execute()
        associations_dept_prof.append(rec)
    elif prof["cargo"] == "Coordenador":
        # Para coordenadores, associar ao departamento do curso que coordenam (usando o id do curso vinculado ao TCC do professor)
        curso_coord = next((c for c in cursos if c["id_curso"] == prof["id_tcc"]), None)
        dpt_id = curso_coord["id_departamento"] if curso_coord else None
        rec = {
            "id_professor": prof["id_professor"],
            "id_departamento": dpt_id if dpt_id is not None else 0
        }
        supabase.table("departamento_professor").insert(rec).execute()
        associations_dept_prof.append(rec)
    else:
        dpt_id = random.choice([1, 2, 3])
        rec = {
            "id_professor": prof["id_professor"],
            "id_departamento": dpt_id
        }
        supabase.table("departamento_professor").insert(rec).execute()
        associations_dept_prof.append(rec)
print("✅ Associação departamento_professor:")
print(associations_dept_prof)
print("")

print("✅ Script concluído com sucesso!\n")
