import type { Room } from "../../types/room";

import "./join_room_form.css";

function RoomOption({ room }: { room: Room }) {
  const innerText =
    `${room.room_name} ` +
    `(${room.joined_players.length}/${room.player_count}) ` +
    room.joined_players.map((player) => player.name).join(", ");
  return (
    <option
      key={room.room_name}
      value={room.room_name}
      disabled={room.joined_players.length == room.player_count}
    >
      {innerText}
    </option>
  );
}

export function JoinRoomForm({ rooms }: { rooms: Array<Room> }) {
  return (
    <form id="join_room_form" action="">
      Select a room to join
      <select id="room_list" size={4}>
        {rooms.map((room) => RoomOption({ room }))}
      </select>
      <div id="join_room_buttons">
        <button type="button" id="refresh_room_list">
          Refresh room list
        </button>
        <button type="submit">Join room</button>
      </div>
    </form>
  );
}
