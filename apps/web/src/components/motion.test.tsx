import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MotionProvider, Reveal } from "./motion";

describe("Reveal", () => {
  it("renders its children", () => {
    render(
      <MotionProvider>
        <Reveal>
          <p>Hello</p>
        </Reveal>
      </MotionProvider>,
    );

    expect(screen.getByText("Hello")).toBeInTheDocument();
  });
});
