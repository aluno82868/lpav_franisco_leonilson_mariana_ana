import copy
from constants import ROWS, COLS

def create_board():
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range((r + 1) % 2, COLS, 2):
            if r < 3: board[r][c] = 2 
            elif r > 4: board[r][c] = 1 
    return board

def get_moves(board, r, c):
    p = board[r][c]
    moves, caps = [], {}
    dirs = [(-1,-1), (-1,1), (1,-1), (1,1)] if p > 2 else ([(-1,-1), (-1,1)] if p==1 else [(1,-1), (1,1)])
    
    for dr, dc in dirs:
        step = 1
        while True:
            tr, tc = r + step*dr, c + step*dc
            if not (0 <= tr < ROWS and 0 <= tc < COLS): break
            if board[tr][tc] == 0:
                if step == 1 or p > 2: moves.append((tr, tc))
            else:
                if board[tr][tc] % 2 != p % 2:
                    val_inimigo = 10 if board[tr][tc] > 2 else 1
                    for jump in range(1, 8):
                        fr, fc = tr + jump*dr, tc + jump*dc
                        if 0 <= fr < ROWS and 0 <= fc < COLS and board[fr][fc] == 0:
                            caps[(fr, fc)] = {'enemy': (tr, tc), 'value': val_inimigo}
                            if p <= 2: break
                        else: break
                break 
            if p <= 2: break 
            step += 1
    return moves, caps

def evaluate_capture_sequence(board, r, c):
    _, caps = get_moves(board, r, c)
    if not caps: return 0, 0
    best_qty, best_qual = 0, 0
    for dest, info in caps.items():
        qty, qual = evaluate_capture_sequence(simulate_move(board, ((r,c), dest, info['enemy'])), dest[0], dest[1])
        if (1 + qty > best_qty) or (1 + qty == best_qty and info['value'] + qual > best_qual):
            best_qty, best_qual = 1 + qty, info['value'] + qual
    return best_qty, best_qual

def get_all_valid_moves(board, color):
    all_caps = []
    piece_simples = []
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != 0 and board[r][c] % 2 == color % 2:
                simples, caps = get_moves(board, r, c)
                for dest, info in caps.items():
                    qty, qual = evaluate_capture_sequence(board, r, c)
                    all_caps.append(((r,c), dest, info['enemy'], qty, qual))
                if not all_caps:
                    for dest in simples: piece_simples.append(((r,c), dest, None))
    if all_caps:
        max_q = max(m[3] for m in all_caps)
        filt = [m for m in all_caps if m[3] == max_q]
        max_v = max(m[4] for m in filt)
        return [m[:3] for m in filt if m[4] == max_v]
    return piece_simples

def simulate_move(board, move):
    (r1, c1), (r2, c2), enemy = move
    nb = copy.deepcopy(board)
    is_promotion = False
    # Promoção ocorre apenas se o movimento terminar na última linha
    if nb[r1][c1] == 1 and r2 == 0: is_promotion = True
    if nb[r1][c1] == 2 and r2 == 7: is_promotion = True
    
    nb[r2][c2] = (nb[r1][c1] + 2) if is_promotion else nb[r1][c1]
    nb[r1][c1] = 0
    if enemy: nb[enemy[0]][enemy[1]] = 0
    return nb