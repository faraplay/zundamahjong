import "./name_form.css";

export function NameForm() {
  return (
    <form id="name_form" method="POST" action="/zundamahjong/login/">
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
