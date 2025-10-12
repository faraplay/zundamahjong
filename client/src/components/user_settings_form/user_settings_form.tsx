import { useContext } from "preact/hooks";

import "./user_settings_form.css";
import { Emitter } from "../emitter/emitter";

export function UserSettingsForm({ goToLobby }: { goToLobby: () => void }) {
  const emit = useContext(Emitter);

  const onGoToLobbyClick = (e: Event) => {
    e.preventDefault();
    goToLobby();
  };

  const goToLobbyButton = (
    <button type="button" onClick={onGoToLobbyClick}>
      Go back to lobby
    </button>
  );

  const submitSettings = (e: SubmitEvent) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const cur_password = formData.get("cur_password");
    const new_password_2 = formData.get("new_password_2");
    const new_password = formData.get("new_password");

    if (cur_password && new_password == new_password_2) {
      emit("change_password", cur_password, new_password);
    }
  };

  return (
    <div id="user_settings">
      <p>User settings</p>

      <form id="user_settings_form" action="" onSubmit={submitSettings}>
        <label for="cur_password">Current Password:</label>
        <input id="cur_password" name="cur_password" type="password" />

        <label for="new_password">New Password:</label>
        <input id="new_password" name="new_password" type="password" />

        <label for="new_password_2">Confirm Password:</label>
        <input id="new_password_2" name="new_password_2" type="password" />

        <div id="submit_settings_buttons">
          <button type="submit">Submit</button>
          {goToLobbyButton}
        </div>
      </form>
    </div>
  );
}
