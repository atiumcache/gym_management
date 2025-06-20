import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

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
