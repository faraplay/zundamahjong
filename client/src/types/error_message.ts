export type Severity = "ERROR" | "WARNING" | "INFO";

export type ErrorMessage = {
  index: number;
  severity: Severity;
  message: string;
};
