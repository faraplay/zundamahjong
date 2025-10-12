import { useContext } from "preact/hooks";

import type { Player } from "../../types/player";

import "./user_settings_form.css";
import { Emitter } from "../emitter/emitter";

export function UserSettingsForm({
  myPlayer,
  showSettings,
  goToSettings,
}: {
  myPlayer: Player;
  showSettings: boolean;
  goToSettings: () => void;
}) {
  const emit = useContext(Emitter);

  const onGoToSettingsClick = (e: Event) => {
    e.preventDefault();
    goToSettings();
  };

  let button_message;
  if (showSettings) {
    button_message = "Go back to lobby";
  } else {
    button_message = "Change user settings";
  }

  const goToSettingsButton = (
    <button type="button" onClick={onGoToSettingsClick}>
      {button_message}
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

  let welcome_message;
  if (myPlayer.new_account) {
    welcome_message = "Account succesfully created";
  } else {
    welcome_message = `Welcome back, ${myPlayer.name}`;
  }

  if (myPlayer.logged_in && !showSettings) {
    return (
      <div id="user_settings">
        {welcome_message} {goToSettingsButton}
      </div>
    );
  }

  if (myPlayer.logged_in && showSettings) {
    return (
      <div id="user_settings">
        <p>Welcome to the user settings</p>

        <form id="user_settings_form" action="" onSubmit={submitSettings}>
          <label for="cur_password">Current Password:</label>
          <input id="cur_password" name="cur_password" type="password" />

          <label for="new_password">New Password:</label>
          <input id="new_password" name="new_password" type="password" />

          <label for="new_password_2">Confirm Password:</label>
          <input id="new_password_2" name="new_password_2" type="password" />

          <div id="submit_settings_buttons">
            <button type="submit">Submit</button>
            {goToSettingsButton}
          </div>
        </form>
      </div>
    );
  }
}
