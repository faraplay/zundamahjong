import { useContext } from "preact/hooks";

import type { BasicRoom } from "../../types/room";

import { Emitter } from "../emitter/emitter";

export function RoomInfo({ room }: { room: BasicRoom }) {
  const emit = useContext(Emitter);
  const room_info_text =
    `Room ${room.room_name} --- ` +
    `${room.player_count} player game --- ` +
    `Players: ${room.joined_players.map((player) => player.name).join(", ")}`;
  const leaveRoom = (e: MouseEvent) => {
    e.preventDefault();
    emit("leave_room");
    emit("get_rooms");
  };
  return (
    <>
      <span id="room_info">{room_info_text}</span>
      <button type="button" id="leave_room" onClick={leaveRoom}>
        Leave room
      </button>
    </>
  );
}
