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

        <main className="flex flex-col flex-1 py-4.5 px-1 items-center">
          <Header />
          <div className="px-8 max-w-[1280px] w-full">{children}</div>
        </main>
      </SidebarProvider>
      <Toaster />
    </>
  );
}
