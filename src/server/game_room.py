from __future__ import annotations
from threading import Lock
from typing import Optional
import logging

from src.mahjong.game_options import GameOptions

from .sio import sio
from .player_info import Player, PlayerConnection
from .game_controller import GameController

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

rooms: dict[str, GameRoom] = {}
player_rooms: dict[str, GameRoom] = {}
rooms_lock = Lock()


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
        self.joined_player_connections: list[PlayerConnection] = [
            PlayerConnection(player=creator)
        ]
        self.avatars = {creator.id: 0}
        self.avatar_lock = Lock()

    @property
    def joined_players(self):
        return [
            player_connection.player
            for player_connection in self.joined_player_connections
        ]

    @property
    def room_info(self):
        return {
            "room_name": self.room_name,
            "player_count": self.player_count,
            "joined_players": [player.model_dump() for player in self.joined_players],
        }

    @property
    def room_avatar_info(self):
        return {**self.room_info, "avatars": self.avatars}

    @classmethod
    def emit_rooms_list(cls, sid):
        sio.emit(
            "rooms_info", [game_room.room_info for game_room in rooms.values()], sid
        )

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
        with rooms_lock:
            return player_rooms.get(player.id)

    @classmethod
    def create_room(cls, creator: Player, room_name: str, player_count: int):
        with rooms_lock:
            if creator.id in player_rooms:
                raise Exception(f"Player {creator.id} is already in a room!")
            if room_name in rooms:
                raise Exception(f"Room {room_name} name already exists!")
            game_room = cls(creator, room_name, player_count)
            player_rooms[creator.id] = game_room
            rooms[room_name] = game_room
        logger.info(f"Player {creator.id} has created room {room_name}")
        game_room.broadcast_room_info()
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
            with game_room.avatar_lock:
                game_room.joined_player_connections.append(
                    PlayerConnection(player=player)
                )
                game_room.avatars[player.id] = 0
            player_rooms[player.id] = game_room
        # broadcast new player to room
        game_room.broadcast_room_info()
        return game_room

    def _remove_player(self, player_connection: PlayerConnection):
        with self.avatar_lock:
            self.joined_player_connections.remove(player_connection)
            self.avatars.pop(player_connection.player.id)
        player_rooms.pop(player_connection.player.id)
        if len(self.joined_players) == 0:
            logger.info(f"Room {self.room_name} is now empty, removing from rooms dict")
            rooms.pop(self.room_name)

    @classmethod
    def leave_room(cls, player: Player):
        with rooms_lock:
            try:
                game_room = player_rooms[player.id]
            except KeyError:
                raise Exception("Player is not in a room!")
            if game_room.game_controller:
                raise Exception("Game already in progress!")
            player_connection = game_room.get_player_connection(player)
            game_room._remove_player(player_connection)
        sio.emit("room_info", None, to=player.id)
        game_room.broadcast_room_info()
        return game_room

    def broadcast_room_info(self):
        for player in self.joined_players:
            sio.emit("room_info", self.room_avatar_info, to=player.id)

    def broadcast_game_end(self):
        for player in self.joined_players:
            sio.emit("game_end", self.room_info, to=player.id)

    def get_player_connection(self, player: Player):
        return next(
            player_connection
            for player_connection in self.joined_player_connections
            if player_connection.player == player
        )

    @classmethod
    def try_disconnect(cls, player: Player):
        with rooms_lock:
            game_room = player_rooms.get(player.id)
            if game_room is None:
                return
            player_connection = game_room.get_player_connection(player)
            player_connection.is_connected = False
            if game_room.game_controller is None:
                game_room._remove_player(player_connection)
                game_room.broadcast_room_info()
            else:
                is_any_connections = any(
                    player_connection.is_connected
                    for player_connection in game_room.joined_player_connections
                )
                if not is_any_connections:
                    print(
                        f"Room {game_room.room_name} has no connections, closing room"
                    )
                    for player in game_room.joined_players:
                        player_rooms.pop(player.id)
                    with game_room.avatar_lock:
                        game_room.joined_player_connections.clear()
                        game_room.avatars.clear()
                    rooms.pop(game_room.room_name)

    @classmethod
    def try_reconnect(cls, player: Player):
        with rooms_lock:
            game_room = player_rooms.get(player.id)
            if game_room is not None:
                game_room.get_player_connection(player).is_connected = True
        sio.emit(
            "room_info",
            game_room.room_info if game_room is not None else None,
            to=player.id,
        )
        return game_room

    @classmethod
    def set_avatar(cls, player: Player, avatar: int):
        game_room = cls.get_player_room(player)
        with game_room.avatar_lock:
            game_room.avatars[player.id] = avatar
        game_room.broadcast_room_info()

    def start_game(self, game_options: GameOptions):
        if game_options.player_count != self.player_count:
            raise Exception("Wrong number of players specified!")
        with rooms_lock:
            if len(self.joined_players) != self.player_count:
                raise Exception("Room is not full!")
            if self.game_controller is not None:
                raise Exception("Game is already in progress!")
            self.game_controller = GameController(self.joined_players, game_options)

    def end_game(self):
        with rooms_lock:
            if not self.game_controller._game.is_game_end:
                raise Exception("Game is not over yet!")
            self.game_controller = None
        self.broadcast_game_end()
