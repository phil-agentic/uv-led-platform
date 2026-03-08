import "./globals.css";

export const metadata = {
  title: "UV LED Knowledge Platform",
  description: "Research intelligence and community insights for UV LED technology.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
