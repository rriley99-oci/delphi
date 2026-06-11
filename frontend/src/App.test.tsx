import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { App } from "./App";

describe("App shell", () => {
  afterEach(() => {
    window.history.replaceState(null, "", "#overview");
  });

  it("renders the required navigation and backend health state", () => {
    render(<App />);

    const navigation = screen.getByRole("navigation", { name: /primary navigation/i });
    expect(within(navigation).getByRole("link", { name: /overview/i })).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: /datasets/i })).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: /violations/i })).toBeInTheDocument();
    expect(screen.getByText(/backend healthy/i)).toBeInTheDocument();
    expect(screen.getByText(/local/i)).toBeInTheDocument();
  });

  it("updates route content when primary navigation changes the hash", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("link", { name: /violations/i }));
    window.location.hash = "#violations";
    fireEvent(window, new HashChangeEvent("hashchange"));

    expect(screen.getByRole("heading", { name: "Violations" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /violations/i })).toHaveAttribute("aria-current", "page");
  });

  it("renders shared status treatments for operational states", () => {
    window.history.replaceState(null, "", "#violations");

    render(<App />);

    expect(screen.getByText("critical")).toHaveClass("badge-danger");
    expect(screen.getByText("warning")).toHaveClass("badge-warning");
    expect(screen.getByText("open")).toHaveClass("badge-danger");
    expect(screen.getByText("acknowledged")).toHaveClass("badge-warning");
    expect(screen.getByText("resolved")).toHaveClass("badge-success");
  });

  it("renders shared empty, loading, and error primitives", () => {
    window.history.replaceState(null, "", "#datasets/orders");

    render(<App />);

    expect(screen.getByText("No contract yet")).toBeInTheDocument();
    expect(screen.getByText("Loading evaluation history")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveTextContent("Backend unavailable");
  });

  it("renders the datasets route and configured backend URL", () => {
    window.history.replaceState(null, "", "#datasets");

    render(<App />);

    expect(screen.getByRole("heading", { name: "Datasets" })).toBeInTheDocument();
    expect(screen.getByText("/api")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /datasets/i })).toHaveAttribute("aria-current", "page");
  });

  it("renders the dataset detail route", () => {
    window.history.replaceState(null, "", "#datasets/orders");

    render(<App />);

    expect(screen.getByText("Dataset detail")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "source.sales.orders" })).toBeInTheDocument();
    expect(screen.getByText("No contract yet")).toBeInTheDocument();
  });

  it("renders the violations route", () => {
    window.history.replaceState(null, "", "#violations");

    render(<App />);

    expect(screen.getByRole("heading", { name: "Violations" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /violations/i })).toHaveAttribute("aria-current", "page");
    expect(screen.getByText("late_shipments_sql")).toBeInTheDocument();
  });
});
