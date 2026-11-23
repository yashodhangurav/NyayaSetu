"use client";

import "./dashboard.css";

import * as React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Bell,
  CalendarCheck,
  CalendarClock,
  Check,
  ChevronDown,
  FileText,
  FolderLock,
  Globe,
  Menu,
  MessageSquareText,
  MessagesSquare,
  ScanLine,
  Scale,
  ShieldCheck,
  Siren,
  Sparkles,
  UserRound,
  X,
  type LucideIcon,
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import { DashboardUIProvider, useDashboardUI } from "@/lib/dashboard-ui-context";
import { languageLabels } from "@/data/dashboard-mock-data";
import type { Language } from "@/types/dashboard";
import { dh, formatDateTime } from "@/lib/dashboard-utils";
import { BrandLogo } from "@/components/dashboard/shared";
import { PageLoader } from "@/components/dashboard/ui";
import { cn } from "@/lib/utils";

interface NavItem {
  to: string;
  label: string;
  icon: LucideIcon;
  end?: boolean;
  badge?: string;
}

const groups: Array<{ title?: string; items: NavItem[] }> = [
  {
    items: [
      { to: "/dashboard", label: "Home", icon: Scale, end: true },
      { to: "/dashboard/chat", label: "AI Legal Assistant", icon: Sparkles },
      { to: "/dashboard/cases", label: "My Cases", icon: FolderLock },
      { to: "/dashboard/deadlines", label: "Court Deadlines", icon: CalendarClock, badge: "3" },
      { to: "/dashboard/bookings", label: "Consultations", icon: CalendarCheck },
      { to: "/dashboard/messages", label: "Messages", icon: MessagesSquare, badge: "3" },
    ],
  },
  {
    title: "Legal Services",
    items: [
      { to: "/dashboard/advocates", label: "Find an Advocate", icon: Scale },
      { to: "/dashboard/self-help", label: "Self-Help Guides", icon: FileText },
      { to: "/dashboard/vault", label: "Document Vault", icon: ShieldCheck },
      { to: "/dashboard/scan", label: "Scan & Explain", icon: ScanLine },
    ],
  },
  {
    title: "Account",
    items: [{ to: "/dashboard/profile", label: "Profile & Privacy", icon: UserRound }],
  },
];

const mobileTabs: NavItem[] = [
  { to: "/dashboard", label: "Home", icon: Scale, end: true },
  { to: "/dashboard/cases", label: "Cases", icon: FolderLock },
  { to: "/dashboard/vault", label: "Vault", icon: ShieldCheck },
  { to: "/dashboard/messages", label: "Messages", icon: MessagesSquare },
  { to: "/dashboard/profile", label: "Profile", icon: UserRound },
];

function useOutside<T extends HTMLElement>(onClose: () => void) {
  const ref = React.useRef<T>(null);
  React.useEffect(() => {
    const handler = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) onClose();
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [onClose]);
  return ref;
}

function isActive(pathname: string, item: NavItem): boolean {
  return item.end ? pathname === item.to : pathname.startsWith(item.to);
}

function SidebarItem({ item, onNavigate }: { item: NavItem; onNavigate?: () => void }) {
  const pathname = usePathname();
  const active = isActive(pathname, item);
  const Icon = item.icon;
  return (
    <Link
      href={item.to}
      onClick={onNavigate}
      className={cn(
        "group flex h-10 items-center gap-2.5 rounded-[2px] px-3 text-xs font-sans uppercase tracking-[0.08em] font-medium transition-all duration-150 select-none",
        active
          ? "bg-[#2a1c12] text-[#fffaf2] shadow-xs"
          : "text-[#5b4a3b] hover:bg-[#ebe1d1]/50 hover:text-[#2a1c12]"
      )}
    >
      <Icon
        className={cn(
          "size-[16px] shrink-0",
          active ? "text-[#d1a46a]" : "text-[#85725f] group-hover:text-[#2a1c12]"
        )}
        strokeWidth={active ? 2.2 : 1.8}
        aria-hidden="true"
      />
      <span className="flex-1 truncate">{item.label}</span>
      {active && <span className="size-1.5 rounded-full bg-[#d1a46a]" aria-hidden="true" />}
      {item.badge && !active && (
        <span className="grid h-4.5 min-w-4.5 place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1] px-1 text-[10px] font-mono text-[#5b4a3b]">
          {item.badge}
        </span>
      )}
    </Link>
  );
}

function SidebarContent({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full flex-col bg-[#fffaf2]">
      <div className="px-5 pt-6 pb-4 border-b border-[#e2d5c1]/60">
        <BrandLogo onClick={onNavigate} />
      </div>

      <nav className="flex-1 space-y-6 overflow-y-auto px-3.5 py-5">
        {groups.map((group, gi) => (
          <div key={gi}>
            {group.title && (
              <p className="mb-2 px-3 text-[10px] font-sans uppercase tracking-[0.14em] font-semibold text-[#85725f]">
                {group.title}
              </p>
            )}
            <div className="space-y-1">
              {group.items.map((item) => (
                <SidebarItem key={item.to} item={item} onNavigate={onNavigate} />
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="px-3.5 pb-4 pt-2 border-t border-[#e2d5c1]/60 space-y-2">
        <div className="rounded-[2px] border border-[#e2d5c1] bg-[#ebe1d1]/35 p-3.5">
          <p className="flex items-center gap-1.5 text-xs font-semibold text-[#2a1c12]">
            <MessageSquareText className="size-3.5 text-[#9a6a35]" aria-hidden="true" />
            Free Legal Aid (NALSA/DLSA)
          </p>
          <p className="mt-1 text-[11.5px] leading-relaxed text-[#5b4a3b]">
            Eligible citizens can access free advocate services through court legal aid cells.
          </p>
          <a
            href="tel:15100"
            className="mt-2.5 inline-flex h-8 w-full items-center justify-center rounded-[2px] border border-[#2a1c12] bg-[#2a1c12] text-[11px] font-sans uppercase tracking-[0.1em] font-semibold text-[#fffaf2] transition hover:bg-[#9a6a35] hover:border-[#9a6a35]"
          >
            Call 15100 Helpline
          </a>
        </div>
        <p className="px-1 text-[10.5px] leading-4 text-[#85725f] text-center">
          NyayaSetu Bharat · Established 2026
        </p>
      </div>
    </div>
  );
}

function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-[264px] border-r border-[#e2d5c1] bg-[#fffaf2] lg:block">
      <SidebarContent />
    </aside>
  );
}

function LanguageSwitcher() {
  const { language, setLanguage } = useAuth();
  const [open, setOpen] = React.useState(false);
  const ref = useOutside<HTMLDivElement>(() => setOpen(false));

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-haspopup="listbox"
        className="inline-flex h-9 cursor-pointer items-center gap-1.5 rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] px-2.5 text-xs font-medium text-[#2a1c12] transition hover:bg-[#ebe1d1]/40"
      >
        <Globe className="size-3.5 text-[#85725f]" aria-hidden="true" />
        <span className="hidden sm:inline">{languageLabels[language]}</span>
        <span className="sm:hidden">{language.toUpperCase()}</span>
        <ChevronDown className={cn("size-3 text-[#85725f] transition", open && "rotate-180")} aria-hidden="true" />
      </button>

      {open && (
        <div
          role="listbox"
          className="absolute right-0 z-60 mt-1.5 w-56 overflow-hidden rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] p-1 shadow-[0_8px_30px_rgba(42,28,18,0.1)] animate-in-up"
        >
          {(Object.keys(languageLabels) as Language[]).map((lang) => (
            <button
              key={lang}
              type="button"
              role="option"
              aria-selected={language === lang}
              onClick={() => {
                setLanguage(lang);
                setOpen(false);
              }}
              className={cn(
                "flex h-9 w-full cursor-pointer items-center justify-between rounded-[2px] px-3 text-xs font-medium transition hover:bg-[#ebe1d1]/40",
                language === lang ? "bg-[#ebe1d1]/60 text-[#2a1c12] font-semibold" : "text-[#5b4a3b]"
              )}
            >
              {languageLabels[lang]}
              {language === lang && <Check className="size-3.5 text-[#9a6a35]" aria-hidden="true" />}
            </button>
          ))}
          <p className="px-3 pt-2 pb-1 text-[10.5px] leading-relaxed text-[#85725f] border-t border-[#e2d5c1]/60 mt-1">
            Core statutory guidance and navigation adapt to your choice.
          </p>
        </div>
      )}
    </div>
  );
}

function NotificationBell() {
  const { notifications, markAllRead, markRead } = useDashboardUI();
  const [open, setOpen] = React.useState(false);
  const ref = useOutside<HTMLDivElement>(() => setOpen(false));
  const router = useRouter();
  const unread = notifications.filter((n) => !n.read).length;

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label={`Notifications, ${unread} unread`}
        aria-expanded={open}
        className="relative grid size-9 cursor-pointer place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] transition hover:bg-[#ebe1d1]/40"
      >
        <Bell className="size-4 text-[#2a1c12]" aria-hidden="true" />
        {unread > 0 && (
          <span className="absolute -top-1 -right-1 grid size-4.5 place-items-center rounded-full border border-[#fffaf2] bg-[#c0392b] text-[9px] font-mono font-bold text-[#fffaf2]">
            {unread}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 z-60 mt-1.5 w-[min(92vw,360px)] overflow-hidden rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] shadow-[0_8px_30px_rgba(42,28,18,0.1)] animate-in-up">
          <div className="flex items-center justify-between border-b border-[#e2d5c1] px-4 py-3 bg-[#ebe1d1]/30">
            <p className="text-xs font-sans uppercase tracking-[0.12em] font-semibold text-[#2a1c12]">Notifications</p>
            <button
              type="button"
              onClick={markAllRead}
              className="cursor-pointer text-xs font-medium text-[#9a6a35] hover:underline"
            >
              Mark all read
            </button>
          </div>
          <div className="max-h-[340px] overflow-y-auto divide-y divide-[#e2d5c1]/60">
            {notifications.map((n) => (
              <button
                key={n.id}
                type="button"
                onClick={() => {
                  markRead(n.id);
                  if (n.href) {
                    router.push(dh(n.href));
                    setOpen(false);
                  }
                }}
                className="flex w-full cursor-pointer gap-3 px-4 py-3 text-left transition hover:bg-[#ebe1d1]/30"
              >
                <span
                  className={cn(
                    "mt-1.5 size-1.5 shrink-0 rounded-full",
                    n.read ? "bg-[#cfbe9e]" : "bg-[#2e7d32]"
                  )}
                />
                <span className="min-w-0">
                  <span className="block text-xs font-semibold text-[#2a1c12]">{n.title}</span>
                  <span className="mt-0.5 block text-xs leading-relaxed text-[#5b4a3b]">{n.body}</span>
                  <span className="mt-1 block text-[10px] font-mono text-[#85725f]">{formatDateTime(n.at)}</span>
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Header() {
  const { user } = useAuth();
  const [drawer, setDrawer] = React.useState(false);

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-[#e2d5c1] bg-[#f4efe6]/90 backdrop-blur-md">
        <div className="flex h-16 items-center gap-3 px-4 sm:px-6 lg:px-8">
          <button
            type="button"
            onClick={() => setDrawer(true)}
            aria-label="Open menu"
            className="grid size-9 cursor-pointer place-items-center rounded-[2px] border border-[#e2d5c1] bg-[#fffaf2] lg:hidden"
          >
            <Menu className="size-4" aria-hidden="true" />
          </button>

          <div className="lg:hidden">
            <BrandLogo compact />
          </div>

          <div className="hidden flex-1 items-center gap-2 lg:flex">
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 text-[11px] font-sans uppercase tracking-[0.14em] font-medium border border-[#e2d5c1] bg-[#dceada]/50 text-[#2e7d32] rounded-[2px]">
              <span className="size-1.5 rounded-full bg-[#2e7d32]" aria-hidden="true" />
              Verified Legal Portal
            </span>
            <span className="text-xs text-[#85725f]">Statutory information & advocate directory</span>
          </div>

          <div className="ml-auto flex items-center gap-2">
            <LanguageSwitcher />
            <NotificationBell />
            <Link
              href="/dashboard/profile"
              className="ml-1 grid size-9 place-items-center rounded-full border border-[#2a1c12] bg-[#2a1c12] text-xs font-serif font-medium text-[#fffaf2] transition hover:bg-[#9a6a35] hover:border-[#9a6a35]"
              aria-label="Open profile"
            >
              {user?.name?.slice(0, 1).toUpperCase() ?? "R"}
            </Link>
          </div>
        </div>
      </header>

      {drawer && (
        <div className="fixed inset-0 z-70 lg:hidden">
          <div className="absolute inset-0 animate-fade bg-[#24180f]/75 backdrop-blur-xs" onClick={() => setDrawer(false)} />
          <div className="absolute inset-y-0 left-0 w-[82%] max-w-[320px] bg-[#fffaf2] shadow-[0_20px_50px_rgba(36,24,15,0.25)] animate-in-up">
            <button
              type="button"
              onClick={() => setDrawer(false)}
              aria-label="Close menu"
              className="absolute top-4 right-3 z-10 grid size-8 cursor-pointer place-items-center rounded-[2px] text-[#85725f] hover:text-[#2a1c12] hover:bg-[#ebe1d1]/50"
            >
              <X className="size-4.5" />
            </button>
            <SidebarContent onNavigate={() => setDrawer(false)} />
          </div>
        </div>
      )}
    </>
  );
}

function Footer() {
  return (
    <footer className="mt-12 border-t border-[#e2d5c1] px-4 py-6 pb-24 sm:px-6 lg:px-8 lg:pb-6">
      <div className="mx-auto flex max-w-6xl flex-col gap-2.5 text-xs text-[#85725f] sm:flex-row sm:items-center sm:justify-between">
        <p className="font-medium">
          <span className="mr-1.5 inline-block size-1.5 rounded-full bg-[#2e7d32] align-middle" aria-hidden="true" />
          Preliminary AI assessments do not constitute formal legal advice.
        </p>
        <nav aria-label="Footer" className="flex flex-wrap items-center gap-x-4 gap-y-1 pr-16 sm:pr-20 lg:pr-32">
          <Link href="/dashboard/profile" className="hover:text-[#2a1c12] underline-offset-4 hover:underline">
            Privacy & DPDP Choices
          </Link>
          <a href="tel:15100" className="hover:text-[#2a1c12] underline-offset-4 hover:underline">
            Free Legal Aid: 15100
          </a>
          <span>© 2026 NyayaSetu Bharat</span>
        </nav>
      </div>
    </footer>
  );
}

function BottomNav() {
  const pathname = usePathname();
  const { notifications } = useDashboardUI();
  const unread = notifications.filter((n) => !n.read).length;

  return (
    <nav
      aria-label="Primary"
      className="fixed inset-x-0 bottom-0 z-40 border-t border-[#e2d5c1] bg-[#fffaf2]/95 pb-[env(safe-area-inset-bottom)] backdrop-blur-md lg:hidden"
    >
      <div className="grid h-16 grid-cols-5">
        {mobileTabs.map((tab) => {
          const Icon = tab.icon;
          const active = isActive(pathname, tab);
          const showBadge = tab.to === "/dashboard/messages" && unread > 0;
          return (
            <Link
              key={tab.to}
              href={tab.to}
              className={cn(
                "relative flex min-h-11 flex-col items-center justify-center gap-1 text-[10.5px] font-sans uppercase tracking-[0.08em] font-medium transition",
                active ? "text-[#9a6a35] font-semibold" : "text-[#85725f]"
              )}
            >
              <span className="relative">
                <Icon
                  className={cn("size-[19px]", active && "text-[#9a6a35]")}
                  strokeWidth={active ? 2.2 : 1.8}
                  aria-hidden="true"
                />
                {showBadge && (
                  <span className="absolute -top-1 -right-1.5 size-2 rounded-full bg-[#c0392b] ring-2 ring-[#fffaf2]" />
                )}
              </span>
              <span>{tab.label}</span>
              {active && <span className="absolute bottom-1 size-1 rounded-full bg-[#9a6a35]" aria-hidden="true" />}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

function EmergencyButton() {
  const pathname = usePathname();
  const active = pathname === "/dashboard/emergency";

  return (
    <Link
      href="/dashboard/emergency"
      aria-label="Open emergency help"
      className={cn(
        "fixed right-3 bottom-20 z-40 inline-flex h-11 w-11 items-center justify-center rounded-[2px] border border-[#c0392b] bg-[#c0392b] text-xs font-sans uppercase tracking-[0.1em] font-semibold text-[#fffaf2] shadow-sm transition-all duration-150",
        "hover:bg-[#a93226] active:scale-[0.98]",
        "lg:right-6 lg:bottom-6 lg:h-11 lg:w-auto lg:justify-start lg:gap-2 lg:px-4",
        active && "opacity-75"
      )}
    >
      <span className="relative grid size-5 place-items-center">
        <Siren className="size-4" aria-hidden="true" />
      </span>
      <span className="hidden lg:inline">Emergency Helpline</span>
    </Link>
  );
}

function DashboardShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { user } = useAuth();
  // The AI Legal Assistant owns the viewport: no page scroll and no dashboard footer.
  const isChatPage = pathname === "/dashboard/chat";

  React.useEffect(() => {
    if (typeof window === "undefined") return;
    const storedToken = localStorage.getItem("nyayasetu_token");
    if (!storedToken && !user) router.push("/login");
  }, [user, router]);

  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
  }, [pathname]);

  return (
    <div
      className={cn(
        "dashboard-scope bg-[#f4efe6] text-[#2a1c12]",
        isChatPage ? "h-dvh overflow-hidden" : "min-h-screen"
      )}
    >
      <Sidebar />
      <div
        className={cn(
          "flex flex-col lg:pl-[264px]",
          isChatPage ? "h-dvh overflow-hidden" : "min-h-screen"
        )}
      >
        <Header />
        <main
          id="main-content"
          tabIndex={-1}
          className={cn(
            "focus:outline-none",
            isChatPage
              ? "min-h-0 flex-1 overflow-hidden px-3 pb-[calc(5rem+env(safe-area-inset-bottom))] pt-3 sm:px-4 sm:pt-4 lg:px-6 lg:pb-3"
              : "flex-1 px-4 py-6 sm:px-6 sm:py-8 lg:px-8"
          )}
        >
          <div
            className={cn(
              "mx-auto w-full",
              isChatPage ? "h-full min-h-0 max-w-none" : "max-w-6xl"
            )}
          >
            {children}
          </div>
        </main>
        {!isChatPage && <Footer />}
      </div>
      <BottomNav />
      <EmergencyButton />
    </div>
  );
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <DashboardUIProvider>
      <React.Suspense
        fallback={
          <div className="dashboard-scope min-h-screen bg-[#f4efe6] p-6">
            <div className="mx-auto w-full max-w-6xl">
              <PageLoader />
            </div>
          </div>
        }
      >
        <DashboardShell>{children}</DashboardShell>
      </React.Suspense>
    </DashboardUIProvider>
  );
}
