"use client";

import * as React from "react";
import { Container } from "@/components/layout/container";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input, Textarea, Select } from "@/components/ui/input";
import { CheckCircle2, RotateCcw } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ConflictCheckFormData, FormErrors } from "@/types";

export function ConflictIntakeSection() {
  const [formData, setFormData] = React.useState<ConflictCheckFormData>({
    fullName: "",
    companyName: "",
    email: "",
    phone: "",
    matterType: "disputes",
    adverseParties: "",
    urgency: "none-yet",
    nonConfidentialAcknowledged: false,
  });

  const [errors, setErrors] = React.useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [isSubmitted, setIsSubmitted] = React.useState(false);

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.fullName.trim() || formData.fullName.trim().split(" ").length < 2) {
      newErrors.fullName = "Please provide your first and last name.";
    }
    if (!formData.companyName.trim()) {
      newErrors.companyName = "City/State or court jurisdiction is required.";
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim() || !emailRegex.test(formData.email.trim())) {
      newErrors.email = "Please enter a valid email address.";
    }
    if (!formData.phone.trim() || formData.phone.replace(/\D/g, "").length < 10) {
      newErrors.phone = "Valid 10-digit mobile number required (+91).";
    }
    if (!formData.adverseParties.trim()) {
      newErrors.adverseParties = "Brief description of legal issue and opposing parties is required.";
    }
    if (!formData.nonConfidentialAcknowledged) {
      newErrors.nonConfidentialAcknowledged = "You must acknowledge this notice before submitting.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    // Simulate brief processing for authentic feedback
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
    }, 600);
  };

  const handleReset = () => {
    setFormData({
      fullName: "",
      companyName: "",
      email: "",
      phone: "",
      matterType: "disputes",
      adverseParties: "",
      urgency: "none-yet",
      nonConfidentialAcknowledged: false,
    });
    setErrors({});
    setIsSubmitted(false);
  };

  const steps = [
    {
      num: "01",
      title: "Instant AI Legal Assessment",
      desc: "Our AI evaluates your factual dispute under applicable Indian statutes (BNS, BNSS, Contract Act, NI Act, RERA) in your preferred language.",
    },
    {
      num: "02",
      title: "Verified Advocate Matching",
      desc: "Get paired with Bar Council-verified advocates based on practice area, jurisdiction (District Court to Supreme Court), and language fluency.",
    },
    {
      num: "03",
      title: "Direct Consultation with Fixed Fees",
      desc: "Book a 30-minute strategic consultation with transparent fee schedules starting at ₹999 with zero hidden charges.",
    },
    {
      num: "04",
      title: "Court Tracking & Document Management",
      desc: "Access cause list updates, limitation period countdowns, document checklists, and order summaries via your secure dashboard.",
    },
  ];

  return (
    <section id="conflict-check" className="border-b border-[#e2d5c1] bg-[#ebe1d1]/40 py-16 lg:py-28">
      <Container size="xl">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-start">
          {/* Left Column: 4-Step Process Explanation (5 cols) */}
          <div className="lg:col-span-5 space-y-8">
            <div className="space-y-4">
              <Badge variant="stamp">LEGAL TRIAGE & MATCH</Badge>
              <h2 className="font-serif text-[34px] sm:text-[48px] lg:text-[58px] leading-[0.98] tracking-[-0.045em] font-normal text-[#2a1c12]">
                Request an AI legal assessment.
              </h2>
              <p className="text-[15px] sm:text-[16px] text-[#5b4a3b] leading-[1.6]">
                Direct legal clarity begins here. Get an instant preliminary analysis under Indian law and connect with verified advocates practicing in your jurisdiction.
              </p>
            </div>

            {/* 4 Steps List */}
            <div className="space-y-6 pt-4 border-t border-[#e2d5c1]">
              {steps.map((s) => (
                <div key={s.num} className="flex items-start space-x-4">
                  <span className="font-serif text-2xl text-[#9a6a35] font-normal shrink-0">
                    {s.num}
                  </span>
                  <div className="space-y-1">
                    <h4 className="font-sans font-medium text-sm text-[#2a1c12]">
                      {s.title}
                    </h4>
                    <p className="text-xs text-[#5b4a3b] leading-relaxed">
                      {s.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {/* Office & Helpline Note */}
            <div className="p-4 border border-[#e2d5c1] bg-[#fffaf2] text-xs font-mono text-[#85725f] space-y-1">
              <div className="text-[#2a1c12] font-semibold uppercase tracking-wider">
                NyayaSetu Bharat · Legal Triage & Coordination Desk
              </div>
              <div>New Delhi · Mumbai · Bengaluru · Kolkata · Chennai · Hyderabad</div>
              <div>Toll-Free: 1800-NYAYA-SETU (1800-692-9273) · Mon-Sat 9 AM - 8 PM IST</div>
            </div>
          </div>

          {/* Right Column: Interactive Form Card (7 cols) */}
          <div className="lg:col-span-7 border border-[#e2d5c1] bg-[#fffaf2] p-6 sm:p-10 shadow-[0_8px_30px_rgba(42,28,18,0.04)]">
            <AnimatePresence mode="wait">
              {isSubmitted ? (
                /* Success Confirmation View */
                <motion.div
                  key="success"
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
                    <Badge variant="gold">ASSESSMENT INITIATED</Badge>
                    <h3 className="font-serif text-[30px] sm:text-[34px] font-normal leading-[1.1] text-[#2a1c12]">
                      Legal assessment dossier initiated.
                    </h3>
                    <p className="text-sm text-[#5b4a3b] leading-relaxed">
                      Our legal AI engine is analyzing the statutory provisions and relevant case precedents for your matter in{" "}
                      <span className="font-semibold text-[#2a1c12]">{formData.companyName}</span>.
                    </p>
                  </div>

                  <div className="border border-[#e2d5c1] bg-[#ebe1d1]/30 p-5 space-y-3 text-xs">
                    <div className="font-mono text-[#85725f] uppercase tracking-wider">
                      Advocate Matching Window:
                    </div>
                    <p className="text-[#2a1c12] leading-relaxed">
                      A preliminary legal dossier and matched Bar Council-verified advocates will be sent to <span className="font-mono font-medium">{formData.email}</span> and via WhatsApp to your mobile within 4 hours.
                    </p>
                    <div className="pt-2 text-[11px] text-[#85725f]">
                      For emergency bail hearings or urgent injunctions within 24 hours, call the urgent triage desk at <span className="font-mono font-semibold text-[#9a6a35]">1800-692-9273</span>.
                    </div>
                  </div>

                  <div className="pt-4">
                    <Button
                      variant="outline"
                      size="md"
                      onClick={handleReset}
                      className="inline-flex items-center"
                    >
                      <RotateCcw className="mr-2 h-4 w-4" />
                      <span>Submit another legal inquiry</span>
                    </Button>
                  </div>
                </motion.div>
              ) : (
                /* The Intake Form */
                <motion.form
                  key="form"
                  onSubmit={handleSubmit}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="space-y-6"
                >
                  <div className="border-b border-[#e2d5c1] pb-4 flex items-center justify-between">
                    <div>
                      <h3 className="font-serif text-2xl font-normal text-[#2a1c12]">
                        AI Legal Intake & Matching
                      </h3>
                      <p className="text-xs text-[#85725f] mt-0.5">
                        Preliminary statutory analysis with verified advocate matching across India
                      </p>
                    </div>
                    <Badge variant="stamp">CONFIDENTIAL</Badge>
                  </div>

                  {/* Name & Jurisdiction */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <Input
                      label="Full Name *"
                      placeholder="e.g. Rajesh Sharma"
                      value={formData.fullName}
                      onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                      error={errors.fullName}
                    />
                    <Input
                      label="City, State / Court Jurisdiction *"
                      placeholder="e.g. Mumbai, Bombay High Court"
                      value={formData.companyName}
                      onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
                      error={errors.companyName}
                    />
                  </div>

                  {/* Email & Phone */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <Input
                      label="Email Address *"
                      type="email"
                      placeholder="r.sharma@example.com"
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      error={errors.email}
                    />
                    <Input
                      label="Mobile / WhatsApp Number *"
                      type="tel"
                      placeholder="+91 98765 43210"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      error={errors.phone}
                    />
                  </div>

                  {/* Practice Area Dropdown */}
                  <Select
                    label="Legal Practice Area *"
                    value={formData.matterType}
                    onChange={(e) => setFormData({ ...formData, matterType: e.target.value })}
                    options={[
                      { value: "civil-property", label: "01 Civil & Property Law (RERA, title, partition, tenancy)" },
                      { value: "startup-corporate", label: "02 Startup & Corporate Law (MCA, SHA, founder agreements, contracts)" },
                      { value: "criminal-defense", label: "03 Criminal Defense & Bail (BNS, BNSS, anticipatory bail, FIRs)" },
                      { value: "cheque-debt", label: "04 Cheque Bounce & Debt Recovery (Sec 138 NI Act, DRT, IBC)" },
                      { value: "family-matrimonial", label: "05 Family & Matrimonial Law (Mutual divorce, 498A, maintenance)" },
                      { value: "consumer-cyber", label: "06 Consumer & Cyber Law (Consumer forum, IT Act 66D, 1930 portal)" },
                    ]}
                  />

                  {/* Dispute Details & Opposing Parties */}
                  <Textarea
                    label="Summary of Legal Issue & Opposing Parties *"
                    rows={3}
                    placeholder="Describe what occurred, key dates, notices or summons received, and any opposing individuals or companies..."
                    value={formData.adverseParties}
                    onChange={(e) => setFormData({ ...formData, adverseParties: e.target.value })}
                    error={errors.adverseParties}
                    helperText="Under Bar Council standards, your case summary is kept confidential and shared only with counsel you select."
                  />

                  {/* Urgency Radio Selector */}
                  <div className="space-y-2">
                    <label className="block text-xs font-sans uppercase tracking-[0.12em] font-medium text-[#5b4a3b]">
                      Urgency / Timeline
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                      {[
                        { id: "urgent-48h", label: "Urgent (< 48 hrs / Notice)" },
                        { id: "upcoming-30d", label: "Active (30 days / Court)" },
                        { id: "none-yet", label: "Preliminary Advice" },
                      ].map((item) => (
                        <button
                          key={item.id}
                          type="button"
                          onClick={() => setFormData({ ...formData, urgency: item.id as ConflictCheckFormData["urgency"] })}
                          className={`p-2.5 text-xs text-center border transition-colors cursor-pointer ${
                            formData.urgency === item.id
                              ? "border-[#2a1c12] bg-[#2a1c12] text-[#fffaf2] font-medium"
                              : "border-[#e2d5c1] bg-[#ebe1d1]/30 text-[#5b4a3b] hover:bg-[#ebe1d1]"
                          }`}
                        >
                          {item.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Non-Confidential / Ethics Disclaimer Checkbox */}
                  <div className="space-y-1 pt-2">
                    <label className="flex items-start space-x-3 text-xs text-[#5b4a3b] cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.nonConfidentialAcknowledged}
                        onChange={(e) =>
                          setFormData({ ...formData, nonConfidentialAcknowledged: e.target.checked })
                        }
                        className="mt-0.5 h-4 w-4 rounded-none border-[#e2d5c1] accent-[#9a6a35] cursor-pointer"
                      />
                      <span className="leading-relaxed">
                        I understand that NyayaSetu provides an AI-assisted preliminary legal assessment and advocate discovery platform. It does not provide guaranteed legal outcomes or replace independent advice from a licensed advocate under the Advocates Act, 1961.
                      </span>
                    </label>
                    {errors.nonConfidentialAcknowledged && (
                      <p className="text-xs text-[#9e2a2b] font-medium pl-7">
                        {errors.nonConfidentialAcknowledged}
                      </p>
                    )}
                  </div>

                  {/* Submit Button */}
                  <div className="pt-2">
                    <Button
                      type="submit"
                      variant="primary"
                      size="lg"
                      isLoading={isSubmitting}
                      className="w-full text-sm font-medium uppercase tracking-wider"
                    >
                      Request Legal Assessment & Advocate Match
                    </Button>
                  </div>
                </motion.form>
              )}
            </AnimatePresence>
          </div>
        </div>
      </Container>
    </section>
  );
}

