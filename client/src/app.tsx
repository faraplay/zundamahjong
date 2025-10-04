import { useRef, useEffect, useState } from "preact/hooks";
import { io, Socket } from "socket.io-client";

import type { ErrorMessage } from "./types/error_message";
import type { Player } from "./types/player";
import type { DetailedRoom, BasicRoom } from "./types/room";
import { RoundStatus, type AllInfo } from "./types/game";
import type { EmitFunc } from "./types/emit_func";

import { Emitter } from "./components/emitter/emitter";

import { ErrorList } from "./components/error_list/error_list";
import { NameForm } from "./components/name_form/name_form";
import { JoinRoomForm } from "./components/join_room_form/join_room_form";
import { CreateRoomForm } from "./components/create_room_form/create_room_form";
import { RoomInfo } from "./components/room/room_info/room_info";
import { AvatarDisplay } from "./components/room/avatar_selector/avatar_selector";
import { GameOptionsForm } from "./components/room/game_options_form/game_options_form";

import { GameScreen } from "./components/game/game_screen/game_screen";

import "./fonts.css";
import "./app.css";

export function App() {
  const [errors, setErrors] = useState<{
    currentIndex: number;
    list: ErrorMessage[];
  }>({ currentIndex: 0, list: [] });

  const [myPlayer, setMyPlayer] = useState<Player>();
  const [rooms, setRooms] = useState<BasicRoom[]>([]);
  const [myRoom, setMyRoom] = useState<DetailedRoom>();

  const [info, setInfo] = useState<AllInfo>();
  const [actionSubmitted, setActionSubmitted] = useState<boolean>(false);
  const [seeResults, setSeeResults] = useState(false);

  const socket = useRef<Socket>();
  const emit: EmitFunc = (event, ...args) =>
    socket.current?.emit(event, ...args);

  useEffect(() => {
    socket.current = io();

    socket.current.on("message", (message: string) => {
      console.log(message);
      setErrors((errors) => {
        return {
          currentIndex: errors.currentIndex + 1,
          list: errors.list.concat([{ index: errors.currentIndex, message }]),
        };
      });
    });
    socket.current.on("player_info", (player: Player) => {
      setMyPlayer(player);
    });
    socket.current.on("rooms_info", (rooms: Array<BasicRoom>) => {
      setRooms(rooms);
    });
    socket.current.on("room_info", (room: DetailedRoom | undefined) => {
      setMyRoom(room);
    });
    socket.current.on("info", (info: AllInfo | undefined) => {
      setInfo(info);
      setActionSubmitted(false);
      if (info && info.round_info.status != RoundStatus.END) {
        setSeeResults(false);
      }
    });

    return () => {
      socket.current?.disconnect();
    };
  }, []);

  const screen = getScreen(
    myPlayer,
    rooms,
    myRoom,
    info,
    actionSubmitted,
    setActionSubmitted,
    seeResults,
    setSeeResults,
  );
  return (
    <Emitter.Provider value={emit}>
      {screen}
      <ErrorList
        errors={errors.list}
        removeError={(index) => {
          setErrors({
            currentIndex: errors.currentIndex,
            list: errors.list.filter((error) => error.index != index),
          });
        }}
      />
    </Emitter.Provider>
  );
}

function getScreen(
  myPlayer: Player | undefined,
  rooms: BasicRoom[],
  myRoom: DetailedRoom | undefined,
  info: AllInfo | undefined,
  actionSubmitted: boolean,
  setActionSubmitted: (value: boolean) => void,
  seeResults: boolean,
  setSeeResults: (value: boolean) => void,
) {
  if (!myPlayer) {
    return (
      <div id="name_screen" class="screen">
        <NameForm />
      </div>
    );
  }
  if (!myRoom) {
    return (
      <div id="lobby_screen" class="screen">
        <JoinRoomForm rooms={rooms} />
        <CreateRoomForm />
      </div>
    );
  }
  if (!info) {
    return (
      <div id="room_screen" class="screen">
        <RoomInfo room={myRoom} />
        <AvatarDisplay
          myPlayer={myPlayer}
          players={myRoom.joined_players}
          avatars={myRoom.avatars}
        />
        <GameOptionsForm
          gameOptions={myRoom.game_options}
          isEditable={myRoom.joined_players[0].id == myPlayer.id}
          can_start={myRoom.joined_players.length == myRoom.player_count}
        />
      </div>
    );
  }
  return (
    <GameScreen
      players={myRoom.joined_players}
      playerAvatarIds={myRoom.avatars}
      info={info}
      actionSubmitted={actionSubmitted}
      setActionSubmitted={() => setActionSubmitted(true)}
      seeResults={seeResults}
      goToResults={() => setSeeResults(true)}
    />
  );
}
