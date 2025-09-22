import { useRef, useEffect, type MutableRef } from "preact/hooks";
import { io, Socket } from "socket.io-client";
import { NameForm } from "./components/name_form";
import "./app.css";

export function App() {
  const socket = useRef() as MutableRef<Socket>;
  useEffect(() => {
    socket.current = io();
    return () => {
      socket.current.disconnect();
    };
  }, []);
  return (
    <>
      <div id="name_screen" class="screen">
        <NameForm
          emit={(event, ...args) => socket.current.emit(event, ...args)}
        />
      </div>
    </>
  );
}
