import type { Metadata } from "next";
import { Inter, Noto_Naskh_Arabic } from "next/font/google";
import "./globals.css";

import { Sidebar } from "@/components/Sidebar";
import { ThemeProvider } from "@/components/ThemeProvider";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const notoNaskh = Noto_Naskh_Arabic({
  variable: "--font-naskh",
  subsets: ["arabic"],
});

export const metadata: Metadata = {
  title: "Bakhteyar-AI — Balochi Language Tools",
  description:
    "Translate English to Balochi and generate natural Balochi speech in Latin and Arabic script.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${inter.variable} ${notoNaskh.variable} h-full antialiased`}
    >
      <body className="min-h-full">
        <ThemeProvider>
          <div className="flex min-h-screen flex-col md:flex-row">
            <Sidebar />
            <main className="flex-1">
              <div className="mx-auto w-full max-w-3xl px-5 py-10 md:px-8 md:py-14">
                {children}
              </div>
            </main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
