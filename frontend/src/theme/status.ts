import type { BadgeTone } from "../components/primitives";

export const statusTones = {
  healthy: "success",
  unhealthy: "danger",
  open: "danger",
  acknowledged: "warning",
  resolved: "success"
} satisfies Record<string, BadgeTone>;
