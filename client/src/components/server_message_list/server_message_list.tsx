import type { ServerMessage } from "../../types/server_message";

import "./server_message_list.css";

function MessageListItem({
  serverMessage,
  removeThisMessage,
}: {
  serverMessage: ServerMessage;
  removeThisMessage: () => void;
}) {
  const onClick = (e: Event) => {
    e.preventDefault();
    removeThisMessage();
  };
  return (
    <div
      class={`server_message_list_item ${serverMessage.severity.toLowerCase()}`}
    >
      <span>{serverMessage.message}</span>
      <button onClick={onClick}>&times;</button>
    </div>
  );
}

export function ServerMessageList({
  serverMessages,
  removeMessage,
}: {
  serverMessages: ReadonlyArray<ServerMessage>;
  removeMessage: (messageIndex: number) => void;
}) {
  return (
    <div class="server_message_list">
      {serverMessages.map((serverMessage) => (
        <MessageListItem
          key={serverMessage.index}
          serverMessage={serverMessage}
          removeThisMessage={() => removeMessage(serverMessage.index)}
        />
      ))}
    </div>
  );
}
