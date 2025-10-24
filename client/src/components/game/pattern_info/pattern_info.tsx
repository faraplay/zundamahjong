import "./pattern_info.css";

export function PatternInfo({
  pattern,
  han,
}: {
  pattern: string;
  han: number;
}) {
  return (
    <div class="pattern">
      <span class="pattern_name">{pattern}</span>
      <span class="pattern_han">{han}</span>
    </div>
  );
}
