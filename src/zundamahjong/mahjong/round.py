from __future__ import annotations

from collections.abc import Callable, Sequence
from enum import IntEnum
from typing import final

from zundamahjong.mahjong.scoring import Scorer

from .action import (
    Action,
    ActionList,
    ActionType,
    SimpleAction,
    call_action_types,
)
from .call import Call, get_call_tiles
from .deck import (
    Deck,
    four_player_deck,
    four_player_flowers,
    three_player_deck,
    three_player_flowers,
)
from .discard_pool import Discard, DiscardPool
from .exceptions import InvalidMoveException
from .game_options import GameOptions
from .hand import Hand
from .tile import TileId, get_tile_value
from .win import Win


class RoundStatus(IntEnum):
    """
    Enum representing the state of a round of mahjong.
    """

    START = 0  # Options: nothing, flower
    "Start of the round, when everyone exchanges their flowers."
    PLAY = 1  # Options: discard, added kan, closed kan, flower, tsumo
    "A player has drawn a tile, and needs to discard."
    CALLED_PLAY = 2  # Options: discard
    "A player has called a chii or pon, and needs to discard."
    ADD_KAN_AFTER = 3  # Options: nothing, ron (chankan)
    "A player has just called an added kan."
    CLOSED_KAN_AFTER = 4  # Options: nothing, ron (chankan)
    "A player has just called a closed kan."
    DISCARDED = 5  # Options: draw, chi, pon, open kan, ron
    "A player has just discarded a tile. Other players can call the discarded tile."
    LAST_DISCARDED = 6  # Options: nothing, ron
    "A player has just discarded a tile, and there are no draws left in the deck."
    END = 7
    "The round has ended."


_allowed_actions_funcs: dict[RoundStatus, AllowedActionsFunc] = {}
_do_action_funcs: dict[ActionType, DoActionFunc] = {}


def _register_allowed_actions(
    round_status: RoundStatus,
) -> Callable[[AllowedActionsFunc], AllowedActionsFunc]:
    def _register_allowed_action_inner(
        _allowed_actions_func: AllowedActionsFunc,
    ) -> AllowedActionsFunc:
        _allowed_actions_funcs[round_status] = _allowed_actions_func
        return _allowed_actions_func

    return _register_allowed_action_inner


def _register_do_action(
    action_type: ActionType,
) -> Callable[[DoActionFunc], DoActionFunc]:
    def _register_do_action_inner(
        _do_action_func: DoActionFunc,
    ) -> DoActionFunc:
        _do_action_funcs[action_type] = _do_action_func
        return _do_action_func

    return _register_do_action_inner


@final
class Round:
    """
    Represents a round of mahjong.

    :param wind_round: The wind round that this round is in.
    :param sub_round: The sub-round number of this round.
    :param draw_count: The number of consecutive draws before this round.
    :param tiles: (Optional) A list of :py:class:`TileId`s forming the deck to
                  use in this game. If set to ``None``, then the round will use
                  a shuffled deck.
    :param options: (Optional) A :py:class:`GameOptions` object containing the
                    game options. If set to ``None``, the default game options
                    will be used.
    :param round_end_callback: (Optional) A callback function to call when
                               the round ends.
    """

    def __init__(
        self,
        *,
        wind_round: int = 0,
        sub_round: int = 0,
        draw_count: int = 0,
        tiles: list[TileId] | None = None,
        options: GameOptions | None = None,
        round_end_callback: Callable[[], None] = lambda: None,
    ):
        if options is not None:
            _options = options
        else:
            _options = GameOptions()
        self._wind_round = wind_round
        self._sub_round = sub_round
        self._draw_count = draw_count
        self._player_count = _options.player_count
        self._options = _options
        self._end_callback = round_end_callback
        if tiles is not None:
            self._deck = Deck(tiles)
        else:
            if _options.player_count == 3:
                deck = three_player_deck.copy()
                if _options.use_flowers:
                    deck.extend(three_player_flowers)
            else:
                deck = four_player_deck.copy()
                if _options.use_flowers:
                    deck.extend(four_player_flowers)
            self._deck = Deck.shuffled_deck(deck)
        self._discard_pool = DiscardPool()
        self._hands = [Hand(self._deck) for _ in range(self._player_count)]
        for tile_count in [4, 4, 4, 1]:
            for wind in range(self._player_count):
                self._hands[(sub_round + wind) % self._player_count].add_to_hand(
                    tile_count
                )
        self._hands[sub_round].draw()

        for hand in self._hands:
            hand.sort()

        self._current_player = sub_round
        self._status = RoundStatus.START
        self._last_tile: TileId = 0
        self._history: list[tuple[int, Action]] = []
        self._win: Win | None = None

        self._calculate_allowed_actions()

        self._flower_pass_count = 0
        if self._options.auto_replace_flowers:
            while self._status == RoundStatus.START:
                player = self._current_player
                flower_actions = self._hands[player].get_flowers()
                for flower_action in flower_actions:
                    self.do_action(player, flower_action)
                self.do_action(player, SimpleAction(action_type=ActionType.CONTINUE))

    def get_hand(self, player: int) -> Sequence[TileId]:
        """
        Get a given player's hand's tiles.
        Does not include flowers or tiles in calls.

        :param player: The index of the player to check.
        """
        return self._hands[player].tiles

    def get_discard_tiles(self, player: int) -> Sequence[TileId]:
        """
        Get a given player's discarded tiles.

        :param player: The index of the player to check.
        """
        return [
            discard.tile
            for discard in self._discard_pool.discards
            if discard.player == player
        ]

    def get_calls(self, player: int) -> Sequence[Call]:
        """
        Get a given player's calls.

        :param player: The index of the player to check.
        """
        return self._hands[player].calls

    def get_flowers(self, player: int) -> Sequence[TileId]:
        """
        Get a given player's flowers.

        :param player: The index of the player to check.
        """
        return self._hands[player].flowers

    @property
    def player_count(self) -> int:
        "The number of players."
        return self._player_count

    @property
    def current_player(self) -> int:
        "The index of the player whose turn it is."
        return self._current_player

    @property
    def status(self) -> RoundStatus:
        "The current status of the round."
        return self._status

    @property
    def wind_round(self) -> int:
        "The wind round number of the round."
        return self._wind_round

    @property
    def allowed_actions(self) -> tuple[ActionList, ...]:
        "A tuple of :py:class:`ActionList` s of the legal actions for each player."
        return self._allowed_actions

    @property
    def discards(self) -> Sequence[Discard]:
        "The round's discards, as a sequence of :py:class:`Discard` s."
        return self._discard_pool.discards

    @property
    def discard_tiles(self) -> Sequence[TileId]:
        "The round's discards, as a sequence of :py:class:`TileId` s."
        return [discard.tile for discard in self._discard_pool.discards]

    @property
    def last_tile(self) -> TileId:
        "The last discarded tile."
        return self._last_tile

    @property
    def wall_count(self) -> int:
        "The number of tiles currently left in the deck."
        return len(self._deck.tiles)

    @property
    def tiles_left(self) -> int:
        "The number of tile draws currently left in the round."
        return len(self._deck.tiles) - self._options.end_wall_count

    @property
    def history(self) -> list[tuple[int, Action]]:
        "A list of all the actions taken in this round."
        return self._history

    @property
    def win(self) -> Win | None:
        """
        A :py:class:`Win` object representing the win of this round,
        or ``None`` if no player has won yet.
        """
        return self._win

    def display_info(self) -> None:
        "Print the current status of the round. For debug purposes."
        print(
            f"Current player: {self.current_player}, "
            + f"Status: {self.status}, "
            + f"Tiles left: {self.tiles_left}"
        )
        for player, hand in enumerate(self._hands):
            print(
                f"Player {player}: ",
                hand.tiles,
                [get_call_tiles(call) for call in hand.calls],
            )
        print("Discards:", self.discard_tiles)

    def _calculate_allowed_actions(self) -> None:
        self._allowed_actions = tuple(
            _allowed_actions_funcs[self._status](
                self, player, self._hands[player], self._last_tile
            )
            for player in range(self._player_count)
        )
        self._all_allowed_actions = sorted(
            (
                (player, action)
                for player, action_list in enumerate(self._allowed_actions)
                for action in action_list.actions
            ),
            key=lambda playeraction: (
                -playeraction[1].action_type,
                (playeraction[0] - self._current_player) % self._player_count,
            ),
        )

    def do_action(self, player: int, action: Action) -> None:
        """
        Have a player perform an action in the round of mahjong.

        :param player: The index of the player performing an action.
        :param action: The action to perform.
        """
        if action not in self.allowed_actions[player].actions:
            raise InvalidMoveException(action, self.allowed_actions[player].actions)
        _do_action_funcs[action.action_type](self, player, action)
        self._history.append((player, action))
        self._calculate_allowed_actions()
        if self._status == RoundStatus.END:
            self._end_callback()

    def get_priority_action(
        self, actions: Sequence[Action | None]
    ) -> tuple[int, Action] | None:
        """
        Determine the highest priority action, given actions that
        each player has submitted.

        If all players have submitted legal actions, then the highest
        priority action out of all submitted actions is selected.

        * If a player submits an illegal action, they are treated as
          having submitted their default action.
        * If a player has only one legal action, they are treated as having
          submitted that legal action regardless of whether they have actually
          submitted an action.

        If not all players have submitted actions, then this function
        determines whether the highest priority action can be deduced
        from what has already been submitted.
        If all legal actions of players who have not submitted have a
        lower priority than the highest priority submitted action,
        then the highest priority submitted action will be returned.
        Otherwise, the highest priority action cannot yet be determined,
        and ``None`` is returned.

        :param actions: The action each player has submitted, or ``None``
                        if the player has not yet submitted an action.
        :return: The highest priority action and the player who performs it,
                 or ``None`` if this cannot yet be determined.
        """
        if len(actions) != self._player_count:
            raise Exception("Incorrect number of elements in actions")
        validated_actions: list[Action | None] = []
        for player, action in enumerate(actions):
            allowed_actions = self.allowed_actions[player]
            if action is None:
                valid_action = allowed_actions.auto
            elif action not in allowed_actions.actions:
                valid_action = allowed_actions.default
            else:
                valid_action = action
            validated_actions.append(valid_action)

        for player, action in self._all_allowed_actions:
            if validated_actions[player] == action:
                return player, action
            elif validated_actions[player] is None:
                return None
        assert False

    def _previous_player(self, player: int) -> int:
        return (player - 1) % self._player_count

    def _next_player(self, player: int) -> int:
        return (player + 1) % self._player_count

    def _is_instant(self, player: int, history_items: list[tuple[int, Action]]) -> bool:
        return all(
            (action.action_type not in call_action_types)
            and not (
                action.action_type == ActionType.DISCARD and history_player == player
            )
            for history_player, action in history_items
        )

    @_register_allowed_actions(RoundStatus.START)
    def _allowed_actions_start(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self._current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
            actions.add_actions(hand.get_flowers())
            return actions
        else:
            return ActionList()

    @_register_allowed_actions(RoundStatus.PLAY)
    def _allowed_actions_play(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self._current_player == player:
            flower_actions = hand.get_flowers()
            if self._options.auto_replace_flowers and len(flower_actions) > 0:
                return ActionList(flower_actions[0])
            else:
                discard_actions = hand.get_discards()
                actions = ActionList(discard_actions[-1])
                actions.add_actions(discard_actions[:-1])
                if self._options.allow_riichi:
                    actions.add_actions(hand.get_riichis())
                actions.add_actions(hand.get_add_kans())
                actions.add_actions(hand.get_closed_kans())
                actions.add_actions(flower_actions)
                if self._can_tsumo(player):
                    actions.add_simple_action(ActionType.TSUMO)
                return actions
        else:
            return ActionList()

    @_register_allowed_actions(RoundStatus.CALLED_PLAY)
    def _allowed_actions_called_play(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self._current_player == player:
            flower_actions = hand.get_flowers()
            if self._options.auto_replace_flowers and len(flower_actions) > 0:
                return ActionList(flower_actions[0])
            else:
                discard_actions = hand.get_discards()
                actions = ActionList(discard_actions[-1])
                actions.add_actions(discard_actions[:-1])
                actions.add_actions(flower_actions)
                return actions
        else:
            return ActionList()

    @_register_allowed_actions(RoundStatus.ADD_KAN_AFTER)
    def _allowed_actions_add_kan_after(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self.current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
        else:
            actions = ActionList()
            if self._can_ron(player):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.CLOSED_KAN_AFTER)
    def _allowed_actions_closed_kan_after(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self.current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
        else:
            actions = ActionList()
            if self._can_ron(player):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.DISCARDED)
    def _allowed_actions_discarded(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self._current_player == self._previous_player(player):
            actions = ActionList(SimpleAction(action_type=ActionType.DRAW))
        else:
            actions = ActionList()
        if self._current_player == self._previous_player(player):
            actions.add_actions(hand.get_chiis(last_tile))
        if self._current_player != player:
            actions.add_actions(hand.get_pons(last_tile))
            actions.add_actions(hand.get_open_kans(last_tile))
            if self._can_ron(player):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.LAST_DISCARDED)
    def _allowed_actions_last_discarded(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        if self.current_player == player:
            actions = ActionList(SimpleAction(action_type=ActionType.CONTINUE))
        else:
            actions = ActionList()
            if self._can_ron(player):
                actions.add_simple_action(ActionType.RON)
        return actions

    @_register_allowed_actions(RoundStatus.END)
    def _allowed_actions_end(
        self, player: int, hand: Hand, last_tile: TileId
    ) -> ActionList:
        return ActionList()

    @_register_do_action(ActionType.PASS)
    def _pass(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.PASS
        assert False

    @_register_do_action(ActionType.CONTINUE)
    def _continue(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.CONTINUE
        if self._status == RoundStatus.START:
            self._hands[player].sort()
            self._flower_pass_count += 1
            if self._flower_pass_count >= self._player_count + 1:
                self._current_player = self._sub_round
                self._status = RoundStatus.PLAY
            else:
                self._current_player = self._next_player(self._current_player)
        elif (
            self._status == RoundStatus.ADD_KAN_AFTER
            or self._status == RoundStatus.CLOSED_KAN_AFTER
        ):
            self._status = RoundStatus.PLAY
            self._last_tile = 0
        elif self._status == RoundStatus.LAST_DISCARDED:
            self._status = RoundStatus.END

    @_register_do_action(ActionType.DRAW)
    def _draw(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.DRAW
        self._hands[player].draw()
        self._current_player = player
        self._status = RoundStatus.PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.DISCARD)
    def _discard(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.DISCARD
        tile = action.tile
        self._hands[player].discard(tile)
        self._discard_pool.append(player, tile, self._hands[player].is_riichi)
        if self.tiles_left > 0:
            self._status = RoundStatus.DISCARDED
        else:
            self._status = RoundStatus.LAST_DISCARDED
        self._last_tile = tile

    @_register_do_action(ActionType.RIICHI)
    def _riichi(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.RIICHI
        tile = action.tile
        self._hands[player].riichi(tile)
        self._discard_pool.append(player, tile, self._hands[player].is_riichi)
        if self.tiles_left > 0:
            self._status = RoundStatus.DISCARDED
        else:
            self._status = RoundStatus.LAST_DISCARDED
        self._last_tile = tile

    @_register_do_action(ActionType.CHII)
    def _chii(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.CHII
        self._discard_pool.pop()
        self._hands[player].chii(
            self._current_player, self._last_tile, action.other_tiles
        )
        self._current_player = player
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.PON)
    def _pon(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.PON
        self._discard_pool.pop()
        self._hands[player].pon(
            self._current_player, self._last_tile, action.other_tiles
        )
        self._current_player = player
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.OPEN_KAN)
    def _open_kan(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.OPEN_KAN
        self._discard_pool.pop()
        self._hands[player].open_kan(
            self._current_player, self._last_tile, action.other_tiles
        )
        self._current_player = player
        self._status = RoundStatus.CALLED_PLAY
        self._last_tile = 0

    @_register_do_action(ActionType.ADD_KAN)
    def _add_kan(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.ADD_KAN
        self._hands[player].add_kan(action.tile, action.pon_call)
        self._status = RoundStatus.ADD_KAN_AFTER
        self._last_tile = action.tile

    @_register_do_action(ActionType.CLOSED_KAN)
    def _closed_kan(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.CLOSED_KAN
        self._hands[player].closed_kan(action.tiles)
        self._status = RoundStatus.CLOSED_KAN_AFTER
        self._last_tile = action.tiles[0]

    @_register_do_action(ActionType.FLOWER)
    def _flower(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.FLOWER
        self._hands[player].flower(action.tile)
        self._flower_pass_count = 0

    @_register_do_action(ActionType.RON)
    def _ron(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.RON
        self._win = self._get_win_ron(player)
        self._status = RoundStatus.END

    @_register_do_action(ActionType.TSUMO)
    def _tsumo(self, player: int, action: Action) -> None:
        assert action.action_type == ActionType.TSUMO
        self._win = self._get_win_tsumo(player)
        self._status = RoundStatus.END

    def _get_riichi_flags(self, player: int) -> tuple[bool, bool, bool]:
        riichi_index = next(
            (
                index
                for index, history_item in enumerate(self._history)
                if history_item[0] == player
                and history_item[1].action_type == ActionType.RIICHI
            ),
            None,
        )
        if riichi_index is not None:
            return (
                True,
                self._is_instant(player, self._history[:riichi_index]),
                self._is_instant(player, self._history[riichi_index:]),
            )
        else:
            return (False, False, False)

    def _get_win_ron(self, player: int) -> Win | None:
        hand = self._hands[player]
        last_tile = self._last_tile
        waits = hand.waits
        if get_tile_value(last_tile) not in waits:
            return None

        is_riichi, is_double_riichi, is_ippatsu = self._get_riichi_flags(player)
        is_chankan = (
            self._status == RoundStatus.ADD_KAN_AFTER
            or self._status == RoundStatus.CLOSED_KAN_AFTER
        )
        is_houtei = self._status == RoundStatus.LAST_DISCARDED
        return Win(
            win_player=player,
            lose_player=self._current_player,
            hand=list(hand.tiles) + [last_tile],
            calls=list(hand.calls),
            flowers=list(hand.flowers),
            player_count=self._player_count,
            wind_round=self._wind_round,
            sub_round=self._sub_round,
            draw_count=self._draw_count,
            is_riichi=is_riichi,
            is_double_riichi=is_double_riichi,
            is_ippatsu=is_ippatsu,
            is_chankan=is_chankan,
            is_houtei=is_houtei,
        )

    def _get_win_tsumo(self, player: int) -> Win | None:
        hand = self._hands[player]
        if not hand.can_tsumo():
            return None

        after_flower_count = 0
        after_kan_count = 0
        for player, action in reversed(self._history):
            action_type = action.action_type
            if action_type == ActionType.FLOWER:
                after_flower_count += 1
            elif action_type == ActionType.ADD_KAN:
                after_kan_count += 1
            elif action_type == ActionType.CLOSED_KAN:
                after_kan_count += 1
            elif action_type == ActionType.CONTINUE:
                pass
            else:
                break

        is_riichi, is_double_riichi, is_ippatsu = self._get_riichi_flags(player)
        is_haitei = self.tiles_left <= 0
        is_tenhou = False
        is_chiihou = False
        if self._is_instant(player, self._history):
            if player == self._sub_round:
                is_tenhou = True
            else:
                is_chiihou = True
        return Win(
            win_player=player,
            lose_player=None,
            hand=list(hand.tiles),
            calls=list(hand.calls),
            flowers=list(hand.flowers),
            player_count=self._player_count,
            wind_round=self._wind_round,
            sub_round=self._sub_round,
            draw_count=self._draw_count,
            after_flower_count=after_flower_count,
            after_kan_count=after_kan_count,
            is_riichi=is_riichi,
            is_double_riichi=is_double_riichi,
            is_ippatsu=is_ippatsu,
            is_haitei=is_haitei,
            is_tenhou=is_tenhou,
            is_chiihou=is_chiihou,
        )

    def _is_valid_win(self, win: Win | None) -> bool:
        if win is None:
            return False
        scoring = Scorer.score(win, self._options)
        return scoring.han >= self._options.min_han

    def _can_ron(self, player: int) -> bool:
        return self._is_valid_win(self._get_win_ron(player))

    def _can_tsumo(self, player: int) -> bool:
        return self._is_valid_win(self._get_win_tsumo(player))


AllowedActionsFunc = Callable[[Round, int, Hand, TileId], ActionList]
DoActionFunc = Callable[[Round, int, Action], None]
