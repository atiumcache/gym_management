import { Outlet } from 'react-router';
import { DashboardLayout } from '@/layouts/DashboardLayout';

export function Dashboard() {
  return (
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  );
}
