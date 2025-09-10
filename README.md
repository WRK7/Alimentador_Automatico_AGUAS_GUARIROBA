# 🤖 Alimentador Automático - Águas Guariroba

Sistema completo para processamento e automação de dados de clientes, dividido em duas partes principais.

## 📋 Estrutura do Projeto

### Parte 1 - Processamento de Arquivos (Pronta)
- **`main.py`** - Script principal de processamento de CSV
- **`requirements.txt`** - Dependências do projeto
- **`ARQUIVOS_ORIGINAIS/`** - Pasta com arquivos originais

### Parte 2 - Automação Web (Nova)
- **`automacao.py`** - Sistema de automação com Playwright
- **`sistema_completo.py`** - Integração das duas partes
- **`config.py`** - Configurações do sistema

## 🚀 Como Usar

### Instalação
```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar navegadores do Playwright
playwright install
```

### Execução

#### Opção 1: Sistema Completo (Recomendado)
```bash
python sistema_completo.py
```

#### Opção 2: Executar Partes Separadamente
```bash
# Apenas processamento
python main.py

# Apenas automação
python automacao.py

# Teste específico da seleção de fila
python teste_fila.py
```

## 📊 Funcionalidades

### Processamento de Arquivos
- ✅ Leitura de arquivos CSV com diferentes separadores
- ✅ Limpeza de dados (CPF/CNPJ, telefones)
- ✅ Geração de códigos únicos
- ✅ Remoção de duplicatas
- ✅ Divisão em arquivos de 25.000 linhas
- ✅ Organização em pastas com timestamps
- ✅ Backup automático dos originais
- ✅ Relatórios detalhados

### Automação Web
- ✅ Login automático no sistema
- ✅ Navegação inteligente
- ✅ Detecção automática de botões
- ✅ Seleção automática da fila "URA-AGUAS"
- ✅ Integração com arquivos processados
- ✅ Interface amigável

## ⚙️ Configurações

Edite o arquivo `config.py` para personalizar:

```python
# Credenciais do sistema
CREDENCIAIS = {
    "url": "https://portesmarinho.alimentador.vonixcc.com.br/session/new",
    "usuario": "portes",
    "senha": "portes1234"
}

# Configurações do navegador
NAVEGADOR = {
    "headless": False,  # True para executar sem interface
    "timeout": 30000,
    "delay_entre_acoes": 1
}
```

## 📁 Estrutura de Saída

### Pasta Principal (Destino)
```
S:\BACKOFFICE\Controle de Discadores e Uras\Uras\URA AGUAS BASE TODA\
├── URA_AGUASG_DD_MM_YYYY_1.csv
├── URA_AGUASG_DD_MM_YYYY_2.csv
├── URA_AGUASG_DD_MM_YYYY_3.csv
└── ... (até o último arquivo)
```

### Backup Local
```
PROCESSAMENTO_YYYYMMDD_HHMMSS/
├── CLIENTES_PROCESSADOS_COMPLETO.csv
├── RELATORIO_PROCESSAMENTO.txt
└── backup_original/
    └── arquivo_original.csv
```

## 🔧 Próximos Passos

- [ ] Implementar upload automático de arquivos
- [ ] Adicionar validações de dados
- [ ] Sistema de logs detalhado
- [ ] Interface gráfica (opcional)
- [ ] Agendamento automático

## 🐛 Solução de Problemas

### Erro de Login
- Verifique as credenciais em `config.py`
- Confirme se o site está acessível

### Botão "Importar" não encontrado
- O sistema tenta múltiplos seletores automaticamente
- Verifique se a página carregou completamente

### Arquivos não processados
- Execute primeiro `python main.py`
- Verifique se há arquivos CSV na pasta raiz

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Logs de erro no terminal
2. Arquivo de relatório gerado
3. Configurações em `config.py`
