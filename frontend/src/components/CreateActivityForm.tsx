'use client';

import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { CheckIcon, ChevronsUpDown, XCircle } from 'lucide-react';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { DatePicker } from '@/components/DatePicker';
import type { User } from '@/types/api';
import { API_BASE_URL, API_ENDPOINTS } from '@/config';

const formSchema = z.object({
  name: z.string().min(1, 'Name is required').max(50),
  description: z.string().min(1, 'Description is required'),
  coach_id: z.number().min(1, 'Please select a coach'),
  start_time: z.date({
    required_error: 'Please select a date and time',
  }),
  duration: z.number().min(1, 'Duration must be at least 1 minute'),
  credits_required: z.number().min(0, 'Credits cannot be negative'),
  max_capacity: z.number().min(1, 'Capacity must be at least 1'),
});

// TODO: Make sure this formSchema aligns with backend schema

export function CreateActivityForm() {
  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      credits_required: 1,
      max_capacity: 10,
      duration: 60, // 60 minutes default
      start_time: new Date(), // Set default to current time
    },
  });

  // 2. Define a submit handler.
  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    console.log('Form submitted with values:', values);
    console.log('Coach ID:', values.coach_id); // Log the coach_id

    if (!values.coach_id) {
      console.error('No coach selected');
      setError('Please select a coach');
      return;
    }

    setError(null);

    try {
      const apiUrl = `${API_BASE_URL}/api/v1/activity/create/`;
      console.log('Sending request to:', apiUrl);

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...values,
          start_time: values.start_time.toISOString(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to create activity');
      }

      console.log('Success:', data);
      alert('Activity created successfully!');
      form.reset();
    } catch (error) {
      console.error('Error:', error);
      setError(error instanceof Error ? error.message : 'Something went wrong');
    }
  };

  useEffect(() => {
    console.log('Form state:', form.formState);
    console.log('Form errors:', form.formState.errors);
  }, [form.formState]);

  const [coaches, setCoaches] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCoaches() {
      try {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.COACH}`);
        if (!response.ok) {
          throw new Error('Failed to fetch coaches');
        }
        const data = await response.json();
        setCoaches(data as User[]);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error('Error fetching coaches:', err);
      } finally {
        setIsLoading(false);
      }
    }

    fetchCoaches();
  }, []);

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <XCircle className="h-5 w-5 text-red-500" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Class Name</FormLabel>
              <FormControl>
                <Input placeholder="Barbell Club" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="coach_id"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Coach</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant="outline"
                      role="combobox"
                      className={cn(
                        'w-[200px] justify-between',
                        !field.value && 'text-muted-foreground'
                      )}
                    >
                      {isLoading
                        ? 'Loading coaches...'
                        : error
                        ? 'Error loading coaches'
                        : field.value
                        ? `${
                            coaches.find((c) => c.id === field.value)
                              ?.first_name || ''
                          } ${
                            coaches.find((c) => c.id === field.value)
                              ?.last_name || ''
                          }`.trim()
                        : 'Select a coach'}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-[200px] p-0">
                  <Command>
                    <CommandInput placeholder="Search coach..." />
                    <CommandList>
                      <CommandEmpty>No coaches found.</CommandEmpty>
                      <CommandGroup>
                        {coaches.map((coach) => {
                          const fullName =
                            `${coach.first_name} ${coach.last_name}`.trim();
                          return (
                            <CommandItem
                              value={fullName}
                              key={coach.id}
                              onSelect={() => {
                                console.log(
                                  'Selected coach:',
                                  coach.id,
                                  fullName
                                );
                                form.setValue('coach_id', coach.id, {
                                  shouldValidate: true,
                                });
                              }}
                            >
                              <CheckIcon
                                className={cn(
                                  'mr-2 h-4 w-4',
                                  coach.id === field.value
                                    ? 'opacity-100'
                                    : 'opacity-0'
                                )}
                              />
                              {fullName}
                            </CommandItem>
                          );
                        })}
                      </CommandGroup>
                    </CommandList>
                  </Command>
                </PopoverContent>
              </Popover>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Input placeholder="We will lift weights and..." {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="start_time"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Start Date/Time</FormLabel>
              <FormControl>
                <DatePicker
                  selected={field.value}
                  onChange={(date) => field.onChange(date)}
                  showTimeSelect
                  timeFormat="HH:mm"
                  timeIntervals={15}
                  dateFormat="MMMM d, yyyy h:mm aa"
                  className="w-full p-2 border rounded"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="duration"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Duration (minutes)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min="1"
                  {...field}
                  onChange={(e) => field.onChange(parseInt(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="credits_required"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Credits required</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min="1"
                  {...field}
                  onChange={(e) => field.onChange(parseInt(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="max_capacity"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Max attendees</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min="1"
                  {...field}
                  onChange={(e) => field.onChange(parseInt(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          onClick={() => console.log('Submit button clicked')}
        >
          Create Class
        </Button>
      </form>
    </Form>
  );
}
