import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from './ui/button';
import { Link } from 'react-router';

export interface ClientCardProps {
  id: number;
  first_name: string;
  last_name: string;
  phone: string;
  email: string;
  membership_status?: string;
  credits_balance?: number;
  last_activity?: Date;
}

export function ClientCard({
  id,
  first_name,
  last_name,
  phone,
  email,
  membership_status = 'Active',
  credits_balance = 0,
  last_activity,
}: ClientCardProps) {
  return (
    <Card className="hover:shadow-lg transition-all duration-200 h-full flex flex-col">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div className="flex-1 min-w-0 mr-4">
            <CardTitle className="text-lg text-left">{`${first_name} ${last_name}`}</CardTitle>
            <CardDescription className="text-left truncate" title={email}>
              {email}
            </CardDescription>
          </div>
          <CardAction className="text-sm font-medium text-primary hover:text-primary/80 transition-colors whitespace-nowrap">
            <Link to={`/dashboard/clients/${id}`}>
              <Button variant="default">View</Button>
            </Link>
          </CardAction>
        </div>
      </CardHeader>
      <CardContent className="flex-1 pb-3">
        <div className="space-y-3">
          <div className="flex items-center text-sm">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 mr-2 opacity-70"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
              />
            </svg>
            <span className="truncate" title={phone}>
              {phone}
            </span>
          </div>
          <div className="flex flex-wrap gap-2 text-xs">
            <span
              className={`px-2 py-1 rounded-full ${
                membership_status === 'Active'
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                  : 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400'
              }`}
            >
              {membership_status}
            </span>
            <span className="px-2 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 rounded-full">
              {credits_balance} Credits
            </span>
          </div>
        </div>
      </CardContent>
      {last_activity && (
        <CardFooter className="text-xs text-muted-foreground pt-0 border-t dark:border-gray-800">
          <div className="flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-3.5 w-3.5 mr-1 opacity-60"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Last activity:{' '}
            {new Date(last_activity).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
            })}
          </div>
        </CardFooter>
      )}
    </Card>
  );
}

export function SkeletonClientCard() {
  return (
    <div className="flex flex-col space-y-3 p-4 border rounded-lg bg-card text-card-foreground shadow-sm animate-pulse">
      <div className="flex justify-between items-start">
        <div className="space-y-2">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-32" />
        </div>
        <Skeleton className="h-4 w-16" />
      </div>
      <div className="space-y-2">
        <Skeleton className="h-4 w-full" />
        <div className="flex justify-between">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-16" />
        </div>
      </div>
      <Skeleton className="h-3 w-40 mt-2" />
    </div>
  );
}
