# Configurações do Alimentador Automático

# Credenciais do sistema
CREDENCIAIS = {
    "url": "https://portesmarinho.alimentador.vonixcc.com.br/session/new",
    "usuario": "portes",
    "senha": "portes1234"
}

# Configurações de processamento
PROCESSAMENTO = {
    "linhas_por_arquivo": 25000,
    "separador_csv": ";",
    "encoding": "utf-8"
}

# Configurações do navegador
NAVEGADOR = {
    "headless": False,  # True para executar sem interface gráfica
    "timeout": 30000,   # Timeout em milissegundos
    "delay_entre_acoes": 1  # Delay em segundos entre ações
}

# Pastas do projeto
PASTAS = {
    "originais": "ARQUIVOS_ORIGINAIS",
    "processados": "PROCESSAMENTO_",
    "divididos": "arquivos_divididos",
    "backup": "backup_original"
}
