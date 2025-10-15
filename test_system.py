# test_system.py

import logging
import time
import sys
import os
import pygame
import visualization as vis

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.example_data import create_example_delivery_points, create_example_fleet
from algorithms.genetic_algorithm import GeneticAlgorithm

logging.basicConfig(level=logging.INFO, format='INFO:%(name)s:%(message)s')

# --- CONSTANTES ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GENERATIONS_TO_RUN = 2000
CAPTION = "Tech Challenge - Dashboard de Otimizacao de Rotas"

def run_visual_test():
    """Executa o dashboard completo com dois gráficos e todos os painéis de status."""
    print("\n" + "=" * 60)
    print("🚀 INICIANDO DASHBOARD DE DESEMPENHO")
    print("=" * 60)
    print("A simulação terminará após", GENERATIONS_TO_RUN, "gerações.")

    # --- Definição das Áreas da Tela ---
    ROUTE_AREA_WIDTH = int(SCREEN_WIDTH * 0.65)
    SIDE_PANEL_WIDTH = SCREEN_WIDTH - ROUTE_AREA_WIDTH
    
    delivery_points = create_example_delivery_points(
        num_points=35, width=ROUTE_AREA_WIDTH - 50, height=SCREEN_HEIGHT - 50
    )
    fleet = create_example_fleet(num_vehicles=4)
    points_dict = {p.id: p for p in delivery_points}
    
    ga = GeneticAlgorithm(
        delivery_points=delivery_points, fleet=fleet,
        population_size=150, generations=GENERATIONS_TO_RUN, mutation_probability=0.15
    )
    
    screen, font = vis.init_pygame(SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION)
    clock = pygame.time.Clock()

    # --- LAYOUT CORRIGIDO DO PAINEL LATERAL (DIVIDIDO EM 4 SEÇÕES) ---
    panel_y_quarter = SCREEN_HEIGHT / 4
    panel_start_x = ROUTE_AREA_WIDTH + 10
    panel_width = SIDE_PANEL_WIDTH - 20
    
    # Cada painel agora tem sua própria área Y, sem sobreposição
    graph_fitness_rect = pygame.Rect(panel_start_x, 10, panel_width, panel_y_quarter * 1.5 - 20)
    graph_distance_rect = pygame.Rect(panel_start_x, panel_y_quarter * 1.5, panel_width, panel_y_quarter - 20)
    vehicle_status_rect = pygame.Rect(panel_start_x, panel_y_quarter * 2.5 - 10, panel_width, panel_y_quarter)
    info_rect = pygame.Rect(panel_start_x, panel_y_quarter * 3.5 - 5, panel_width, panel_y_quarter)

    simulation_state = "SIMULATING"
    start_time = time.time()
    total_time = 0
    running = True
    best_solution_overall, best_metrics_overall = None, {}

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        if simulation_state == "SIMULATING":
            ga.run_one_generation()
            current_best_solution, current_best_metrics = ga.get_best_solution_and_metrics()
            if not best_solution_overall or current_best_metrics.get("fitness", float('inf')) < best_metrics_overall.get("fitness", float('inf')):
                 best_solution_overall = current_best_solution
                 best_metrics_overall = current_best_metrics
            if ga.current_generation >= ga.generations:
                simulation_state = "FINISHED"
                total_time = time.time() - start_time
                print("\nSimulação concluída! Exibindo resumo final.")
        
        # --- DESENHO DO DASHBOARD ---
        screen.fill(vis.WHITE)
        
        # Área Principal (Esquerda)
        vis.draw_delivery_points(screen, delivery_points)
        if best_solution_overall:
            vis.draw_routes(screen, best_solution_overall, points_dict, fleet)
            
        # Linha Divisória
        pygame.draw.line(screen, vis.DARK_GREY, (ROUTE_AREA_WIDTH, 0), (ROUTE_AREA_WIDTH, SCREEN_HEIGHT), 3)

        # Painel Lateral (Direita) - AGORA COM LAYOUT CORRETO
        vis.draw_performance_graph(screen, font, ga.fitness_history, graph_fitness_rect, "Fitness (Custo Total) por Geracao")
        vis.draw_performance_graph(screen, font, ga.distance_history, graph_distance_rect, "Distancia Pura por Geracao")
        vis.draw_vehicle_status(screen, font, vehicle_status_rect, fleet, best_metrics_overall)
        vis.display_info(screen, font, info_rect, ga.current_generation, best_metrics_overall)
        
        # Resumo Final por cima de tudo
        if simulation_state == "FINISHED":
            vis.draw_final_summary(screen, font, best_metrics_overall, total_time, ga.generations)
            
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    print("✅ Programa encerrado.")

def main():
    run_visual_test()

if __name__ == "__main__":
    main()