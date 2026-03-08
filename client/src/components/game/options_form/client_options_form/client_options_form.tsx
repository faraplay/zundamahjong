import { useId } from "preact/hooks";

import type { ClientOptions } from "../../../../types/client_options";

import { clientInputPropsList } from "../input_props";
import {
  flattenInputPropsList,
  OptionsInputList,
} from "../options_input/options_input";

export function getClientOptions(formId: string) {
  const formData = new FormData(
    document.getElementById(formId) as HTMLFormElement,
  );
  const formObject = {} as ClientOptions;
  for (const inputProps of flattenInputPropsList(clientInputPropsList)) {
    if (inputProps.type == "number") {
      formObject[inputProps.name] = Number(formData.get(inputProps.name));
    } else {
      formObject[inputProps.name] = formData.has(inputProps.name);
    }
  }
  return formObject;
}
export function ClientOptionsForm({
  clientOptions,
  setClientOptions,
}: {
  clientOptions: ClientOptions;
  setClientOptions: (value: ClientOptions) => void;
}) {
  const formId = useId();

  const setOptions = () => {
    setClientOptions(getClientOptions(formId));
  };

  return (
    <div class="option_controls client_option_controls">
      <form id={formId} hidden />
      <div class="options client_options">
        <OptionsInputList
          inputPropsList={clientInputPropsList}
          options={clientOptions}
          isEditable={true}
          formId={formId}
          setOptions={setOptions}
        />
      </div>
    </div>
  );
}
