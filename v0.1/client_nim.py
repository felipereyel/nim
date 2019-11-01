import json
import socket
import os
import time
import platform

PORT = 5000            # Porta que o Servidor esta

if platform.system() == 'Linux':
    clearCommand = 'clear'
else:
    clearCommand = 'cls'

class Player:
	
	def __init__(self, name, ip):
		self.name = name
		
		self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._s.connect((ip, PORT))
		
		self._send_player_info()

	def _send(self, msg):
		#print(msg)
		self._s.send(bytes(msg, 'UTF-8'))
		
	def _recv(self):
		return self._s.recv(1024)

	def finish(self):
		self._s.close()
		
	def _send_player_info(self):
		json_data = {"name": self.name}
		self._send(json.dumps(json_data))
		
	def recv_game_data(self):
		return json.loads(self._recv())
		
	def send_player_move(self, resp_data):
		self._send(json.dumps(resp_data))
		


		
class ClientSideGame:
	def __init__(self, player):
		self.player = player
		
	def print_board(self, board):
		for row_idx in range(len(board)):
			print('Row {}: '.format(row_idx) + board[row_idx]*'@')
		
	def my_turn(self, game_data):
		
		resp_data = {'name': self.player.name}
		
		os.system(clearCommand)
		
		print('Sua vez, jogador {}!\n'.format(self.player.name))
		self.print_board(game_data['board'])
		
		print('Qual grupo? {}'.format(game_data['not_empty_rows']))
		resp_data['row'] = int(input('>'))
		
		print('Quantas pecas? (1 - {})'.format(game_data['board'][resp_data['row']]))
		resp_data['pebles'] = int(input('>'))
		
		print('Espere :) \n')
		
		self.player.send_player_move(resp_data)
		
	def try_turn(self):
		game_data = self.player.recv_game_data()
		
		if not game_data['is_game_over']: # JOGO AINDA ESTA ROLANDO
			
			if game_data['turns_player'] == self.player.name: # SUA VEZ
				self.my_turn(game_data)
			
			else: # VEZ DO OPONENTE
				print('Espere a vez')
				
			return True
				
		else: # JOGO ACABOU
			
			if game_data['loser'] == self.player.name: # VOCE GANHOU
				print('Voce perdeu :(')
				
			else: # VOCE PERDEU
				print('Voce ganhou!!! O jogador {} perdeu'.format(game_data['loser']))
			
			self.player.finish()
			
			time.sleep(10)
			
			return False
			
	def main(self):
		while(self.try_turn()):
			pass
		

name = input('Nome do jogador: ')
ip = input('IP do servidor: ')

playerX = Player(name, ip)
myGame = ClientSideGame(playerX)

print('Inicio do jogo, aguarde sua vez\n')
myGame.main()
