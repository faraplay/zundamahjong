import { render } from "preact";
import { NameForm } from "./components/name_form/name_form";

import "./components/server_message_list/server_message_list.css";

import "./index.css";
import "./fonts.css";
import "./app.css";

function App() {
  return (
    <div id="name_screen" class="screen">
      <NameForm />
    </div>
  );
}

render(<App />, document.getElementById("app")!);
