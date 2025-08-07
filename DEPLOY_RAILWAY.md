# 🚂 Deploy no Railway - Guia Passo a Passo

## 🎯 Railway: A Melhor Opção para Seu Backend

**Por que Railway:**
- ✅ 500 horas grátis/mês (cerca de 20 dias 24/7)
- ✅ Deploy automático via GitHub
- ✅ SSL/HTTPS automático
- ✅ Configuração super simples
- ✅ Perfeito para Flask/Python

## 📋 **Pré-requisitos**
- Conta no GitHub
- Código da aplicação (já temos!)
- Chave API do PinPag

## 🚀 **Passo a Passo**

### 1. **Criar Conta no Railway**
- Acesse: https://railway.app
- Clique em "Sign Up"
- Faça login com GitHub

### 2. **Preparar Código para Deploy**
Vou criar os arquivos necessários:

#### `requirements.txt`:
```
Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0
flask-cors==4.0.0
```

#### `Procfile`:
```
web: gunicorn main:app
```

#### `runtime.txt`:
```
python-3.11.0
```

### 3. **Criar Repositório no GitHub**
```bash
# No seu computador
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/seuusuario/consulta-veicular.git
git push -u origin main
```

### 4. **Deploy no Railway**
1. No Railway, clique **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha seu repositório
4. Railway detectará automaticamente que é Python
5. Deploy iniciará automaticamente!

### 5. **Configurar Variáveis de Ambiente**
No painel do Railway:
1. Clique na aba **"Variables"**
2. Adicione:
   - `X_API_KEY`: sua_chave_pinpag_aqui
   - `SESSION_SECRET`: uma_chave_secreta_aleatoria

### 6. **Obter URL da Aplicação**
- Após deploy, Railway fornecerá uma URL
- Exemplo: `https://consulta-veicular-production.up.railway.app`

## 🔗 **Integrar com Seu Site no Hostinger**

### Modificação no Backend (para CORS):
```python
# app.py - Adicionar no início
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://seusite.hostinger.com'])  # Seu domínio
```

### JavaScript no Seu Site:
```html
<!-- No seu site HTML (Hostinger) -->
<script>
const API_URL = 'https://sua-app.up.railway.app';

async function consultarDebitos() {
    const renavam = document.getElementById('renavam').value;
    const placa = document.getElementById('placa').value;
    
    try {
        const response = await fetch(`${API_URL}/consultar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                renavam: renavam,
                license_plate: placa,
                uf: 'SP'
            })
        });
        
        if (response.ok) {
            // Redirecionar para página de resultados
            window.location.href = `${API_URL}/resultados`;
        } else {
            alert('Erro na consulta');
        }
    } catch (error) {
        console.error('Erro:', error);
    }
}
</script>
```

## 💰 **Custos Railway**

### Plano Gratuito:
- **500 horas/mês** de execução
- **1GB RAM** 
- **1GB disco**
- **SSL automático**
- **Domínio incluso**

### Se exceder (improvável):
- **$5/mês** por serviço adicional
- Cobrança apenas pelo uso excedente

## 🔧 **Outras Plataformas (Alternativas)**

### Render (100% Gratuito):
- Deploy: Conectar GitHub
- Limitação: Aplicação "dorme" após 15min inativo
- Desperta automaticamente quando recebe requisição

### Replit (Atual):
- Clique em **"Deploy"** no seu Replit
- Domínio: `https://seu-projeto.replit.app`
- Gratuito com limitações

## 🏁 **Resumo do Processo**

```
Seu Site (Hostinger) ←→ Backend (Railway) ←→ API PinPag
   HTML/CSS/JS              Python/Flask         Consulta Débitos
```

## 🎯 **Próximos Passos**

1. **Escolher plataforma**: Railway (recomendado)
2. **Criar repositório** no GitHub
3. **Fazer deploy**
4. **Configurar X_API_KEY**
5. **Testar integração**

Quer que eu prepare os arquivos específicos para deploy na Railway ou em outra plataforma?