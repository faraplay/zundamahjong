import { useRef, useEffect, type MutableRef, useState } from "preact/hooks";
import { io, Socket } from "socket.io-client";

import type { ErrorMessage } from "./types/error_message";
import type { Player } from "./types/player";
import type { Room } from "./types/room";
import { RoundStatus, type AllInfo } from "./types/game";
import type { EmitFunc } from "./types/emit_func";

import { Emitter } from "./components/emitter/emitter";

import { ErrorList } from "./components/error_list/error_list";
import { NameForm } from "./components/name_form/name_form";
import { JoinRoomForm } from "./components/join_room_form/join_room_form";
import { CreateRoomForm } from "./components/create_room_form/create_room_form";
import { RoomInfo } from "./components/room_info/room_info";
import { GameOptionsForm } from "./components/game_options_form/game_options_form";

import { GameScreen } from "./components/game/game_screen/game_screen";

import "./fonts.css";
import "./app.css";
import { AvatarDisplay } from "./components/avatar_selector/avatar_selector";
import { type AvatarIdDict } from "./types/avatars";

export function App() {
  const [errors, setErrors] = useState<{
    currentIndex: number;
    list: ErrorMessage[];
  }>({ currentIndex: 0, list: [] });

  const [myPlayer, setMyPlayer] = useState<Player>();
  const [rooms, setRooms] = useState<Array<Room>>([]);
  const [myRoom, setMyRoom] = useState<Room>();
  const [avatars, setAvatars] = useState<AvatarIdDict>({});

  const [info, setInfo] = useState<AllInfo>();
  const [actionSubmitted, setActionSubmitted] = useState<boolean>(false);
  const [seeResults, setSeeResults] = useState(false);

  const socket = useRef() as MutableRef<Socket>;
  const emit: EmitFunc = (event, ...args) =>
    socket.current.emit(event, ...args);

  useEffect(() => {
    socket.current = io();

    socket.current.on("message", (message: string) => {
      console.log(message);
      setErrors((errors) => {
        errors.list.push({ index: errors.currentIndex, message });
        errors.currentIndex++;
        return errors;
      });
    });
    socket.current.on("player_info", (player: Player) => {
      setMyPlayer(player);
    });
    socket.current.on("rooms_info", (rooms: Array<Room>) => {
      setRooms(rooms);
    });
    socket.current.on("room_info", (room: Room) => {
      setMyRoom(room);
    });
    socket.current.on("room_avatars", (avatars: AvatarIdDict) => {
      setAvatars(avatars);
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

  const screen = getScreen(
    myPlayer,
    myRoom,
    rooms,
    avatars,
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
  myRoom: Room | undefined,
  rooms: Room[],
  avatars: AvatarIdDict,
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
          avatars={avatars}
        />
        {myRoom && myRoom.joined_players[0].id == myPlayer.id ? (
          <GameOptionsForm
            player_count={myRoom.player_count}
            can_start={myRoom.joined_players.length == myRoom.player_count}
          />
        ) : (
          <></>
        )}
      </div>
    );
  }
  return (
    <GameScreen
      info={info}
      actionSubmitted={actionSubmitted}
      setActionSubmitted={() => setActionSubmitted(true)}
      seeResults={seeResults}
      goToResults={() => setSeeResults(true)}
    />
  );
}
