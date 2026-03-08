import { useContext, useState } from "preact/hooks";

import { GameOptionsForm } from "../options_form/game_options_form/game_options_form";
import { ClientOptionsForm } from "../options_form/client_options_form/client_options_form";
import { OptionsContext } from "../../options_context/options_context";

import "./options_bar.css";

export function OptionsBar() {
  const [isOpen, setIsOpen] = useState(false);
  const options = useContext(OptionsContext)!;

  const showHideOptions = (e: Event) => {
    e.preventDefault();
    setIsOpen(!isOpen);
  };

  return (
    <div class={`options_bar ${isOpen ? "open" : "closed"}`}>
      <button type="button" class="open_close" onClick={showHideOptions}>
        {isOpen ? "Hide options" : "View options"}
      </button>
      <div class="sidebar">
        <div class="game_options_title">Client Options</div>
        <ClientOptionsForm
          clientOptions={options.client_options}
          setClientOptions={options.set_client_options}
        />
        <div class="game_options_title">Game Options</div>
        <GameOptionsForm
          gameOptions={options.game_options}
          isEditable={false}
          can_start={false}
        />
      </div>
    </div>
  );
}
