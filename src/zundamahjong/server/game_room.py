from __future__ import annotations

import logging
from threading import Lock
from typing import final

from pydantic import BaseModel

from ..database.avatars import get_avatar, save_avatar
from ..mahjong.game_options import GameOptions
from ..types.avatar import Avatar
from ..types.player import BotPlayer, Player, PlayerConnection, UserPlayer
from .game_controller import GameController
from .sio import sio

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

rooms: dict[str, GameRoom] = {}
user_player_rooms: dict[str, GameRoom] = {}
rooms_lock = Lock()


class RoomBasicInfo(BaseModel):
    """
    The basic info of a game room, to be displayed in the list of game rooms.
    """

    room_name: str
    player_count: int
    joined_players: list[Player]


class RoomDetailedInfo(RoomBasicInfo):
    """
    The info of a game room, broadcasted to all players in the game room.
    """

    avatars: dict[str, Avatar]
    game_options: GameOptions


@final
class GameRoom:
    """
    Represents a game room that players can join.
    """

    def __init__(
        self,
        creator: UserPlayer,
        room_name: str,
        game_options: GameOptions,
    ) -> None:
        self.room_name = room_name
        self.player_count = game_options.player_count
        self.game_options = game_options
        self.game_controller: GameController | None = None
        self.joined_player_connections: list[PlayerConnection] = [
            PlayerConnection(player=creator)
        ]
        self.avatars = {creator.id: get_avatar(creator)}
        self.avatar_lock = Lock()

    @property
    def joined_players(self) -> list[Player]:
        """
        A list of players who have joined the room.
        """
        return [
            player_connection.player
            for player_connection in self.joined_player_connections
        ]

    @property
    def room_basic_info(self) -> RoomBasicInfo:
        """
        A :py:class:`RoomBasicInfo` with the basic data for the room.
        """
        return RoomBasicInfo(
            room_name=self.room_name,
            player_count=self.player_count,
            joined_players=self.joined_players,
        )

    @property
    def room_detailed_info(self) -> RoomDetailedInfo:
        """
        A :py:class:`RoomDetailedInfo` with the detailed data for the room.
        """
        return RoomDetailedInfo(
            room_name=self.room_name,
            player_count=self.player_count,
            joined_players=self.joined_players,
            avatars=self.avatars,
            game_options=self.game_options,
        )

    @classmethod
    def emit_rooms_list(cls, sid: str) -> None:
        """
        Emit a list of all game rooms to the given Socket.IO session id.

        :param sid: The Socket.IO session id to send the list to.
        """
        sio.emit(
            "rooms_info",
            [game_room.room_basic_info.model_dump() for game_room in rooms.values()],
            to=sid,
        )

    @classmethod
    def verify_room_name(cls, room_name: str) -> None:
        """
        Raise an exception if the room name is empty or too long.

        :param room_name: The room name to verify.
        """
        if room_name == "":
            raise Exception("Room name cannot be empty!")
        if len(room_name) > 20:
            raise Exception(f"Room name {room_name} is over 20 characters long!")

    @classmethod
    def verify_player_count(cls, player_count: int) -> None:
        """
        Raise an exception if the player count is not 3 or 4.

        :param player_count: The player count to verify.
        """
        if not (player_count == 3 or player_count == 4):
            raise Exception("Player count is not 3 or 4!")

    @classmethod
    def get_player_room(cls, player: Player) -> GameRoom | None:
        """
        Get the game room a player is in, or ``None`` if the player
        is not in a room.

        :param player: The player to find the game room of.
        """
        with rooms_lock:
            return user_player_rooms.get(player.id)

    @classmethod
    def create_room(
        cls, creator: UserPlayer, room_name: str, game_options: GameOptions
    ) -> GameRoom:
        """
        Create a game room.

        :param creator: The player who is creating the room.
        :param room_name: The name of the room.
        :param player_count: The number of players the room should hold.
        """
        with rooms_lock:
            if creator.id in user_player_rooms:
                raise Exception(f"Player {creator.id} is already in a room!")
            if room_name in rooms:
                raise Exception(f"Room {room_name} name already exists!")
            game_room = cls(creator, room_name, game_options)
            user_player_rooms[creator.id] = game_room
            rooms[room_name] = game_room
        logger.info(f"Player {creator.id} has created room {room_name}")
        game_room.broadcast_room_info()
        return game_room

    @classmethod
    def join_room(cls, player: UserPlayer, room_name: str) -> GameRoom:
        """
        Make a user player join a game room.

        The player should not already be in a game room.

        :param player: The player to add to a game room.
        :param room_name: The name of the game room to add the player to.
        """
        with rooms_lock:
            if player.id in user_player_rooms:
                raise Exception(f"Player {player.id} is already in a room!")
            game_room = rooms.get(room_name)
            if not game_room:
                raise Exception(
                    f"Room '{room_name}' no longer exists! Please refresh the room list."
                )
            if game_room.game_controller:
                raise Exception("Game already in progress!")
            if len(game_room.joined_players) >= game_room.player_count:
                raise Exception(f"Room {game_room.room_name} is full!")
            with game_room.avatar_lock:
                game_room.joined_player_connections.append(
                    PlayerConnection(player=player)
                )
                game_room.avatars[player.id] = get_avatar(player)
            user_player_rooms[player.id] = game_room
        # broadcast new player to room
        game_room.broadcast_room_info()
        return game_room

    @classmethod
    def add_bot_to_room(cls, player: UserPlayer) -> GameRoom:
        """
        Adds a bot to the room the user player is in.

        :param player: The player who is adding a bot.
        """
        with rooms_lock:
            try:
                game_room = user_player_rooms[player.id]
            except KeyError:
                raise Exception("Player is not in a room!")
            if game_room.game_controller:
                raise Exception("Game already in progress!")
            if len(game_room.joined_players) >= game_room.player_count:
                raise Exception(f"Room {game_room.room_name} is full!")
            bot_index = next(
                index
                for index in range(1, game_room.player_count + 1)
                if not any(
                    isinstance(player_connection.player, BotPlayer)
                    and player_connection.player.name_index == index
                    for player_connection in game_room.joined_player_connections
                )
            )
            bot = BotPlayer(name_index=bot_index)
            with game_room.avatar_lock:
                game_room.joined_player_connections.append(PlayerConnection(player=bot))
                game_room.avatars[bot.id] = Avatar(0)
        # broadcast new player to room
        game_room.broadcast_room_info()
        return game_room

    def _remove_player(self, player_connection: PlayerConnection) -> None:
        player = player_connection.player
        with self.avatar_lock:
            self.joined_player_connections.remove(player_connection)
            if isinstance(player, UserPlayer):
                save_avatar(player, self.avatars[player.id])
            self.avatars.pop(player.id)
        if isinstance(player, UserPlayer):
            user_player_rooms.pop(player.id)
        if all(isinstance(player, BotPlayer) for player in self.joined_players):
            logger.info(f"Room {self.room_name} is now empty, removing from rooms dict")
            rooms.pop(self.room_name)

    @classmethod
    def leave_room(cls, player: Player) -> GameRoom:
        """
        Remove a player from the game room they are in.

        :param player: The player to remove from a room.
        """
        with rooms_lock:
            try:
                game_room = user_player_rooms[player.id]
            except KeyError:
                raise Exception("Player is not in a room!")
            if game_room.game_controller:
                raise Exception("Game already in progress!")
            player_connection = game_room.get_player_connection(player.id)
            game_room._remove_player(player_connection)
        sio.emit("room_info", None, to=player.id)
        game_room.broadcast_room_info()
        return game_room

    @classmethod
    def kick_from_room(cls, player: Player, kick_player_id: str) -> GameRoom:
        """
        Kick the player with a specified id from a game room.
        The player doing the kicking should be in the same game room.

        :param player: The player kicking someone from a room.
        :param kick_player_id: The id of the player to be kicked.
        """
        with rooms_lock:
            try:
                game_room = user_player_rooms[player.id]
            except KeyError:
                raise Exception("Player is not in a room!")
            if game_room.game_controller:
                raise Exception("Game already in progress!")
            player_connection = game_room.get_player_connection(kick_player_id)
            game_room._remove_player(player_connection)
        sio.emit("room_info", None, to=kick_player_id)
        game_room.broadcast_room_info()
        return game_room

    def broadcast_room_info(self) -> None:
        """
        Send detailed room info to every player in the room.
        """
        for player in self.joined_players:
            sio.emit("room_info", self.room_detailed_info.model_dump(), to=player.id)

    def broadcast_game_end(self) -> None:
        """
        Send to every player in the room an event saying the game room's
        game has ended.
        """
        for player in self.joined_players:
            sio.emit("info", None, to=player.id)

    def get_player_connection(self, player_id: str) -> PlayerConnection:
        """
        Get the :py:class:`PlayerConnection` object associated to a player
        in the game room.

        :param player_id: The player id to look up.
        """
        return next(
            player_connection
            for player_connection in self.joined_player_connections
            if player_connection.player.id == player_id
        )

    @classmethod
    def try_disconnect(cls, player: UserPlayer) -> None:
        """
        Set a player's connection status to disconnected in the game room
        they are in, and remove them from the game room if a game is not in progress.

        :param player: The player to set as disconnected.
        """
        with rooms_lock:
            game_room = user_player_rooms.get(player.id)
            if game_room is None:
                return
            player_connection = game_room.get_player_connection(player.id)
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
                    for joined_player in game_room.joined_players:
                        user_player_rooms.pop(joined_player.id)
                    with game_room.avatar_lock:
                        game_room.joined_player_connections.clear()
                        game_room.avatars.clear()
                    rooms.pop(game_room.room_name)

    @classmethod
    def try_reconnect(cls, player: UserPlayer) -> GameRoom | None:
        """
        Set a player's connection status to connected in the game room
        they are in (if they are in a game room).
        Then emit an event to the player saying which game room (if any)
        they are in.

        :param player: The player to reconnect.
        """
        with rooms_lock:
            game_room = user_player_rooms.get(player.id)
            if game_room is not None:
                game_room.get_player_connection(player.id).is_connected = True
        sio.emit(
            "room_info",
            game_room.room_detailed_info.model_dump()
            if game_room is not None
            else None,
            to=player.id,
        )
        return game_room

    @classmethod
    def set_avatar(cls, player: Player, avatar_player_id: str, avatar: Avatar) -> None:
        """
        Set a player's avatar in the game room the player is in.

        :param player: The player setting the avatar.
        :param avatar_player_id: The player to set an avatar for.
        :param avatar: The avatar to set.
        """
        game_room = cls.get_player_room(player)
        if game_room is None:
            raise Exception("Player is not in a room!")
        with game_room.avatar_lock:
            if avatar_player_id in game_room.avatars:
                game_room.avatars[avatar_player_id] = avatar
        game_room.broadcast_room_info()

    def _save_avatars(self) -> None:
        for player_connection in self.joined_player_connections:
            player = player_connection.player
            if isinstance(player, UserPlayer):
                save_avatar(player, self.avatars[player.id])

    @classmethod
    def set_game_options(cls, player: UserPlayer, game_options: GameOptions) -> None:
        """
        Set the game options for the game room a player is in.

        :param player: The player whose game room's options are to be modified.
        :param game_options: The value of the game options to set.
        """
        game_room = cls.get_player_room(player)
        if game_room is None:
            raise Exception("Player is not in a room!")
        game_room.game_options = game_options
        game_room.broadcast_room_info()

    def start_game(self) -> None:
        """
        Start a game in this game room.
        """
        if self.game_options.player_count != self.player_count:
            raise Exception("Wrong number of players!")
        with rooms_lock:
            if len(self.joined_players) != self.player_count:
                raise Exception("Room is not full!")
            if self.game_controller is not None:
                raise Exception("Game is already in progress!")
            self._save_avatars()
            self.game_controller = GameController(
                self.joined_players, self.game_options
            )

    def end_game(self) -> None:
        """
        End the game in this game room. There must be a game in progress
        and it must have reached the end of the final round.
        """
        if self.game_controller is None:
            raise Exception("Game hasn't started!")
        with rooms_lock:
            self.game_controller = None
        self.broadcast_game_end()
