import { useState } from "preact/hooks";
import {
  patternDescs,
  type Pattern,
  type PatternData,
} from "../../../../types/pattern";

function PatternInputLabel({
  displayName,
  description,
}: {
  displayName: string;
  description: string;
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
    <label onMouseOver={onHoverStart} onMouseOut={onHoverEnd}>
      {displayName}
      {isHover ? (
        <div class="description">
          <p>{description}</p>
        </div>
      ) : (
        <></>
      )}
    </label>
  );
}

export function GameOptionsPatternInput({
  isEditable,
  name,
  data,
  formId,
  sendGameOptions,
}: {
  isEditable: boolean;
  name: Pattern;
  data: PatternData;
  formId: string;
  sendGameOptions: () => void;
}) {
  const onChange = (e: Event) => {
    e.preventDefault();
    sendGameOptions();
  };
  const editableProps = isEditable ? { onChange } : { readonly: true };
  return (
    <>
      <PatternInputLabel {...patternDescs[name]} />
      <input
        form={formId}
        name={`${name}___han`}
        type="number"
        value={data.han}
        {...editableProps}
      />
      <input
        form={formId}
        name={`${name}___fu`}
        type="number"
        value={data.fu}
        {...editableProps}
      />
    </>
  );
}
