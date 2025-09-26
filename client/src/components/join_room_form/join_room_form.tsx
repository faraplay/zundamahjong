import { useContext } from "preact/hooks";
import type { Room } from "../../types/room";

import "./join_room_form.css";
import { Emitter } from "../emitter/emitter";

function RoomOption({ room }: { room: Room }) {
  const roomCapacityString = `(${room.joined_players.length}/${room.player_count})`;
  const roomPlayersString = room.joined_players
    .map((player) => player.name)
    .join(", ");
  return (
    <option
      key={room.room_name}
      value={room.room_name}
      disabled={room.joined_players.length == room.player_count}
    >
      {`${room.room_name} ${roomCapacityString} ${roomPlayersString}`}
    </option>
  );
}

export function JoinRoomForm({ rooms }: { rooms: Array<Room> }) {
  const emit = useContext(Emitter);
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const room_name = formData.get("room_name");
    if (room_name) {
      emit("join_room", room_name);
    }
  };
  const refreshRooms = (e: MouseEvent) => {
    e.preventDefault();
    emit("get_rooms");
  };

  return (
    <form id="join_room_form" action="" onSubmit={onSubmit}>
      Select a room to join
      <select id="join_room_room_name" name="room_name" size={4}>
        {rooms.map((room) => RoomOption({ room }))}
      </select>
      <div id="join_room_buttons">
        <button type="button" id="refresh_room_list" onClick={refreshRooms}>
          Refresh room list
        </button>
        <button type="submit">Join room</button>
      </div>
    </form>
  );
}
