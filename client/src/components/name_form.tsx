import "./name_form.css";

export function NameForm() {
  return (
    <form id="name_form" action="">
      Enter a name
      <div>
        <label for="name_input">Name</label>
        <input id="name_input" type="text" />
      </div>
      <button type="submit">Set name</button>
    </form>
  );
}
