import {
  AlertCircle,
  CheckCircle2,
  Database,
  Gauge,
  LayoutDashboard,
  ShieldAlert
} from "lucide-react";
import {
  Badge,
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
import { statusTones } from "./theme/status";

type DatasetRow = {
  id: string;
  identity: string;
  owner: string;
  health: "healthy" | "unhealthy";
  violations: number;
  updated: string;
};

type ViolationRow = {
  id: string;
  dataset: string;
  severity: "critical" | "warning" | "info";
  status: "open" | "acknowledged" | "resolved";
  rule: string;
  lastSeen: string;
};

const navItems: NavItem[] = [
  { label: "Overview", href: "#overview", icon: LayoutDashboard },
  { label: "Datasets", href: "#datasets", icon: Database },
  { label: "Violations", href: "#violations", icon: ShieldAlert }
];

const datasets: DatasetRow[] = [
  {
    id: "orders",
    identity: "source.sales.orders",
    owner: "Revenue Data",
    health: "unhealthy",
    violations: 2,
    updated: "12 min ago"
  },
  {
    id: "customers",
    identity: "source.crm.customers",
    owner: "Customer Ops",
    health: "healthy",
    violations: 0,
    updated: "41 min ago"
  },
  {
    id: "shipments",
    identity: "source.fulfillment.shipments",
    owner: "Logistics",
    health: "unhealthy",
    violations: 1,
    updated: "1 hr ago"
  }
];

const violations: ViolationRow[] = [
  {
    id: "v-101",
    dataset: "source.sales.orders",
    severity: "critical",
    status: "open",
    rule: "freshness_lag_under_15m",
    lastSeen: "12 min ago"
  },
  {
    id: "v-102",
    dataset: "source.sales.orders",
    severity: "warning",
    status: "acknowledged",
    rule: "row_count_minimum",
    lastSeen: "19 min ago"
  },
  {
    id: "v-103",
    dataset: "source.fulfillment.shipments",
    severity: "info",
    status: "resolved",
    rule: "late_shipments_sql",
    lastSeen: "Yesterday"
  }
];

const datasetColumns: Column<DatasetRow>[] = [
  {
    key: "identity",
    header: "Dataset",
    render: (row) => <span className="mono">{row.identity}</span>
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
  { key: "updated", header: "Updated", render: (row) => row.updated }
];

const violationColumns: Column<ViolationRow>[] = [
  {
    key: "dataset",
    header: "Dataset",
    render: (row) => <span className="mono">{row.dataset}</span>
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
  { key: "rule", header: "Rule", render: (row) => row.rule },
  { key: "lastSeen", header: "Last seen", render: (row) => row.lastSeen }
];

function severityTone(severity: ViolationRow["severity"]): BadgeTone {
  if (severity === "critical") {
    return "danger";
  }
  if (severity === "warning") {
    return "warning";
  }
  return "neutral";
}

export function App() {
  return (
    <AppShell
      navItems={navItems}
      activeHref="#overview"
      environment="local"
      health={{
        label: "Backend healthy",
        tone: statusTones.healthy,
        icon: CheckCircle2
      }}
    >
      <PageHeader
        eyebrow="Operational overview"
        title="Dataset health"
        description="Current trust posture across registered PostgreSQL datasets."
        actions={<Badge tone={statusTones.open}>3 open violations</Badge>}
      />

      <section className="metric-grid" aria-label="Dataset health summary">
        <Card title="Registered datasets" value="3" />
        <Card title="Healthy" value="1" tone="success" icon={CheckCircle2} />
        <Card title="Unhealthy" value="2" tone="danger" icon={AlertCircle} />
        <Card title="Evaluation posture" value="Live" tone="info" icon={Gauge} />
      </section>

      <section className="content-band" id="datasets">
        <PageHeader
          title="Datasets"
          description="Scan identity, ownership, and current health before opening a detail view."
        />
        <DataTable columns={datasetColumns} rows={datasets} getRowKey={(row) => row.id} />
      </section>

      <section className="content-band" id="violations">
        <PageHeader
          title="Violations"
          description="Triage active and recently resolved quality issues."
        />
        <DataTable columns={violationColumns} rows={violations} getRowKey={(row) => row.id} />
      </section>

      <section className="state-grid" aria-label="Shared state primitives">
        <EmptyState
          title="No contract yet"
          description="Register a contract to evaluate this dataset against freshness, row count, and SQL rules."
        />
        <LoadingState label="Loading evaluation history" />
        <ErrorState title="Backend unavailable" description="Health checks will retry when the API responds." />
      </section>
    </AppShell>
  );
}
