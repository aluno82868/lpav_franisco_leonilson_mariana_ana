import pygame, sys, time
from constants import *
from rules import *
from ai import minimax

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Damas Portuguesas - Oficial")

def draw_screen(board, selected, turn, game_over, win_txt, time_left, p_color, m_count):
    WIN.fill(CREAM)
    for r in range(ROWS):
        for c in range((r+1)%2, COLS, 2):
            pygame.draw.rect(WIN, BROWN, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    all_v = get_all_valid_moves(board, turn) if p_color != 0 and not game_over else []
    for r in range(ROWS):
        for c in range(COLS):
            p = board[r][c]
            center = (c*SQUARE_SIZE+SQUARE_SIZE//2, r*SQUARE_SIZE+SQUARE_SIZE//2)
            if p != 0:
                pygame.draw.circle(WIN, WHITE if p%2!=0 else BLACK, center, SQUARE_SIZE//2-12)
                if p > 2: pygame.draw.circle(WIN, GOLD, center, SQUARE_SIZE//4)
                if selected == (r,c): pygame.draw.circle(WIN, RED, center, SQUARE_SIZE//2-12, 4)
            if selected and any(m[0]==selected and m[1]==(r,c) for m in all_v):
                pygame.draw.circle(WIN, GREEN, center, 10)

    pygame.draw.rect(WIN, GRAY, (0, BOARD_SIZE, WIDTH, STATUS_HEIGHT))
    m, s = divmod(max(0, int(time_left)), 60)
    WIN.blit(BIG_FONT.render(f"{m:02d}:{s:02d}", 1, BLACK), (WIDTH-140, BOARD_SIZE+30))
    WIN.blit(FONT.render(f"Turno: {'BRANCAS' if turn==1 else 'PRETAS'} | Empate: {m_count}/{LIMIT_EMPATE}", 1, BLACK), (20, BOARD_SIZE+15))
    
    bw = bb = br = be = None
    if p_color == 0:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((255,255,255,200)); WIN.blit(overlay, (0,0))
        bw, bb = pygame.Rect(WIDTH//2-210, 250, 200, 100), pygame.Rect(WIDTH//2+10, 250, 200, 100)
        pygame.draw.rect(WIN, WHITE, bw, border_radius=15); pygame.draw.rect(WIN, BLACK, bb, border_radius=15)
        WIN.blit(FONT.render("JOGAR BRANCAS", 1, BLACK), (bw.x+35, bw.y+40)); WIN.blit(FONT.render("JOGAR PRETAS", 1, WHITE), (bb.x+40, bb.y+40))
        
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); overlay.fill((0,0,0,180)); WIN.blit(overlay, (0,0))
        txt = BIG_FONT.render(win_txt, 1, GOLD)
        WIN.blit(txt, (WIDTH//2 - txt.get_width()//2, 200))
        br, be = pygame.Rect(WIDTH//2-120, 300, 110, 50), pygame.Rect(WIDTH//2+10, 300, 110, 50)
        pygame.draw.rect(WIN, BLUE, br, border_radius=10); pygame.draw.rect(WIN, RED, be, border_radius=10)
        WIN.blit(FONT.render("REINICIAR", 1, WHITE), (br.x+15, br.y+15)); WIN.blit(FONT.render("SAIR", 1, WHITE), (be.x+35, be.y+15))
        
    return bw, bb, br, be

def main():
    board, turn, selected, p_color = create_board(), 1, None, 0
    game_over, win_txt, time_left, m_count = False, "", MAX_TIME, 0
    last_t = time.time()
    
    while True:
        dt = time.time() - last_t
        last_t = time.time()
        
        if p_color != 0 and not game_over:
            time_left -= dt
            if time_left <= 0: game_over, win_txt = True, "TEMPO ESGOTADO!"
            if m_count >= LIMIT_EMPATE: game_over, win_txt = True, "EMPATE POR LANCES"
            if not get_all_valid_moves(board, turn): 
                game_over, win_txt = True, "IA VENCEU!" if turn==p_color else "HUMANO VENCEU!"
        
        bw, bb, br, be = draw_screen(board, selected, turn, game_over, win_txt, time_left, p_color, m_count)
        pygame.display.update()

        # IA
        if not game_over and p_color != 0 and turn != p_color:
            _, move = minimax(board, 6, -float('inf'), float('inf'), turn == 1)
            if move:
                m_count = 0 if move[2] else m_count + 1
                board = simulate_move(board, move)
                # Verifica apenas capturas OBRIGATÓRIAS para a mesma peça
                all_v = get_all_valid_moves(board, turn)
                can_capture_more = any(m[0] == move[1] and m[2] is not None for m in all_v)
                if move[2] and can_capture_more:
                    pass 
                else:
                    turn = 3 - turn
                last_t = time.time()
            continue

        # HUMANO
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if p_color == 0:
                    if bw and bw.collidepoint(e.pos): p_color = 1
                    if bb and bb.collidepoint(e.pos): p_color = 2; last_t = time.time()
                elif game_over:
                    if br and br.collidepoint(e.pos): main()
                    if be and be.collidepoint(e.pos): pygame.quit(); sys.exit()
                elif turn == p_color:
                    r, c = e.pos[1]//SQUARE_SIZE, e.pos[0]//SQUARE_SIZE
                    if r < ROWS:
                        all_v = get_all_valid_moves(board, turn)
                        move = next((m for m in all_v if m[0]==selected and m[1]==(r,c)), None)
                        
                        if move:
                            board = simulate_move(board, move)
                            m_count = 0 if move[2] else m_count + 1
                            
                            # LOGICA DE TURNO REFEITA:
                            all_v_next = get_all_valid_moves(board, turn)
                            # Só continua se: 1. Foi uma captura AND 2. A peça ainda TEM capturas para fazer
                            can_capture_more = any(m[0] == (r,c) and m[2] is not None for m in all_v_next)
                            
                            if move[2] and can_capture_more:
                                selected = (r,c)
                            else:
                                turn, selected = 3-turn, None
                        
                        elif board[r][c] != 0 and board[r][c]%2 == turn%2:
                            if any(m[0] == (r,c) for m in all_v): selected = (r,c)
                        else:
                            selected = None

if __name__ == "__main__": main()