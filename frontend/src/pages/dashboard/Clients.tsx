import {
  ClientCard,
  type ClientCardProps,
  SkeletonClientCard,
} from '@/components/ClientCard';
import { useEffect, useState } from 'react';
import { API_BASE_URL, API_ENDPOINTS } from '@/config';
import { CalendarPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { AddClientForm } from '@/components/AddClientForm';

export function Clients() {
  const [clients, setClients] = useState<ClientCardProps[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchClients = async () => {
    // TODO: Remove this delay in production
    setIsLoading(true);
    await new Promise((r) => setTimeout(r, 2000));
    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ENDPOINTS.GET_ALL_USERS}`
      );
      if (!response.ok) {
        throw new Error('Failed to fetch activities');
      }
      const data = await response.json();
      setClients(data as ClientCardProps[]);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching activities:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchClients();
  }, []);

  return (
    <>
      <div className="flex justify-between items-start pt-8">
        <h2 className="text-xl pb-8">All Clients</h2>

        <Button variant="default" onClick={() => setIsModalOpen(true)}>
          <CalendarPlus className="mr-2 h-4 w-4" />
          Add New Client
        </Button>
      </div>

      {error && (
        <div className="text-red-500 mb-4">
          Error: {error}.{' '}
          <button onClick={fetchClients} className="underline">
            Try again
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols2 lg:grid-cols-3 gap-4">
        {isLoading
          ? // Show 6 skeleton cards while loading
            Array(6)
              .fill(0)
              .map((_, index) => (
                <SkeletonClientCard key={`skeleton-${index}`} />
              ))
          : // Show actual activity cards when loaded
            clients.map((client) => <ClientCard key={client.id} {...client} />)}
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
            <AddClientForm
              onSuccess={() => {
                fetchClients();
                setIsModalOpen(false);
                toast.success('Client created successfully!');
              }}
            />
          </div>
        </div>
      )}
    </>
  );
}
