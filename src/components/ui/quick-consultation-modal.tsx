"use client";

import * as React from "react";
import { Modal } from "./modal";
import { Button } from "./button";
import { Input, Textarea, Select } from "./input";
import { CheckCircle2, RotateCcw } from "lucide-react";

interface QuickConsultationModalProps {
  isOpen: boolean;
  onClose: () => void;
  defaultPractice?: string;
  defaultPartner?: string;
}

export function QuickConsultationModal({
  isOpen,
  onClose,
  defaultPractice = "Trials & Disputes",
  defaultPartner,
}: QuickConsultationModalProps) {
  const [fullName, setFullName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [phone, setPhone] = React.useState("");
  const [company, setCompany] = React.useState("");
  const [practice, setPractice] = React.useState(defaultPractice);
  const [prevDefaultPractice, setPrevDefaultPractice] = React.useState(defaultPractice);
  const [adverseParty, setAdverseParty] = React.useState("");
  const [summary, setSummary] = React.useState("");
  const [acknowledged, setAcknowledged] = React.useState(false);

  const [errors, setErrors] = React.useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [isSubmitted, setIsSubmitted] = React.useState(false);
  const [caseReference, setCaseReference] = React.useState("");

  if (defaultPractice !== prevDefaultPractice) {
    setPrevDefaultPractice(defaultPractice);
    setPractice(defaultPractice);
  }

  const validate = () => {
    const newErrors: Record<string, string> = {};
    if (!fullName.trim() || fullName.trim().split(" ").length < 2) {
      newErrors.fullName = "Please enter your first and last name.";
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim() || !emailRegex.test(email.trim())) {
      newErrors.email = "Valid business email required.";
    }
    if (!phone.trim() || phone.replace(/\D/g, "").length < 10) {
      newErrors.phone = "Valid telephone required (min 10 digits).";
    }
    if (!adverseParty.trim()) {
      newErrors.adverseParty = "Adverse party names required for conflict clearance.";
    }
    if (!acknowledged) {
      newErrors.acknowledged = "Disclosure acknowledgment required.";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
      const randomCode = Math.floor(1000 + Math.random() * 9000);
      setCaseReference(`EK-2026-QC-${randomCode}`);
    }, 750);
  };

  const handleReset = () => {
    setFullName("");
    setEmail("");
    setPhone("");
    setCompany("");
    setAdverseParty("");
    setSummary("");
    setAcknowledged(false);
    setErrors({});
    setIsSubmitted(false);
  };

  const handleModalClose = () => {
    onClose();
    // keep state or clear after modal closes
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleModalClose}
      title={isSubmitted ? "Inquiry Received" : "Direct Partner Consultation"}
      description={
        isSubmitted
          ? "Simulated Conflict Ledger Notification"
          : defaultPartner
          ? `Direct intake inquiry with ${defaultPartner} · LaSalle Street Floor`
          : "30-minute introductory strategy conference with an equity partner"
      }
    >
      {isSubmitted ? (
        <div className="space-y-6 pt-2">
          <div className="border border-[#e2d5c1] bg-[#ebe1d1]/30 p-6 space-y-4">
            <div className="flex items-center space-x-3 text-[#2a1c12]">
              <CheckCircle2 className="h-6 w-6 text-[#9a6a35]" />
              <div className="font-serif text-lg font-medium">
                Simulation Conflict Dossier Generated
              </div>
            </div>

            <div className="space-y-2 text-xs font-mono text-[#5b4a3b] border-t border-[#e2d5c1] pt-3">
              <div className="flex justify-between">
                <span>DOCKET ID:</span>
                <span className="font-semibold text-[#2a1c12]">{caseReference}</span>
              </div>
              <div className="flex justify-between">
                <span>INTAKE LEAD:</span>
                <span className="text-[#2a1c12]">{defaultPartner || "Duty Intake Partner"}</span>
              </div>
              <div className="flex justify-between">
                <span>ADVERSE PARTIES:</span>
                <span className="text-[#2a1c12]">{adverseParty}</span>
              </div>
              <div className="flex justify-between">
                <span>SLA CLEARANCE:</span>
                <span className="text-[#9a6a35]">Within 4 Business Hours</span>
              </div>
            </div>
          </div>

          <div className="bg-[#fffaf2] border border-[#e2d5c1] p-4 text-xs text-[#85725f] leading-relaxed">
            <strong className="text-[#2a1c12]">Demonstration Disclaimer:</strong> This is a client-side simulated submission for user-interface verification. No real communications or legal retainers were created.
          </div>

          <div className="flex items-center justify-between pt-2">
            <button
              type="button"
              onClick={handleReset}
              className="inline-flex items-center text-xs font-mono text-[#85725f] hover:text-[#2a1c12] transition-colors cursor-pointer"
            >
              <RotateCcw className="mr-1.5 h-3.5 w-3.5" />
              New Inquiry
            </button>

            <Button variant="primary" size="sm" onClick={handleModalClose}>
              Done / Close
            </Button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4 pt-2">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Full Name"
              placeholder="e.g. Katherine Reynolds"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              error={errors.fullName}
              required
            />
            <Input
              label="Entity / Company Name"
              placeholder="e.g. LaSalle Holdings LLC"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input
              label="Corporate Email"
              type="email"
              placeholder="katherine@lasalleholdings.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={errors.email}
              required
            />
            <Input
              label="Direct Telephone"
              type="tel"
              placeholder="(312) 555-0199"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              error={errors.phone}
              required
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Select
              label="Practice Area"
              value={practice}
              onChange={(e) => setPractice(e.target.value)}
              options={[
                { value: "Trials & Disputes", label: "Commercial Trials & Disputes" },
                { value: "Corporate & M&A", label: "Corporate Sales & M&A" },
                { value: "Employment", label: "Executive Departure & Covenants" },
                { value: "Investigations", label: "Government & Internal Inquiries" },
                { value: "Real Estate", label: "Commercial Real Estate" },
                { value: "IP & Technology", label: "IP Audits & Technology" },
              ]}
            />
            <Input
              label="Adverse Party Name(s)"
              placeholder="Opposing entities / individuals"
              value={adverseParty}
              onChange={(e) => setAdverseParty(e.target.value)}
              error={errors.adverseParty}
              required
            />
          </div>

          <Textarea
            label="Brief Matter Overview"
            rows={2}
            placeholder="Brief procedural posture or deal scope (do not transmit confidential evidence until cleared)..."
            value={summary}
            onChange={(e) => setSummary(e.target.value)}
          />

          <div className="border border-[#e2d5c1] bg-[#ebe1d1]/20 p-3">
            <label className="flex items-start space-x-2 text-xs text-[#5b4a3b] cursor-pointer">
              <input
                type="checkbox"
                checked={acknowledged}
                onChange={(e) => setAcknowledged(e.target.checked)}
                className="mt-0.5 h-4 w-4 border-[#e2d5c1] text-[#2a1c12] rounded-none focus:ring-[#9a6a35]"
              />
              <span className="leading-tight">
                I understand that transmission of this inquiry does not create an attorney-client relationship.
              </span>
            </label>
            {errors.acknowledged && (
              <p className="mt-1.5 text-[11px] text-[#9a6a35] font-medium">
                {errors.acknowledged}
              </p>
            )}
          </div>

          <div className="pt-2 flex items-center justify-between">
            <button
              type="button"
              onClick={handleModalClose}
              className="text-xs font-mono text-[#85725f] hover:text-[#2a1c12] transition-colors cursor-pointer"
            >
              Cancel
            </button>

            <Button
              type="submit"
              variant="primary"
              disabled={isSubmitting}
              className="bg-[#2a1c12] text-[#fffaf2] hover:bg-[#9a6a35]"
            >
              {isSubmitting ? (
                <span className="inline-flex items-center">
                  <span className="inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-solid border-[#fffaf2] border-r-transparent mr-2" />
                  Checking Conflict Ledger...
                </span>
              ) : (
                "Request Strategy Call"
              )}
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}

