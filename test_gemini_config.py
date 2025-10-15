import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_gemini_config():
    print("🚀 TESTANDO CONEXÃO COM GEMINI...")
    
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY não encontrada no .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...")
    
    try:
        genai.configure(api_key=api_key)
        
        # Listar modelos disponíveis
        print("🔍 Procurando modelos disponíveis...")
        models = genai.list_models()
        
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)
                print(f"   ✅ {model.name}")
        
        if not available_models:
            print("❌ Nenhum modelo compatível encontrado")
            return False
            
        # Tentar usar o modelo mais comum
        if "models/gemini-1.0-pro" in available_models:
            model_name = "gemini-1.0-pro"
        elif "models/gemini-pro" in available_models:
            model_name = "gemini-pro"
        else:
            model_name = available_models[0].split('/')[-1]
            
        print(f"🎯 Usando modelo: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            "Explique em uma frase o conceito de Vehicle Routing Problem com restrições de capacidade."
        )
        
        print("✅ Conexão com Gemini: SUCESSO!")
        print(f"📝 Resposta: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    test_gemini_config()