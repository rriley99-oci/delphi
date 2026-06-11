import type { LucideIcon } from "lucide-react";
import { Activity, DatabaseZap } from "lucide-react";
import { Badge, type BadgeTone } from "./primitives";

export type NavItem = {
  label: string;
  href: string;
  icon: LucideIcon;
};

export type AppShellProps = {
  navItems: NavItem[];
  activeHref: string;
  environment: string;
  health: {
    label: string;
    tone: BadgeTone;
    icon?: LucideIcon;
  };
  children: React.ReactNode;
};

export function AppShell({ navItems, activeHref, environment, health, children }: AppShellProps) {
  const HealthIcon = health.icon ?? Activity;

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <a className="brand" href="#overview" aria-label="Delphi overview">
          <span className="brand-mark">
            <DatabaseZap size={20} aria-hidden="true" />
          </span>
          <span>
            <strong>Delphi</strong>
            <small>Data trust</small>
          </span>
        </a>

        <nav className="nav-list" aria-label="Primary navigation">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = item.href === activeHref;

            return (
              <a
                className={isActive ? "nav-item nav-item-active" : "nav-item"}
                href={item.href}
                key={item.href}
                aria-current={isActive ? "page" : undefined}
              >
                <Icon size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>
      </aside>

      <div className="workspace">
        <header className="top-bar">
          <div>
            <span className="top-label">Environment</span>
            <strong>{environment}</strong>
          </div>
          <Badge tone={health.tone}>
            <HealthIcon size={14} aria-hidden="true" />
            {health.label}
          </Badge>
        </header>
        <main className="page-stack" id="overview">
          {children}
        </main>
      </div>
    </div>
  );
}
