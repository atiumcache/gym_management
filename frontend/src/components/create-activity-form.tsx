'use client';

import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { CheckIcon, ChevronsUpDown } from 'lucide-react';
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
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { DatePicker } from '@/components/date-picker';
import type { User } from '@/types/api';
import { API_BASE_URL, API_ENDPOINTS } from '@/config';

const formSchema = z.object({
  name: z.string().min(1).max(50),
  description: z.string(),
  coach_id: z.number(),
  datetime: z.date(),
  start_time: z.string(),
  duration: z.string(),
  credits_required: z.number(),
  max_capacity: z.number(),
});

export function CreateActivityForm() {
  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      credits_required: 1,
    },
  });

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values);
  }

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
                      variant="ghost"
                      role="combobox"
                      className={cn(
                        'w-[200px] justify-between text-muted',
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
                                form.setValue('coach_id', coach.id);
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
          name="datetime"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel>Start Date/Time</FormLabel>
              <FormControl>
                <DatePicker
                  value={field.value}
                  onChange={(date) => {
                    field.onChange(date);
                  }}
                  label="Date"
                  className="flex gap-8"
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
        <Button type="submit">Create Class</Button>
      </form>
    </Form>
  );
}
