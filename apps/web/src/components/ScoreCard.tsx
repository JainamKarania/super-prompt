import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { Analysis } from "@/lib/schema";

export function ScoreCard({ analysis }: { analysis: Analysis }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Overall score: {analysis.overall.toFixed(1)} / 10</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {analysis.dimensions.map((d) => (
          <div key={d.name}>
            <div className="flex justify-between text-sm font-medium capitalize">
              <span>{d.name}</span>
              <span>{d.score}/10</span>
            </div>
            <Progress value={d.score * 10} className="mt-1" />
            <p className="mt-1 text-sm text-muted-foreground">{d.feedback}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}