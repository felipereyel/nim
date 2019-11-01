import json
import socket
HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

class GameServer:
	
	def __init__(self, number_rows, row_size, number_players):
		self.number_rows = number_rows
		self.row_size = row_size
		self.number_players = number_players
		self.whos_turn = number_players - 1
		self.is_game_over = False
		
		self.board = []
		for i in range(number_rows):
			self.board.append(row_size)
		
		self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._s.bind((HOST, PORT))
		self._s.listen(number_players)
		
		self._init_players()
		
	def _init_players(self):
		self.players = []
		print('Jogadores:')
		for i in range(self.number_players):
		
			con, cli = self._s.accept()
			player_info = self.recv_data(con)
			player_info['con'] = con
			self.players.append(player_info)

			print(i, '-', player_info['name'])
		print('\n')
		
	def recv_data(self, con):
		return json.loads(self._recv(con))
		
	def send_data(self, resp_data, con):
		self._send(json.dumps(resp_data), con)
		
	def _send(self, msg, con):
		#print(msg)
		con.send(bytes(msg, 'UTF-8'))
		
	def _recv(self, con):
		return con.recv(1024)
		
	def finish(self):
		for player in self.players:
			game_data = {
				'is_game_over': self.is_game_over,
				'loser': self.players[self.whos_turn]['name']
			}
			self.send_data(game_data, player['con'])
			player['con'].close()
		print('O jogador {} perdeu'.format(self.players[self.whos_turn]['name']))
			
	def print_board(self):
		for row_idx in range(self.number_rows):
			print('Row {}: '.format(row_idx) + self.board[row_idx]*'@')
		print('\n')
            
	def not_empty_rows(self):
		not_empty_rows = []
		for idx in range(self.number_rows):
			if self.board[idx] > 0:
				not_empty_rows.append(idx)
		return not_empty_rows
            
	def is_not_over(self):
		if len(self.not_empty_rows()) < 1:
			self.is_game_over = True
			return False
		return True
    
	def turn(self):
        
		# Manda a informacao do jogo para o jogador
		game_data = {
			'is_game_over': self.is_game_over,
			'turns_player': self.players[self.whos_turn]['name'],
			'board': self.board,
			'not_empty_rows': self.not_empty_rows()
		}
		self.send_data(game_data, self.players[self.whos_turn]['con'])
        
		# Recebe informacoes da jogada do jogador
		resp_data = self.recv_data(self.players[self.whos_turn]['con'])
        
		# Imprime a jogada do Jogador
		print('Jogada de {}: '.format(self.players[self.whos_turn]['name']), end='')
		print('Grupo {}'.format(resp_data['row']), end='')
		print(' Pecas {}'.format(resp_data['pebles'])+'\n')

		self.board[resp_data['row']] -= resp_data['pebles']
        
		# Imprime o tabuleiro resultante da jogada
		self.print_board()
            
	def main(self):
		print('Inicio de Jogo!\n')
		self.print_board()
        
		while(self.is_not_over()):
			self.whos_turn = (self.whos_turn + 1)%self.number_players
			self.turn()

		self.finish()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print('IP do servidor: {}'.format(s.getsockname()[0]))
s.close()

numberOfRows = int(input('Numero de grupos: '))
rowSize = int(input('Numero de pecas: '))
numberOfPlayers = int(input('Numero de jogadores: '))

myGame = GameServer(numberOfRows, rowSize, numberOfPlayers)

myGame.main()
