"""
Teste específico para a seleção da fila URA-AGUAS
"""

from automacao import AlimentadorAutomatico

def testar_selecao_fila():
    """Testa apenas a seleção da fila URA-AGUAS"""
    print("🧪 TESTE DE SELEÇÃO DE FILA URA-AGUAS")
    print("=" * 50)
    
    alimentador = AlimentadorAutomatico()
    
    try:
        # 1. Iniciar navegador
        print("1️⃣ Iniciando navegador...")
        alimentador.iniciar_navegador(headless=False)
        
        # 2. Fazer login
        print("2️⃣ Fazendo login...")
        if not alimentador.fazer_login():
            print("❌ Falha no login")
            return False
        
        # 3. Clicar em Importar
        print("3️⃣ Clicando em Importar...")
        if not alimentador.encontrar_botao_importar():
            print("❌ Falha ao clicar em Importar")
            return False
        
        # 4. Selecionar fila URA-AGUAS
        print("4️⃣ Selecionando fila URA-AGUAS...")
        if not alimentador.selecionar_fila_ura_aguas():
            print("❌ Falha ao selecionar fila")
            return False
        
        print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("🎯 Fila 'URA-AGUAS' selecionada corretamente!")
        
        # Manter navegador aberto para verificação
        input("\n⏸️  Pressione Enter para fechar o navegador...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False
        
    finally:
        alimentador.fechar_navegador()

if __name__ == "__main__":
    testar_selecao_fila()
