import "./create_room_form.css";

export function CreateRoomForm() {
  return (
    <form id="create_room_form" action="">
      Or create a room
      <div>
        <label for="create_room_name">Room name:</label>
        <input id="create_room_name" type="text" />
      </div>
      <div>
        <label for="player_count_select">Number of players:</label>
        <select id="player_count_select">
          <option value={3}>3</option>
          <option value={4}>4</option>
        </select>
      </div>
      <button type="submit">Create room</button>
    </form>
  );
}
