"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { CalendarClock, CalendarPlus, CheckCircle2, Clock, Download, MessageSquare, Star } from 'lucide-react';
import { listBookings, downloadIcs } from '@/services/dashboard/bookings';
import type { Booking } from '@/types/dashboard';
import { formatDate, formatInr, dh } from '@/lib/dashboard-utils';
import {
  Badge,
  Button,
  EmptyState,
  Tabs,
} from '@/components/dashboard/ui';
import { PageHeader } from '@/components/dashboard/shared';

const statusTone = {
  pending_payment: 'warn',
  confirmed: 'mint',
  completed: 'brand',
  cancelled: 'neutral',
  refunded: 'neutral',
} as const;

export default function BookingsPage() {
  const router = useRouter();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [tab, setTab] = useState<'upcoming' | 'past'>('upcoming');

  useEffect(() => {
    void listBookings().then(setBookings);
  }, []);

  const upcoming = bookings.filter((b) => b.status === 'confirmed' || b.status === 'pending_payment');
  const past = bookings.filter((b) => b.status === 'completed' || b.status === 'cancelled' || b.status === 'refunded');
  const list = tab === 'upcoming' ? upcoming : past;

  return (
    <div className="animate-fade space-y-6">
      <PageHeader
        title="Consultations"
        backTo={dh("/")}
      />

      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#e2d5c1] pb-4">
        <Tabs
          value={tab}
          onChange={setTab}
          options={[
            { value: 'upcoming', label: 'Upcoming', count: upcoming.length },
            { value: 'past', label: 'Past', count: past.length },
          ]}
        />
        <Button size="sm" variant="secondary" onClick={() => router.push(dh('/advocates'))}>
          Book consultation
        </Button>
      </div>

      {list.length === 0 ? (
        <EmptyState
          icon={<CalendarClock className="size-5 text-[#9a6a35]" />}
          title={tab === 'upcoming' ? 'No Active Hearings Scheduled' : 'No Concluded Hearings'}
          body="Book a 30-minute call with a verified advocate."
          action={<Button onClick={() => router.push(dh('/advocates'))}>Find advocate</Button>}
        />
      ) : (
        <div className="space-y-4">
          {list.map((b) => (
            <div key={b.id} className="rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-5 sm:p-6 transition hover:border-[#9a6a35]">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div className="flex items-start gap-4">
                  <span className="grid size-12 shrink-0 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#f4efe6] font-mono text-[14px] font-medium text-[#2a1c12]">
                    {new Date(b.date).getDate()}
                  </span>
                  <div>
                    <h3 className="font-serif text-[18px] font-normal text-[#2a1c12]">Adv. {b.advocateName}</h3>
                    <p className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-[12.5px] text-[#5b4a3b]">
                      <span className="inline-flex items-center gap-1.5 font-medium text-[#2a1c12]">
                        <CalendarPlus className="size-3.5 text-[#9a6a35]" aria-hidden />
                        {formatDate(b.date, { day: 'numeric', month: 'short' })}
                      </span>
                      <span className="inline-flex items-center gap-1.5">
                        <Clock className="size-3.5 text-[#85725f]" aria-hidden />
                        {b.time}
                      </span>
                      <span className="capitalize">{b.mode.replace('-', ' ')}</span>
                    </p>
                    <p className="mt-1.5 font-mono text-[11px] text-[#85725f]">Docket Ref: #{b.id} · Fee: {formatInr(b.amount)}</p>
                  </div>
                </div>
                <Badge tone={statusTone[b.status]}>{b.status.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase())}</Badge>
              </div>

              <div className="mt-4 flex flex-wrap items-center gap-2.5 pt-4 border-t border-[#e2d5c1]">
                {b.status === 'confirmed' && (
                  <>
                    <Button size="sm" onClick={() => router.push(dh('/messages'))}>
                      <MessageSquare className="size-3.5" aria-hidden /> Message
                    </Button>
                    <Button size="sm" variant="secondary" onClick={() => downloadIcs(b)}>
                      <Download className="size-3.5" aria-hidden /> Add to Calendar
                    </Button>
                  </>
                )}
                {b.status === 'completed' && !b.feedbackGiven && (
                  <Button size="sm" onClick={() => router.push(dh(`/feedback/${b.id}`))}>
                    <Star className="size-3.5" aria-hidden /> Leave review
                  </Button>
                )}
                {b.status === 'completed' && b.feedbackGiven && (
                  <p className="flex items-center gap-1.5 text-[12px] font-medium text-[#2a6b3b]">
                    <CheckCircle2 className="size-3.5" aria-hidden /> Evaluation registered.
                  </p>
                )}
                <Button size="sm" variant="ghost" onClick={() => router.push(dh(`/booking/${b.advocateId}`))}>
                  Re-schedule Slot
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}


    </div>
  );
}
