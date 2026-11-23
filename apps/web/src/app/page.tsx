import Link from "next/link";
import { Reveal } from "@/components/motion";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const steps = [
  {
    title: "Score it",
    body: "Your prompt is rated on key areas such as clarity, context, constraints, format and examples, with feedback for each.",
  },
  {
    title: "Rewrite it",
    body: "An AI coach rewrites the prompt to fix the weakest areas, then checks that the new version scores higher.",
  },
  {
    title: "Learn why",
    body: "Every rewrite lists the prompting techniques behind it, with a link to the source, so you learn the pattern and not just the fix.",
  },
];

export default function Home() {
  return (
    <main className="mx-auto max-w-4xl px-6">
      <section className="relative space-y-6 py-16 text-center md:py-24">
        <div
          aria-hidden
          className="absolute inset-x-0 -top-10 -z-10 mx-auto size-72 rounded-full bg-primary/10 blur-3xl"
        />
        <Reveal>
          <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
            Write better prompts. Get better answers.
          </h1>
        </Reveal>
        <Reveal delay={0.1}>
          <p className="mx-auto max-w-2xl text-lg text-muted-foreground">
            Paste a prompt and super-prompt scores it, rewrites it, and shows
            you which techniques made it better.
          </p>
        </Reveal>
        <Reveal delay={0.2}>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Link href="/analyze" className={buttonVariants({ size: "lg" })}>
              Analyze a prompt
            </Link>
            <a
              href="#how-it-works"
              className={buttonVariants({ size: "lg", variant: "outline" })}
            >
              See how it works
            </a>
          </div>
        </Reveal>
      </section>

      <section id="how-it-works" className="scroll-mt-8 space-y-6 py-12">
        <Reveal inView>
          <h2 className="text-2xl font-semibold">How it works</h2>
        </Reveal>
        <ol className="grid gap-4 md:grid-cols-3">
          {steps.map((step, index) => (
            <li key={step.title}>
              <Reveal inView delay={index * 0.12} className="h-full">
                <div className="h-full space-y-2 rounded-lg border p-5 transition duration-200 hover:-translate-y-1 hover:shadow-md">
                  <span className="flex size-8 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
                    {index + 1}
                  </span>
                  <h3 className="font-semibold">{step.title}</h3>
                  <p className="text-sm text-muted-foreground">{step.body}</p>
                </div>
              </Reveal>
            </li>
          ))}
        </ol>
      </section>

      <section className="space-y-6 py-12">
        <Reveal inView>
          <h2 className="text-2xl font-semibold">A quick example</h2>
        </Reveal>
        <div className="grid gap-4 md:grid-cols-2">
          <Reveal inView>
            <div className="h-full space-y-2 rounded-lg border p-5">
              <p className="text-sm font-medium text-muted-foreground">
                Before
              </p>
              <p className="text-sm">Write a blog post about coffee.</p>
            </div>
          </Reveal>
          <Reveal inView delay={0.25}>
            <div className="h-full space-y-2 rounded-lg border border-primary/40 bg-muted/40 p-5">
              <p className="text-sm font-medium text-muted-foreground">After</p>
              <p className="text-sm">
                You are an experienced food writer. Write a 600-word blog post
                about how beginners can brew better coffee at home. Use a
                friendly tone, a short intro, three numbered tips with one
                example each, and a one-sentence takeaway. Format it with
                Markdown headings.
              </p>
            </div>
          </Reveal>
        </div>
        <Reveal inView>
          <p className="text-sm text-muted-foreground">
            The rewrite adds a role, an audience, constraints and an output
            format, which are the things most prompts are missing.
          </p>
        </Reveal>
      </section>

      <section className="space-y-4 py-16 text-center">
        <Reveal inView>
          <h2 className="text-2xl font-semibold">
            Try it on your own prompt
          </h2>
        </Reveal>
        <Reveal inView delay={0.1}>
          <Link
            href="/analyze"
            className={cn(buttonVariants({ size: "lg" }), "mx-auto")}
          >
            Analyze a prompt
          </Link>
        </Reveal>
      </section>
    </main>
  );
}
