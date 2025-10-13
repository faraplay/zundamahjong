export type Severity = "ERROR" | "WARNING" | "INFO";

export type ServerMessage = {
  index: number;
  severity: Severity;
  message: string;
};
