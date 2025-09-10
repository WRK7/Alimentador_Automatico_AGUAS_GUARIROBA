"""
Teste de diagnóstico do dropdown
"""

from automacao import AlimentadorAutomatico

def testar_diagnostico_dropdown():
    """Testa apenas o diagnóstico do dropdown"""
    print("🔬 TESTE DE DIAGNÓSTICO DO DROPDOWN")
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
        
        # 4. Fazer diagnóstico do dropdown
        print("4️⃣ Fazendo diagnóstico do dropdown...")
        if not alimentador.diagnosticar_dropdown():
            print("❌ Falha no diagnóstico")
            return False
        
        print("\n✅ DIAGNÓSTICO CONCLUÍDO!")
        print("📋 Verifique as informações acima para entender o tipo de dropdown")
        
        # Manter navegador aberto para inspeção manual
        input("\n⏸️  Pressione Enter para fechar o navegador...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False
        
    finally:
        alimentador.fechar_navegador()

if __name__ == "__main__":
    testar_diagnostico_dropdown()
