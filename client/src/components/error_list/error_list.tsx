import type { ErrorMessage } from "../../types/error_message";

import "./error_list.css";

function ErrorListItem({
  errorMessage,
  removeThisError,
}: {
  errorMessage: string;
  removeThisError: () => void;
}) {
  const onClick = (e: Event) => {
    e.preventDefault();
    removeThisError();
  };
  return (
    <div class="error_list_item">
      <button onClick={onClick}>&times;</button>
      <span>{errorMessage}</span>
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
          errorMessage={error.message}
          removeThisError={() => removeError(error.index)}
        />
      ))}
    </div>
  );
}
