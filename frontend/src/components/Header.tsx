import { SidebarTrigger } from '@/components/ui/sidebar';

export function Header() {
  return (
    <header className="flex justify-start w-full">
      <SidebarTrigger />
    </header>
  );
}
