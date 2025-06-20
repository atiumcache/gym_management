import { Calendar, Home, Inbox, Search, Settings } from 'lucide-react';

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar';
import { useLocation } from 'react-router';

// Menu items.
const items = [
  {
    title: 'Home',
    path: '/dashboard',
    icon: Home,
  },
  {
    title: 'Create Activity',
    path: '/dashboard/create-activity',
    icon: Inbox,
  },
  {
    title: 'Calendar',
    path: '#',
    icon: Calendar,
  },
  {
    title: 'Search',
    path: '#',
    icon: Search,
  },
  {
    title: 'Settings',
    path: '#',
    icon: Settings,
  },
];

export function AppSidebar() {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <Sidebar side="left" variant="floating" collapsible="icon">
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => {
                const isActive =
                  currentPath === item.path ||
                  (item.path !== '/' && currentPath == item.path);
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild isActive={isActive}>
                      <a href={item.path}>
                        <item.icon />
                        <span>{item.title}</span>
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
