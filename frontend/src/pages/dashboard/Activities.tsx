import {
  ActivityCard,
  type ActivityCardProps,
  SkeletonActivityCard,
} from '@/components/ActivityCard';
import { useEffect, useState } from 'react';
import { API_BASE_URL, API_ENDPOINTS } from '@/config';
import { CalendarPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { CreateActivityForm } from '@/components/CreateActivityForm';
import { toast } from 'sonner';

export function Activities() {
  const [activities, setActivities] = useState<ActivityCardProps[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchActivities = async () => {
    // TODO: Remove this delay in production
    await new Promise((r) => setTimeout(r, 2000));
    setIsLoading(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ENDPOINTS.GET_ACTIVITIES}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch activities');
      }
      const data = await response.json();
      setActivities(data as ActivityCardProps[]);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching activities:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchActivities();
  }, []);

  return (
    <>
      <div className="flex justify-between items-start pt-8">
        <h2 className="text-xl pb-8">All Scheduled Classes</h2>

        <Button variant="default" onClick={() => setIsModalOpen(true)}>
          <CalendarPlus className="mr-2 h-4 w-4" />
          Create New Class
        </Button>
      </div>

      {error && (
        <div className="text-red-500 mb-4">
          Error: {error}.{' '}
          <button onClick={fetchActivities} className="underline">
            Try again
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {isLoading
          ? // Show 6 skeleton cards while loading
            Array(6)
              .fill(0)
              .map((_, index) => (
                <SkeletonActivityCard key={`skeleton-${index}`} />
              ))
          : // Show actual activity cards when loaded
            activities.map((activity) => (
              <ActivityCard key={activity.id} {...activity} />
            ))}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-background rounded-lg w-full max-w-4xl h-[90vh] overflow-auto p-6">
            <div className="flex justify-end mb-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsModalOpen(false)}
              >
                Close
              </Button>
            </div>
            <CreateActivityForm
              onSuccess={() => {
                fetchActivities();
                setIsModalOpen(false);
                toast.success('Activity created successfully!');
              }}
            />
          </div>
        </div>
      )}
    </>
  );
}

// const sampleActivities = [
//   {
//     name: 'Morning Yoga Flow',
//     description:
//       'Start your day with a refreshing vinyasa flow to energize your body and mind. All levels welcome!',
//     coach_id: 101,
//     start_time: new Date('2025-06-21T07:00:00-07:00'),
//     duration: 60, // minutes
//     credits_required: 15,
//     max_capacity: 20,
//     spots_left: 8,
//   },
//   {
//     name: 'High-Intensity Interval Training',
//     description:
//       'Burn calories and build strength with this intense HIIT workout. Modifications available for all fitness levels.',
//     coach_id: 102,
//     start_time: new Date('2025-06-21T18:00:00-07:00'),
//     duration: 45,
//     credits_required: 20,
//     max_capacity: 15,
//     spots_left: 2,
//   },
//   {
//     name: 'Power Lifting 101',
//     description:
//       'Learn proper form and technique for squats, deadlifts, and bench press. Perfect for beginners!',
//     coach_id: 103,
//     start_time: new Date('2025-06-22T10:00:00-07:00'),
//     duration: 90,
//     credits_required: 25,
//     max_capacity: 10,
//     spots_left: 10,
//   },
//   {
//     name: 'Evening Stretch & Relax',
//     description:
//       'Gentle stretching and relaxation techniques to unwind after a long day. Perfect for all fitness levels.',
//     coach_id: 101,
//     start_time: new Date('2025-06-21T19:30:00-07:00'),
//     duration: 30,
//     credits_required: 10,
//     max_capacity: 25,
//     spots_left: 5,
//   },
// ];
