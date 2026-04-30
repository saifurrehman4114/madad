import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { HealthBadge } from "../HealthBadge";

describe("HealthBadge", () => {
  it("shows backend when healthy", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "ok", backend: "ollama", model: "gemma4:e4b" }),
    }) as any;
    render(<HealthBadge />);
    await waitFor(() => expect(screen.getByText(/ollama/)).toBeTruthy());
  });

  it("shows offline when API down", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("net")) as any;
    render(<HealthBadge />);
    await waitFor(() => expect(screen.getByText(/none/)).toBeTruthy());
  });
});
