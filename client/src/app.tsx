import { useRef, useEffect, type MutableRef, useState } from "preact/hooks";
import { io, Socket } from "socket.io-client";

import type { Player } from "./types/player";
import type { Room } from "./types/room";
import { RoundStatus, type AllInfo } from "./types/game";
import type { EmitFunc } from "./types/emit_func";

import { Emitter } from "./components/emitter/emitter";
import { NameForm } from "./components/name_form/name_form";
import { JoinRoomForm } from "./components/join_room_form/join_room_form";
import { CreateRoomForm } from "./components/create_room_form/create_room_form";
import { RoomInfo } from "./components/room_info/room_info";
import { GameOptionsForm } from "./components/game_options_form/game_options_form";

import { GameScreen } from "./components/game/game_screen/game_screen";

import "./fonts.css";
import "./app.css";

export function App() {
  const socket = useRef() as MutableRef<Socket>;
  const emit: EmitFunc = (event, ...args) =>
    socket.current.emit(event, ...args);

  const [myPlayer, setMyPlayer] = useState<Player>();
  const [rooms, setRooms] = useState<Array<Room>>([]);
  const [myRoom, setMyRoom] = useState<Room>();
  const [info, setInfo] = useState<AllInfo>();
  const [actionSubmitted, setActionSubmitted] = useState<boolean>(false);
  const [seeResults, setSeeResults] = useState(false);

  useEffect(() => {
    socket.current = io();

    socket.current.on("player_info", (player: Player) => {
      setMyPlayer(player);
    });
    socket.current.on("rooms_info", (rooms: Array<Room>) => {
      setRooms(rooms);
    });
    socket.current.on("room_info", (room: Room) => {
      setMyRoom(room);
    });
    socket.current.on("info", (info: AllInfo) => {
      setInfo(info);
      setActionSubmitted(false);
      if (info.round_info.status != RoundStatus.END) {
        setSeeResults(false);
      }
    });

    return () => {
      socket.current.disconnect();
    };
  }, []);

  if (!myPlayer) {
    return (
      <Emitter.Provider value={emit}>
        <div id="name_screen" class="screen">
          <NameForm />
        </div>
      </Emitter.Provider>
    );
  }
  if (!myRoom) {
    return (
      <Emitter.Provider value={emit}>
        <div id="lobby_screen" class="screen">
          <JoinRoomForm rooms={rooms} />
          <CreateRoomForm />
        </div>
      </Emitter.Provider>
    );
  }
  if (!info) {
    return (
      <Emitter.Provider value={emit}>
        <div id="room_screen" class="screen">
          <RoomInfo room={myRoom} />
          {myRoom && myRoom.joined_players[0].id == myPlayer.id ? (
            <GameOptionsForm
              player_count={myRoom.player_count}
              can_start={myRoom.joined_players.length == myRoom.player_count}
            />
          ) : (
            <></>
          )}
        </div>
      </Emitter.Provider>
    );
  }
  return (
    <Emitter.Provider value={emit}>
      <GameScreen
        info={info}
        actionSubmitted={actionSubmitted}
        setActionSubmitted={() => setActionSubmitted(true)}
        seeResults={seeResults}
        goToResults={() => setSeeResults(true)}
      />
    </Emitter.Provider>
  );
}
