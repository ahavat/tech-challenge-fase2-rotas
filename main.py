import logging
import time
from data.example_data import create_example_delivery_points, create_example_fleet, get_points_dict
from algorithms.genetic_algorithm import GeneticAlgorithm
from utils.llm_helper import LLMHelper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 INICIANDO SISTEMA DE OTIMIZAÇÃO DE ROTAS HOSPITALARES")
    print("=" * 60)
    
    # Criar dados de exemplo
    delivery_points = create_example_delivery_points()
    fleet = create_example_fleet()
    
    print(f"📦 Pontos de entrega: {len(delivery_points)}")
    print(f"🚚 Frota disponível: {len(fleet)} veículos")
    print(f"⚠️  Entregas críticas: {sum(1 for p in delivery_points if p.priority == 1)}")
    
    # Executar algoritmo genético
    print("\n🧬 EXECUTANDO ALGORITMO GENÉTICO...")
    start_time = time.time()
    
    ga = GeneticAlgorithm(
        delivery_points=delivery_points,
        fleet=fleet,
        population_size=40,
        generations=80,
        mutation_probability=0.15
    )
    
    best_solution, metrics = ga.run()
    
    execution_time = time.time() - start_time
    print(f"⏱️  Tempo de execução: {execution_time:.2f} segundos")
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("🎯 MELHOR SOLUÇÃO ENCONTRADA:")
    print("=" * 60)
    
    total_deliveries = 0
    for vehicle_id, route in best_solution.items():
        vehicle = next(v for v in fleet if v.id == vehicle_id)
        critical_in_route = sum(1 for pid in route 
                              if next(p for p in delivery_points if p.id == pid).priority == 1)
        
        print(f"\n🚚 {vehicle.name} (Capacidade: {vehicle.capacity}, Autonomia: {vehicle.autonomy}km):")
        print(f"   📍 Rota com {len(route)} entregas ({critical_in_route} críticas)")
        print(f"   🛣️  Pontos: {route}")
        total_deliveries += len(route)
    
    print(f"\n📊 TOTAL: {total_deliveries} entregas distribuídas")
    
    # Gerar instruções com LLM
    print("\n" + "=" * 60)
    print("🤖 GERANDO INSTRUÇÕES COM IA...")
    print("=" * 60)
    
    llm = LLMHelper()  # Usará mock se não tiver API key
    points_data = get_points_dict(delivery_points)
    
    instructions = llm.generate_delivery_instructions(best_solution, points_data, metrics)
    print(instructions)
    
    # Gerar relatório de desempenho
    print("\n" + "=" * 60)
    print("📈 RELATÓRIO DE DESEMPENHO:")
    print("=" * 60)
    
    report = llm.generate_performance_report(metrics)
    print(report)
    
    print("\n✅ SISTEMA EXECUTADO COM SUCESSO!")
    print("💡 Dica: Configure OPENAI_API_KEY no ambiente para instruções mais detalhadas")

if __name__ == "__main__":
    main()