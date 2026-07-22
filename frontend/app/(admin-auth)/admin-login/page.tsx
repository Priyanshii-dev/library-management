import { LoginForm } from '@/features/auth/components/LoginForm';

export default function AdminLoginPage() {
  return (
    <main className="min-h-screen grid place-items-center bg-background p-6">
      <LoginForm 
        title="Admin Portal" 
        description="Sign in to the library management system" 
      />
    </main>
  );
}
