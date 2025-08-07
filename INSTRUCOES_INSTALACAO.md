# 📋 Instruções de Instalação - Consulta de Débitos Veiculares

## 📁 Estrutura do Projeto

```
projeto/
├── app.py                 # Aplicação Flask principal
├── main.py               # Ponto de entrada (importa app)
├── requirements.txt      # Dependências Python
├── services/
│   └── pinpag_api.py    # Integração com API PinPag
├── templates/
│   ├── base.html        # Template base
│   ├── index.html       # Página inicial
│   └── results.html     # Página de resultados
├── static/
│   ├── css/
│   │   └── custom.css   # Estilos personalizados
│   └── js/
│       └── app.js       # JavaScript da aplicação
└── README.md            # Documentação
```

## 🛠️ Pré-requisitos

- **Python 3.11+**
- **PIP** (gerenciador de pacotes Python)
- **Chave API do PinPag** (X_API_KEY)

## 📦 Instalação

### 1. Descompactar os Arquivos
```bash
# Extrair o arquivo
tar -xzf consulta_veicular_completa.tar.gz
cd consulta_veicular/
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
# Instalar as dependências
pip install flask requests gunicorn
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```bash
# .env
X_API_KEY=sua_chave_api_do_pinpag_aqui
SESSION_SECRET=uma_chave_secreta_para_sessoes
```

### 5. Executar a Aplicação

#### Desenvolvimento (Flask dev server):
```bash
python app.py
```

#### Produção (Gunicorn):
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## 🔧 Configuração da API

### Obter Chave API do PinPag
1. Entre em contato com a equipe PinPag
2. Solicite acesso ao ambiente de homologação
3. Receba sua `X_API_KEY` (válida por 30 dias)
4. Configure a chave nas variáveis de ambiente

### URLs da API
- **Homologação**: `https://integrador.homolog.pinpag.com.br`
- **Produção**: `https://integrador.pinpag.com.br`

## 🌐 Deployment

### Apache/Nginx + WSGI
```python
# wsgi.py
from main import app
application = app

if __name__ == "__main__":
    application.run()
```

### Docker (Opcional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install flask requests gunicorn

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## 🧪 Dados de Teste

Use estes dados no ambiente de homologação:

**Veículos para teste:**
- RENAVAM: `965082296` | Placa: `EBU4E67`
- RENAVAM: `1324972332` | Placa: `FOI3E01` 
- RENAVAM: `974985228` | Placa: `EDS4C97`

**Cartões para teste:**
- Aprovado: `0000.0000.0000.0000` ou `0000.0000.0000.0001`
- Recusado: `0000.0000.0000.0002`
- Nome: `João Accept` (sucesso) ou `Maria Rejected` (falha)

## ⚙️ Configurações Importantes

### Horário de Funcionamento (Homologação)
- **Segunda a Sexta:** 9h às 20h
- Fora deste horário, a API pode não responder

### Limitações
- Apenas veículos de **São Paulo (SP)**
- Pagamentos apenas com **cartão de crédito**
- Parcelamento até **21x**
- Até **4 cartões** por transação

## 🔒 Segurança

- Nunca commit suas chaves API no código
- Use variáveis de ambiente para configurações sensíveis
- Configure HTTPS em produção
- Mantenha as dependências atualizadas

## 📞 Suporte

- **Produção**: implantacao@pinpag.com.br
- Envie 3 evidências: 2 casos de sucesso + 1 de falha

## 🐛 Troubleshooting

### Erro: "X_API_KEY não configurada"
- Verifique se a variável de ambiente está configurada
- Confirme se a chave está ativa (válida por 30 dias)

### Erro: "Consulta pendente por muito tempo"
- Teste em horário comercial (9h-20h)
- Verifique sua conexão com a internet
- Use os dados de teste fornecidos

### Erro 401/403 na API
- Chave API inválida ou expirada
- Solicite nova chave à equipe PinPag

---

✅ **Aplicação pronta para usar!**