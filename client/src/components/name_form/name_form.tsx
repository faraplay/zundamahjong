import { useContext } from "preact/hooks";

import { Emitter } from "../emitter/emitter";

import "./name_form.css";

export function NameForm() {
  const emit = useContext(Emitter);
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const name = formData.get("name");
    const password = formData.get("password");
    if (name) {
      emit("set_name", name, password);
      emit("get_rooms");
    }
  };
  return (
    <form id="name_form" action="" onSubmit={onSubmit}>
      Enter a name
      <div>
        <label for="name_input">Name</label>
        <input id="name_input" name="name" type="text" />
      </div>
      <div>
        <label for="password_input">Password</label>
        <input id="password_input" name="password" type="password" />
      </div>
      <button type="submit">Set name</button>
    </form>
  );
}
