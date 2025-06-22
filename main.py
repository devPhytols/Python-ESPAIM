from pymem import Pymem
from pyray import *
from helper import *
from ctypes import *
import math

def init():
    win = get_window_info("AssaultCube")
    set_trace_log_level(5)
    set_target_fps(0)
    set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED)
    set_config_flags(ConfigFlags.FLAG_WINDOW_MOUSE_PASSTHROUGH)
    set_config_flags(ConfigFlags.FLAG_WINDOW_TRANSPARENT)
    set_config_flags(ConfigFlags.FLAG_WINDOW_TOPMOST)
    init_window(win[2], win[3], "AssaultCube ESP")
    set_window_position(win[0], win[1])

def draw_esp_box(head_screen, feet_screen, color, player_name, health, distance):
    # Calculando as dimensões da box usando posições reais da cabeça e pé do miseravewl
    box_height = abs(feet_screen.y - head_screen.y)
    box_width = box_height * 0.4  # Proporção padrão do AssaultCube[6]
    # Definundo dimensões mínimas para jogadores caso a distancia fique muito longe
    if box_height < 40:
        box_height = 40
        box_width = 20
    # Posicionando os itens da box (fixar depois a cabeça e pés)
    box_x = head_screen.x - box_width // 2
    box_y = head_screen.y  # Defidndo o topo da box na cabeça
    # Montando a box principal pra inimigos e time
    draw_rectangle_lines(int(box_x), int(box_y), int(box_width), int(box_height), color)
    # Exibindo infos (Testes)
    info_text = f"{player_name.decode('utf-8', errors='ignore')}"
    health_text = f"HP: {health}"
    distance_text = f"{distance:.0f}m"
    # Posicionando alguns textos (em cima da box)
    text_y = box_y - 45
    text_x = head_screen.x - len(info_text) * 3
    # Nome do Personagem
    draw_text(info_text, int(text_x), int(text_y), 12, WHITE)
    # ESP de vida do boneco
    health_color = GREEN if health > 75 else (ORANGE if health > 25 else RED)
    draw_text(health_text, int(text_x), int(text_y + 15), 10, health_color)
    # Distância
    draw_text(distance_text, int(text_x), int(text_y + 30), 10, GRAY)
    # Barra de saúde horizontal (abaixo da box)
    bar_width = box_width * 0.8
    bar_height = 4
    bar_x = head_screen.x - bar_width // 2
    bar_y = box_y + box_height + 5
    # Fundo da barra
    draw_rectangle(int(bar_x), int(bar_y), int(bar_width), int(bar_height), BLACK)
    # Barra de saúde preenchida
    health_percentage = max(0, min(health / 100.0, 1.0))
    filled_width = bar_width * health_percentage
    draw_rectangle(int(bar_x), int(bar_y), int(filled_width), int(bar_height), health_color)

def calculate_distance(pos1, pos2):
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    dz = pos1.z - pos2.z
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def main():
    proc = Pymem("ac_client.exe")
    base = proc.base_address
    
    while not window_should_close():
        matrix = proc.read_ctype(base + Pointer.view_matrix, (16 * c_float)())[:]
        player_count = proc.read_int(base + Pointer.player_count)
        # Pega o player local
        local_player_addr = proc.read_int(base + Pointer.local_player)
        local_player = proc.read_ctype(local_player_addr, Entity())
        
        begin_drawing()
        clear_background(BLANK)
        draw_fps(0, 0)
        
        if player_count > 1:
            ents = proc.read_ctype(proc.read_int(base + Pointer.entity_list), (player_count * c_int)())[1:]
            
            for ent_addr in ents:
                ent_obj = proc.read_ctype(ent_addr, Entity())
                
                if ent_obj.health > 0:
                    try:
                        # Calcular distância
                        distance = calculate_distance(local_player.pos, ent_obj.pos)
                        # Posições corretas da cabeça e pés
                        # A posição base está próxima aos pés
                        head_pos_3d = Vec3()
                        head_pos_3d.x = ent_obj.pos.x
                        head_pos_3d.y = ent_obj.pos.y
                        head_pos_3d.z = ent_obj.pos.z + 0.8  # Altura da cabeça
                        feet_pos_3d = Vec3()
                        feet_pos_3d.x = ent_obj.pos.x
                        feet_pos_3d.y = ent_obj.pos.y
                        feet_pos_3d.z = ent_obj.pos.z - 5   # Base dos pés
                        # Converter para coordenadas de tela
                        head_screen = world_to_screen(matrix, head_pos_3d)
                        feet_screen = world_to_screen(matrix, feet_pos_3d)
                        # Snapline, usar posição central
                        center_pos_3d = Vec3()
                        center_pos_3d.x = ent_obj.pos.x
                        center_pos_3d.y = ent_obj.pos.y
                        center_pos_3d.z = ent_obj.pos.z + 0.4  # Centro do corpo
                        center_screen = world_to_screen(matrix, center_pos_3d)
                        # Cor baseada no team
                        player_color = GREEN if ent_obj.team == local_player.team else RED
                        # Desenhando a ESP box
                        draw_esp_box(head_screen, feet_screen, player_color, ent_obj.name, ent_obj.health, distance)
                        # Linha do centro da tela (snapline)
                        draw_line(get_screen_width() // 2, get_screen_height() // 2, 
                                center_screen.x, center_screen.y, player_color)
                        
                    except Exception as e:
                        continue
        
        draw_text("ESP Status: Active", 10, 30, 12, GREEN)
        draw_text(f"Players: {player_count}", 10, 45, 12, WHITE)
        
        end_drawing()

if __name__ == '__main__':
    init()
    main()
