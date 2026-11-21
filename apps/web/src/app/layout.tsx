import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { SiteHeader } from "@/components/SiteHeader";
import { Toaster } from "@/components/ui/sonner"; // added
import "./globals.css";
import { Suspense } from "react";
import { SiteFooter } from "@/components/SiteFooter";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "super-prompt",
  description:
    "Score your AI prompts, get a better rewrite, and learn the techniques behind it.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Suspense fallback={<div className="mx-auto max-w-4xl p-6">Loading...</div>}>
          <SiteHeader />
          {children}
          <Toaster />
          <SiteFooter />
        </Suspense>
      </body>
    </html>
  );
}