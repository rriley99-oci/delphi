import { appConfig } from "./config";

export type DatasetRead = {
  id: string;
  database_name: string;
  schema_name: string;
  table_name: string;
  owner: string | null;
  description: string | null;
  created_at: string;
  updated_at: string;
};

export type ContractRuleRead = {
  id: string;
  rule_type: string;
  severity: string;
  name: string | null;
  config: Record<string, unknown>;
  created_at: string;
};

export type ContractVersionRead = {
  id: string;
  contract_id: string;
  version_number: number;
  change_reason: string;
  previous_version_id: string | null;
  created_at: string;
  rules: ContractRuleRead[];
};

export type ContractRead = {
  id: string;
  dataset_id: string;
  name: string;
  status: string;
  current_version_id: string | null;
  created_at: string;
  updated_at: string;
  current_version: ContractVersionRead | null;
};

export type EvaluationResultRead = {
  id: string;
  rule_id: string;
  rule_type: string;
  severity: string;
  status: "pass" | "fail" | "error";
  message: string;
  evidence: Record<string, unknown>;
  created_at: string;
};

export type EvaluationRunRead = {
  id: string;
  dataset_id: string;
  contract_version_id: string;
  status: "queued" | "running" | "completed" | "failed";
  summary_status: "healthy" | "unhealthy" | "unknown";
  total_rules: number;
  passed_rules: number;
  failed_rules: number;
  triggered_at: string;
  completed_at: string | null;
  results: EvaluationResultRead[];
};

export type ViolationRead = {
  id: string;
  dataset_id: string;
  contract_id: string | null;
  contract_version_id: string | null;
  rule_id: string;
  evaluation_run_id: string | null;
  evaluation_result_id: string | null;
  rule_type: string;
  severity: "low" | "medium" | "high" | "critical";
  status: "open" | "acknowledged" | "resolved";
  message: string;
  evidence: Record<string, unknown>;
  first_seen_at: string;
  last_seen_at: string;
  acknowledged_at: string | null;
  resolved_at: string | null;
  resolution_note: string | null;
  created_at: string;
  updated_at: string;
};

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${appConfig.backendBaseUrl}${path}`, {
      headers: {
        "Content-Type": "application/json"
      },
      ...init
    });
  } catch {
    throw new ApiError(0, "Backend unavailable");
  }

  if (!response.ok) {
    let detail = response.statusText || "Request failed";

    try {
      const body = (await response.json()) as { detail?: string };
      detail = body.detail ?? detail;
    } catch {
      // Keep the HTTP status text when the response is not JSON.
    }

    throw new ApiError(response.status, detail);
  }

  return (await response.json()) as T;
}

export function fetchDatasets() {
  return request<{ items: DatasetRead[] }>("/datasets");
}

export function fetchDataset(datasetId: string) {
  return request<DatasetRead>(`/datasets/${datasetId}`);
}

export function fetchContracts() {
  return request<{ items: ContractRead[] }>("/contracts");
}

export function fetchViolations(params?: { status?: string; datasetId?: string }) {
  const search = new URLSearchParams();
  if (params?.status) {
    search.set("status", params.status);
  }
  if (params?.datasetId) {
    search.set("dataset_id", params.datasetId);
  }

  const suffix = search.size > 0 ? `?${search.toString()}` : "";
  return request<{ items: ViolationRead[] }>(`/violations${suffix}`);
}

export function fetchEvaluation(evaluationId: string) {
  return request<EvaluationRunRead>(`/evaluations/${evaluationId}`);
}

export function triggerEvaluation(datasetId: string) {
  return request<EvaluationRunRead>("/evaluations", {
    method: "POST",
    body: JSON.stringify({ dataset_id: datasetId })
  });
}

export function isBackendUnavailableError(error: unknown) {
  return error instanceof ApiError && error.status === 0;
}
