import "./name_form.css";

export function NameForm({
  emit,
}: {
  emit: (event: string, ...args: any[]) => any;
}) {
  const onSubmit = (e: SubmitEvent) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget as HTMLFormElement);
    const name = formData.get("name");
    if (name) {
      emit("set_name", name);
    }
  };
  return (
    <form id="name_form" action="" onSubmit={onSubmit}>
      Enter a name
      <div>
        <label for="name_input">Name</label>
        <input id="name_input" name="name" type="text" />
      </div>
      <button type="submit">Set name</button>
    </form>
  );
}
