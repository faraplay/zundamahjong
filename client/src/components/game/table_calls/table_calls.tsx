import {
  CallType,
  type AddKanCall,
  type Call,
  type ClosedKanCall,
  type OpenCall,
  type OpenKanCall,
} from "../../../types/call";

import { Tile3D, Tile3DList } from "../tile_3d/tile_3d";

import "./table_calls.css";

function TableNotClosedKanCall({
  call,
  player_index,
}: {
  call: OpenCall | OpenKanCall | AddKanCall;
  player_index: number;
}) {
  const tiles_list = call.other_tiles.map((tile) => (
    <Tile3D key={tile} tile={tile} />
  ));
  const relative_seat = (call.called_player_index - player_index + 4) % 4;
  const insert_index =
    call.call_type == CallType.OPEN_KAN && relative_seat == 1
      ? 4
      : 3 - relative_seat;
  const called_tiles =
    call.call_type == CallType.ADD_KAN ? (
      <>
        <Tile3D tile={call.called_tile} />
        <Tile3D tile={call.added_tile} />
      </>
    ) : (
      <Tile3D tile={call.called_tile} />
    );
  tiles_list.splice(
    insert_index,
    0,
    <div class="called_tile_div">{called_tiles}</div>,
  );
  return <span class={`call call_type_${call.call_type}`}>{tiles_list}</span>;
}

function TableClosedKanCall({ call }: { call: ClosedKanCall }) {
  return (
    <span class={`call call_type_${call.call_type}`}>
      <Tile3DList tiles={call.tiles} />
    </span>
  );
}

function TableCall({
  call,
  player_index,
}: {
  call: Call;
  player_index: number;
}) {
  if (call.call_type == CallType.CLOSED_KAN) {
    return <TableClosedKanCall call={call} />;
  }
  return <TableNotClosedKanCall call={call} player_index={player_index} />;
}

export function TableCalls({
  player_index,
  calls,
}: {
  player_index: number;
  calls: ReadonlyArray<Call>;
}) {
  return (
    <div class={`player_calls player_${player_index}`}>
      {calls.map((call) => (
        <TableCall key={call} call={call} player_index={player_index} />
      ))}
    </div>
  );
}
