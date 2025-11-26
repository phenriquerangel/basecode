import json

dados = []
topicos = ["Matemática Básica", "Álgebra", "Geometria Plana", "Trigonometria", "Estatística"]

# 1. Criar Tópicos
for i, nome in enumerate(topicos, 1):
    dados.append({
        "model": "questoes.topico",
        "pk": i,
        "fields": {
            "nome": nome,
            "descricao": f"Exercícios e problemas sobre {nome}"
        }
    })

# 2. Criar Questões (3 para cada tópico)
pk_count = 1
for i, topico in enumerate(topicos, 1):
    for j in range(1, 4):
        # Cria enunciados um pouco mais realistas
        enunciado = f"Questão {j} sobre {topico}: Calcule o valor de X na expressão dada."
        if topico == "Geometria Plana":
            enunciado = f"Questão {j}: Qual a área de um triângulo com base {j*2} e altura {j*3}?"
        elif topico == "Álgebra":
            enunciado = f"Questão {j}: Resolva a equação 2x + {j*5} = 0."

        dados.append({
            "model": "questoes.questao",
            "pk": pk_count,
            "fields": {
                "enunciado": enunciado,
                "topico": i,
                "dificuldade": "F" if j==1 else "M" if j==2 else "D",
                "alternativa_a": "10",
                "alternativa_b": "15",
                "alternativa_c": "20",
                "alternativa_d": "25",
                "correta": "B",
                "justificativa": f"Resolução passo a passo da questão de {topico}.",
                "criado_em": "2024-01-01T12:00:00Z"
            }
        })
        pk_count += 1

# Salvar arquivo JSON
with open("dados_iniciais.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)

print("✅ Arquivo 'dados_iniciais.json' gerado com 20 registros!")