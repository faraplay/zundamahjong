import { useRef, useEffect, useState } from "preact/hooks";
import { io, Socket } from "socket.io-client";

import type { ServerMessage, Severity } from "./types/server_message";
import type { Player } from "./types/player";
import type { DetailedRoom, BasicRoom } from "./types/room";
import { RoundStatus, type AllServerInfo } from "./types/game";
import { processInfo, type AllInfo } from "./process_info";
import type { EmitFunc } from "./types/emit_func";

import { Emitter } from "./components/emitter/emitter";

import { ServerMessageList } from "./components/server_message_list/server_message_list";
import { NameForm } from "./components/name_form/name_form";
import { UserWelcome } from "./components/user_welcome/user_welcome";
import { UserSettingsForm } from "./components/user_settings_form/user_settings_form";
import { JoinRoomForm } from "./components/join_room_form/join_room_form";
import { CreateRoomForm } from "./components/create_room_form/create_room_form";
import { RoomInfo } from "./components/room/room_info/room_info";
import { AvatarDisplay } from "./components/room/avatar_selector/avatar_selector";
import { GameOptionsForm } from "./components/room/game_options_form/game_options_form";

import { GameScreen } from "./components/game/game_screen/game_screen";

import "./fonts.css";
import "./app.css";
import { GameOptionsContext } from "./components/game_options_context/game_options_context";
import { AudioCollection } from "./components/audio_collection/audio_collection";

export function App() {
  const [serverMessages, setServerMessages] = useState<{
    currentIndex: number;
    list: ServerMessage[];
  }>({ currentIndex: 0, list: [] });

  const [myPlayer, setMyPlayer] = useState<Player>();
  const [rooms, setRooms] = useState<BasicRoom[]>([]);
  const [myRoom, setMyRoom] = useState<DetailedRoom>();

  const [info, setInfo] = useState<AllInfo>();
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const [actionSubmitted, setActionSubmitted] = useState<boolean>(false);
  const [seeResults, setSeeResults] = useState<boolean>(false);

  const socket = useRef<Socket>();
  const emit: EmitFunc = (event, ...args) =>
    socket.current?.emit(event, ...args);

  useEffect(() => {
    socket.current = io();

    socket.current.on(
      "server_message",
      ({ message, severity }: { message: string; severity: Severity }) => {
        console.log(message);
        setServerMessages((serverMessages) => {
          return {
            currentIndex: serverMessages.currentIndex + 1,
            list: serverMessages.list.concat([
              { index: serverMessages.currentIndex, severity, message },
            ]),
          };
        });
      },
    );
    socket.current.on("player_info", (player: Player) => {
      setMyPlayer(player);
    });
    socket.current.on("unset_name", () => {
      setMyPlayer(undefined);
    });
    socket.current.on("rooms_info", (rooms: Array<BasicRoom>) => {
      setRooms(rooms);
    });
    socket.current.on("room_info", (room: DetailedRoom | undefined) => {
      setMyRoom(room);
    });
    socket.current.on("info", (info: AllServerInfo | undefined) => {
      if (info) {
        setInfo(processInfo(info));
      } else {
        setInfo(undefined);
      }
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
    showSettings,
    setShowSettings,
  );
  return (
    <Emitter.Provider value={emit}>
      <AudioCollection />
      {screen}
      <ServerMessageList
        serverMessages={serverMessages.list}
        removeMessage={(index) => {
          setServerMessages({
            currentIndex: serverMessages.currentIndex,
            list: serverMessages.list.filter((msg) => msg.index != index),
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
  showSettings: boolean,
  setShowSettings: (value: boolean) => void,
) {
  if (!myPlayer) {
    return (
      <div id="name_screen" class="screen">
        <NameForm />
      </div>
    );
  }
  if (showSettings) {
    return (
      <div id="settings_screen" class="screen">
        <UserSettingsForm goToLobby={() => setShowSettings(false)} />
      </div>
    );
  }
  if (!myRoom) {
    return (
      <div id="lobby_screen" class="screen">
        <UserWelcome
          myPlayer={myPlayer}
          goToSettings={() => setShowSettings(true)}
        />
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
    <GameOptionsContext.Provider value={myRoom.game_options}>
      <GameScreen
        playerAvatarIds={myRoom.avatars}
        info={info}
        actionSubmitted={actionSubmitted}
        setActionSubmitted={() => setActionSubmitted(true)}
        seeResults={seeResults}
        goToResults={() => setSeeResults(true)}
      />
    </GameOptionsContext.Provider>
  );
}
