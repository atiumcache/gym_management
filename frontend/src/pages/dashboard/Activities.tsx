import {
  ActivityCard,
  type ActivityCardProps,
} from '@/components/ActivityCard';
import { useEffect, useState } from 'react';
import { API_BASE_URL, API_ENDPOINTS } from '@/config';

const sampleActivities = [
  {
    name: 'Morning Yoga Flow',
    description:
      'Start your day with a refreshing vinyasa flow to energize your body and mind. All levels welcome!',
    coach_id: 101,
    start_time: new Date('2025-06-21T07:00:00-07:00'),
    duration: 60, // minutes
    credits_required: 15,
    max_capacity: 20,
    spots_left: 8,
  },
  {
    name: 'High-Intensity Interval Training',
    description:
      'Burn calories and build strength with this intense HIIT workout. Modifications available for all fitness levels.',
    coach_id: 102,
    start_time: new Date('2025-06-21T18:00:00-07:00'),
    duration: 45,
    credits_required: 20,
    max_capacity: 15,
    spots_left: 2,
  },
  {
    name: 'Power Lifting 101',
    description:
      'Learn proper form and technique for squats, deadlifts, and bench press. Perfect for beginners!',
    coach_id: 103,
    start_time: new Date('2025-06-22T10:00:00-07:00'),
    duration: 90,
    credits_required: 25,
    max_capacity: 10,
    spots_left: 10,
  },
  {
    name: 'Evening Stretch & Relax',
    description:
      'Gentle stretching and relaxation techniques to unwind after a long day. Perfect for all fitness levels.',
    coach_id: 101,
    start_time: new Date('2025-06-21T19:30:00-07:00'),
    duration: 30,
    credits_required: 10,
    max_capacity: 25,
    spots_left: 5,
  },
];

export function Activities() {
  const [activities, setActivities] = useState<ActivityCardProps[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchActivities() {
      try {
        const response = await fetch(
          `${API_BASE_URL}${API_ENDPOINTS.GET_ACTIVITIES}`
        );
        if (!response.ok) {
          throw new Error('Failed to fetch activities');
        }
        const data = await response.json();
        setActivities(data as ActivityCardProps[]);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error('Error fetching activities:', err);
      } finally {
        setIsLoading(false);
      }
    }
    fetchActivities();
  }, []);

  return (
    <>
      <h2 className="text-xl pb-8">All Scheduled Classes</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {activities.map((activity) => (
          <ActivityCard key={activity.name} {...activity} />
        ))}
      </div>
    </>
  );
}
