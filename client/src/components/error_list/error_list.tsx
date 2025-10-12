import type { ErrorMessage } from "../../types/error_message";

import "./error_list.css";

function ErrorListItem({
  error,
  removeThisError,
}: {
  error: ErrorMessage;
  removeThisError: () => void;
}) {
  const onClick = (e: Event) => {
    e.preventDefault();
    removeThisError();
  };
  return (
    <div class={`error_list_item ${error.severity.toLowerCase()}`}>
      <button onClick={onClick}>&times;</button>
      <span>{error.message}</span>
    </div>
  );
}

export function ErrorList({
  errors,
  removeError,
}: {
  errors: ReadonlyArray<ErrorMessage>;
  removeError: (errorIndex: number) => void;
}) {
  return (
    <div class="error_list">
      {errors.map((error) => (
        <ErrorListItem
          key={error.index}
          error={error}
          removeThisError={() => removeError(error.index)}
        />
      ))}
    </div>
  );
}
