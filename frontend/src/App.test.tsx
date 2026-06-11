import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { App } from "./App";

describe("App shell", () => {
  it("renders the required navigation and backend health state", () => {
    render(<App />);

    const navigation = screen.getByRole("navigation", { name: /primary navigation/i });
    expect(within(navigation).getByRole("link", { name: /overview/i })).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: /datasets/i })).toBeInTheDocument();
    expect(within(navigation).getByRole("link", { name: /violations/i })).toBeInTheDocument();
    expect(screen.getByText(/backend healthy/i)).toBeInTheDocument();
    expect(screen.getByText(/local/i)).toBeInTheDocument();
  });

  it("renders shared status treatments for operational states", () => {
    render(<App />);

    expect(screen.getByText("healthy")).toHaveClass("badge-success");
    expect(screen.getAllByText("unhealthy")[0]).toHaveClass("badge-danger");
    expect(screen.getByText("open")).toHaveClass("badge-danger");
    expect(screen.getByText("acknowledged")).toHaveClass("badge-warning");
    expect(screen.getByText("resolved")).toHaveClass("badge-success");
  });

  it("renders shared empty, loading, and error primitives", () => {
    render(<App />);

    expect(screen.getByText("No contract yet")).toBeInTheDocument();
    expect(screen.getByText("Loading evaluation history")).toBeInTheDocument();
    expect(screen.getByRole("alert")).toHaveTextContent("Backend unavailable");
  });
});
