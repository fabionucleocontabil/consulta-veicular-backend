# 🔑 Configuração da Chave API - Onde Armazenar

## 📍 Localização da Chave API

A chave API (`X_API_KEY`) deve ser armazenada como **variável de ambiente** e **NUNCA** no código fonte.

## 🏠 Local de Armazenamento por Ambiente

### 1. **Desenvolvimento Local**

#### Opção A: Arquivo `.env` (Recomendado)
Crie um arquivo `.env` na raiz do projeto:
```bash
# .env (na pasta raiz do projeto)
X_API_KEY=sua_chave_api_aqui
SESSION_SECRET=uma_chave_secreta_aleatoria
```

#### Opção B: Variáveis do Sistema
```bash
# Windows (CMD)
set X_API_KEY=sua_chave_api_aqui
set SESSION_SECRET=uma_chave_secreta

# Windows (PowerShell)
$env:X_API_KEY="sua_chave_api_aqui"
$env:SESSION_SECRET="uma_chave_secreta"

# Linux/Mac
export X_API_KEY="sua_chave_api_aqui"
export SESSION_SECRET="uma_chave_secreta"
```

### 2. **Replit (atual ambiente)**
- Vá em **Secrets** no painel lateral
- Adicione: `X_API_KEY` com sua chave
- Adicione: `SESSION_SECRET` com uma chave aleatória

### 3. **Servidor de Produção**

#### Apache/Nginx + WSGI
```apache
# Arquivo .htaccess ou configuração do Apache
SetEnv X_API_KEY "sua_chave_api_aqui"
SetEnv SESSION_SECRET "sua_chave_secreta"
```

#### Docker
```dockerfile
# Dockerfile
ENV X_API_KEY=""
ENV SESSION_SECRET=""

# Ou no docker-compose.yml
environment:
  - X_API_KEY=sua_chave_api_aqui
  - SESSION_SECRET=sua_chave_secreta
```

#### Heroku
```bash
heroku config:set X_API_KEY=sua_chave_api_aqui
heroku config:set SESSION_SECRET=sua_chave_secreta
```

## 🔍 Como o Código Acessa a Chave

### No código Python:
```python
import os

# A aplicação busca a chave automaticamente
api_key = os.environ.get("X_API_KEY", "default-api-key")
secret_key = os.environ.get("SESSION_SECRET", "dev-secret")
```

### Arquivos onde é usada:
- `services/pinpag_api.py`: Linha 11 - Configura a chave para API
- `app.py`: Linha 10 - Configura chave de sessão

## ⚠️ IMPORTANTES - Segurança

### ✅ FAÇA:
- Use variáveis de ambiente
- Mantenha `.env` no `.gitignore`
- Use chaves diferentes para desenvolvimento/produção
- Renove a chave a cada 30 dias

### ❌ NUNCA FAÇA:
```python
# NUNCA faça isso:
api_key = "sua_chave_aqui"  # ❌ Nunca no código!
```

- Nunca commite chaves no Git
- Nunca deixe chaves em código público
- Nunca compartilhe chaves por email/chat

## 🔄 Onde Alterar se Precisar Mudar

Se quiser mudar onde a aplicação busca a chave:

### Arquivo: `services/pinpag_api.py`
```python
# Linha 11 - Altere se necessário
self.api_key = os.environ.get("SUA_VARIAVEL_PERSONALIZADA", "default")
```

### Arquivo: `app.py`
```python
# Linha 10 - Altere se necessário  
app.secret_key = os.environ.get("SUA_VARIAVEL_SESSION", "default")
```

## 📋 Checklist de Configuração

- [ ] Chave API obtida do PinPag
- [ ] Variável `X_API_KEY` configurada no ambiente
- [ ] Variável `SESSION_SECRET` configurada  
- [ ] Arquivo `.env` criado (se desenvolvimento local)
- [ ] Arquivo `.env` adicionado ao `.gitignore`
- [ ] Aplicação reiniciada após configurar variáveis

---

**Sua chave ficará segura e invisível no código!** 🔒