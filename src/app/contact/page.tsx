"use client";

import * as React from "react";
import Link from "next/link";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input, Textarea, Select } from "@/components/ui/input";
import {
  MapPin,
  Phone,
  Mail,
  Clock,
  Train,
  Car,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  RotateCcw,
  ShieldCheck,
  Building2,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface MultiStepFormData {
  // Step 1: Contact & Entity
  fullName: string;
  companyName: string;
  email: string;
  phone: string;
  role: string;
  // Step 2: Practice & Adverse Parties
  practiceGroup: string;
  adverseParties: string;
  adverseCounsel: string;
  // Step 3: Matter Scope & Urgency
  urgency: "emergency-24h" | "urgent-48h" | "standard-30d" | "exploratory";
  matterSummary: string;
  preferredConsultDate: string;
  preferredConsultTime: string;
  // Step 4: Disclaimers
  nonConfidentialAcknowledged: boolean;
  conflictClearanceAcknowledged: boolean;
}

export default function ContactPage() {
  const [currentStep, setCurrentStep] = React.useState<1 | 2 | 3 | 4>(1);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [isSubmitted, setIsSubmitted] = React.useState(false);
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  const [formData, setFormData] = React.useState<MultiStepFormData>({
    fullName: "",
    companyName: "",
    email: "",
    phone: "",
    role: "",
    practiceGroup: "disputes",
    adverseParties: "",
    adverseCounsel: "",
    urgency: "standard-30d",
    matterSummary: "",
    preferredConsultDate: "",
    preferredConsultTime: "11:30 AM CT",
    nonConfidentialAcknowledged: false,
    conflictClearanceAcknowledged: false,
  });

  const validateStep = (step: number): boolean => {
    const newErrors: Record<string, string> = {};

    if (step === 1) {
      if (!formData.fullName.trim() || formData.fullName.trim().split(" ").length < 2) {
        newErrors.fullName = "Please enter your first and last name.";
      }
      if (!formData.companyName.trim()) {
        newErrors.companyName = "Company or entity name is required.";
      }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!formData.email.trim() || !emailRegex.test(formData.email.trim())) {
        newErrors.email = "Please enter a valid corporate email address.";
      }
      if (!formData.phone.trim() || formData.phone.replace(/\D/g, "").length < 10) {
        newErrors.phone = "Valid telephone required (minimum 10 digits).";
      }
    }

    if (step === 2) {
      if (!formData.practiceGroup) {
        newErrors.practiceGroup = "Please select a practice group.";
      }
      if (!formData.adverseParties.trim()) {
        newErrors.adverseParties = "Adverse party names are required to run conflict database checks.";
      }
    }

    if (step === 3) {
      if (!formData.matterSummary.trim() || formData.matterSummary.trim().length < 20) {
        newErrors.matterSummary = "Please provide at least a brief 1-2 sentence description (min 20 characters).";
      }
    }

    if (step === 4) {
      if (!formData.nonConfidentialAcknowledged) {
        newErrors.nonConfidentialAcknowledged = "You must acknowledge this non-confidentiality disclosure.";
      }
      if (!formData.conflictClearanceAcknowledged) {
        newErrors.conflictClearanceAcknowledged = "You must acknowledge the conflict clearance protocol.";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep((prev) => Math.min(4, prev + 1) as any);
    }
  };

  const handleBack = () => {
    setErrors({});
    setCurrentStep((prev) => Math.max(1, prev - 1) as any);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateStep(4)) return;

    setIsSubmitting(true);
    // Realistic simulated intake feedback
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
    }, 700);
  };

  const handleReset = () => {
    setFormData({
      fullName: "",
      companyName: "",
      email: "",
      phone: "",
      role: "",
      practiceGroup: "disputes",
      adverseParties: "",
      adverseCounsel: "",
      urgency: "standard-30d",
      matterSummary: "",
      preferredConsultDate: "",
      preferredConsultTime: "11:30 AM CT",
      nonConfidentialAcknowledged: false,
      conflictClearanceAcknowledged: false,
    });
    setErrors({});
    setCurrentStep(1);
    setIsSubmitted(false);
  };

  return (
    <div className="min-h-screen bg-[#f3ece1] text-[#2a1c12]">
      {/* 1. Header Hero */}
      <section className="border-b border-[#e2d5c1] py-16 lg:py-24 bg-[#ebe1d1]/30">
        <Container size="xl">
          <div className="max-w-3xl space-y-6">
            <div className="flex items-center space-x-3">
              <Badge variant="stamp">CONTACT & INTAKE</Badge>
              <span className="text-xs uppercase tracking-[0.14em] text-[#85725f] font-mono">
                LaSalle Street · Chicago
              </span>
            </div>

            <h1 className="font-serif text-[42px] sm:text-[64px] lg:text-[84px] leading-[0.95] tracking-[-0.045em] font-normal text-[#2a1c12]">
              Start with a conflict check.
            </h1>

            <p className="font-serif text-[22px] sm:text-[28px] leading-[1.2] text-[#5b4a3b]">
              All engagements begin with same-day conflict clearance on adverse parties before substantive strategy calls.
            </p>

            <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.65]">
              Under Illinois professional ethics rules, we must clear all adverse individuals, corporations, and subsidiaries before entering into confidential attorney-client discussions. Complete the intake form below or call our 31st-floor reception directly.
            </p>
          </div>
        </Container>
      </section>

      {/* 2. Main Content Grid: Multi-Step Form (Left) & Office Directions (Right) */}
      <section className="py-16 sm:py-20 lg:py-28">
        <Container size="xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-start">
            {/* Left Column: Multi-Step Conflict Check Form (7 cols) */}
            <div className="lg:col-span-7 border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-10 shadow-[0_8px_30px_rgba(42,28,18,0.04)]">
              <AnimatePresence mode="wait">
                {isSubmitted ? (
                  /* Success State */
                  <motion.div
                    key="success-card"
                    initial={{ opacity: 0, scale: 0.98 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="space-y-6 py-6"
                  >
                    <div className="inline-flex items-center justify-center h-14 w-14 rounded-full bg-[#ebe1d1] text-[#9a6a35]">
                      <CheckCircle2 className="h-8 w-8" />
                    </div>

                    <div className="space-y-2">
                      <Badge variant="gold">SIMULATED INTAKE TRANSMITTED</Badge>
                      <h2 className="font-serif text-[30px] sm:text-[36px] font-normal leading-[1.1] text-[#2a1c12]">
                        Conflict check initiated.
                      </h2>
                      <p className="text-sm text-[#5b4a3b] leading-relaxed">
                        In our actual practice, our conflicts committee and intake counsel at 224 S. LaSalle Street immediately run the adverse parties listed for{" "}
                        <span className="font-semibold text-[#2a1c12]">{formData.companyName}</span> against our active client ledger.
                      </p>
                    </div>

                    {/* Summary of submitted details */}
                    <div className="border border-[#e2d5c1] bg-[#ebe1d1]/30 p-5 space-y-2.5 text-xs font-mono">
                      <div className="text-[11px] uppercase tracking-wider text-[#85725f]">
                        Simulated Submission Summary:
                      </div>
                      <div>Contact: {formData.fullName} ({formData.role || "Client Representative"})</div>
                      <div>Email: {formData.email} · Tel: {formData.phone}</div>
                      <div>Practice Area: {formData.practiceGroup.toUpperCase()}</div>
                      <div>Adverse Parties Searched: {formData.adverseParties}</div>
                      <div>Urgency Tier: {formData.urgency.toUpperCase()}</div>
                    </div>

                    <div className="p-4 border border-[#e2d5c1] bg-[#fffaf2] text-xs text-[#5b4a3b] space-y-2">
                      <div className="font-semibold text-[#2a1c12] uppercase font-mono tracking-wider">
                        Turnaround Protocol:
                      </div>
                      <p>
                        Intake counsel contacts prospective clients by phone or secure email within 3 business hours. For emergency temporary restraining orders (TROs) requiring court appearance within 24 hours, call our urgent line directly at{" "}
                        <span className="font-mono font-semibold text-[#9a6a35]">(312) 555-0163</span>.
                      </p>
                    </div>

                    <div className="pt-4">
                      <Button
                        type="button"
                        variant="outline"
                        size="md"
                        onClick={handleReset}
                        className="inline-flex items-center"
                      >
                        <RotateCcw className="mr-2 h-4 w-4" />
                        <span>Submit another conflict inquiry</span>
                      </Button>
                    </div>
                  </motion.div>
                ) : (
                  /* Multi-Step Intake Form */
                  <div key="form-container" className="space-y-8">
                    {/* Step Progress Header */}
                    <div className="border-b border-[#e2d5c1] pb-6 space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="font-serif text-2xl font-normal text-[#2a1c12]">
                          Conflict Check Intake
                        </span>
                        <Badge variant="stamp">
                          Step 0{currentStep} of 04
                        </Badge>
                      </div>

                      {/* Step Progress Bar */}
                      <div className="grid grid-cols-4 gap-2">
                        {[1, 2, 3, 4].map((stepNum) => (
                          <div
                            key={stepNum}
                            className={`h-1.5 transition-colors ${
                              stepNum <= currentStep ? "bg-[#2a1c12]" : "bg-[#e2d5c1]"
                            }`}
                          />
                        ))}
                      </div>

                      <div className="text-xs font-mono text-[#85725f]">
                        {currentStep === 1 && "Step 1: Prospective Client & Entity Details"}
                        {currentStep === 2 && "Step 2: Practice Group & Adverse Party List"}
                        {currentStep === 3 && "Step 3: Matter Scope, Timing & Consultation"}
                        {currentStep === 4 && "Step 4: Non-Confidential Disclosure & Sign-off"}
                      </div>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                      {/* STEP 1: Client & Company Information */}
                      {currentStep === 1 && (
                        <motion.div
                          key="step1"
                          initial={{ opacity: 0, x: 8 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -8 }}
                          className="space-y-5"
                        >
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <Input
                              label="Full Name *"
                              placeholder="e.g. Margaret Ellery"
                              value={formData.fullName}
                              onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                              error={errors.fullName}
                            />
                            <Input
                              label="Title / Corporate Role"
                              placeholder="e.g. General Counsel / CEO"
                              value={formData.role}
                              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                            />
                          </div>

                          <Input
                            label="Company / Entity Name *"
                            placeholder="e.g. LaSalle Logistics LLC"
                            value={formData.companyName}
                            onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
                            error={errors.companyName}
                            helperText="List the exact corporate or LLC entity seeking legal counsel."
                          />

                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <Input
                              label="Work Email *"
                              type="email"
                              placeholder="counsel@company.com"
                              value={formData.email}
                              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                              error={errors.email}
                            />
                            <Input
                              label="Direct Telephone *"
                              type="tel"
                              placeholder="(312) 555-0100"
                              value={formData.phone}
                              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                              error={errors.phone}
                            />
                          </div>
                        </motion.div>
                      )}

                      {/* STEP 2: Practice & Adverse Parties */}
                      {currentStep === 2 && (
                        <motion.div
                          key="step2"
                          initial={{ opacity: 0, x: 8 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -8 }}
                          className="space-y-5"
                        >
                          <Select
                            label="Primary Practice Group *"
                            value={formData.practiceGroup}
                            onChange={(e) => setFormData({ ...formData, practiceGroup: e.target.value })}
                            error={errors.practiceGroup}
                            options={[
                              { value: "disputes", label: "01 Trials & Disputes (Commercial contract litigation & arbitrations)" },
                              { value: "corporate", label: "02 Corporate & M&A (Company sales, LOIs & platform recapitalizations)" },
                              { value: "employment", label: "03 Employment (Executive departures, covenants & board reviews)" },
                              { value: "investigations", label: "04 Investigations (Subpoenas, DOJ, SEC inquiries & whistleblower audits)" },
                              { value: "real-estate", label: "05 Real Estate (Commercial leases, acquisitions & build-to-suit)" },
                              { value: "ip-tech", label: "06 IP & Technology (Software licensing, OSS audits & BIPA defense)" },
                            ]}
                          />

                          <Textarea
                            label="Adverse Individuals & Entities *"
                            rows={3}
                            placeholder="List all adverse individuals, corporations, parent companies, subsidiaries, and key officers..."
                            value={formData.adverseParties}
                            onChange={(e) => setFormData({ ...formData, adverseParties: e.target.value })}
                            error={errors.adverseParties}
                            helperText="Mandatory under Illinois ethics rules so we can run our active client database."
                          />

                          <Input
                            label="Opposing Law Firm / Counsel (if known)"
                            placeholder="e.g. National Litigation LLP"
                            value={formData.adverseCounsel}
                            onChange={(e) => setFormData({ ...formData, adverseCounsel: e.target.value })}
                          />
                        </motion.div>
                      )}

                      {/* STEP 3: Matter Scope & Timing */}
                      {currentStep === 3 && (
                        <motion.div
                          key="step3"
                          initial={{ opacity: 0, x: 8 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -8 }}
                          className="space-y-5"
                        >
                          <div className="space-y-2">
                            <label className="block text-xs font-sans uppercase tracking-[0.12em] font-medium text-[#5b4a3b]">
                              Matter Urgency / Timeline *
                            </label>
                            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                              {[
                                { id: "emergency-24h", label: "Emergency (< 24h)" },
                                { id: "urgent-48h", label: "Urgent (< 48h)" },
                                { id: "standard-30d", label: "Within 30 Days" },
                                { id: "exploratory", label: "Exploratory" },
                              ].map((item) => (
                                <button
                                  key={item.id}
                                  type="button"
                                  onClick={() => setFormData({ ...formData, urgency: item.id as any })}
                                  className={`p-2.5 text-xs text-center border transition-colors cursor-pointer ${
                                    formData.urgency === item.id
                                      ? "border-[#2a1c12] bg-[#2a1c12] text-[#fffaf2] font-semibold"
                                      : "border-[#e2d5c1] bg-[#ebe1d1]/30 text-[#5b4a3b] hover:bg-[#ebe1d1]"
                                  }`}
                                >
                                  {item.label}
                                </button>
                              ))}
                            </div>
                          </div>

                          <Textarea
                            label="Brief Matter Description *"
                            rows={4}
                            placeholder="Provide a concise 2-4 sentence non-confidential description of the dispute, transaction, or inquiry..."
                            value={formData.matterSummary}
                            onChange={(e) => setFormData({ ...formData, matterSummary: e.target.value })}
                            error={errors.matterSummary}
                            helperText="Do not disclose privileged trial strategies or trade secrets in this preliminary intake."
                          />

                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <Input
                              label="Preferred Consultation Date"
                              type="date"
                              value={formData.preferredConsultDate}
                              onChange={(e) => setFormData({ ...formData, preferredConsultDate: e.target.value })}
                            />
                            <Select
                              label="Preferred Time (Central)"
                              value={formData.preferredConsultTime}
                              onChange={(e) => setFormData({ ...formData, preferredConsultTime: e.target.value })}
                              options={[
                                { value: "9:00 AM CT", label: "9:00 AM Central" },
                                { value: "11:30 AM CT", label: "11:30 AM Central" },
                                { value: "2:00 PM CT", label: "2:00 PM Central" },
                                { value: "4:30 PM CT", label: "4:30 PM Central" },
                              ]}
                            />
                          </div>
                        </motion.div>
                      )}

                      {/* STEP 4: Disclaimers & Sign-off */}
                      {currentStep === 4 && (
                        <motion.div
                          key="step4"
                          initial={{ opacity: 0, x: 8 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -8 }}
                          className="space-y-6"
                        >
                          <div className="p-4 border border-[#e2d5c1] bg-[#ebe1d1]/30 space-y-3 text-xs leading-relaxed text-[#5b4a3b]">
                            <div className="font-semibold text-[#2a1c12] uppercase font-mono">
                              Illinois State Bar Regulatory Notice
                            </div>
                            <p>
                              Under the Illinois Rules of Professional Conduct, transmitting information to Ellery Kowal LLP via this intake portal does not create an attorney-client relationship. Confidential information must not be transmitted until formal conflict clearance is completed and an engagement letter is countersigned.
                            </p>
                          </div>

                          <div className="space-y-4 pt-2">
                            <div>
                              <label className="flex items-start space-x-3 text-xs text-[#2a1c12] cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={formData.nonConfidentialAcknowledged}
                                  onChange={(e) =>
                                    setFormData({ ...formData, nonConfidentialAcknowledged: e.target.checked })
                                  }
                                  className="mt-0.5 h-4 w-4 rounded-none border-[#e2d5c1] accent-[#9a6a35] cursor-pointer"
                                />
                                <span>
                                  I acknowledge that submitting this conflict inquiry does not establish an attorney-client relationship. *
                                </span>
                              </label>
                              {errors.nonConfidentialAcknowledged && (
                                <p className="text-xs text-[#9e2a2b] font-medium pl-7 mt-1">
                                  {errors.nonConfidentialAcknowledged}
                                </p>
                              )}
                            </div>

                            <div>
                              <label className="flex items-start space-x-3 text-xs text-[#2a1c12] cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={formData.conflictClearanceAcknowledged}
                                  onChange={(e) =>
                                    setFormData({ ...formData, conflictClearanceAcknowledged: e.target.checked })
                                  }
                                  className="mt-0.5 h-4 w-4 rounded-none border-[#e2d5c1] accent-[#9a6a35] cursor-pointer"
                                />
                                <span>
                                  I confirm that the adverse parties listed above are complete and accurate to the best of my knowledge. *
                                </span>
                              </label>
                              {errors.conflictClearanceAcknowledged && (
                                <p className="text-xs text-[#9e2a2b] font-medium pl-7 mt-1">
                                  {errors.conflictClearanceAcknowledged}
                                </p>
                              )}
                            </div>
                          </div>
                        </motion.div>
                      )}

                      {/* Navigation Controls */}
                      <div className="pt-6 border-t border-[#e2d5c1] flex items-center justify-between">
                        {currentStep > 1 ? (
                          <Button
                            type="button"
                            variant="outline"
                            size="md"
                            onClick={handleBack}
                            className="inline-flex items-center"
                          >
                            <ArrowLeft className="mr-2 h-4 w-4" />
                            <span>Previous Step</span>
                          </Button>
                        ) : (
                          <div />
                        )}

                        {currentStep < 4 ? (
                          <Button
                            type="button"
                            variant="primary"
                            size="md"
                            onClick={handleNext}
                            className="inline-flex items-center"
                          >
                            <span>Next: Step 0{currentStep + 1}</span>
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        ) : (
                          <Button
                            type="submit"
                            variant="primary"
                            size="lg"
                            isLoading={isSubmitting}
                          >
                            Submit for Same-Day Clearance
                          </Button>
                        )}
                      </div>
                    </form>
                  </div>
                )}
              </AnimatePresence>
            </div>

            {/* Right Column: Office Location, Transit & Hotline (5 cols) */}
            <div className="lg:col-span-5 space-y-8">
              {/* Office Location Card */}
              <div className="border border-[#e2d5c1] bg-[#fffaf2] p-8 space-y-6 shadow-[0_4px_24px_rgba(42,28,18,0.03)]">
                <div className="flex items-center space-x-3 border-b border-[#e2d5c1] pb-4">
                  <Building2 className="h-5 w-5 text-[#9a6a35]" />
                  <span className="font-serif text-xl font-normal text-[#2a1c12]">
                    Chicago LaSalle Office
                  </span>
                </div>

                <div className="space-y-3 text-xs sm:text-sm text-[#5b4a3b]">
                  <div className="text-sm font-medium text-[#2a1c12]">
                    Ellery Kowal LLP
                  </div>
                  <div>224 S. LaSalle Street, 31st Floor</div>
                  <div>Chicago, Illinois 60604</div>
                  <div className="pt-2 text-xs font-mono text-[#85725f]">
                    Located in the Historic Rookery & Financial District Corridor
                  </div>
                </div>

                <div className="pt-4 border-t border-[#e2d5c1] space-y-2 text-xs font-mono">
                  <div className="flex items-center justify-between">
                    <span className="text-[#85725f]">Reception:</span>
                    <a href="tel:3125550147" className="font-semibold text-[#2a1c12] hover:text-[#9a6a35]">
                      (312) 555-0147
                    </a>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#85725f]">Emergency TRO:</span>
                    <a href="tel:3125550163" className="font-semibold text-[#9a6a35] hover:underline">
                      (312) 555-0163
                    </a>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#85725f]">Direct Email:</span>
                    <a href="mailto:intake@ellerykowal.com" className="text-[#2a1c12] hover:underline">
                      intake@ellerykowal.com
                    </a>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#85725f]">Office Hours:</span>
                    <span className="text-[#2a1c12]">Mon–Fri: 8:00 AM – 6:30 PM CT</span>
                  </div>
                </div>
              </div>

              {/* Transit & Commuter Access Directions */}
              <div className="border border-[#e2d5c1] bg-[#fffaf2] p-8 space-y-6 shadow-[0_4px_24px_rgba(42,28,18,0.03)]">
                <div className="flex items-center space-x-3 border-b border-[#e2d5c1] pb-4">
                  <Train className="h-5 w-5 text-[#9a6a35]" />
                  <span className="font-serif text-xl font-normal text-[#2a1c12]">
                    Commuter & Transit Directions
                  </span>
                </div>

                <div className="space-y-4 text-xs text-[#5b4a3b]">
                  {/* Metra Trains */}
                  <div className="space-y-1">
                    <div className="font-semibold text-[#2a1c12] uppercase font-mono tracking-wider">
                      Metra Stations (5–8 Minute Walk):
                    </div>
                    <p>
                      • <span className="font-medium text-[#2a1c12]">Union Station (Canal & Adams):</span> 3 blocks west via Adams Street.
                    </p>
                    <p>
                      • <span className="font-medium text-[#2a1c12]">Ogilvie Transportation Center (Madison & Canal):</span> 5 blocks northwest.
                    </p>
                  </div>

                  {/* CTA 'L' Subway */}
                  <div className="space-y-1 pt-3 border-t border-[#e2d5c1]/60">
                    <div className="font-semibold text-[#2a1c12] uppercase font-mono tracking-wider">
                      CTA 'L' Transit:
                    </div>
                    <p>
                      • <span className="font-medium text-[#2a1c12]">Quincy / Wells Station:</span> 1 block west (Brown, Orange, Pink, Purple Lines).
                    </p>
                    <p>
                      • <span className="font-medium text-[#2a1c12]">Jackson Station:</span> 1 block east (Blue & Red Lines).
                    </p>
                  </div>

                  {/* Driving & Parking */}
                  <div className="space-y-1 pt-3 border-t border-[#e2d5c1]/60">
                    <div className="font-semibold text-[#2a1c12] uppercase font-mono tracking-wider">
                      Parking & Courier Deliveries:
                    </div>
                    <p>
                      Valet and visitor parking is available at the 209 S. LaSalle and 231 S. LaSalle public parking garages. Messenger and legal service deliveries should report to the building security desk on the ground floor.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Container>
      </section>
    </div>
  );
}

