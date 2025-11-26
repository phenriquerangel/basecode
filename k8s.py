import os

def create_file(path, content):
    # Cria os diretórios necessários
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Escreve o conteúdo
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"✅ Criado: {path}")

# --- CONTEÚDO DOS ARQUIVOS YAML (MANIFESTOS) ---

# 1. SECRETS (Senhas e Configurações Sensíveis)
yaml_secrets = """
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: estudos
type: Opaque
stringData:
  # Dados do Banco
  DB_NAME: "banco_questoes"
  DB_USER: "usuario_questoes"
  DB_PASSWORD: "senha_super_segura_123"
  DB_HOST: "postgres-db"
  # Dados do Django
  SECRET_KEY: "django-insecure-chave-k8s-prod"
  DEBUG: "True"
"""

# 2. DATABASE (PostgreSQL)
yaml_database = """
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: estudos
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: estudos
spec:
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_NAME
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DB_PASSWORD
        volumeMounts:
        - mountPath: /var/lib/postgresql/data
          name: postgres-storage
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-db
  namespace: estudos
spec:
  ports:
  - port: 5432
  selector:
    app: postgres
  type: ClusterIP
"""

# 3. BACKEND (Django API)
yaml_backend = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: estudos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      initContainers:
      - name: migrate
        image: phenriquernagel/banco-questoes-backend:v2
        command: ["python", "manage.py", "migrate"]
        envFrom:
        - secretRef:
            name: app-secrets
      containers:
      - name: backend
        image: phenriquernagel/banco-questoes-backend:v2
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: app-secrets
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: estudos
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: NodePort
"""

# 4. FRONTEND (React + Nginx)
yaml_frontend = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: estudos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: phenriquernagel/banco-questoes-frontend:v2
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: estudos
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
"""

# --- EXECUÇÃO CORRIGIDA ---
# Define a pasta raiz correta: basecode
root = "basecode/k8s"

files = {
    f"{root}/01-secrets.yaml": yaml_secrets,
    f"{root}/02-database.yaml": yaml_database,
    f"{root}/03-backend.yaml": yaml_backend,
    f"{root}/04-frontend.yaml": yaml_frontend,
}

print(f"🚀 Gerando manifestos Kubernetes na pasta '{root}'...")

for path, content in files.items():
    create_file(path, content)

print("\n✨ Arquivos K8s gerados com sucesso na pasta 'basecode/k8s'!")
print(f"👉 Para aplicar: kubectl apply -f {root}/")