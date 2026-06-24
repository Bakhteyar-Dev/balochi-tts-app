export type ScriptKey = "latin" | "arabic";

export interface ScriptMeta {
  key: ScriptKey;
  label: string;
  buttonLabel: string;
  direction: "ltr" | "rtl";
  align: "left" | "right";
  fontClass: string;
  placeholder: string;
}

export const TRANSLATION_SCRIPTS: Record<ScriptKey, ScriptMeta> = {
  latin: {
    key: "latin",
    label: "Latin",
    buttonLabel: "Balochi-Latin",
    direction: "ltr",
    align: "left",
    fontClass: "font-sans",
    placeholder: "Type English text here... (e.g. The weather is nice today.)",
  },
  arabic: {
    key: "arabic",
    label: "Arabic",
    buttonLabel: "Balochi-Arabic",
    direction: "ltr",
    align: "left",
    fontClass: "font-sans",
    placeholder: "Type English text here... (e.g. The weather is nice today.)",
  },
};

export const TTS_SCRIPTS: Record<ScriptKey, ScriptMeta> = {
  latin: {
    key: "latin",
    label: "Latin",
    buttonLabel: "Balochi-Latin",
    direction: "ltr",
    align: "left",
    fontClass: "font-sans",
    placeholder: "Type Latin-script Balochi text here... (e.g. Man wati zobáná gapp janán)",
  },
  arabic: {
    key: "arabic",
    label: "Arabic",
    buttonLabel: "Balochi-Arabic",
    direction: "rtl",
    align: "right",
    fontClass: "font-naskh",
    placeholder: "Type Arabic-script Balochi text here... (e.g. من ءَ بلوچی زبان دوست بیت)",
  },
};
