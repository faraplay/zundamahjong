import "./yaku_info.css";

export function YakuInfo({ yaku, han }: { yaku: string; han: number }) {
  return (
    <div class="yaku">
      <span class="yaku_name">{yaku}</span>
      <span class="yaku_han">{han}</span>
    </div>
  );
}
