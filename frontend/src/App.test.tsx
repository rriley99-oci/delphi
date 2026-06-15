import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

const DATASETS = {
  items: [
    {
      id: "dataset-1",
      database_name: "warehouse",
      schema_name: "analytics",
      table_name: "orders",
      owner: "Revenue Data",
      description: "Daily order facts.",
      created_at: "2026-06-14T12:00:00Z",
      updated_at: "2026-06-15T12:00:00Z"
    },
    {
      id: "dataset-2",
      database_name: "warehouse",
      schema_name: "crm",
      table_name: "customers",
      owner: "Customer Ops",
      description: null,
      created_at: "2026-06-13T12:00:00Z",
      updated_at: "2026-06-15T11:30:00Z"
    }
  ]
};

const CONTRACTS = {
  items: [
    {
      id: "contract-1",
      dataset_id: "dataset-1",
      name: "Orders contract",
      status: "active",
      current_version_id: "version-1",
      created_at: "2026-06-14T12:00:00Z",
      updated_at: "2026-06-15T12:05:00Z",
      current_version: {
        id: "version-1",
        contract_id: "contract-1",
        version_number: 1,
        change_reason: "Initial launch rules",
        previous_version_id: null,
        created_at: "2026-06-14T12:00:00Z",
        rules: [
          {
            id: "rule-1",
            rule_type: "freshness",
            severity: "critical",
            name: "Orders freshness",
            config: { max_lag_minutes: 60 },
            created_at: "2026-06-14T12:00:00Z"
          }
        ]
      }
    }
  ]
};

const VIOLATIONS = {
  items: [
    {
      id: "violation-1",
      dataset_id: "dataset-1",
      contract_id: "contract-1",
      contract_version_id: "version-1",
      rule_id: "rule-1",
      evaluation_run_id: "eval-previous",
      evaluation_result_id: "result-1",
      rule_type: "freshness",
      severity: "critical",
      status: "open",
      message: "Orders freshness is above threshold.",
      evidence: { observed_lag_minutes: 180 },
      first_seen_at: "2026-06-15T10:00:00Z",
      last_seen_at: "2026-06-15T11:50:00Z",
      acknowledged_at: null,
      resolved_at: null,
      resolution_note: null,
      created_at: "2026-06-15T10:00:00Z",
      updated_at: "2026-06-15T11:50:00Z"
    },
    {
      id: "violation-2",
      dataset_id: "dataset-2",
      contract_id: null,
      contract_version_id: null,
      rule_id: "rule-2",
      evaluation_run_id: null,
      evaluation_result_id: null,
      rule_type: "row_count",
      severity: "medium",
      status: "resolved",
      message: "Customer row count recovered.",
      evidence: {},
      first_seen_at: "2026-06-14T10:00:00Z",
      last_seen_at: "2026-06-15T08:00:00Z",
      acknowledged_at: "2026-06-14T11:00:00Z",
      resolved_at: "2026-06-15T08:00:00Z",
      resolution_note: "Resolved after backfill.",
      created_at: "2026-06-14T10:00:00Z",
      updated_at: "2026-06-15T08:00:00Z"
    }
  ]
};

const PREVIOUS_EVALUATION = {
  id: "eval-previous",
  dataset_id: "dataset-1",
  contract_version_id: "version-1",
  status: "completed",
  summary_status: "unhealthy",
  total_rules: 1,
  passed_rules: 0,
  failed_rules: 1,
  triggered_at: "2026-06-15T11:45:00Z",
  completed_at: "2026-06-15T11:46:00Z",
  results: [
    {
      id: "result-1",
      rule_id: "rule-1",
      rule_type: "freshness",
      severity: "critical",
      status: "fail",
      message: "Orders freshness breached the SLA.",
      evidence: { observed_lag_minutes: 180 },
      created_at: "2026-06-15T11:46:00Z"
    }
  ]
};

const NEW_EVALUATION = {
  id: "eval-new",
  dataset_id: "dataset-1",
  contract_version_id: "version-1",
  status: "completed",
  summary_status: "healthy",
  total_rules: 1,
  passed_rules: 1,
  failed_rules: 0,
  triggered_at: "2026-06-15T12:10:00Z",
  completed_at: "2026-06-15T12:11:00Z",
  results: [
    {
      id: "result-new",
      rule_id: "rule-1",
      rule_type: "freshness",
      severity: "critical",
      status: "pass",
      message: "Orders freshness is within threshold.",
      evidence: { observed_lag_minutes: 12 },
      created_at: "2026-06-15T12:11:00Z"
    }
  ]
};

function installFetchMock(options?: {
  violations?: typeof VIOLATIONS;
  datasets?: typeof DATASETS;
  overviewError?: boolean;
}) {
  globalThis.fetch = vi.fn(async (input, init) => {
    const url = String(input);

    if (options?.overviewError && (url.endsWith("/datasets") || url.endsWith("/violations"))) {
      throw new TypeError("Failed to fetch");
    }

    if (url.endsWith("/datasets")) {
      return jsonResponse(options?.datasets ?? DATASETS);
    }
    if (url.endsWith("/contracts")) {
      return jsonResponse(CONTRACTS);
    }
    if (url.endsWith("/violations")) {
      return jsonResponse(options?.violations ?? VIOLATIONS);
    }
    if (url.includes("/violations?dataset_id=dataset-1")) {
      return jsonResponse({ items: VIOLATIONS.items.filter((item) => item.dataset_id === "dataset-1") });
    }
    if (url.endsWith("/datasets/dataset-1")) {
      return jsonResponse(DATASETS.items[0]);
    }
    if (url.endsWith("/evaluations/eval-previous")) {
      return jsonResponse(PREVIOUS_EVALUATION);
    }
    if (url.endsWith("/evaluations") && init?.method === "POST") {
      return jsonResponse(NEW_EVALUATION, 201);
    }

    return new Response("Not found", { status: 404 });
  }) as typeof fetch;
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json"
    }
  });
}

describe("App shell", () => {
  beforeEach(() => {
    installFetchMock();
  });

  afterEach(() => {
    window.history.replaceState(null, "", "#overview");
    vi.restoreAllMocks();
  });

  it("renders the required navigation and overview metrics", async () => {
    render(<App />);

    const navigation = screen.getByRole("navigation", { name: /primary navigation/i });
    expect(within(navigation).getByRole("link", { name: /overview/i })).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: /datasets/i })).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: /violations/i })).toBeInTheDocument();

    expect(await screen.findByText(/backend healthy/i)).toBeInTheDocument();
    expect(screen.getByText(/local/i)).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("1 open violations")).toBeInTheDocument();
    expect(screen.getByText("warehouse.analytics.orders")).toBeInTheDocument();
  });

  it("updates route content when primary navigation changes the hash", async () => {
    render(<App />);

    fireEvent.click(screen.getByRole("link", { name: /violations/i }));
    window.location.hash = "#violations";
    fireEvent(window, new HashChangeEvent("hashchange"));

    expect(await screen.findByRole("heading", { name: "Violations" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /violations/i })).toHaveAttribute("aria-current", "page");
  });

  it("renders dataset detail and triggers an evaluation", async () => {
    window.history.replaceState(null, "", "#datasets/dataset-1");

    render(<App />);

    expect(await screen.findByRole("heading", { name: "warehouse.analytics.orders" })).toBeInTheDocument();
    expect(screen.getByText("Orders contract")).toBeInTheDocument();
    expect(screen.getByText("Orders freshness breached the SLA.")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /run evaluation/i }));

    expect(await screen.findByText("Orders freshness is within threshold.")).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText("healthy")).toBeInTheDocument();
    });
  });

  it("renders violations filters and row detail", async () => {
    window.history.replaceState(null, "", "#violations");

    render(<App />);

    expect(await screen.findByRole("heading", { name: "Violations" })).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText("Status"), { target: { value: "resolved" } });

    expect(await screen.findByText("Resolved after backfill.")).toBeInTheDocument();
    expect(screen.getByText("Customer row count recovered.")).toBeInTheDocument();
  });

  it("renders the datasets route with empty state messaging", async () => {
    window.history.replaceState(null, "", "#datasets");
    installFetchMock({ datasets: { items: [] }, violations: { items: [] } });

    render(<App />);

    expect(await screen.findByRole("heading", { name: "Datasets" })).toBeInTheDocument();
    expect(screen.getByText("No datasets registered yet")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /datasets/i })).toHaveAttribute("aria-current", "page");
  });

  it("renders backend unavailable treatment", async () => {
    installFetchMock({ overviewError: true });

    render(<App />);

    expect(await screen.findByText(/backend unavailable/i)).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveTextContent("Backend unavailable");
  });
});
