import { render } from "preact";
import { NameForm } from "./components/name_form/name_form";

import "./base.css";
import "./login.css";
import "./fonts.css";

function App() {
  return (
    <div id="name_screen" class="screen">
      <NameForm />
    </div>
  );
}

render(<App />, document.getElementById("app")!);
