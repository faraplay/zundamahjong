import { useContext, useId, useState } from "preact/hooks";

import type { ClientOptions } from "../../../types/client_options";
import { GameOptionsForm } from "../../room/game_options_form/game_options_form";
import { OptionsContext } from "../../options_context/options_context";

import "./options_bar.css";

function getClientOptions(formId: string) {
  const formData = new FormData(
    document.getElementById(formId) as HTMLFormElement,
  );
  const formObject = {} as ClientOptions;
  formObject.show_tile_numbers = formData.has("show_tile_numbers");
  return formObject;
}

export function OptionsBar() {
  const [isOpen, setIsOpen] = useState(false);
  const options = useContext(OptionsContext)!;

  const clientOptionsFormId = useId();
  const tileNumbersInputId = useId();

  const showHideOptions = (e: Event) => {
    e.preventDefault();
    setIsOpen(!isOpen);
  };

  const onChange = (e: Event) => {
    e.preventDefault();
    options.set_client_options(getClientOptions(clientOptionsFormId));
  };

  return (
    <div class={`options_bar ${isOpen ? "open" : "closed"}`}>
      <button type="button" class="open_close" onClick={showHideOptions}>
        {isOpen ? "Hide options" : "View options"}
      </button>
      <div class="sidebar">
        <div class="game_options_title">Client Options</div>
        <form id={clientOptionsFormId} hidden />
        <label for={tileNumbersInputId}>Show tile numbers</label>
        <input
          form={clientOptionsFormId}
          id={tileNumbersInputId}
          checked={options.client_options.show_tile_numbers}
          name="show_tile_numbers"
          type="checkbox"
          onChange={onChange}
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
