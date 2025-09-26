import "./player_icon.css";

function PlayerIcon({
  player_index,
  player_name,
}: {
  player_index: number;
  player_name: string;
}) {
  return <div class={`player_name player_${player_index}`}>{player_name}</div>;
}

export function PlayerIcons({ player_names }: { player_names: string[] }) {
  return (
    <div id="player_names">
      {player_names.map((name, index) => (
        <PlayerIcon key={index} player_index={index} player_name={name} />
      ))}
    </div>
  );
}
