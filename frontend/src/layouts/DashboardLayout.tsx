// src/layouts/DashboardLayout.tsx
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar';
import { AppSidebar } from '@/components/AppSidebar';
import { Header } from '@/components/Header';
import { Toaster } from '@/components/ui/sonner';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SidebarProvider>
        <AppSidebar />

        <main className="flex-1">
          <Header />
          {children}
        </main>
      </SidebarProvider>
      <Toaster />
    </>
  );
}
