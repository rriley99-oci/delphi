import type { BadgeTone } from "../components/primitives";

export const statusTones = {
  healthy: "success",
  unhealthy: "danger",
  unknown: "neutral",
  open: "danger",
  acknowledged: "warning",
  resolved: "success",
  completed: "success",
  failed: "danger",
  queued: "info",
  running: "warning",
  pass: "success",
  fail: "danger",
  error: "warning"
} satisfies Record<string, BadgeTone>;
