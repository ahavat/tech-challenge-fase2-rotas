# visualization.py

import pygame

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREY = (240, 240, 240)
DARK_GREY = (50, 50, 50)
DEPOT_COLOR = (0, 0, 139)
PRIORITY_HIGHLIGHT_COLOR = (255, 215, 0)

# Cores da barra de carga
LOAD_BAR_GREEN = (0, 180, 0)
LOAD_BAR_YELLOW = (255, 200, 0)
LOAD_BAR_RED = (220, 20, 20)

ROUTE_COLORS = [
    (29, 108, 224), (24, 163, 114), (230, 111, 16),
    (118, 54, 204), (204, 54, 155)
]

def init_pygame(width, height, caption):
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption(caption)
    # Fonte levemente ajustada para melhor encaixe
    font = pygame.font.SysFont('Arial', 17)
    return screen, font

def draw_delivery_points(screen, delivery_points):
    for point in delivery_points:
        if point.is_depot:
            pygame.draw.circle(screen, WHITE, (point.x, point.y), 12)
            pygame.draw.circle(screen, DEPOT_COLOR, (point.x, point.y), 10)
        else:
            if point.priority == 1:
                pygame.draw.circle(screen, PRIORITY_HIGHLIGHT_COLOR, (point.x, point.y), 11)
            pygame.draw.circle(screen, RED, (point.x, point.y), 7)

def draw_routes(screen, solution, points_dict, fleet):
    color_index = 0
    depot = next((p for p in points_dict.values() if p.is_depot), None)
    if not depot: return
    for vehicle_id, route_pids in solution.items():
        if not route_pids: continue
        color = ROUTE_COLORS[color_index % len(ROUTE_COLORS)]
        full_route_pids = [depot.id] + route_pids + [depot.id]
        for i in range(len(full_route_pids) - 1):
            from_point = points_dict[full_route_pids[i]]
            to_point = points_dict[full_route_pids[i+1]]
            pygame.draw.line(screen, color, (from_point.x, from_point.y), (to_point.x, to_point.y), 3)
        color_index += 1

def display_info(screen, font, position_rect, generation, metrics):
    pygame.draw.rect(screen, GREY, position_rect)
    pygame.draw.rect(screen, DARK_GREY, position_rect, 2)
    line_height, start_y = 22, position_rect.y + 10
    texts = [
        f"Geracao: {generation}",
        f"Fitness (Custo Total): {metrics.get('fitness', 0):.2f}",
        f"Distancia Total: {metrics.get('total_distance', 0):.2f}",
        f"Penalidade (Capacidade): {metrics.get('capacity_penalty', 0):.2f}",
        f"Penalidade (Autonomia): {metrics.get('autonomy_penalty', 0):.2f}",
        f"Penalidade (Prioridade): {metrics.get('priority_penalty', 0):.2f}",
    ]
    for i, text in enumerate(texts):
        rendered_text = font.render(text, True, DARK_GREY)
        screen.blit(rendered_text, (position_rect.x + 15, start_y + i * line_height))

def draw_performance_graph(screen, font, history, position_rect, title):
    """Função de desenho do gráfico com lógica de escala aprimorada."""
    pygame.draw.rect(screen, GREY, position_rect)
    pygame.draw.rect(screen, DARK_GREY, position_rect, 2)
    title_text = font.render(title, True, DARK_GREY)
    screen.blit(title_text, (position_rect.x + 10, position_rect.y + 10))
    if len(history) < 2: return

    # --- LÓGICA DE ESCALA CORRIGIDA ---
    max_value = max(history) if history else 0
    min_value = min(history) if history else 0
    value_range = max_value - min_value
    # Adiciona um pequeno padding ao range para evitar que o gráfico fique colado no topo/fundo
    if value_range == 0: value_range = 1
    
    graph_points = []
    drawable_area = position_rect.inflate(-10, -40) # Área útil para o desenho

    for i, value in enumerate(history):
        # Posição X proporcional ao número de gerações
        x = drawable_area.x + (i / (len(history) - 1)) * drawable_area.width
        # Posição Y proporcional ao valor, mapeado para a altura da área útil
        y = drawable_area.bottom - ((value - min_value) / value_range) * drawable_area.height
        graph_points.append((x, y))

    if len(graph_points) >= 2:
        pygame.draw.lines(screen, (29, 108, 224), False, graph_points, 2)
        
    # Legendas
    gen_label = font.render(f"Gerações: {len(history)}", True, DARK_GREY)
    screen.blit(gen_label, (position_rect.x + 10, position_rect.bottom - 25))
    
    curr_fit_label = font.render(f"Fitness Atual: {history[-1]:.0f}", True, DARK_GREY)
    text_width, _ = curr_fit_label.get_size()
    screen.blit(curr_fit_label, (position_rect.right - text_width - 10, position_rect.y + 10))

def draw_vehicle_status(screen, font, position_rect, fleet, metrics):
    pygame.draw.rect(screen, GREY, position_rect)
    pygame.draw.rect(screen, DARK_GREY, position_rect, 2)
    title_text = font.render("Status da Frota (Carga)", True, DARK_GREY)
    screen.blit(title_text, (position_rect.x + 10, position_rect.y + 10))
    line_height, bar_height = 35, 15
    start_y = position_rect.y + 40
    for i, vehicle in enumerate(fleet):
        load = metrics.get('vehicle_loads', {}).get(vehicle.id, 0)
        capacity = vehicle.capacity
        load_percent = min(1.0, (load / capacity)) if capacity > 0 else 0 # Garante que não passe de 100%
        
        vehicle_text = font.render(f"{vehicle.name}: {load:.1f} / {capacity:.1f}", True, DARK_GREY)
        screen.blit(vehicle_text, (position_rect.x + 15, start_y + i * line_height))

        # --- BARRAS DE CARGA CORRIGIDAS ---
        bar_x = position_rect.x + 160
        bar_width = position_rect.width - 175 # Espaço para a barra
        bar_color = LOAD_BAR_GREEN
        if load_percent > 0.95: bar_color = LOAD_BAR_RED
        elif load_percent > 0.75: bar_color = LOAD_BAR_YELLOW
        fill_width = bar_width * load_percent
        
        pygame.draw.rect(screen, DARK_GREY, (bar_x, start_y + i * line_height + 2, bar_width, bar_height))
        if fill_width > 0:
            pygame.draw.rect(screen, bar_color, (bar_x, start_y + i * line_height + 2, fill_width, bar_height))

def draw_final_summary(screen, font, metrics, total_time, generations):
    # (código inalterado)
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    title_text = title_font.render("Simulação Concluída", True, WHITE)
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, 100))
    screen.blit(title_text, title_rect)
    summary_font = pygame.font.SysFont('Arial', 28)
    texts = [
        f"Total de Gerações Executadas: {generations}",
        f"Tempo de Otimização: {total_time:.2f} segundos", "---",
        "MELHOR SOLUÇÃO ENCONTRADA:",
        f"  - Custo (Fitness) Final: {metrics.get('fitness', 0):.2f}",
        f"  - Distância Total: {metrics.get('total_distance', 0):.2f}",
        f"  - Penalidades Finais (Cap/Aut/Prio): {metrics.get('capacity_penalty', 0):.0f} / {metrics.get('autonomy_penalty', 0):.0f} / {metrics.get('priority_penalty', 0):.0f}",
    ]
    for i, text in enumerate(texts):
        rendered_text = summary_font.render(text, True, WHITE if "---" not in text else GREY)
        text_rect = rendered_text.get_rect(center=(screen.get_width() / 2, 200 + i * 40))
        screen.blit(rendered_text, text_rect)