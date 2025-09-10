import re
import os
import glob
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
import time

class AlimentadorAutomatico:
    def __init__(self):
        self.url = "https://portesmarinho.alimentador.vonixcc.com.br/session/new"
        self.usuario = "portes"
        self.senha = "portes1234"
        self.browser = None
        self.context = None
        self.page = None
    
    def iniciar_navegador(self, headless=False):
        """Inicia o navegador e abre a página"""
        print("🚀 Iniciando navegador...")
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
        print(f"🌐 Acessando: {self.url}")
        self.page.goto(self.url)
        print("✅ Página carregada com sucesso!")
    
    def fazer_login(self):
        """Realiza o login no sistema"""
        print("🔐 Realizando login...")
        
        try:
            # Preencher usuário
            print("  📝 Preenchendo usuário...")
            self.page.locator("#username").click()
            self.page.locator("#username").fill(self.usuario)
            
            # Preencher senha
            print("  🔑 Preenchendo senha...")
            self.page.get_by_role("textbox", name="Senha").click()
            self.page.get_by_role("textbox", name="Senha").fill(self.senha)
            
            # Clicar em entrar
            print("  🎯 Clicando em 'Entrar'...")
            self.page.get_by_role("button", name="Entrar").click()
            
            # Aguardar carregamento da página após login
            print("  ⏳ Aguardando carregamento...")
            time.sleep(3)
            
            print("✅ Login realizado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante o login: {e}")
            return False
    
    def encontrar_botao_importar(self):
        """Encontra e clica no botão 'Importar'"""
        print("🔍 Procurando botão 'Importar'...")
        
        try:
            # Seletor efetivo identificado no log
            print("  🔎 Usando seletor: a:has-text('Importar')")
            botao = self.page.locator("a:has-text('Importar')")
            
            if botao.count() > 0:
                print("  ✅ Botão encontrado!")
                botao.click()
                print("✅ Botão 'Importar' clicado com sucesso!")
                return True
            else:
                print("❌ Botão 'Importar' não encontrado")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao procurar botão 'Importar': {e}")
            return False
    
    def diagnosticar_dropdown(self):
        """Diagnostica o tipo de dropdown e suas propriedades"""
        print("🔬 DIAGNÓSTICO DO DROPDOWN")
        print("=" * 40)
        
        try:
            # Procurar o dropdown de fila
            dropdown = self.page.locator("#shipment_queue_id")
            
            if dropdown.count() == 0:
                print("❌ Dropdown não encontrado!")
                return False
            
            print("✅ Dropdown encontrado!")
            
            # Analisar propriedades do elemento
            print("\n📋 PROPRIEDADES DO ELEMENTO:")
            print(f"  Tag: {dropdown.evaluate('el => el.tagName')}")
            print(f"  Tipo: {dropdown.get_attribute('type')}")
            print(f"  Classe: {dropdown.get_attribute('class')}")
            print(f"  ID: {dropdown.get_attribute('id')}")
            print(f"  Name: {dropdown.get_attribute('name')}")
            print(f"  Disabled: {dropdown.get_attribute('disabled')}")
            print(f"  Readonly: {dropdown.get_attribute('readonly')}")
            
            # Verificar se é um select nativo
            tag_name = dropdown.evaluate('el => el.tagName')
            if tag_name.upper() == "SELECT":
                print("\n✅ É um SELECT nativo!")
                return self.analisar_select_nativo(dropdown)
            else:
                print(f"\n⚠️  Não é um SELECT nativo! Tag: {tag_name}")
                return self.analisar_dropdown_customizado(dropdown)
                
        except Exception as e:
            print(f"❌ Erro no diagnóstico: {e}")
            return False
    
    def analisar_select_nativo(self, dropdown):
        """Analisa um select nativo"""
        print("\n🔍 ANALISANDO SELECT NATIVO:")
        
        try:
            # Contar opções
            opcoes = dropdown.locator("option")
            total_opcoes = opcoes.count()
            print(f"  📊 Total de opções: {total_opcoes}")
            
            # Listar algumas opções
            print("\n📋 PRIMEIRAS 10 OPÇÕES:")
            for i in range(min(10, total_opcoes)):
                try:
                    opcao = opcoes.nth(i)
                    texto = opcao.text_content().strip()
                    valor = opcao.get_attribute("value")
                    print(f"  {i+1:2d}. '{texto}' (value='{valor}')")
                except:
                    print(f"  {i+1:2d}. [Erro ao ler opção]")
            
            if total_opcoes > 10:
                print(f"  ... e mais {total_opcoes - 10} opções")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao analisar select: {e}")
            return False
    
    def analisar_dropdown_customizado(self, dropdown):
        """Analisa um dropdown customizado"""
        print("\n🔍 ANALISANDO DROPDOWN CUSTOMIZADO:")
        
        try:
            # Tentar clicar para abrir
            print("  🖱️  Tentando abrir dropdown...")
            dropdown.click()
            time.sleep(2)
            
            # Procurar por elementos que possam ser opções
            seletores_opcoes = [
                "option",
                "[role='option']",
                ".option",
                ".dropdown-item",
                ".select-option",
                "li",
                "div[data-value]",
                "span[data-value]"
            ]
            
            for seletor in seletores_opcoes:
                opcoes = self.page.locator(seletor)
                count = opcoes.count()
                if count > 0:
                    print(f"  ✅ Encontradas {count} opções com seletor: {seletor}")
                    
                    # Listar algumas opções
                    print(f"  📋 PRIMEIRAS 5 OPÇÕES ({seletor}):")
                    for i in range(min(5, count)):
                        try:
                            opcao = opcoes.nth(i)
                            texto = opcao.text_content().strip()
                            valor = opcao.get_attribute("value") or opcao.get_attribute("data-value") or "N/A"
                            print(f"    {i+1}. '{texto}' (value='{valor}')")
                        except:
                            print(f"    {i+1}. [Erro ao ler opção]")
                    break
            else:
                print("  ❌ Nenhuma opção encontrada com seletores conhecidos")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao analisar dropdown customizado: {e}")
            return False
    
    def selecionar_fila_ura_aguas(self):
        """Seleciona a fila 'URA-AGUAS' no dropdown"""
        print("📋 Selecionando fila 'URA-AGUAS'...")
        
        try:
            # Aguardar carregamento
            print("  ⏳ Aguardando carregamento da página...")
            time.sleep(2)
            
            # Fazer diagnóstico primeiro
            if not self.diagnosticar_dropdown():
                return False
            
            print("\n" + "=" * 40)
            print("🎯 TENTANDO SELECIONAR URA-AGUAS...")
            print("=" * 40)
            
            # Aqui vamos implementar a lógica baseada no diagnóstico
            # Por enquanto, vamos tentar o método original
            return self.tentar_selecao_original()
                
        except Exception as e:
            print(f"❌ Erro ao selecionar fila: {e}")
            return False
    
    def tentar_selecao_original(self):
        """Tenta a seleção usando métodos específicos para SELECT nativo"""
        try:
            dropdown = self.page.locator("#shipment_queue_id")
            
            print("  🎯 Tentando seleção por value...")
            # Método 1: Selecionar por value usando select_option
            try:
                dropdown.select_option(value="10")
                time.sleep(1)
                
                # Verificar se foi selecionada
                valor_selecionado = dropdown.input_value()
                if valor_selecionado == "10":
                    print("  ✅ Selecionada com sucesso por value!")
                    return True
                else:
                    print(f"  ❌ Falha na seleção por value. Valor atual: '{valor_selecionado}'")
            except Exception as e:
                print(f"  ❌ Erro na seleção por value: {e}")
            
            print("  🎯 Tentando seleção por texto...")
            # Método 2: Selecionar por texto
            try:
                dropdown.select_option(label="URA-AGUAS")
                time.sleep(1)
                
                # Verificar se foi selecionada
                valor_selecionado = dropdown.input_value()
                if valor_selecionado == "10":
                    print("  ✅ Selecionada com sucesso por texto!")
                    return True
                else:
                    print(f"  ❌ Falha na seleção por texto. Valor atual: '{valor_selecionado}'")
            except Exception as e:
                print(f"  ❌ Erro na seleção por texto: {e}")
            
            print("  🎯 Tentando seleção por índice...")
            # Método 3: Encontrar o índice e selecionar
            try:
                opcoes = dropdown.locator("option")
                total_opcoes = opcoes.count()
                
                for i in range(total_opcoes):
                    opcao = opcoes.nth(i)
                    texto = opcao.text_content().strip()
                    valor = opcao.get_attribute("value")
                    
                    if "URA-AGUAS" in texto.upper():
                        print(f"  🎯 Encontrada no índice {i}: '{texto}' (value='{valor}')")
                        
                        # Selecionar por índice
                        dropdown.select_option(index=i)
                        time.sleep(1)
                        
                        # Verificar seleção
                        valor_selecionado = dropdown.input_value()
                        if valor_selecionado == valor:
                            print(f"  ✅ Selecionada com sucesso por índice!")
                            return True
                        else:
                            print(f"  ❌ Falha na seleção por índice. Valor atual: '{valor_selecionado}'")
                        break
            except Exception as e:
                print(f"  ❌ Erro na seleção por índice: {e}")
            
            print("  ❌ Todos os métodos de seleção falharam")
            return False
            
        except Exception as e:
            print(f"❌ Erro na seleção: {e}")
            return False
    
    def listar_arquivos_processados(self):
        """Lista os arquivos processados disponíveis"""
        print("📁 Procurando arquivos processados...")
        
        # Pasta de destino específica
        pasta_destino = r"S:\BACKOFFICE\Controle de Discadores e Uras\Uras\URA AGUAS BASE TODA"
        
        if not os.path.exists(pasta_destino):
            print(f"❌ Pasta de destino não encontrada: {pasta_destino}")
            print("💡 Execute primeiro o main.py para processar os arquivos")
            return []
        
        # Obter data de hoje para filtrar apenas arquivos de hoje
        from datetime import datetime
        data_hoje = datetime.now().strftime("%d_%m_%Y")
        print(f"📅 Filtrando arquivos da data: {data_hoje}")
        
        # BUSCAR ARQUIVOS SEQUENCIALMENTE (1, 2, 3, 4...)
        arquivos = []
        numero = 1
        
        print("🔍 Buscando arquivos sequencialmente...")
        
        while True:
            nome_esperado = f"URA_AGUASG_{data_hoje}_{numero}.csv"
            caminho_esperado = os.path.join(pasta_destino, nome_esperado)
            
            if os.path.exists(caminho_esperado):
                arquivos.append(caminho_esperado)
                print(f"  ✅ {numero:2d}. {nome_esperado}")
                numero += 1
            else:
                # Se não encontrou o arquivo, verificar se há mais arquivos
                # Procurar por arquivos com números maiores
                arquivos_restantes = []
                for i in range(numero, numero + 100):  # Verificar até 100 arquivos à frente
                    nome_teste = f"URA_AGUASG_{data_hoje}_{i}.csv"
                    caminho_teste = os.path.join(pasta_destino, nome_teste)
                    if os.path.exists(caminho_teste):
                        arquivos_restantes.append((i, caminho_teste))
                
                if arquivos_restantes:
                    # Pular para o próximo arquivo disponível
                    proximo_numero, proximo_caminho = min(arquivos_restantes, key=lambda x: x[0])
                    print(f"  ⏭️  Pulando para arquivo {proximo_numero}")
                    numero = proximo_numero
                else:
                    # Não há mais arquivos
                    break
        
        if not arquivos:
            print(f"❌ Nenhum arquivo URA_AGUASG de hoje ({data_hoje}) encontrado em: {pasta_destino}")
            print("💡 Execute primeiro o main.py para processar os arquivos")
            return []
        
        print(f"\n📊 Total de arquivos encontrados: {len(arquivos)}")
        
        print(f"📄 Encontrados {len(arquivos)} arquivos para importar:")
        
        for i, arquivo in enumerate(arquivos, 1):
            nome_arquivo = os.path.basename(arquivo)
            tamanho = os.path.getsize(arquivo)
            data_modificacao = os.path.getmtime(arquivo)
            data_formatada = datetime.fromtimestamp(data_modificacao).strftime("%d/%m/%Y %H:%M")
            print(f"  {i}. {nome_arquivo} ({tamanho:,} bytes) - {data_formatada}")
        
        return arquivos
    
    def fazer_upload_arquivo(self, caminho_arquivo):
        """Faz upload de um arquivo específico"""
        print(f"📤 Fazendo upload do arquivo: {os.path.basename(caminho_arquivo)}")
        
        try:
            # Localizar o input de arquivo
            input_arquivo = self.page.locator("#shipment_batch")
            
            if input_arquivo.count() == 0:
                print("❌ Input de arquivo não encontrado!")
                return False
            
            print("  ✅ Input de arquivo encontrado")
            
            # Fazer upload do arquivo
            print("  📁 Selecionando arquivo...")
            input_arquivo.set_input_files(caminho_arquivo)
            
            # Aguardar um pouco para o arquivo ser processado
            time.sleep(2)
            
            print("  ✅ Arquivo selecionado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao fazer upload: {e}")
            return False
    
    def clicar_iniciar_importacao(self):
        """Clica no botão 'Iniciar importação'"""
        print("🚀 Clicando em 'Iniciar importação'...")
        
        try:
            # Localizar o botão de submit
            botao_importar = self.page.locator("#shipment_submit")
            
            if botao_importar.count() == 0:
                print("❌ Botão 'Iniciar importação' não encontrado!")
                return False
            
            print("  ✅ Botão encontrado")
            
            # Clicar no botão
            botao_importar.click()
            print("  ✅ Botão clicado com sucesso!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao clicar no botão: {e}")
            return False
    
    def aguardar_importacao(self, minutos=3):
        """Aguarda a importação ser concluída"""
        print(f"⏳ Aguardando {minutos} minutos para importação...")
        
        for i in range(minutos):
            print(f"  ⏰ {i+1}/{minutos} minutos...")
            time.sleep(60)  # Aguardar 1 minuto
        
        print("  ✅ Tempo de espera concluído!")
    
    def processar_todos_arquivos(self):
        """Processa todos os arquivos sequencialmente"""
        print("🔄 PROCESSANDO TODOS OS ARQUIVOS")
        print("=" * 50)
        
        # Obter lista de arquivos
        arquivos = self.listar_arquivos_processados()
        
        if not arquivos:
            print("❌ Nenhum arquivo para processar!")
            return False
        
        print(f"📊 Total de arquivos para processar: {len(arquivos)}")
        
        # Processar cada arquivo
        for i, arquivo in enumerate(arquivos, 1):
            print(f"\n{'='*60}")
            print(f"📁 PROCESSANDO ARQUIVO {i}/{len(arquivos)}")
            print(f"📄 Arquivo: {os.path.basename(arquivo)}")
            print(f"{'='*60}")
            
            try:
                # 1. Fazer upload do arquivo
                if not self.fazer_upload_arquivo(arquivo):
                    print(f"❌ Falha no upload do arquivo {i}")
                    continue
                
                # 2. Clicar em iniciar importação
                if not self.clicar_iniciar_importacao():
                    print(f"❌ Falha ao iniciar importação do arquivo {i}")
                    continue
                
                # 3. Aguardar importação (exceto no último arquivo)
                if i < len(arquivos):
                    self.aguardar_importacao(3)
                    
                    # 4. Voltar para a página de importação para o próximo arquivo
                    print("🔄 Voltando para página de importação...")
                    if not self.encontrar_botao_importar():
                        print("❌ Falha ao voltar para importação")
                        break
                    
                    if not self.selecionar_fila_ura_aguas():
                        print("❌ Falha ao selecionar fila novamente")
                        break
                
                print(f"✅ Arquivo {i} processado com sucesso!")
                
            except Exception as e:
                print(f"❌ Erro ao processar arquivo {i}: {e}")
                continue
        
        print(f"\n🎉 PROCESSAMENTO CONCLUÍDO!")
        print(f"📊 Total de arquivos processados: {len(arquivos)}")
        return True
    
    def fechar_navegador(self):
        """Fecha o navegador"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        print("🔒 Navegador fechado")

def executar_fluxo_completo():
    """Executa o fluxo completo de automação"""
    print("=" * 60)
    print("🤖 INICIANDO AUTOMAÇÃO DO ALIMENTADOR")
    print("=" * 60)
    
    alimentador = AlimentadorAutomatico()
    
    try:
        # 1. Iniciar navegador
        alimentador.iniciar_navegador(headless=False)
        
        # 2. Fazer login
        if not alimentador.fazer_login():
            print("❌ Falha no login. Encerrando...")
            return False
        
        # 3. Procurar botão Importar
        if not alimentador.encontrar_botao_importar():
            print("❌ Botão 'Importar' não encontrado. Encerrando...")
            return False
        
        # 4. Selecionar fila URA-AGUAS
        if not alimentador.selecionar_fila_ura_aguas():
            print("❌ Falha ao selecionar fila 'URA-AGUAS'. Encerrando...")
            return False
        
        # 5. Listar arquivos disponíveis
        arquivos = alimentador.listar_arquivos_processados()
        
        print("\n" + "=" * 60)
        print("✅ FLUXO INICIAL CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("📋 Próximos passos:")
        print("  1. Implementar upload de arquivos")
        print("  2. Configurar processamento automático")
        print("  3. Adicionar validações e tratamento de erros")
        
        # Manter navegador aberto para testes
        input("\n⏸️  Pressione Enter para fechar o navegador...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return False
        
    finally:
        alimentador.fechar_navegador()

if __name__ == "__main__":
    executar_fluxo_completo()
