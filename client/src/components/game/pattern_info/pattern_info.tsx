import type { JSX } from "preact/jsx-runtime";
import type { PatternData } from "../../../types/game_options";
import "./pattern_info.css";

export function PatternInfo({ data }: { data: PatternData }) {
  const children: JSX.Element[] = [];
  if (data.han != 0) {
    children.push(<span class="han">{`${data.han} han`}</span>);
  }
  if (data.fu != 0) {
    children.push(<span class="fu">{`${data.fu} fu`}</span>);
  }
  return (
    <div class="pattern">
      <span class="display_name">{data.display_name}</span>
      <span class="values">{children}</span>
    </div>
  );
}
