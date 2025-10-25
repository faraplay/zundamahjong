import type { Player } from "../../types/player";

import "./user_welcome.css";

export function UserWelcome({
  myPlayer,
  goToSettings,
}: {
  myPlayer: Player;
  goToSettings: () => void;
}) {
  const onGoToSettingsClick = (e: Event) => {
    e.preventDefault();
    goToSettings();
  };

  const goToSettingsButton = (
    <button type="button" onClick={onGoToSettingsClick}>
      Change user settings
    </button>
  );

  const logoutButton = (
    <button type="button" onClick={() => (window.location.href = "./logout")}>
      Logout
    </button>
  );

  const welcome_message =
    myPlayer.has_account && !myPlayer.new_user
      ? `Welcome back, ${myPlayer.name}`
      : `Welcome, ${myPlayer.name}`;

  if (myPlayer.has_account) {
    return (
      <div id="user_welcome">
        {welcome_message} {goToSettingsButton} {logoutButton}
      </div>
    );
  }

  return (
    <div id="user_welcome">
      {welcome_message} {logoutButton}
    </div>
  );
}
