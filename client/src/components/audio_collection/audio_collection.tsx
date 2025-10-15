import discardSound from "../../assets/audio/discard.mp3";
import { voiceCollections, voiceLines } from "../../types/audio";

export function CommonAudioCollection() {
  return (
    <>
      <audio class="discard" src={discardSound} preload="auto" />
    </>
  );
}

export function VoiceCollection({ avatarId }: { avatarId: number }) {
  const voiceCollection = voiceCollections[avatarId] || voiceCollections[0];
  return (
    <>
      {voiceLines.map((voiceLine) => (
        <audio
          key={voiceLine}
          class={`avatar_${avatarId} ${voiceLine}`}
          src={voiceCollection[voiceLine]}
          preload="auto"
        />
      ))}
    </>
  );
}
