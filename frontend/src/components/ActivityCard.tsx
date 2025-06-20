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

export interface ActivityCardProps {
  name: string;
  description: string;
  coach_id: number;
  start_time: Date;
  duration: number;
  credits_required: number;
  max_capacity: number;
  spots_left: number;
}

export function ActivityCard({
  name,
  description,
  coach_id,
  start_time,
  duration,
  credits_required,
  max_capacity,
  spots_left,
}: ActivityCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{name}</CardTitle>
        <CardDescription>{description}</CardDescription>
        <CardAction>Edit</CardAction>
      </CardHeader>
      <CardContent>
        <p>Card Content</p>
      </CardContent>
      <CardFooter>
        <p>
          Credits Required: {credits_required} | Spots Left: {spots_left}/
          {max_capacity}
        </p>
      </CardFooter>
    </Card>
  );
}

export function SkeletonActivityCard() {
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
        <Skeleton className="h-4 w-3/4" />
      </div>
      <div className="flex justify-between items-center pt-2">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-9 w-24 rounded-md" />
      </div>
    </div>
  );
}
