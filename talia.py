import time
from dataclasses import dataclass
from typing import Any


class EndGameException(Exception):
    pass


@dataclass
class Tile:
    id: int


@dataclass
class Player:
    tile: Tile


class Game:
    player: Player
    tiles: list[Tile]

    env: dict[str, Any]

    def __init__(self, player: Player, tiles: list[Tile]) -> None:
        self.player = player
        self.tiles = tiles

        self.env = {}

    def end_game(self) -> None:
        raise EndGameException

    def parse_logic(self, filename: str) -> None:
        with open(filename) as f:
            source: str = f.read()

        self.env["player"] = self.player
        self.env["tiles"] = self.tiles

        self.env["sleep"] = time.sleep
        self.env["write"] = print
        self.env["end"] = self.end_game

        exec(source, self.env)

    def run(self) -> None:
        self.env["on_start"]()

        self.running = True
        while True:
            try:
                self.env["on_turn"]()
            except EndGameException:
                break


def main() -> None:
    tiles = [Tile(0), Tile(1), Tile(2), Tile(3), Tile(4)]
    game = Game(Player(tiles[0]), tiles)

    game.parse_logic("basic.talia")
    game.run()


if __name__ == '__main__':
    main()
