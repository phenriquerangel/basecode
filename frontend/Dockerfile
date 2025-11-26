# Arquivo: frontend/Dockerfile

# --- Estágio 1: Build ---
FROM node:18-alpine as build

WORKDIR /app

# CORREÇÃO: Copia apenas o package.json (sem o lock)
COPY package.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código
COPY . .

# Gera a versão de produção
RUN npm run build

# --- Estágio 2: Serve com Nginx ---
FROM nginx:alpine

# Copia os arquivos gerados (pasta dist)
COPY --from=build /app/dist /usr/share/nginx/html

# Copia a configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]