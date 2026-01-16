import { render } from "preact";
import "./base.css";
import { App } from "./app.tsx";

import "./assets/icon.png";

render(<App />, document.getElementById("app")!);
