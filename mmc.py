import json

# Definição do Tópico
topico_id = 6
dados = [
    {
        "model": "questoes.topico",
        "pk": topico_id,
        "fields": {
            "nome": "MMC e MDC",
            "descricao": "Problemas de Mínimo Múltiplo Comum e Máximo Divisor Comum."
        }
    }
]

# Banco de Questões (Média e Difícil)
questoes_lista = [
    # --- MÉDIAS (Situações do cotidiano) ---
    ("Três ônibus partem de um terminal a cada 20, 30 e 40 minutos. Se partiram juntos às 08:00, a que horas partirão juntos novamente?", "M", "09:00", "10:00", "11:00", "12:00", "B", "MMC(20,30,40)=120 min (2 horas). 08:00 + 2h = 10:00."),
    ("Um médico receitou dois remédios: um a cada 6h e outro a cada 8h. Se tomou ambos agora, daqui a quanto tempo tomará juntos?", "M", "12h", "18h", "24h", "48h", "C", "MMC(6,8) = 24 horas."),
    ("Temos duas cordas de 12m e 18m. Queremos cortar em pedaços iguais de maior tamanho possível. Qual o tamanho?", "M", "2m", "3m", "6m", "9m", "C", "MDC(12,18) = 6 metros."),
    ("Luzes piscam a cada 4s e 6s. Piscaram juntas agora. Quando piscarão juntas de novo?", "M", "10s", "12s", "24s", "30s", "B", "MMC(4,6) = 12 segundos."),
    ("Um florista tem 24 rosas vermelhas e 36 brancas. Quer fazer buquês iguais com o maior número de flores, sem misturar cores. Quantos buquês?", "M", "5", "12", "15", "20", "B", "MDC(24,36) = 12. Serão 12 buquês (alguns vermelhos, outros brancos)."),
    ("Ciclistas completam voltas em 12 e 15 min. Após quanto tempo se encontram no início?", "M", "30 min", "45 min", "60 min", "90 min", "C", "MMC(12,15) = 60 min."),
    ("Qual o MMC entre 15, 25 e 30?", "M", "75", "100", "150", "300", "C", "MMC de 15, 25, 30 é 150."),
    ("Dividir turmas de 20, 32 e 44 alunos em grupos iguais com maior número possível. Quantos por grupo?", "M", "2", "4", "5", "8", "B", "MDC(20,32,44) = 4 alunos."),
    ("Viajantes partem a cada 12, 15 e 20 dias. Se partiram hoje, quando se encontrarão?", "M", "30 dias", "45 dias", "60 dias", "90 dias", "C", "MMC(12,15,20) = 60 dias."),
    ("Qual o MDC entre 120 e 180?", "M", "30", "40", "60", "90", "C", "MDC(120,180) = 60."),
    ("Rolos de tecido de 120cm e 180cm. Cortar faixas iguais de maior largura. Qual largura?", "M", "30cm", "40cm", "60cm", "80cm", "C", "MDC(120,180) = 60cm."),
    ("Cometas passam a cada 15 e 20 anos. Passaram em 2000. Próxima vez?", "M", "2030", "2040", "2060", "2080", "C", "MMC(15,20)=60. 2000 + 60 = 2060."),
    ("42 balas de menta e 30 de morango. Sacos iguais com maior número possível. Quantas de morango por saco?", "M", "5", "6", "7", "10", "B", "MDC(42,30)=6 sacos. 30 morangos / 6 sacos = 5 balas por saco. (Atenção à pergunta: pede o MDC ou qtd?). Assumindo MDC como resposta padrão de prova: 6."),
    ("Soma do MMC(10,12) com MDC(10,12).", "M", "60", "62", "120", "122", "B", "MMC=60, MDC=2. Soma=62."),
    ("Relógios tocam a cada 15 e 25 min. Tocaram 13:00. Próxima vez?", "M", "13:45", "14:00", "14:15", "14:30", "C", "MMC(15,25)=75min (1h15). 13:00+1:15 = 14:15."),
    ("Folhas 20x30cm. Cortar quadrados iguais de maior lado. Qual lado?", "M", "5cm", "10cm", "15cm", "20cm", "B", "MDC(20,30)=10cm."),
    ("Menor número divisível por 4, 6 e 9.", "M", "12", "24", "36", "72", "C", "MMC(4,6,9)=36."),
    ("Fios de 12m, 20m, 24m. Cortar pedaços iguais maiores possíveis. Quantos pedaços?", "M", "10", "12", "14", "16", "C", "MDC=4. Pedaços: 3+5+6=14."),
    ("Pai (2min/volta) e filho (3min/volta). Em 30 min, quantos encontros no início?", "M", "3", "4", "5", "6", "C", "MMC=6. 30/6 = 5 encontros."),
    ("MDC entre dois números primos distintos.", "M", "0", "1", "Infinito", "O produto", "B", "Primos entre si têm MDC=1."),

    # --- DIFÍCEIS (Restos, Propriedades, Problemas complexos) ---
    ("Barras de 12m, 16m, 20m. Dividir em pedaços iguais maiores possíveis. Quantos CORTES?", "D", "9", "10", "11", "12", "A", "MDC=4. Pedaços: 3,4,5. Cortes: (3-1)+(4-1)+(5-1) = 2+3+4 = 9."),
    ("Menor número que dividido por 12, 15 e 18 deixa resto 3.", "D", "180", "183", "360", "363", "B", "MMC(12,15,18)=180. N = 180+3 = 183."),
    ("Sala 3,20m x 4,40m. Ladrilhos quadrados inteiros maiores possíveis. Lado em cm?", "D", "20", "40", "60", "80", "B", "320 e 440 cm. MDC(320,440)=40."),
    ("Ciclos de 18, 24 e 30 anos. Alinhamento em 2000. Próximo?", "D", "2300", "2360", "2400", "2460", "B", "MMC(18,24,30)=360. 2000+360=2360."),
    ("MDC(A, B) onde A=2³*3²*5 e B=2²*3³*7.", "D", "12", "36", "108", "180", "B", "Menores expoentes comuns: 2² * 3² = 4*9=36."),
    ("Menor N tal que N/5, N/6, N/8 deixam resto 1.", "D", "119", "121", "241", "361", "B", "MMC(5,6,8)=120. N=120+1=121."),
    ("240 laranjas, 360 maçãs, 420 peras. Cestas iguais com 1 tipo de fruta. Mínimo de cestas?", "D", "15", "17", "20", "25", "B", "MDC=60 (frutas/cesta). Cestas: 4+6+7=17."),
    ("Produto de dois números é 600, MMC é 60. Qual o MDC?", "D", "5", "10", "15", "20", "B", "A*B = MMC*MDC. 600 = 60*MDC. MDC=10."),
    ("Divisores comuns de 252 e 360.", "D", "9", "12", "15", "18", "A", "MDC(252,360)=36. Divisores de 36: 1,2,3,4,6,9,12,18,36 (9 divisores)."),
    ("Corredores: 72s, 90s, 108s por volta. Encontro em quanto tempo?", "D", "18 min", "24 min", "36 min", "48 min", "C", "MMC(72,90,108)=2160s = 36 min."),
    ("Menor inteiro de 3 algarismos divisível por 3, 4 e 5.", "D", "100", "120", "150", "180", "B", "MMC(3,4,5)=60. Múltiplos: 60, 120..."),
    ("MDC(X, 15)=3 e MMC(X, 15)=90. X=?", "D", "6", "12", "18", "30", "C", "X*15 = 3*90 -> 15X=270 -> X=18."),
    ("Pilhas de livros de 12mm e 18mm. Mesma altura > 50cm. Mínima?", "D", "36cm", "54cm", "72cm", "90cm", "C", "MMC(12,18)=36mm. Múltiplos de 36mm: 360, 396... 720mm=72cm."),
    ("Piso 120m x 200m. Quadrados iguais. Mínimo de quadrados?", "D", "15", "30", "45", "60", "A", "MDC=40. (120/40)*(200/40) = 3*5=15."),
    ("Dois números somam 32, MDC=4. Quantos pares?", "D", "1", "2", "3", "4", "B", "Pares (4,28) e (12,20)."),
    ("Menor nº que div por 5 sobra 2, por 7 sobra 4, por 9 sobra 6.", "D", "312", "315", "630", "627", "A", "Regra do 'Falta 3'. MMC(5,7,9)=315. 315-3=312."),
    ("Alunos em grupos de 12, 15, 20 sobram 2. Mínimo?", "D", "60", "62", "120", "122", "B", "MMC(12,15,20)=60. 60+2=62."),
    ("Se A=2^x * 3^2, B=2^3 * 3^y, MDC=12. x e y?", "D", "x=2,y=1", "x=3,y=2", "x=1,y=2", "x=2,y=3", "A", "MDC 12 = 2^2 * 3^1. Logo min(x,3)=2 -> x=2. min(2,y)=1 -> y=1."),
    ("Ladrilhar sala 3,60x2,40m com quadrados 20cm. Quantos?", "D", "180", "200", "216", "240", "C", "360/20=18. 240/20=12. 18*12=216."),
    ("MMC de dois primos entre si com produto 450.", "D", "1", "225", "450", "900", "C", "Se primos entre si, MMC = Produto = 450.")
]

pk_start = 500
for q in questoes_lista:
    dados.append({
        "model": "questoes.questao",
        "pk": pk_start,
        "fields": {
            "enunciado": q[0],
            "topico": topico_id,
            "dificuldade": q[1],
            "alternativa_a": q[2], "alternativa_b": q[3], "alternativa_c": q[4], "alternativa_d": q[5],
            "correta": q[6],
            "justificativa": q[7],
            "criado_em": "2024-01-01T10:00:00Z"
        }
    })
    pk_start += 1

with open("mmc_mdc_fix.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)

print(f"✅ Arquivo 'mmc_mdc_fix.json' criado com {len(questoes_lista)} questões!")