"""
Sistema Completo de Alimentador Automático
Integra o processamento de arquivos com a automação web
"""

import os
import sys
from datetime import datetime
from automacao import AlimentadorAutomatico
from main import processar_csv
from config import CREDENCIAIS, NAVEGADOR

class SistemaCompleto:
    def __init__(self):
        self.alimentador = AlimentadorAutomatico()
        self.arquivos_processados = []
    
    def executar_processamento(self):
        """Executa o processamento dos arquivos CSV"""
        print("=" * 60)
        print("📊 EXECUTANDO PROCESSAMENTO DE ARQUIVOS")
        print("=" * 60)
        
        try:
            processar_csv()
            print("✅ Processamento concluído com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro durante processamento: {e}")
            return False
    
    def executar_automatizacao(self):
        """Executa a automação web"""
        print("=" * 60)
        print("🤖 EXECUTANDO AUTOMAÇÃO WEB")
        print("=" * 60)
        
        try:
            # Iniciar navegador
            self.alimentador.iniciar_navegador(headless=NAVEGADOR["headless"])
            
            # Fazer login
            if not self.alimentador.fazer_login():
                print("❌ Falha no login")
                return False
            
            # Encontrar botão importar
            if not self.alimentador.encontrar_botao_importar():
                print("❌ Botão 'Importar' não encontrado")
                return False
            
            # Selecionar fila URA-AGUAS
            if not self.alimentador.selecionar_fila_ura_aguas():
                print("❌ Falha ao selecionar fila 'URA-AGUAS'")
                return False
            
            # Listar arquivos disponíveis
            self.arquivos_processados = self.alimentador.listar_arquivos_processados()
            
            print("✅ Automação inicial concluída!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante automação: {e}")
            return False
        finally:
            # Manter navegador aberto para testes
            input("\n⏸️  Pressione Enter para fechar o navegador...")
            self.alimentador.fechar_navegador()
    
    def executar_fluxo_completo(self):
        """Executa o fluxo completo: processamento + automação"""
        print("🚀 INICIANDO SISTEMA COMPLETO")
        print("=" * 60)
        
        # 1. Processar arquivos
        if not self.executar_processamento():
            print("❌ Falha no processamento. Encerrando...")
            return False
        
        # 2. Executar automação
        if not self.executar_automatizacao():
            print("❌ Falha na automação. Encerrando...")
            return False
        
        print("\n🎉 SISTEMA COMPLETO EXECUTADO COM SUCESSO!")
        return True
    
    def executar_processamento_arquivos(self):
        """Executa o processamento automático de todos os arquivos"""
        print("=" * 60)
        print("🔄 EXECUTANDO PROCESSAMENTO AUTOMÁTICO DE ARQUIVOS")
        print("=" * 60)
        
        try:
            # Iniciar navegador
            self.alimentador.iniciar_navegador(headless=NAVEGADOR["headless"])
            
            # Fazer login
            if not self.alimentador.fazer_login():
                print("❌ Falha no login")
                return False
            
            # Clicar em Importar
            if not self.alimentador.encontrar_botao_importar():
                print("❌ Falha ao clicar em Importar")
                return False
            
            # Selecionar fila URA-AGUAS
            if not self.alimentador.selecionar_fila_ura_aguas():
                print("❌ Falha ao selecionar fila URA-AGUAS")
                return False
            
            # Processar todos os arquivos
            if not self.alimentador.processar_todos_arquivos():
                print("❌ Falha no processamento de arquivos")
                return False
            
            print("✅ Processamento automático concluído!")
            return True
            
        except Exception as e:
            print(f"❌ Erro durante processamento: {e}")
            return False
            
        finally:
            # Manter navegador aberto para verificação
            input("\n⏸️  Pressione Enter para fechar o navegador...")
            self.alimentador.fechar_navegador()
    
    def executar_fluxo_completo_automatico(self):
        """Executa o fluxo completo: processamento + upload automático"""
        print("🚀 INICIANDO SISTEMA COMPLETO AUTOMÁTICO")
        print("=" * 60)
        
        # 1. Processar arquivos CSV
        print("📊 ETAPA 1: Processando arquivos CSV...")
        if not self.executar_processamento():
            print("❌ Falha no processamento de arquivos. Encerrando...")
            return False
        
        print("\n✅ Arquivos CSV processados com sucesso!")
        
        # 2. Inicializar navegador e fazer login
        print("\n🌐 ETAPA 2: Inicializando navegador e fazendo login...")
        if not self.executar_automatizacao():
            print("❌ Falha na inicialização. Encerrando...")
            return False
        
        # 3. Processar todos os arquivos (upload automático)
        print("\n📤 ETAPA 3: Fazendo upload automático de todos os arquivos...")
        if not self.alimentador.processar_todos_arquivos():
            print("❌ Falha no upload automático")
            return False
        
        print("\n🎉 SISTEMA COMPLETO AUTOMÁTICO EXECUTADO COM SUCESSO!")
        print("📊 Todos os arquivos foram processados e enviados automaticamente!")
        return True

def menu_principal():
    """Menu principal do sistema"""
    while True:
        print("\n" + "=" * 60)
        print("🤖 ALIMENTADOR AUTOMÁTICO - MENU PRINCIPAL")
        print("=" * 60)
        print("1. 📊 Processar arquivos CSV apenas")
        print("2. 🤖 Executar automação web apenas")
        print("3. 🚀 Executar fluxo completo (processamento + automação)")
        print("4. 📁 Listar arquivos processados")
        print("5. 🔄 Processar todos os arquivos (upload automático)")
        print("6. 🎯 SISTEMA COMPLETO AUTOMÁTICO (processa + upload)")
        print("7. ❌ Sair")
        print("=" * 60)
        
        opcao = input("Escolha uma opção (1-7): ").strip()
        
        sistema = SistemaCompleto()
        
        if opcao == "1":
            sistema.executar_processamento()
        elif opcao == "2":
            sistema.executar_automatizacao()
        elif opcao == "3":
            sistema.executar_fluxo_completo()
        elif opcao == "4":
            sistema.alimentador.listar_arquivos_processados()
        elif opcao == "5":
            sistema.executar_processamento_arquivos()
        elif opcao == "6":
            sistema.executar_fluxo_completo_automatico()
        elif opcao == "7":
            print("👋 Encerrando sistema...")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
