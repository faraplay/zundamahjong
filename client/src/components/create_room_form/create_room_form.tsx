import { useContext } from "preact/hooks";
import "./create_room_form.css";
import { Emitter } from "../emitter/emitter";
import {
  default_3player_preset,
  default_4player_preset,
} from "../../types/game_options_presets.ts";

export function CreateRoomForm() {
  const emit = useContext(Emitter);
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const room_name = formData.get("room_name");
    const player_count = Number(formData.get("player_count"));
    if (!room_name) return;
    if (!(player_count == 3 || player_count == 4)) return;
    const game_options =
      player_count == 3 ? default_3player_preset : default_4player_preset;
    emit("create_room", room_name, game_options);
  };
  return (
    <form id="create_room_form" action="" onSubmit={onSubmit}>
      Or create a room
      <div>
        <label for="create_room_room_name">Room name:</label>
        <input id="create_room_room_name" name="room_name" type="text" />
      </div>
      <div>
        <label for="create_room_player_count">Number of players:</label>
        <select id="create_room_player_count" name="player_count">
          <option value={3}>3</option>
          <option value={4}>4</option>
        </select>
      </div>
      <button type="submit">Create room</button>
    </form>
  );
}
