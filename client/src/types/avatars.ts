import zundamonURL from "../assets/avatars/zundamon.png";
import zundamonFaceURL from "../assets/avatars/zundamon_face.png";
import metanURL from "../assets/avatars/metan.png";
import metanFaceURL from "../assets/avatars/metan_face.png";
import tsumugiURL from "../assets/avatars/tsumugi.png";
import tsumugiFaceURL from "../assets/avatars/tsumugi_face.png";
import kiritanURL from "../assets/avatars/kiritan.png";
import kiritanFaceURL from "../assets/avatars/kiritan_face.png";

export type AvatarIdDict = { [playerId: string]: number };

export const avatars = [
  { name: "Zundamon", imageURL: zundamonURL, faceURL: zundamonFaceURL },
  { name: "Metan", imageURL: metanURL, faceURL: metanFaceURL },
  { name: "Tsumugi", imageURL: tsumugiURL, faceURL: tsumugiFaceURL },
  { name: "Kiritan", imageURL: kiritanURL, faceURL: kiritanFaceURL },
] as const;
