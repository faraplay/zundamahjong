import { useContext } from "preact/hooks";

import { Emitter } from "../emitter/emitter";

import "./game_options_form.css";

export function GameOptionsForm({
  player_count,
  can_start,
}: {
  player_count: number;
  can_start: boolean;
}) {
  const emit = useContext(Emitter);
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    emit("start_game", Object.fromEntries(formData));
  };
  return (
    <form id="game_options_form" onSubmit={onSubmit}>
      <label for="player_count">Number of players</label>
      <input
        id="game_options_player_count"
        type="number"
        name="player_count"
        value={player_count}
        readonly
      />
      <label for="game_length_wind_rounds">Number of wind rounds</label>
      <input
        type="number"
        name="game_length_wind_rounds"
        min="0"
        max="4"
        step="1"
        value="1"
      />
      <label for="game_length_sub_rounds">Number of sub rounds</label>
      <input
        type="number"
        name="game_length_sub_rounds"
        min="0"
        max="3"
        step="1"
        value="0"
      />
      <label for="score_dealer_ron_base_value">Dealer ron base score</label>
      <input
        id="score_dealer_ron_base_value"
        type="number"
        name="score_dealer_ron_base_value"
        value="1.5"
        step="0.5"
      />
      <label for="score_dealer_tsumo_base_value">Dealer tsumo base score</label>
      <input
        id="score_dealer_tsumo_base_value"
        type="number"
        name="score_dealer_tsumo_base_value"
        value="1.0"
        step="0.5"
      />
      <label for="score_nondealer_ron_base_value">
        Nondealer ron base score
      </label>
      <input
        id="score_nondealer_ron_base_value"
        type="number"
        name="score_nondealer_ron_base_value"
        value="1.0"
        step="0.5"
      />
      <label for="score_nondealer_tsumo_nondealer_base_value">
        Nondealer-nondealer tsumo base score
      </label>
      <input
        id="score_nondealer_tsumo_nondealer_base_value"
        type="number"
        name="score_nondealer_tsumo_nondealer_base_value"
        value="0.5"
        step="0.5"
      />
      <label for="score_nondealer_tsumo_dealer_base_value">
        Nondealer-dealer base score
      </label>
      <input
        id="score_nondealer_tsumo_dealer_base_value"
        type="number"
        name="score_nondealer_tsumo_dealer_base_value"
        value="1.0"
        step="0.5"
      />
      <button type="submit" id="start_game" disabled={!can_start}>
        Start game
      </button>
    </form>
  );
}
