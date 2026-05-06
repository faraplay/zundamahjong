import { useState } from "preact/hooks";
import type { InputLabelProps } from "../input_props";

export function InputLabel({
  inputId,
  inputProps,
}: {
  inputId: string;
  inputProps: InputLabelProps;
}) {
  const [isHover, setIsHover] = useState<boolean>(false);
  const onHoverStart = (e: MouseEvent) => {
    e.preventDefault();
    setIsHover(true);
  };
  const onHoverEnd = (e: MouseEvent) => {
    e.preventDefault();
    setIsHover(false);
  };
  return (
    <label for={inputId} onMouseOver={onHoverStart} onMouseOut={onHoverEnd}>
      {inputProps.labelText}
      {isHover ? (
        <div class="description">
          <p>{inputProps.description}</p>
          {inputProps.subDescription ? (
            <p>{inputProps.subDescription}</p>
          ) : (
            <></>
          )}
        </div>
      ) : (
        <></>
      )}
    </label>
  );
}
