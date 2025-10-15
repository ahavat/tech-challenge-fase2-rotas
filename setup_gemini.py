import os
import subprocess
import sys

def setup_gemini():
    print("🎯 CONFIGURADOR AUTOMÁTICO DO GEMINI")
    print("=" * 50)
    
    # 1. Verificar se as bibliotecas estão instaladas
    print("1. 📦 Verificando dependências...")
    try:
        import google.generativeai
        print("   ✅ google-generativeai já instalado")
    except ImportError:
        print("   🔄 Instalando google-generativeai...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    
    try:
        import dotenv
        print("   ✅ python-dotenv já instalado")
    except ImportError:
        print("   🔄 Instalando python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    
    # 2. Verificar chave de API
    print("\n2. 🔑 Verificando configuração da API Key...")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if api_key:
        print(f"   ✅ GOOGLE_API_KEY encontrada: {api_key[:10]}...")
    else:
        print("   ❌ GOOGLE_API_KEY não configurada")
        print("\n   📝 INSTRUÇÕES PARA CONFIGURAR:")
        print("   👉 1. Acesse: https://aistudio.google.com/app/apikey")
        print("   👉 2. Clique em 'Create API Key'")
        print("   👉 3. Copie a chave gerada")
        print("   👉 4. Execute um dos comandos abaixo:")
        print("\n   PowerShell:")
        print('      $env:GOOGLE_API_KEY="sua_chave_aqui"')
        print("\n   Command Prompt:")
        print("      set GOOGLE_API_KEY=sua_chave_aqui")
        print("\n   Linux/Mac:")
        print('      export GOOGLE_API_KEY="sua_chave_aqui"')
        
        # Oferecer para criar arquivo .env
        create_env = input("\n   Deseja criar um arquivo .env? (s/n): ")
        if create_env.lower() == 's':
            key = input("   Cole sua API Key: ").strip()
            with open('.env', 'w') as f:
                f.write(f'GOOGLE_API_KEY={key}\n')
            print("   ✅ Arquivo .env criado!")
    
    # 3. Testar conexão
    print("\n3. 🚀 Testando conexão com Gemini...")
    if api_key or os.path.exists('.env'):
        try:
            from test_gemini_config import test_gemini_config
            test_gemini_config()
        except:
            print("   ⚠️  Execute: python test_gemini_config.py para testar a conexão")
    else:
        print("   ⚠️  Configure a API Key primeiro")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("👉 Execute: python test_system.py")
    print("👉 Ou: python main.py")

if __name__ == "__main__":
    setup_gemini()