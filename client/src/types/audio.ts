import zundamonChii from "../assets/audio/zundamon/zundamon_chii.mp3";
import zundamonPon from "../assets/audio/zundamon/zundamon_pon.mp3";
import zundamonKan from "../assets/audio/zundamon/zundamon_kan.mp3";
import zundamonFa from "../assets/audio/zundamon/zundamon_fa.mp3";
import zundamonRiichi from "../assets/audio/zundamon/zundamon_riichi.mp3";
import zundamonRon from "../assets/audio/zundamon/zundamon_ron.mp3";
import zundamonTsumo from "../assets/audio/zundamon/zundamon_tsumo.mp3";
import metanChii from "../assets/audio/metan/metan_chii.mp3";
import metanPon from "../assets/audio/metan/metan_pon.mp3";
import metanKan from "../assets/audio/metan/metan_kan.mp3";
import metanFa from "../assets/audio/metan/metan_fa.mp3";
import metanRiichi from "../assets/audio/metan/metan_riichi.mp3";
import metanRon from "../assets/audio/metan/metan_ron.mp3";
import metanTsumo from "../assets/audio/metan/metan_tsumo.mp3";
import tsumugiChii from "../assets/audio/tsumugi/tsumugi_chii.mp3";
import tsumugiPon from "../assets/audio/tsumugi/tsumugi_pon.mp3";
import tsumugiKan from "../assets/audio/tsumugi/tsumugi_kan.mp3";
import tsumugiFa from "../assets/audio/tsumugi/tsumugi_fa.mp3";
import tsumugiRiichi from "../assets/audio/tsumugi/tsumugi_riichi.mp3";
import tsumugiRon from "../assets/audio/tsumugi/tsumugi_ron.mp3";
import tsumugiTsumo from "../assets/audio/tsumugi/tsumugi_tsumo.mp3";
import kiritanChii from "../assets/audio/kiritan/kiritan_chii.mp3";
import kiritanPon from "../assets/audio/kiritan/kiritan_pon.mp3";
import kiritanKan from "../assets/audio/kiritan/kiritan_kan.mp3";
import kiritanFa from "../assets/audio/kiritan/kiritan_fa.mp3";
import kiritanRiichi from "../assets/audio/kiritan/kiritan_riichi.mp3";
import kiritanRon from "../assets/audio/kiritan/kiritan_ron.mp3";
import kiritanTsumo from "../assets/audio/kiritan/kiritan_tsumo.mp3";

export type VoiceCollectionUrls = {
  chii: string;
  pon: string;
  kan: string;
  fa: string;
  riichi: string;
  ron: string;
  tsumo: string;
};

export const voiceLines = [
  "chii",
  "pon",
  "kan",
  "fa",
  "riichi",
  "ron",
  "tsumo",
] as const;

export const voiceCollections = [
  {
    chii: zundamonChii,
    pon: zundamonPon,
    kan: zundamonKan,
    fa: zundamonFa,
    riichi: zundamonRiichi,
    ron: zundamonRon,
    tsumo: zundamonTsumo,
  },
  {
    chii: metanChii,
    pon: metanPon,
    kan: metanKan,
    fa: metanFa,
    riichi: metanRiichi,
    ron: metanRon,
    tsumo: metanTsumo,
  },
  {
    chii: tsumugiChii,
    pon: tsumugiPon,
    kan: tsumugiKan,
    fa: tsumugiFa,
    riichi: tsumugiRiichi,
    ron: tsumugiRon,
    tsumo: tsumugiTsumo,
  },
  {
    chii: kiritanChii,
    pon: kiritanPon,
    kan: kiritanKan,
    fa: kiritanFa,
    riichi: kiritanRiichi,
    ron: kiritanRon,
    tsumo: kiritanTsumo,
  },
] as const;
