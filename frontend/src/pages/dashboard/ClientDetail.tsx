import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useNavigate, Link } from 'react-router';
import { API_BASE_URL, API_ENDPOINTS } from '@/config';

interface Client {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  membership_status: string;
  credits_balance: number;
  last_activity?: string;
}

export function ClientDetail() {
  const { id } = useParams<{ id: string }>();
  const [client, setClient] = useState<Client | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchClient = async () => {
      try {
        setLoading(true);
        // Replace with your actual API endpoint
        const response = await fetch(
          `${API_BASE_URL}${API_ENDPOINTS.USER}${id}`
        );
        if (!response.ok) {
          throw new Error('Failed to fetch client details');
        }
        const data = await response.json();
        setClient(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchClient();
    }
  }, [id]);

  if (loading) {
    return (
      <div className="p-6">
        <Card>
          <CardContent className="p-6">
            <div>Loading client details...</div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <Card>
          <CardContent className="p-6">
            <div className="text-red-500">Error: {error}</div>
            <Button
              variant="outline"
              className="mt-4"
              onClick={() => navigate('/dashboard/clients')}
            >
              Back to Clients
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!client) {
    return (
      <div className="p-6">
        <Card>
          <CardContent className="p-6">
            <div>Client not found</div>
            <Button
              variant="outline"
              className="mt-4"
              onClick={() => navigate('/dashboard/clients')}
            >
              Back to Clients
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Client Details</h1>
        <Link to="/dashboard/clients">
          <Button variant="outline">Back to Clients</Button>
        </Link>
      </div>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>{`${client.first_name} ${client.last_name}`}</CardTitle>
            <div className="flex space-x-2">
              <Button variant="outline" size="sm">
                Edit
              </Button>
              <Button variant="destructive" size="sm">
                Delete
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Email</h3>
              <p>{client.email}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Phone</h3>
              <p>{client.phone}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">
                Membership Status
              </h3>
              <span
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  client.membership_status === 'Active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {client.membership_status}
              </span>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">
                Credits Balance
              </h3>
              <p>{client.credits_balance}</p>
            </div>
            {client.last_activity && (
              <div>
                <h3 className="text-sm font-medium text-gray-500">
                  Last Activity
                </h3>
                <p>{new Date(client.last_activity).toLocaleDateString()}</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
