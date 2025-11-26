# 🎓 MathMaster - Banco de Questões (Full Stack Cloud Native)

Projeto profissional de Banco de Questões de Matemática desenvolvido com **Django**, **React** e **Kubernetes**.

O sistema conta com:
* **Frontend:** Painel do Professor com busca, filtros e geração de PDF no navegador.
* **Backend:** API REST robusta com painel administrativo moderno (Jazzmin).
* **Infra:** Arquitetura de microsserviços rodando em Kubernetes.

---

## 🚀 Guia de Início Rápido (Recriação)

Se você precisa restaurar o projeto do zero (Disaster Recovery), siga esta ordem:

### 1. Regenerar o Código Fonte
Execute o script mestre na raiz do projeto para criar a pasta `basecode`:
```bash
python master_rebuild.py

# 1. Criar o Namespace isolado
kubectl apply -f basecode/k8s/00-namespace.yaml

# 2. Aplicar Banco, Backend e Frontend
kubectl apply -f basecode/k8s/

kubectl rollout restart deployment/backend -n estudos
kubectl rollout restart deployment/frontend -n estudos

kubectl delete namespace estudos

2. Infraestrutura (Kubernetes)
Com o código gerado, suba a infraestrutura no seu cluster (Docker Desktop, Minikube ou Kind).

Iniciar o Ambiente
Bash

# 1. Criar o Namespace isolado
kubectl apply -f basecode/k8s/00-namespace.yaml

# 2. Aplicar Banco, Backend e Frontend
kubectl apply -f basecode/k8s/
Reiniciar/Atualizar Deployments
Se precisar forçar a atualização dos pods:

Bash

kubectl rollout restart deployment/backend -n estudos
kubectl rollout restart deployment/frontend -n estudos
Destruir Tudo (Cuidado!)
Bash

kubectl delete namespace estudos
🗄️ 3. Configuração do Banco de Dados
Após subir a infraestrutura pela primeira vez, o banco estará vazio.

Passo A: Identificar o Pod
Bash

kubectl get pods -n estudos
# Copie o nome do pod do backend (ex: backend-5f789d-xyz)
Passo B: Criar Tabelas e Superusuário
Substitua NOME_DO_POD pelo nome copiado acima:

Bash

# Criar tabelas
kubectl exec -it NOME_DO_POD -n estudos -- python manage.py migrate

# Criar admin (Login)
kubectl exec -it NOME_DO_POD -n estudos -- python manage.py createsuperuser
💾 4. Backup e Restauração (Gerenciamento de Dados)
Use o script auxiliar gerenciar_dados.py para não perder suas questões cadastradas.

Fazer Backup (Salvar dados no PC)
Este comando conecta ao cluster, extrai os dados e salva um arquivo JSON no seu computador.

Bash

python gerenciar_dados.py backup
Arquivo gerado: backup_mathmaster.json

Restaurar Backup (Enviar dados para o K8s)
Este comando pega o JSON do seu computador e injeta no banco de dados do cluster.

Bash

python gerenciar_dados.py restore
🐳 5. Build e Push Manual (Manutenção)
Caso precise alterar o código e gerar novas versões das imagens Docker.

Backend
Bash

cd basecode/backend
# Build (use --no-cache se adicionar bibliotecas novas)
docker build -t phenriquernagel/banco-questoes-backend:v22 .
# Push
docker push phenriquernagel/banco-questoes-backend:v22
Frontend
Bash

cd basecode/frontend
# Build
docker build -t phenriquernagel/banco-questoes-frontend:v23 .
# Push
docker push phenriquernagel/banco-questoes-frontend:v23