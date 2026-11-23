"use client";

import { MotionConfig, motion } from "motion/react";
import type { ReactNode } from "react";

/** Wrap the app once. Users who prefer reduced motion get fades instead of movement. */
export function MotionProvider({ children }: { children: ReactNode }) {
  return <MotionConfig reducedMotion="user">{children}</MotionConfig>;
}

type RevealProps = {
  children: ReactNode;
  /** Seconds to wait before starting, for staggering siblings. */
  delay?: number;
  /** Animate when scrolled into view instead of on page load. */
  inView?: boolean;
  className?: string;
};

const hidden = { opacity: 0, y: 16 };
const shown = { opacity: 1, y: 0 };

export function Reveal({
  children,
  delay = 0,
  inView = false,
  className,
}: RevealProps) {
  const transition = { duration: 0.5, delay, ease: "easeOut" as const };

  if (inView) {
    return (
      <motion.div
        className={className}
        initial={hidden}
        whileInView={shown}
        viewport={{ once: true, margin: "-60px" }}
        transition={transition}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      className={className}
      initial={hidden}
      animate={shown}
      transition={transition}
    >
      {children}
    </motion.div>
  );
}
