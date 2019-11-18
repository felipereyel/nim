# nim_redes
Jogo NIM em python operando em varios computadores utilizando de sockets

### Mensagens trocadas por servidor cliente:

As mensagens são JSONs contendo informações do jogo, dos jogadores ou da jogada

1. mensagem de inicialização enviadada cliente > servidor:
```
{
    "name": "Wanderey"
}
```
2. mensagem de informação do jogo servidor > cliente:
```
{
	'is_game_over': False,
	'turns_player': "Jorge",
	'board': [3, 4, 0],
	'not_empty_rows': [0, 1]
}
```
3. mensagem de jogada cliente > servidor:
```
{
    "name": "Wanderey",
    "row": 1,
    "pebles": 2
}
```
4. mensagem de fim de jogo (um mensagem de informação de jogo modificada) servidor > cliente:
```
{
	'is_game_over': True,
	'loser': "Chrysthianny"
}

```

