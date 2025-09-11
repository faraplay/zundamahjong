from __future__ import annotations
from threading import Lock
from typing import Optional

from flask_socketio import emit, join_room, leave_room, close_room

from src.mahjong.game_options import GameOptions

from .player_info import Player
from .game_controller import GameController

rooms: dict[str, GameRoom] = {}
player_rooms: dict[str, GameRoom] = {}
rooms_lock = Lock()


def make_room_id(name: str):
    return "room:" + name


class GameRoom:
    def __init__(
        self,
        creator: Player,
        room_name: str,
        player_count: int,
    ):
        self.room_name = room_name
        self.player_count = player_count
        self.game_controller: Optional[GameController] = None
        self.joined_players: list[Player] = [creator]

    @property
    def room_id(self):
        return make_room_id(self.room_name)

    @property
    def room_info(self):
        return {
            "room_name": self.room_name,
            "player_count": self.player_count,
            "joined_players": [player.name for player in self.joined_players],
        }

    @classmethod
    def get_rooms(cls):
        return rooms.values()

    @classmethod
    def verify_room_name(cls, room_name):
        if not isinstance(room_name, str):
            raise Exception("Room name is not a string!")
        if room_name == "":
            raise Exception("Room name cannot be empty!")
        if len(room_name) > 20:
            raise Exception(f"Room name {room_name} is over 20 characters long!")

    @classmethod
    def verify_player_count(cls, player_count):
        if not isinstance(player_count, int):
            raise Exception(f"Player count {player_count} is not an integer!")
        if not (player_count == 3 or player_count == 4):
            raise Exception(f"Player count is not 3 or 4!")

    @classmethod
    def get_player_room(cls, player: Player):
        return player_rooms.get(player.id, None)

    @classmethod
    def create_room(
        cls,
        creator: Player,
        room_name: str,
        player_count: int,
    ):
        with rooms_lock:
            if creator.id in player_rooms:
                raise Exception(f"Player {creator.id} is already in a room!")
            if room_name in rooms:
                raise Exception(f"Room {room_name} name already exists!")
            game_room = cls(creator, room_name, player_count)
            player_rooms[creator.id] = game_room
            rooms[room_name] = game_room
        join_room(make_room_id(room_name))
        print(f"Player {creator.id} has created room {room_name}")
        return game_room

    @classmethod
    def join_room(cls, player: Player, room_name: str):
        with rooms_lock:
            if player.id in player_rooms:
                raise Exception(f"Player {player.id} is already in a room!")
            game_room = rooms[room_name]
            if game_room.game_controller:
                raise Exception(f"Game already in progress!")
            if len(game_room.joined_players) >= game_room.player_count:
                raise Exception(f"Room {game_room.room_name} is full!")
            game_room.joined_players.append(player)
            player_rooms[player.id] = game_room
        # broadcast new player to room
        join_room(game_room.room_id)
        game_room.broadcast_room_info()
        return game_room

    @classmethod
    def leave_room(cls, player: Player):
        with rooms_lock:
            try:
                game_room = player_rooms[player.id]
            except KeyError:
                raise Exception("Player is not in a room!")
            if game_room.game_controller:
                raise Exception("Game already in progress!")
            game_room.joined_players.remove(player)
            player_rooms.pop(player.id)
            if len(game_room.joined_players) == 0:
                print(
                    f"Room {game_room.room_name} is now empty, removing from rooms dict"
                )
                rooms.pop(game_room.room_name)
            # broadcast
        leave_room(game_room.room_id)
        game_room.broadcast_room_info()
        return game_room

    def close_room(self):
        with rooms_lock:
            for player in self.joined_players:
                player_rooms.pop(player.id)
            self.joined_players.clear()
            print(f"Room {self.room_name} is now empty, removing from rooms dict")
            rooms.pop(self.room_name)
        close_room(self.room_id)

    def broadcast_room_info(self):
        emit("room_info", self.room_info, to=self.room_id)

    def start_game(self):
        if len(self.joined_players) != self.player_count:
            raise Exception("Room is not full!")
        if self.game_controller is not None:
            raise Exception("Game is already in progress!")
        self.game_controller = GameController(
            self.joined_players, GameOptions(player_count=self.player_count)
        )
        self.game_controller.emit_info_all()

    def end_game(self):
        if not self.game_controller._game.is_game_end:
            raise Exception("Game is not over yet!")
        self.game_controller = None
        emit("game_end", self.room_info, to=self.room_id)
