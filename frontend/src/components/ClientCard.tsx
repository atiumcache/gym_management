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

export interface ClientCardProps {
  first_name: string;
  last_name: string;
  phone: string;
  email: string;
  membership_status?: string;
  credits_balance?: number;
  last_activity?: Date;
}

export function ClientCard({
  first_name,
  last_name,
  phone,
  email,
  membership_status = 'Active',
  credits_balance = 0,
  last_activity,
}: ClientCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle>{`${first_name} ${last_name}`}</CardTitle>
            <CardDescription>{email}</CardDescription>
          </div>
          <CardAction>View Details</CardAction>
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        <p className="text-sm"> {phone}</p>
        <div className="flex justify-between text-sm">
          <span>Status: {membership_status}</span>
          <span>Credits: {credits_balance}</span>
        </div>
      </CardContent>
      {last_activity && (
        <CardFooter className="text-xs text-muted-foreground">
          Last activity: {last_activity.toLocaleDateString()}
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
