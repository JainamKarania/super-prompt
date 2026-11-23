"use client";

import { useEffect, useState } from "react";
import { useReducedMotion } from "motion/react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { Analysis } from "@/lib/schema";

/** A progress bar that fills from empty to its value shortly after it appears. */
function AnimatedProgress({ value, delay }: { value: number; delay: number }) {
  const reduceMotion = useReducedMotion();
  const [shown, setShown] = useState(reduceMotion ? value : 0);

  useEffect(() => {
    const timer = setTimeout(() => setShown(value), delay * 1000);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return <Progress value={shown} className="mt-1" />;
}

export function ScoreCard({ analysis }: { analysis: Analysis }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Overall score: {analysis.overall.toFixed(1)} / 10</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {analysis.dimensions.map((d, index) => (
          <div key={d.name}>
            <div className="flex justify-between text-sm font-medium capitalize">
              <span>{d.name}</span>
              <span>{d.score}/10</span>
            </div>
            <AnimatedProgress value={d.score * 10} delay={0.2 + index * 0.1} />
            <p className="mt-1 text-sm text-muted-foreground">{d.feedback}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
