// This layout overrides the parent admin layout for the login page,
// so the login page is shown full-screen without the sidebar.
export default function AdminLoginLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
