import { startTransition, useEffect, useEffectEvent, useState, useSyncExternalStore } from "react";
import {
  AlertCircle,
  CheckCircle2,
  Database,
  FileClock,
  Gauge,
  LayoutDashboard,
  Play,
  ShieldAlert,
  Sparkles,
  Waypoints
} from "lucide-react";
import {
  Badge,
  Button,
  Card,
  DataTable,
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  type BadgeTone,
  type Column
} from "./components/primitives";
import { AppShell, type NavItem } from "./components/AppShell";
import {
  ApiError,
  type ContractRead,
  type DatasetRead,
  type EvaluationRunRead,
  type ViolationRead,
  fetchContracts,
  fetchDataset,
  fetchDatasets,
  fetchEvaluation,
  fetchViolations,
  isBackendUnavailableError,
  triggerEvaluation
} from "./api";
import { appConfig } from "./config";
import { statusTones } from "./theme/status";

type AsyncState<T> =
  | { status: "loading" }
  | { status: "error"; error: string; backendUnavailable: boolean }
  | { status: "ready"; data: T };

type OverviewData = {
  datasets: DatasetRead[];
  violations: ViolationRead[];
};

type DatasetDetailData = {
  dataset: DatasetRead;
  contract: ContractRead | null;
  violations: ViolationRead[];
  latestEvaluation: EvaluationRunRead | null;
};

const navItems: NavItem[] = [
  { label: "Overview", href: "#overview", icon: LayoutDashboard },
  { label: "Datasets", href: "#datasets", icon: Database },
  { label: "Violations", href: "#violations", icon: ShieldAlert }
];

type RouteId = "overview" | "datasets" | "dataset-detail" | "violations";

type Route = {
  id: RouteId;
  activeHref: string;
  datasetId: string | null;
};

function resolveRoute(hash: string): Route {
  if (hash.startsWith("#datasets/")) {
    return {
      id: "dataset-detail",
      activeHref: "#datasets",
      datasetId: decodeURIComponent(hash.replace("#datasets/", ""))
    };
  }

  if (hash === "#datasets") {
    return { id: "datasets", activeHref: "#datasets", datasetId: null };
  }

  if (hash === "#violations") {
    return { id: "violations", activeHref: "#violations", datasetId: null };
  }

  return { id: "overview", activeHref: "#overview", datasetId: null };
}

function getCurrentHash() {
  return window.location.hash || "#overview";
}

function subscribeToHashChange(onStoreChange: () => void) {
  window.addEventListener("hashchange", onStoreChange);
  return () => window.removeEventListener("hashchange", onStoreChange);
}

function useCurrentRoute() {
  const hash = useSyncExternalStore(subscribeToHashChange, getCurrentHash, () => "#overview");
  return resolveRoute(hash);
}

type DatasetRow = {
  id: string;
  datasetId: string;
  identity: string;
  owner: string;
  health: "healthy" | "unhealthy";
  violations: number;
  updatedLabel: string;
  createdLabel: string;
};

type ViolationRow = {
  id: string;
  datasetId: string;
  datasetIdentity: string;
  severity: ViolationRead["severity"];
  status: ViolationRead["status"];
  ruleType: string;
  message: string;
  firstSeenLabel: string;
  lastSeenLabel: string;
  raw: ViolationRead;
};

const datasetColumns: Column<DatasetRow>[] = [
  {
    key: "identity",
    header: "Dataset",
    render: (row) => (
      <div className="cell-stack">
        <span className="mono">{row.identity}</span>
        <span className="table-subtext">Open detail view</span>
      </div>
    )
  },
  { key: "owner", header: "Owner", render: (row) => row.owner },
  {
    key: "health",
    header: "Health",
    render: (row) => <Badge tone={statusTones[row.health]}>{row.health}</Badge>
  },
  {
    key: "violations",
    header: "Open",
    align: "right",
    render: (row) => row.violations
  },
  {
    key: "updated",
    header: "Lifecycle",
    render: (row) => (
      <div className="cell-stack">
        <span>{row.updatedLabel}</span>
        <span className="table-subtext">{row.createdLabel}</span>
      </div>
    )
  }
];

const violationColumns: Column<ViolationRow>[] = [
  {
    key: "dataset",
    header: "Dataset",
    render: (row) => (
      <div className="cell-stack">
        <span className="mono">{row.datasetIdentity}</span>
        <span className="table-subtext">{row.message}</span>
      </div>
    )
  },
  {
    key: "severity",
    header: "Severity",
    render: (row) => <Badge tone={severityTone(row.severity)}>{row.severity}</Badge>
  },
  {
    key: "status",
    header: "Status",
    render: (row) => <Badge tone={statusTones[row.status]}>{row.status}</Badge>
  },
  { key: "rule", header: "Rule", render: (row) => row.ruleType },
  { key: "firstSeen", header: "First seen", render: (row) => row.firstSeenLabel },
  { key: "lastSeen", header: "Last seen", render: (row) => row.lastSeenLabel }
];

function severityTone(severity: string): BadgeTone {
  if (severity === "critical") {
    return "danger";
  }
  if (severity === "high" || severity === "medium" || severity === "warning") {
    return "warning";
  }
  return "neutral";
}

export function App() {
  const route = useCurrentRoute();
  const overview = useOverviewData();

  return (
    <AppShell
      navItems={navItems}
      activeHref={route.activeHref}
      environment={appConfig.environment}
      health={getHealthIndicator(overview.state)}
    >
      <RouteContent route={route} overview={overview} />
    </AppShell>
  );
}

function getHealthIndicator(overview: AsyncState<OverviewData>) {
  if (overview.status === "loading") {
    return {
      label: "Checking backend",
      tone: "info" as const,
      icon: Gauge
    };
  }

  if (overview.status === "error") {
    return {
      label: overview.backendUnavailable ? "Backend unavailable" : "Backend error",
      tone: "danger" as const,
      icon: AlertCircle
    };
  }

  return {
    label: "Backend healthy",
    tone: "success" as const,
    icon: CheckCircle2
  };
}

function useOverviewData() {
  const [state, setState] = useState<AsyncState<OverviewData>>({ status: "loading" });

  const loadOverview = useEffectEvent(async () => {
    setState({ status: "loading" });

    try {
      const [datasetsResponse, violationsResponse] = await Promise.all([
        fetchDatasets(),
        fetchViolations()
      ]);

      setState({
        status: "ready",
        data: {
          datasets: datasetsResponse.items,
          violations: violationsResponse.items
        }
      });
    } catch (error) {
      setState({
        status: "error",
        error: getErrorMessage(error),
        backendUnavailable: isBackendUnavailableError(error)
      });
    }
  });

  useEffect(() => {
    void loadOverview();
  }, [loadOverview]);

  return { state, reload: () => void loadOverview() };
}

function useDatasetDetail(datasetId: string | null) {
  const [state, setState] = useState<AsyncState<DatasetDetailData>>({ status: "loading" });
  const [latestTriggeredEvaluation, setLatestTriggeredEvaluation] = useState<EvaluationRunRead | null>(null);

  useEffect(() => {
    setLatestTriggeredEvaluation(null);
  }, [datasetId]);

  const loadDetail = useEffectEvent(async () => {
    if (!datasetId) {
      setState({
        status: "error",
        error: "Dataset not found.",
        backendUnavailable: false
      });
      return;
    }

    setState({ status: "loading" });

    try {
      const [dataset, contractsResponse, violationsResponse] = await Promise.all([
        fetchDataset(datasetId),
        fetchContracts(),
        fetchViolations({ datasetId })
      ]);

      const contract =
        contractsResponse.items.find((entry) => entry.dataset_id === datasetId) ?? null;

      const evaluationIds = Array.from(
        new Set(
          violationsResponse.items
            .map((violation) => violation.evaluation_run_id)
            .filter((evaluationId): evaluationId is string => Boolean(evaluationId))
        )
      );

      const evaluations = await Promise.all(evaluationIds.map((evaluationId) => fetchEvaluation(evaluationId)));
      evaluations.sort((left, right) => {
        return Date.parse(right.triggered_at) - Date.parse(left.triggered_at);
      });

      setState({
        status: "ready",
        data: {
          dataset,
          contract,
          violations: violationsResponse.items,
          latestEvaluation: latestTriggeredEvaluation ?? evaluations[0] ?? null
        }
      });
    } catch (error) {
      setState({
        status: "error",
        error: getErrorMessage(error),
        backendUnavailable: isBackendUnavailableError(error)
      });
    }
  });

  useEffect(() => {
    void loadDetail();
  }, [datasetId, latestTriggeredEvaluation, loadDetail]);

  return {
    state,
    latestTriggeredEvaluation,
    setLatestTriggeredEvaluation
  };
}

function RouteContent({
  route,
  overview
}: {
  route: Route;
  overview: { state: AsyncState<OverviewData>; reload: () => void };
}) {
  if (route.id === "datasets") {
    return <DatasetsRoute overview={overview} />;
  }

  if (route.id === "dataset-detail") {
    return <DatasetDetailRoute datasetId={route.datasetId} />;
  }

  if (route.id === "violations") {
    return <ViolationsRoute overview={overview} />;
  }

  return <OverviewRoute overview={overview} />;
}

function OverviewRoute({
  overview
}: {
  overview: { state: AsyncState<OverviewData>; reload: () => void };
}) {
  if (overview.state.status === "loading") {
    return (
      <>
        <PageHeader
          eyebrow="Operational overview"
          title="Dataset health"
          description="Current trust posture across registered datasets."
        />
        <LoadingState label="Loading overview dashboard" />
      </>
    );
  }

  if (overview.state.status === "error") {
    return (
      <>
        <PageHeader
          eyebrow="Operational overview"
          title="Dataset health"
          description="Current trust posture across registered datasets."
          actions={<Button tone="secondary" onClick={overview.reload}>Retry</Button>}
        />
        <ErrorState
          title={overview.state.backendUnavailable ? "Backend unavailable" : "Unable to load overview"}
          description={overview.state.error}
        />
      </>
    );
  }

  const datasetRows = buildDatasetRows(overview.state.data.datasets, overview.state.data.violations);
  const openViolations = overview.state.data.violations.filter((violation) => violation.status === "open").length;
  const healthyDatasets = datasetRows.filter((row) => row.health === "healthy").length;

  return (
    <>
      <PageHeader
        eyebrow="Operational overview"
        title="Dataset health"
        description="Current trust posture across registered datasets."
        actions={<Badge tone={openViolations > 0 ? statusTones.open : statusTones.healthy}>{openViolations} open violations</Badge>}
      />

      <section className="metric-grid" aria-label="Dataset health summary">
        <Card title="Registered datasets" value={String(datasetRows.length)} icon={Database} />
        <Card title="Healthy" value={String(healthyDatasets)} tone="success" icon={CheckCircle2} />
        <Card
          title="Unhealthy"
          value={String(datasetRows.length - healthyDatasets)}
          tone="danger"
          icon={AlertCircle}
        />
        <Card title="Open violations" value={String(openViolations)} tone="warning" icon={ShieldAlert} />
      </section>

      <section className="content-band">
        <PageHeader
          title="Datasets"
          description="Scan identity, ownership, and current health before opening a detail view."
        />
        {datasetRows.length === 0 ? (
          <EmptyState
            title="No datasets registered yet"
            description="Create datasets in the API to populate the overview dashboard."
          />
        ) : (
          <DataTable
            columns={datasetColumns}
            rows={datasetRows}
            getRowKey={(row) => row.id}
            getRowHref={(row) => `#datasets/${row.datasetId}`}
          />
        )}
      </section>
    </>
  );
}

function DatasetsRoute({
  overview
}: {
  overview: { state: AsyncState<OverviewData>; reload: () => void };
}) {
  if (overview.state.status === "loading") {
    return (
      <>
        <PageHeader
          eyebrow="Dataset registry"
          title="Datasets"
          description="Registered source tables using database.schema.table identity."
        />
        <LoadingState label="Loading datasets" />
      </>
    );
  }

  if (overview.state.status === "error") {
    return (
      <>
        <PageHeader
          eyebrow="Dataset registry"
          title="Datasets"
          description="Registered source tables using database.schema.table identity."
          actions={<Button tone="secondary" onClick={overview.reload}>Retry</Button>}
        />
        <ErrorState
          title={overview.state.backendUnavailable ? "Backend unavailable" : "Unable to load datasets"}
          description={overview.state.error}
        />
      </>
    );
  }

  const rows = buildDatasetRows(overview.state.data.datasets, overview.state.data.violations);

  return (
    <>
      <PageHeader
        eyebrow="Dataset registry"
        title="Datasets"
        description="Registered source tables using database.schema.table identity."
        actions={<Badge tone="info">{rows.length} datasets</Badge>}
      />

      <DataTable
        columns={datasetColumns}
        rows={rows}
        getRowKey={(row) => row.id}
        getRowHref={(row) => `#datasets/${row.datasetId}`}
        emptyMessage="No datasets registered yet"
        emptyDescription="Create datasets through the backend API to start the registry."
      />
    </>
  );
}

function DatasetDetailRoute({ datasetId }: { datasetId: string | null }) {
  const detail = useDatasetDetail(datasetId);
  const [triggerError, setTriggerError] = useState<string | null>(null);
  const [isTriggering, setIsTriggering] = useState(false);

  const runEvaluation = useEffectEvent(async () => {
    if (!datasetId) {
      return;
    }

    setIsTriggering(true);
    setTriggerError(null);

    try {
      const evaluation = await triggerEvaluation(datasetId);
      startTransition(() => {
        detail.setLatestTriggeredEvaluation(evaluation);
      });
    } catch (error) {
      setTriggerError(getErrorMessage(error));
    } finally {
      setIsTriggering(false);
    }
  });

  if (detail.state.status === "loading") {
    return (
      <>
        <PageHeader
          eyebrow="Dataset detail"
          title="Loading dataset"
          description="Fetching metadata, contract context, evaluation posture, and related violations."
        />
        <LoadingState label="Loading dataset detail" />
      </>
    );
  }

  if (detail.state.status === "error") {
    return (
      <>
        <PageHeader
          eyebrow="Dataset detail"
          title="Dataset detail"
          description="Primary drill-down route for metadata, current contract, evaluation posture, and related violations."
        />
        <ErrorState
          title={detail.state.backendUnavailable ? "Backend unavailable" : "Unable to load dataset detail"}
          description={detail.state.error}
        />
      </>
    );
  }

  const { dataset, contract, latestEvaluation, violations } = detail.state.data;
  const activeViolations = violations.filter((violation) => violation.status !== "resolved");
  const identity = formatDatasetIdentity(dataset);

  return (
    <>
      <PageHeader
        eyebrow="Dataset detail"
        title={identity}
        description="Primary drill-down route for metadata, current contract, evaluation posture, and related violations."
        actions={
          <div className="page-actions cluster">
            <Badge tone={activeViolations.length > 0 ? statusTones.unhealthy : statusTones.healthy}>
              {activeViolations.length > 0 ? "unhealthy" : "healthy"}
            </Badge>
            <Button disabled={isTriggering || !contract} onClick={() => void runEvaluation()}>
              <Play size={14} aria-hidden="true" />
              {isTriggering ? "Running..." : "Run evaluation"}
            </Button>
          </div>
        }
      />

      <section className="metric-grid" aria-label="Dataset detail summary">
        <Card title="Owner" value={dataset.owner ?? "Unassigned"} icon={Database} />
        <Card title="Open violations" value={String(activeViolations.length)} tone="danger" icon={ShieldAlert} />
        <Card title="Last updated" value={formatDateTime(dataset.updated_at)} tone="info" icon={Waypoints} />
        <Card
          title="Contract status"
          value={contract?.status ?? "No contract"}
          tone={contract ? "success" : "neutral"}
          icon={FileClock}
        />
      </section>

      {triggerError ? (
        <ErrorState title="Evaluation could not start" description={triggerError} />
      ) : null}

      <section className="detail-grid" aria-label="Dataset detail content">
        <article className="content-band">
          <PageHeader
            title="Metadata"
            description={dataset.description ?? "No dataset description provided yet."}
          />
          <dl className="definition-list">
            <div>
              <dt>Identity</dt>
              <dd className="mono">{identity}</dd>
            </div>
            <div>
              <dt>Owner</dt>
              <dd>{dataset.owner ?? "Unassigned"}</dd>
            </div>
            <div>
              <dt>Created</dt>
              <dd>{formatDateTime(dataset.created_at)}</dd>
            </div>
            <div>
              <dt>Updated</dt>
              <dd>{formatDateTime(dataset.updated_at)}</dd>
            </div>
          </dl>
        </article>

        <article className="content-band">
          <PageHeader
            title="Current contract"
            description="The active contract snapshot for this dataset."
          />
          {contract?.current_version ? (
            <div className="stack">
              <div className="inline-metrics">
                <Badge tone="info">{contract.name}</Badge>
                <Badge tone="success">v{contract.current_version.version_number}</Badge>
                <Badge tone="neutral">{contract.current_version.rules.length} rules</Badge>
              </div>
              <p className="muted-text">{contract.current_version.change_reason}</p>
              <div className="rule-list">
                {contract.current_version.rules.map((rule) => (
                  <article className="rule-card" key={rule.id}>
                    <div className="rule-card-header">
                      <strong>{rule.name ?? rule.rule_type}</strong>
                      <Badge tone={severityTone(rule.severity as ViolationRead["severity"])}>{rule.severity}</Badge>
                    </div>
                    <span className="table-subtext">{rule.rule_type}</span>
                  </article>
                ))}
              </div>
            </div>
          ) : (
            <EmptyState
              title="No contract yet"
              description="Register a contract to evaluate this dataset against freshness, row count, and SQL rules."
            />
          )}
        </article>

        <article className="content-band">
          <PageHeader
            title="Latest evaluation"
            description="Most recent evaluation visible from the current backend surface."
          />
          {latestEvaluation ? (
            <div className="stack">
              <div className="inline-metrics">
                <Badge tone={statusTones[latestEvaluation.summary_status]}>{latestEvaluation.summary_status}</Badge>
                <Badge tone={statusTones[latestEvaluation.status]}>{latestEvaluation.status}</Badge>
                <Badge tone="neutral">{latestEvaluation.total_rules} rules</Badge>
              </div>
              <p className="muted-text">
                Triggered {formatDateTime(latestEvaluation.triggered_at)}. Passed{" "}
                {latestEvaluation.passed_rules} of {latestEvaluation.total_rules} rules.
              </p>
              <div className="rule-list">
                {latestEvaluation.results.map((result) => (
                  <article className="rule-card" key={result.id}>
                    <div className="rule-card-header">
                      <strong>{result.rule_type}</strong>
                      <Badge tone={statusTones[result.status]}>{result.status}</Badge>
                    </div>
                    <span className="table-subtext">{result.message}</span>
                  </article>
                ))}
              </div>
            </div>
          ) : (
            <EmptyState
              title="No evaluation available yet"
              description="Run an evaluation from this page to inspect the current rule results immediately."
            />
          )}
        </article>

        <article className="content-band">
          <PageHeader
            title="Related violations"
            description="Current and historical violations tied to this dataset."
          />
          <DataTable
            columns={violationColumns}
            rows={buildViolationRows(violations, [dataset])}
            getRowKey={(row) => row.id}
            emptyMessage="No violations for this dataset"
            emptyDescription="This dataset does not have any visible violations yet."
          />
        </article>
      </section>
    </>
  );
}

function ViolationsRoute({
  overview
}: {
  overview: { state: AsyncState<OverviewData>; reload: () => void };
}) {
  const [statusFilter, setStatusFilter] = useState("all");
  const [datasetFilter, setDatasetFilter] = useState("all");
  const [selectedViolationId, setSelectedViolationId] = useState<string | null>(null);

  useEffect(() => {
    setSelectedViolationId(null);
  }, [statusFilter, datasetFilter]);

  if (overview.state.status === "loading") {
    return (
      <>
        <PageHeader
          eyebrow="Violation workbench"
          title="Violations"
          description="Triage active and recently resolved quality issues."
        />
        <LoadingState label="Loading violations" />
      </>
    );
  }

  if (overview.state.status === "error") {
    return (
      <>
        <PageHeader
          eyebrow="Violation workbench"
          title="Violations"
          description="Triage active and recently resolved quality issues."
          actions={<Button tone="secondary" onClick={overview.reload}>Retry</Button>}
        />
        <ErrorState
          title={overview.state.backendUnavailable ? "Backend unavailable" : "Unable to load violations"}
          description={overview.state.error}
        />
      </>
    );
  }

  const rows = buildViolationRows(overview.state.data.violations, overview.state.data.datasets);
  const filteredRows = rows.filter((row) => {
    const matchesStatus = statusFilter === "all" || row.status === statusFilter;
    const matchesDataset = datasetFilter === "all" || row.datasetId === datasetFilter;
    return matchesStatus && matchesDataset;
  });

  const selectedRow =
    filteredRows.find((row) => row.id === selectedViolationId) ?? filteredRows[0] ?? null;

  return (
    <>
      <PageHeader
        eyebrow="Violation workbench"
        title="Violations"
        description="Triage active and recently resolved quality issues."
      />

      <section className="filter-bar" aria-label="Violation filters">
        <label className="field">
          <span>Status</span>
          <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
            <option value="all">All statuses</option>
            <option value="open">Open</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="resolved">Resolved</option>
          </select>
        </label>

        <label className="field">
          <span>Dataset</span>
          <select value={datasetFilter} onChange={(event) => setDatasetFilter(event.target.value)}>
            <option value="all">All datasets</option>
            {overview.state.data.datasets.map((dataset) => (
              <option key={dataset.id} value={dataset.id}>
                {formatDatasetIdentity(dataset)}
              </option>
            ))}
          </select>
        </label>
      </section>

      <section className="detail-grid">
        <article className="content-band">
          {rows.length === 0 ? (
            <EmptyState
              title="No violations yet"
              description="Once evaluations start failing, violations will show up here for triage."
            />
          ) : filteredRows.length === 0 ? (
            <EmptyState
              title="No results for the current filters"
              description="Try a different status or dataset filter to widen the workbench."
            />
          ) : (
            <DataTable
              columns={violationColumns}
              rows={filteredRows}
              getRowKey={(row) => row.id}
              onRowClick={(row) => setSelectedViolationId(row.id)}
              selectedRowKey={selectedRow?.id ?? null}
            />
          )}
        </article>

        <article className="content-band">
          <PageHeader
            title="Violation detail"
            description="Focused context for triage before acknowledging or resolving the issue."
          />
          {selectedRow ? (
            <div className="stack">
              <div className="inline-metrics">
                <Badge tone={severityTone(selectedRow.severity)}>{selectedRow.severity}</Badge>
                <Badge tone={statusTones[selectedRow.status]}>{selectedRow.status}</Badge>
                <Badge tone="neutral">{selectedRow.ruleType}</Badge>
              </div>
              <p className="muted-text">{selectedRow.message}</p>
              <dl className="definition-list">
                <div>
                  <dt>Dataset</dt>
                  <dd className="mono">{selectedRow.datasetIdentity}</dd>
                </div>
                <div>
                  <dt>First seen</dt>
                  <dd>{formatDateTime(selectedRow.raw.first_seen_at)}</dd>
                </div>
                <div>
                  <dt>Last seen</dt>
                  <dd>{formatDateTime(selectedRow.raw.last_seen_at)}</dd>
                </div>
                <div>
                  <dt>Resolution note</dt>
                  <dd>{selectedRow.raw.resolution_note ?? "No resolution note yet."}</dd>
                </div>
              </dl>
              <div className="detail-callout">
                <Sparkles size={18} aria-hidden="true" />
                <div>
                  <strong>Next step</strong>
                  <p>
                    Review the evidence payload and open the dataset detail page to trigger a fresh
                    evaluation if you need current rule output.
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <EmptyState
              title="Select a violation"
              description="Click a row to inspect its dataset, timestamps, and resolution context."
            />
          )}
        </article>
      </section>
    </>
  );
}

function buildDatasetRows(datasets: DatasetRead[], violations: ViolationRead[]): DatasetRow[] {
  return datasets.map((dataset) => {
    const datasetViolations = violations.filter((violation) => violation.dataset_id === dataset.id);
    const activeViolations = datasetViolations.filter((violation) => violation.status !== "resolved");

    return {
      id: dataset.id,
      datasetId: dataset.id,
      identity: formatDatasetIdentity(dataset),
      owner: dataset.owner ?? "Unassigned",
      health: activeViolations.length > 0 ? "unhealthy" : "healthy",
      violations: datasetViolations.filter((violation) => violation.status === "open").length,
      updatedLabel: `Updated ${formatRelativeTime(dataset.updated_at)}`,
      createdLabel: `Created ${formatRelativeTime(dataset.created_at)}`
    };
  });
}

function buildViolationRows(violations: ViolationRead[], datasets: DatasetRead[]): ViolationRow[] {
  return violations.map((violation) => {
    const dataset = datasets.find((entry) => entry.id === violation.dataset_id);

    return {
      id: violation.id,
      datasetId: violation.dataset_id,
      datasetIdentity: dataset ? formatDatasetIdentity(dataset) : violation.dataset_id,
      severity: violation.severity,
      status: violation.status,
      ruleType: violation.rule_type,
      message: violation.message,
      firstSeenLabel: formatRelativeTime(violation.first_seen_at),
      lastSeenLabel: formatRelativeTime(violation.last_seen_at),
      raw: violation
    };
  });
}

function formatDatasetIdentity(dataset: DatasetRead) {
  return `${dataset.database_name}.${dataset.schema_name}.${dataset.table_name}`;
}

function formatRelativeTime(value: string) {
  const target = new Date(value).getTime();
  const deltaMinutes = Math.round((target - Date.now()) / 60000);

  if (Math.abs(deltaMinutes) < 60) {
    return new Intl.RelativeTimeFormat("en", { numeric: "auto" }).format(deltaMinutes, "minute");
  }

  const deltaHours = Math.round(deltaMinutes / 60);
  if (Math.abs(deltaHours) < 48) {
    return new Intl.RelativeTimeFormat("en", { numeric: "auto" }).format(deltaHours, "hour");
  }

  const deltaDays = Math.round(deltaHours / 24);
  return new Intl.RelativeTimeFormat("en", { numeric: "auto" }).format(deltaDays, "day");
}

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}

function getErrorMessage(error: unknown) {
  if (error instanceof ApiError) {
    return error.detail;
  }
  return "Unexpected frontend error";
}
