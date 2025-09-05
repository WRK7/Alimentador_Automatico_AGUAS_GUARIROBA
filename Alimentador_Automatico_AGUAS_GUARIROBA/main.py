import pandas as pd
import re
import random
import string
import os
from pathlib import Path

def gerar_codigo_aleatorio():
    """Gera um código aleatório de 4 letras seguidas por 4 números"""
    letras = ''.join(random.choices(string.ascii_uppercase, k=4))
    numeros = ''.join(random.choices(string.digits, k=4))
    return letras + numeros

def limpar_cpf_cnpj(texto):
    """Remove caracteres especiais de CPF/CNPJ, mantendo apenas números"""
    if pd.isna(texto):
        return texto
    return re.sub(r'[^\d]', '', str(texto))

def limpar_coluna_d(texto):
    """Remove pontos e outros caracteres especiais da coluna D"""
    if pd.isna(texto):
        return texto
    return re.sub(r'[^\d]', '', str(texto))

def limpar_coluna_e(texto):
    """Limpa números da coluna E"""
    if pd.isna(texto):
        return texto
    return re.sub(r'[^\d]', '', str(texto))

def processar_arquivo_csv(nome_arquivo):
    """Processa um arquivo CSV específico"""
    print(f"\n{'='*60}")
    print(f"PROCESSANDO: {nome_arquivo}")
    print(f"{'='*60}")
    
    # Ler o arquivo CSV
    try:
        # Tentar diferentes separadores e configurações
        separadores = [',', ';', '\t', '|']
        df = None
        
        for sep in separadores:
            try:
                print(f"Tentando separador: '{sep}'")
                df = pd.read_csv(nome_arquivo, sep=sep, encoding='utf-8', on_bad_lines='skip')
                if len(df.columns) > 1:  # Se encontrou múltiplas colunas
                    print(f"Sucesso com separador '{sep}' - {len(df)} linhas e {len(df.columns)} colunas")
                    break
            except Exception as e:
                print(f"Falhou com separador '{sep}': {e}")
                continue
        
        if df is None or len(df.columns) < 2:
            # Última tentativa com configurações mais robustas
            print("Tentando configuração robusta...")
            df = pd.read_csv(nome_arquivo, 
                           sep=',', 
                           encoding='utf-8', 
                           on_bad_lines='skip',
                           quoting=1,  # QUOTE_ALL
                           skipinitialspace=True)
            print(f"Arquivo carregado com {len(df)} linhas e {len(df.columns)} colunas")
        
        if df is None:
            print("Não foi possível ler o arquivo com nenhum separador")
            return None
            
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None
    
    return df

def processar_csv():
    print("Iniciando processamento de arquivos CSV...")
    
    # Encontrar todos os arquivos CSV na pasta
    import glob
    arquivos_csv = glob.glob("*.csv")
    
    # Filtrar arquivos de resultado para não processar novamente
    arquivos_csv = [f for f in arquivos_csv if not f.startswith("CLIENTES_") and not f.startswith("arquivo_processado")]
    
    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado na pasta!")
        return
    
    print(f"Arquivos encontrados: {len(arquivos_csv)}")
    for i, arquivo in enumerate(arquivos_csv, 1):
        print(f"  {i}. {arquivo}")
    
    # Processar cada arquivo
    for arquivo in arquivos_csv:
        df = processar_arquivo_csv(arquivo)
        if df is not None:
            processar_dados(df, arquivo)
        else:
            print(f"❌ Falha ao processar: {arquivo}")
    
    print(f"\n🎉 PROCESSAMENTO EM MASSA CONCLUÍDO!")
    print(f"Total de arquivos processados: {len(arquivos_csv)}")

def processar_dados(df, nome_arquivo_original):
    """Processa os dados de um DataFrame específico"""
    
    # Verificar se as colunas existem
    if len(df.columns) < 5:
        print("Erro: O arquivo deve ter pelo menos 5 colunas (A, B, C, D, E)")
        return
    
    print("Colunas encontradas:", df.columns.tolist())
    
    # PASSO 1: Limpar as colunas B, D e E
    print("\n=== PASSO 1: Limpando colunas B, D e E ===")
    
    # Limpar coluna B (CPF/CNPJ)
    if len(df.columns) > 1:
        df.iloc[:, 1] = df.iloc[:, 1].apply(limpar_cpf_cnpj)
        print("Coluna B (CPF/CNPJ) limpa")
    
    # Limpar coluna D
    if len(df.columns) > 3:
        df.iloc[:, 3] = df.iloc[:, 3].apply(limpar_coluna_d)
        print("Coluna D limpa")
    
    # Limpar coluna E
    if len(df.columns) > 4:
        df.iloc[:, 4] = df.iloc[:, 4].apply(limpar_coluna_e)
        print("Coluna E limpa")
    
    # PASSO 2: Mover nomes da coluna A para B e gerar códigos aleatórios para A
    print("\n=== PASSO 2: Reorganizando colunas A e B ===")
    
    # Salvar nomes da coluna A
    nomes_originais = df.iloc[:, 0].copy()
    
    # Gerar códigos únicos para coluna A
    codigos_gerados = set()
    codigos_unicos = []
    
    for i in range(len(df)):
        while True:
            codigo = gerar_codigo_aleatorio()
            if codigo not in codigos_gerados:
                codigos_gerados.add(codigo)
                codigos_unicos.append(codigo)
                break
    
    # Atualizar colunas A e B
    df.iloc[:, 0] = codigos_unicos  # Nova coluna A com códigos
    df.iloc[:, 1] = nomes_originais  # Coluna B com nomes originais
    
    print(f"Gerados {len(codigos_unicos)} códigos únicos para coluna A")
    print("Nomes movidos da coluna A para coluna B")
    
    # PASSO 3: Remover telefones duplicados da coluna C
    print("\n=== PASSO 3: Removendo telefones duplicados ===")
    
    if len(df.columns) > 2:
        telefones_antes = len(df)
        df = df.drop_duplicates(subset=[df.columns[2]], keep='first')
        telefones_depois = len(df)
        print(f"Removidos {telefones_antes - telefones_depois} telefones duplicados")
        print(f"Restaram {telefones_depois} registros únicos")
    
    # Manter apenas as colunas A, B e C (códigos, nomes, telefones)
    print("\n=== Removendo colunas desnecessárias ===")
    df = df.iloc[:, [0, 1, 2]]  # Manter apenas colunas A, B e C
    df.columns = ['', '', '']  # Remover nomes das colunas
    print("Mantidas apenas as colunas: A, B e C (sem nomes de identificação)")
    
    # PASSO 4 e 5: Dividir em arquivos de 25.000 linhas
    print("\n=== PASSO 4 e 5: Dividindo em arquivos de 25.000 linhas ===")
    
    # Criar estrutura de pastas organizada
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Pasta principal de resultados
    pasta_principal = f"PROCESSAMENTO_{timestamp}"
    pasta_arquivos_divididos = os.path.join(pasta_principal, "arquivos_divididos")
    pasta_backup = os.path.join(pasta_principal, "backup_original")
    
    # Criar todas as pastas
    os.makedirs(pasta_principal, exist_ok=True)
    os.makedirs(pasta_arquivos_divididos, exist_ok=True)
    os.makedirs(pasta_backup, exist_ok=True)
    
    print(f"Estrutura de pastas criada:")
    print(f"  📁 {pasta_principal}/")
    print(f"    📁 arquivos_divididos/")
    print(f"    📁 backup_original/")
    
    total_linhas = len(df)
    linhas_por_arquivo = 25000
    numero_arquivo = 1
    
    # Gerar nome base com data atual
    from datetime import datetime
    data_atual = datetime.now().strftime("%d_%m_%Y")
    nome_base = f"URA_AGUASG_{data_atual}"
    
    for inicio in range(0, total_linhas, linhas_por_arquivo):
        fim = min(inicio + linhas_por_arquivo, total_linhas)
        df_parte = df.iloc[inicio:fim].copy()
        
        nome_arquivo = f"{nome_base}_{numero_arquivo}.csv"
        caminho_arquivo = os.path.join(pasta_arquivos_divididos, nome_arquivo)
        
        df_parte.to_csv(caminho_arquivo, index=False, encoding='utf-8', sep=';', header=False)
        
        print(f"  ✅ {nome_arquivo} - {len(df_parte):,} linhas (linhas {inicio+1:,} a {fim:,})")
        numero_arquivo += 1
    
    # Salvar arquivo principal processado
    arquivo_principal = os.path.join(pasta_principal, "CLIENTES_PROCESSADOS_COMPLETO.csv")
    df.to_csv(arquivo_principal, index=False, encoding='utf-8', sep=';', header=False)
    
    # Fazer backup do arquivo original
    import shutil
    arquivo_backup = os.path.join(pasta_backup, nome_arquivo_original)
    shutil.copy2(nome_arquivo_original, arquivo_backup)
    
    # Mover arquivo original para pasta de backup global
    pasta_originais_global = "ARQUIVOS_ORIGINAIS"
    os.makedirs(pasta_originais_global, exist_ok=True)
    arquivo_original_destino = os.path.join(pasta_originais_global, nome_arquivo_original)
    
    # Se já existe, adicionar timestamp para evitar conflito
    if os.path.exists(arquivo_original_destino):
        nome_base, extensao = os.path.splitext(nome_arquivo_original)
        timestamp_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_original_destino = os.path.join(pasta_originais_global, f"{nome_base}_{timestamp_arquivo}{extensao}")
    
    shutil.move(nome_arquivo_original, arquivo_original_destino)
    print(f"📁 Arquivo original movido para: {pasta_originais_global}/")
    
    # Criar arquivo de relatório
    relatorio_path = os.path.join(pasta_principal, "RELATORIO_PROCESSAMENTO.txt")
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE PROCESSAMENTO DE DADOS\n")
        f.write("=" * 60 + "\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Arquivo original: {nome_arquivo_original}\n")
        f.write(f"Total de registros originais: {len(df) + (telefones_antes - telefones_depois):,}\n")
        f.write(f"Total de registros processados: {len(df):,}\n")
        f.write(f"Telefones duplicados removidos: {telefones_antes - telefones_depois:,}\n")
        f.write(f"Arquivos gerados: {numero_arquivo - 1}\n")
        f.write(f"Registros por arquivo: 25.000 (exceto o último)\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("ESTRUTURA DE ARQUIVOS:\n")
        f.write("=" * 60 + "\n")
        f.write("📁 PROCESSAMENTO_YYYYMMDD_HHMMSS/\n")
        f.write("  📄 CLIENTES_PROCESSADOS_COMPLETO.csv\n")
        f.write("  📄 RELATORIO_PROCESSAMENTO.txt\n")
        f.write("  📁 arquivos_divididos/\n")
        f.write(f"    📄 {nome_base}_1.csv\n")
        f.write(f"    📄 {nome_base}_2.csv\n")
        f.write(f"    📄 ... (até {numero_arquivo - 1})\n")
        f.write("  📁 backup_original/\n")
        f.write(f"    📄 {nome_arquivo_original}\n")
        f.write("📁 ARQUIVOS_ORIGINAIS/ (pasta global)\n")
        f.write(f"  📄 {nome_arquivo_original} (movido da pasta principal)\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write("COLUNAS DOS ARQUIVOS:\n")
        f.write("=" * 60 + "\n")
        f.write("Coluna A: Códigos únicos (4 letras + 4 números)\n")
        f.write("Coluna B: Nomes dos clientes\n")
        f.write("Coluna C: Números de telefone únicos\n")
        f.write("Separador: Ponto e vírgula (;)\n")
        f.write("Encoding: UTF-8\n")
    
    print(f"\n📄 Arquivo principal salvo: CLIENTES_PROCESSADOS_COMPLETO.csv")
    print(f"📄 Relatório criado: RELATORIO_PROCESSAMENTO.txt")
    print(f"💾 Backup do original salvo em: backup_original/")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"=" * 60)
    print(f"📊 Total de registros processados: {len(df):,}")
    print(f"📁 Arquivos gerados: {numero_arquivo - 1}")
    print(f"📂 Pasta principal: {pasta_principal}/")
    print(f"⏰ Processado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"=" * 60)

if __name__ == "__main__":
    processar_csv()
