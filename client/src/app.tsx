import { useRef, useEffect, type MutableRef, useState } from "preact/hooks";
import { io, Socket } from "socket.io-client";

import type { Player } from "./types/player";
import type { Room } from "./types/room";

import { NameForm } from "./components/name_form/name_form";
import { JoinRoomForm } from "./components/join_room_form/join_room_form";
import { CreateRoomForm } from "./components/create_room_form/create_room_form";

import "./app.css";

export function App() {
  const socket = useRef() as MutableRef<Socket>;
  const [myPlayer, setMyPlayer] = useState<Player | undefined>();
  const [rooms, setRooms] = useState<Array<Room>>([]);
  useEffect(() => {
    socket.current = io();

    socket.current.on("player_info", (player: Player) => {
      setMyPlayer(player);
    });
    socket.current.on("rooms_info", (rooms: Array<Room>) => {
      setRooms(rooms);
    });
    return () => {
      socket.current.disconnect();
    };
  }, []);

  if (!myPlayer) {
    return (
      <div id="name_screen" class="screen">
        <NameForm
          emit={(event, ...args) => socket.current.emit(event, ...args)}
        />
      </div>
    );
  }
  return (
    <div id="lobby_screen" class="screen">
      <JoinRoomForm rooms={rooms} />
      <CreateRoomForm />
    </div>
  );
}
