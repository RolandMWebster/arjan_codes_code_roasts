"""
Simple Battleship Game.

TODO: Update game coordinates to index from 1 rather than 0.
"""

from dataclasses import dataclass, field
import numpy as np
import random as rand
from typing import Optional


BLANK_ICON = "O"
MISS_ICON = "X"
SHIP_ICON = "S"

GUESSES = 5
WIDTH = 5
HEIGHT = 5
NUM_SHIPS = 1


@dataclass
class Player:
    name: str


@dataclass
class Ship:
    icon = SHIP_ICON
    x: int
    y: int
    sunk: bool = False

    @property
    def coordinates(self) -> tuple[int, int]:
        return (self.x, self.y)


@dataclass
class Board:
    width: int
    height: int
    grid: np.matrix = field(init=False)
    ships: list[Ship] = field(default_factory=list)
    guess_locations: set[tuple] = field(default_factory=set)

    def __post_init__(self):
        self.grid = np.full((self.width, self.height), BLANK_ICON)

    def add_ship(self, x: int, y: int) -> None:
        """Adds a ship to the board."""
        if (x > self.width) | (y > self.height):
            raise ValueError("Outside the grid!")

        for ship in self.ships:
            if ship.coordinates == (x, y):
                raise ValueError("A ship is already placed there!")

        self.ships.append(
            Ship(x, y)
        )

    def process_guess(self, x: int, y: int) -> None:
        """Processes a user guess and updates the grid and ship sunk status."""
        self.guess_locations.add((x, y))
        for ship in self.ships:
            if (x, y) == ship.coordinates:
                self.grid[x][y] = ship.icon
                ship.sunk = True
            else:
                self.grid[x][y] = MISS_ICON


@dataclass
class Game:
    board: Board
    players: list[Player]
    guesses: int
    winner: Optional[Player] = None

    @property
    def is_finished(self) -> bool:
        """Identifies whether the game is finished because there are no guesses
        remaining, or all ships have been sunk."""
        return (self.guesses <= 0) | all([ship.sunk for ship in self.board.ships])

    def _play_round(self) -> None:
        """Plays a single round of the game by looping through each player and
        processing their guess."""
        print(f"{self.guesses} guesses remaining!")
        for player in self.players:
            if self.is_finished:
                continue
            print(f"{player.name}'s turn to guess!")
            x, y = get_user_guess(
                max_x=self.board.width - 1, max_y=self.board.height - 1
            )
            self.board.process_guess(x, y)
            print(self.board.grid)
            if self.is_finished:
                self.winner = player
        self.guesses -= 1

    def play(self) -> None:
        while not self.is_finished:
            self._play_round()
        if not self.winner:
            print("Nobody won the game!")
            return None
        print(f"{self.winner.name} won the game!")


def get_user_guess(max_x: int, max_y: int) -> tuple[int, int]:
    """Prompts the user for x and y coordinates and returns them as a tuple."""
    while True:
        x = int(input("Select row: "))
        if x > max_x:
            print(f"Row value must be between 0 and {max_x}")
            continue
        else:
            break
    while True:
        y = int(input("Select column: "))
        if y > max_y:
            print(f"Column value must be between 0 and {max_y}")
            continue
        else:
            break
    return (x, y)


def get_players() -> list[Player]:
    """Prompts the user for the number of players"""
    num_players = input("Enter number of players: ")
    return [Player(name=f"Player {i+1}") for i in range(int(num_players))]


def generate_unique_coordinates(n: int, max_x: int, max_y: int) -> set[tuple[int, int]]:
    """Randomly generates a set of n unique coordinates, limited to within a given
    range of coordinate values."""
    coordinates = set()
    while len(coordinates) < n:
        x = rand.randint(0, max_x)
        y = rand.randint(0, max_y)
        coordinates.add((x, y))
    return coordinates


def main():
    board = Board(width=WIDTH, height=HEIGHT)
    ship_coordinates = generate_unique_coordinates(
        n=NUM_SHIPS, max_x=board.width - 1, max_y=board.height - 1
    )
    for x, y in ship_coordinates:
        board.add_ship(x=x, y=y)
    players = get_players()
    game = Game(board=board, players=players, guesses=GUESSES)
    game.play()


if __name__ == "__main__":
    main()
