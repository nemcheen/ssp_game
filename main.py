from typing import List
import random as rd


possible_move = ['stone', 'paper', 'scissors']
game_score = {'total_move': 0,
              'player_score': 0,
              'bot_score': 0}

def bot_turn() -> str:
    bot_move = rd.choice(possible_move)
    print(f'Bot move is {bot_move}.')
    return bot_move

def player_turn() -> str:
    player_input = input("Ваш ход: Камень/Ножницы/Бумага (К/Н/Б).\n \"З\" - Остановить игру\n")
    if player_input.upper() == "К":
        player_move = possible_move[0]
    elif player_input.upper() == "Н":
        player_move = possible_move[2]
    elif player_input.upper() == "Б":
        player_move = possible_move[1]
    elif player_input.upper() == "З":
        player_move = 'З'
    else:
        print('Введи корректный ход')
        return player_turn() 
          
    print(f'Your move is {player_move}.')
    return player_move

def move_result(player_move: str, bot_move: str) -> str:
    game_score['total_move'] += 1
    idx_player_move = possible_move.index(player_move)
    idx_bot_move = possible_move.index(bot_move)
    winner = 'draw'
    if (idx_player_move - idx_bot_move) == 1 or (idx_player_move - idx_bot_move) == -2:
        game_score['player_score'] += 1
        print('Player win')
        winner = 'player'
    elif player_move == bot_move:
        print('draw')
    else:
        game_score['bot_score'] += 1
        print('Bot win')
        winner = 'bot'
    return winner
    


def main_game() -> None:
    while (player_move := player_turn()) != 'З':
        bot_move = bot_turn()
        move_result(player_move, bot_move)

if __name__ == '__main__':
    main_game()
    print(f"Всего игр было сыграно {game_score['total_move']}.\nочки игрока равны {game_score['player_score']}.\nочки бота равны {game_score['bot_score']}.")
