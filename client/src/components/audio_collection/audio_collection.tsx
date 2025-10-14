import discardSound from "../../assets/audio/discard.mp3";

export function AudioCollection() {
  return (
    <>
      <audio class="audio discard" src={discardSound} preload="auto" />
    </>
  );
}
