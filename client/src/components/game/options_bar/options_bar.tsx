import { useContext, useState } from "preact/hooks";

import { GameOptionsForm } from "../../room/game_options_form/game_options_form";
import { GameOptionsContext } from "../../game_options_context/game_options_context";

import "./options_bar.css";

export function OptionsBar() {
  const [isOpen, setIsOpen] = useState(false);
  const gameOptions = useContext(GameOptionsContext)!;

  const onClick = (e: Event) => {
    e.preventDefault();
    setIsOpen(!isOpen);
  };

  return (
    <div class={`options_bar ${isOpen ? "open" : "closed"}`}>
      <button type="button" class="open_close" onClick={onClick}>
        {isOpen ? "Hide options" : "View options"}
      </button>
      <div class="sidebar">
        <div class="game_options_title">Game Options</div>
        <GameOptionsForm
          gameOptions={gameOptions}
          isEditable={false}
          can_start={false}
        />
      </div>
    </div>
  );
}
