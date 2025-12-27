from collections.abc import Iterable
from enum import IntEnum
from typing import Annotated, Literal, final

from pydantic import BaseModel, Field, TypeAdapter

from .call import OpenCall
from .tile import TileId


class ActionType(IntEnum):
    "Represents the type of an action a player can perform in a round of mahjong."

    PASS = 0
    "Indicates a choice not to take any action."
    CONTINUE = 1
    """
    Pass to the next player in the flower-replacement phase at the start of the game,
    or continue to play after making a added or closed kan call.
    """
    DRAW = 2
    "Draw a tile."
    DISCARD = 3
    "Discard a tile."
    RIICHI = 4
    "Riichi and discard a tile."
    CHII = 6
    "Make a chii call."
    PON = 7
    "Make a pon call."
    OPEN_KAN = 8
    "Make an open kan call."
    ADD_KAN = 9
    "Add a tile to an existing pon call to form an added kan."
    CLOSED_KAN = 10
    "Make a closed kan call."
    FLOWER = 11
    "Replace a flower."
    RON = 12
    "Win off another player's discard."
    TSUMO = 13
    "Win from one's own draw."


call_action_types = {
    ActionType.CHII,
    ActionType.PON,
    ActionType.OPEN_KAN,
    ActionType.ADD_KAN,
    ActionType.CLOSED_KAN,
}
"A set consisting of the :py:class:`ActionType` s that form calls."


class SimpleAction(BaseModel, frozen=True):
    "Represents an action with no additional data."

    action_type: Literal[
        ActionType.PASS,
        ActionType.CONTINUE,
        ActionType.DRAW,
        ActionType.RON,
        ActionType.TSUMO,
    ]
    "The :py:class:`ActionType` of the action."


class HandTileAction(BaseModel, frozen=True):
    "Represents an action that uses one tile from the player's hand."

    action_type: Literal[ActionType.DISCARD, ActionType.RIICHI, ActionType.FLOWER]
    "The :py:class:`ActionType` of the action."
    tile: TileId
    "The :py:class:`TileId` of the tile used from the player's hand."


class OpenCallAction(BaseModel, frozen=True):
    "Represents an action that creates a :py:class:`OpenCall` (chii or pon)."

    action_type: Literal[
        ActionType.CHII,
        ActionType.PON,
    ]
    "The :py:class:`ActionType` of the action."
    other_tiles: tuple[TileId, TileId]
    "A tuple of the two tiles from the player's hand that are used to form the call."


class OpenKanAction(BaseModel, frozen=True):
    "Represents an open kan call action."

    action_type: Literal[ActionType.OPEN_KAN] = ActionType.OPEN_KAN
    "The :py:class:`ActionType` of the action."
    other_tiles: tuple[TileId, TileId, TileId]
    """
    A tuple of the three tiles from the player's hand that are used to
    form the open kan.
    """


class AddKanAction(BaseModel, frozen=True):
    "Represents an added kan call action."

    action_type: Literal[ActionType.ADD_KAN] = ActionType.ADD_KAN
    "The :py:class:`ActionType` of the action."
    tile: TileId
    "The :py:class:`TileId` of the tile used from the player's hand."
    pon_call: OpenCall
    "The pon :py:class:`OpenCall` that is replaced by an :py:class:`AddKanCall`."


class ClosedKanAction(BaseModel, frozen=True):
    "Represents a closed kan call action."

    action_type: Literal[ActionType.CLOSED_KAN] = ActionType.CLOSED_KAN
    "The :py:class:`ActionType` of the action."
    tiles: tuple[TileId, TileId, TileId, TileId]
    """
    A tuple of the four tiles from the player's hand that are used to
    form the closed kan.
    """


Action = Annotated[
    SimpleAction
    | HandTileAction
    | OpenCallAction
    | OpenKanAction
    | AddKanAction
    | ClosedKanAction,
    Field(discriminator="action_type"),
]
"Represents an action a player can perform in a round of mahjong."

action_adapter: TypeAdapter[Action] = TypeAdapter(Action)
"Adapter used to validate a Python object as an Action."


@final
class ActionList:
    """
    Holds a list of actions a player can take.

    :param default_action: The default action a player should take.
    """

    def __init__(self, default_action: Action | None = None) -> None:
        if default_action is not None:
            _default_action = default_action
        else:
            _default_action = SimpleAction(action_type=ActionType.PASS)
        self._actions = [_default_action]

    @property
    def default(self) -> Action:
        """
        Return the default action a player should take.

        This can be used for example in place of when the player attempts
        to perform an illegal action.
        """
        return self._actions[0]

    @property
    def auto(self) -> Action | None:
        """
        Return the only action if the list has exactly one action.
        Otherwise, return `None`.
        """
        if len(self._actions) == 1:
            return self._actions[0]
        else:
            return None

    @property
    def actions(self) -> list[Action]:
        "Return the list of actions."
        return self._actions

    def add_simple_action(
        self,
        action_type: Literal[
            ActionType.PASS,
            ActionType.CONTINUE,
            ActionType.DRAW,
            ActionType.RON,
            ActionType.TSUMO,
        ],
    ) -> None:
        """
        Add a :py:class:`SimpleAction` to the list.

        :param action_type: The type of the :py:class:`SimpleAction` to add.
        """
        self._actions.append(SimpleAction(action_type=action_type))

    def add_actions(self, actions: Iterable[Action]) -> None:
        """
        Add :py:class:`Action` s to the list.

        :param actions: An iterable containing the :py:class:`Action` s
                        to add to the list.
        """
        self._actions.extend(actions)
