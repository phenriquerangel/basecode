import json

# Dados simulados para popular o banco
dados = []
topicos = ["Matemática Básica", "Álgebra", "Geometria", "Trigonometria", "Estatística"]

# 1. Criar Tópicos
for i, nome in enumerate(topicos, 1):
    dados.append({
        "model": "questoes.topico",
        "pk": i,
        "fields": {
            "nome": nome,
            "descricao": f"Questões sobre {nome}"
        }
    })

# 2. Criar Questões (3 para cada tópico)
count = 1
for i, topico in enumerate(topicos, 1):
    for j in range(1, 4):
        dados.append({
            "model": "questoes.questao",
            "pk": count,
            "fields": {
                "enunciado": f"Questão {j} de {topico}: Qual o resultado de X + {j}?",
                "topico": i,
                "dificuldade": "M",
                "alternativa_a": "10",
                "alternativa_b": "20",
                "alternativa_c": "30",
                "alternativa_d": "40",
                "correta": "C",
                "justificativa": "Esta é uma questão gerada automaticamente para testes.",
                "criado_em": "2024-01-01T12:00:00Z"
            }
        })
        count += 1

# Salvar arquivo
with open("dados_iniciais.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("✅ Arquivo 'dados_iniciais.json' gerado com sucesso!")
print("Agora execute os comandos para enviar ao Kubernetes.")