import type { Pattern, PatternData } from "../../../types/game_options";

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
      <label>{data.display_name}</label>
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
