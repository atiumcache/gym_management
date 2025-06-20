// In date-picker.tsx
'use client';

import * as React from 'react';
import { ChevronDownIcon } from 'lucide-react';
import { format } from 'date-fns';
import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { cn } from '@/lib/utils';

interface DatePickerProps {
  value?: Date;
  onChange: (date: Date | undefined) => void;
  label?: string;
  className?: string;
  showTime?: boolean;
}

export function DatePicker({
  value,
  onChange,
  label = 'Date',
  className,
  showTime = true,
}: DatePickerProps) {
  const [open, setOpen] = React.useState(false);
  const [selectedDate, setSelectedDate] = React.useState<Date | undefined>(
    value
  );
  const [timeValue, setTimeValue] = React.useState(
    value ? format(value, 'HH:mm') : '12:00'
  );

  const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = e.target.value;
    setTimeValue(time);
    updateDateTime(selectedDate, time);
  };

  const handleDateSelect = (date: Date | undefined) => {
    setSelectedDate(date);
    updateDateTime(date, timeValue);
    setOpen(false);
  };

  const updateDateTime = (date: Date | undefined, time: string) => {
    if (!date) return;

    const [hours, minutes] = time.split(':').map(Number);
    const newDate = new Date(date);
    newDate.setHours(hours, minutes, 0, 0);
    onChange(newDate);
  };

  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex flex-col gap-3">
        <Label htmlFor="date" className="px-1">
          {label}
        </Label>
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              id="date"
              className="w-full justify-between font-normal"
            >
              {selectedDate ? format(selectedDate, 'PPP') : 'Select date'}
              <ChevronDownIcon className="ml-2 h-4 w-4" />
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0" align="start">
            <Calendar
              mode="single"
              selected={selectedDate}
              onSelect={handleDateSelect}
              initialFocus
            />
          </PopoverContent>
        </Popover>
      </div>

      {showTime && (
        <div className="flex flex-col gap-3">
          <Label htmlFor="time-picker" className="px-1">
            Time
          </Label>
          <Input
            type="time"
            id="time-picker"
            value={timeValue}
            onChange={handleTimeChange}
            step="300" // 5 minute steps
            className="bg-background"
          />
        </div>
      )}
    </div>
  );
}
