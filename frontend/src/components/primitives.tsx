import type { LucideIcon } from "lucide-react";
import { AlertTriangle, Loader2, Search } from "lucide-react";

export type BadgeTone = "success" | "danger" | "warning" | "neutral" | "info";

export type PageHeaderProps = {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: React.ReactNode;
};

export function PageHeader({ eyebrow, title, description, actions }: PageHeaderProps) {
  return (
    <div className="page-header">
      <div>
        {eyebrow ? <span className="eyebrow">{eyebrow}</span> : null}
        <h1>{title}</h1>
        {description ? <p>{description}</p> : null}
      </div>
      {actions ? <div className="page-actions">{actions}</div> : null}
    </div>
  );
}

export type BadgeProps = {
  tone?: BadgeTone;
  children: React.ReactNode;
};

export function Badge({ tone = "neutral", children }: BadgeProps) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

export type CardTone = BadgeTone;

export type CardProps = {
  title: string;
  value: string;
  tone?: CardTone;
  icon?: LucideIcon;
};

export function Card({ title, value, tone = "neutral", icon: Icon }: CardProps) {
  return (
    <article className={`metric-card metric-card-${tone}`}>
      <div className="metric-card-header">
        <span>{title}</span>
        {Icon ? <Icon size={18} aria-hidden="true" /> : null}
      </div>
      <strong>{value}</strong>
    </article>
  );
}

export type Column<Row> = {
  key: string;
  header: string;
  align?: "left" | "right";
  render: (row: Row) => React.ReactNode;
};

export type DataTableProps<Row> = {
  columns: Column<Row>[];
  rows: Row[];
  getRowKey: (row: Row) => string;
  emptyMessage?: string;
  emptyDescription?: string;
  getRowHref?: (row: Row) => string;
  onRowClick?: (row: Row) => void;
  selectedRowKey?: string | null;
};

export function DataTable<Row>({
  columns,
  rows,
  getRowKey,
  emptyMessage,
  emptyDescription,
  getRowHref,
  onRowClick,
  selectedRowKey
}: DataTableProps<Row>) {
  if (rows.length === 0) {
    return (
      <EmptyState
        title={emptyMessage ?? "No rows found"}
        description={emptyDescription ?? "Adjust filters or add source data to populate this table."}
      />
    );
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th className={column.align === "right" ? "align-right" : undefined} key={column.key}>
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => {
            const rowKey = getRowKey(row);
            const rowHref = getRowHref?.(row);
            const isInteractive = Boolean(onRowClick || rowHref);
            const isSelected = rowKey === selectedRowKey;

            return (
              <tr
                className={isInteractive ? "table-row-interactive" : undefined}
                key={rowKey}
                onClick={() => {
                  if (rowHref) {
                    window.location.hash = rowHref;
                  }
                  onRowClick?.(row);
                }}
                aria-selected={isSelected || undefined}
              >
              {columns.map((column) => (
                <td className={column.align === "right" ? "align-right" : undefined} key={column.key}>
                  {column.render(row)}
                </td>
              ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export type StateProps = {
  title: string;
  description?: string;
};

export function EmptyState({ title, description }: StateProps) {
  return (
    <div className="state-panel">
      <Search size={20} aria-hidden="true" />
      <strong>{title}</strong>
      {description ? <p>{description}</p> : null}
    </div>
  );
}

export function ErrorState({ title, description }: StateProps) {
  return (
    <div className="state-panel state-panel-danger" role="alert">
      <AlertTriangle size={20} aria-hidden="true" />
      <strong>{title}</strong>
      {description ? <p>{description}</p> : null}
    </div>
  );
}

export function LoadingState({ label }: { label: string }) {
  return (
    <div className="state-panel" aria-live="polite">
      <Loader2 className="spin" size={20} aria-hidden="true" />
      <strong>{label}</strong>
    </div>
  );
}

export type ButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  tone?: "primary" | "secondary";
  type?: "button" | "submit";
};

export function Button({
  children,
  onClick,
  disabled = false,
  tone = "primary",
  type = "button"
}: ButtonProps) {
  return (
    <button className={`button button-${tone}`} disabled={disabled} onClick={onClick} type={type}>
      {children}
    </button>
  );
}
