from rules import get_all_valid_moves, simulate_move, ROWS, COLS

def evaluate(board):
    score = 0
    for r in range(ROWS):
        for c in range(COLS):
            p = board[r][c]
            if p == 0: continue
            is_white = (p % 2 != 0)
            val = 150 if p > 2 else 40 
            val += (7 - r if is_white else r) * 5
            if c == 0 or c == 7: val += 10
            score += val if is_white else -val
    return score

def minimax(board, depth, alpha, beta, max_p):
    if depth == 0: return evaluate(board), None
    moves = get_all_valid_moves(board, 1 if max_p else 2)
    if not moves: return evaluate(board), None
    moves.sort(key=lambda m: m[2] is not None, reverse=True)
    best_move = None
    if max_p:
        v_max = -float('inf')
        for m in moves:
            ev = minimax(simulate_move(board, m), depth-1, alpha, beta, False)[0]
            if ev > v_max: v_max, best_move = ev, m
            alpha = max(alpha, ev)
            if beta <= alpha: break
        return v_max, best_move
    else:
        v_min = float('inf')
        for m in moves:
            ev = minimax(simulate_move(board, m), depth-1, alpha, beta, True)[0]
            if ev < v_min: v_min, best_move = ev, m
            beta = min(beta, ev)
            if beta <= alpha: break
        return v_min, best_move