import { useMemo, useState } from 'react';
import { ClaimLensContext } from './ClaimLensContext';
import { INITIAL_CLAIMS, CLAIMS_BY_ID } from '../data/claims';
import { USERS } from '../data/users';
import { filterClaims } from '../lib/filterClaims';

/**
 * All application state + action handlers of the original single-file App live here.
 * Screens read what they need with `useClaimLens()`.
 * (Prototype choice. For the real app, server state moves to TanStack Query and the handlers become API calls.)
 */
export function ClaimLensProvider({ children }) {
  // Navigation & Auth State
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  const [currentRole, setCurrentRole] = useState('Examiner');
  const currentUser = USERS[currentRole];

  const [activeScreen, setActiveScreen] = useState('queue'); // 'login' | 'queue' | 'submit' | 'verify' | 'detail' | 'supervisor' | 'dashboard'
  const [claims, setClaims] = useState(INITIAL_CLAIMS);
  const [selectedClaimId, setSelectedClaimId] = useState('CLM-2026-00104');
  const [copilotOpen, setCopilotOpen] = useState(false);
  const [showDemoBar, setShowDemoBar] = useState(true);
  const [toastMessage, setToastMessage] = useState(null);

  // Queue Filters
  const [bucketFilter, setBucketFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [checkFilter, setCheckFilter] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  // Claim Detail Sub-state
  const [detailTab, setDetailTab] = useState('findings'); // 'findings' | 'memo' | 'audit'
  const [selectedReasonCode, setSelectedReasonCode] = useState('NCCI-PTP');
  const [actionComment, setActionComment] = useState('');
  const [simulateStaleVersion, setSimulateStaleVersion] = useState(false);

  // Field Verification State (CLM-2026-00042)
  const [verifyUnitsInput, setVerifyUnitsInput] = useState(2);
  const [verifyNpiInput, setVerifyNpiInput] = useState('1245319599');

  // Submit Claim State
  const [submitTab, setSubmitTab] = useState('pdf'); // 'pdf' | 'json' | 'batch'
  const [pdfScanMode, setPdfScanMode] = useState('noisy'); // 'noisy' | 'clean'
  const [jsonPreset, setJsonPreset] = useState('ptp_error');

  // Threshold Config State (Dashboard F16)
  const [thresholds, setThresholds] = useState({
    fieldConfidence: 0.8,
    noteDocRed: 0.3,
    noteDocGreen: 0.7,
    choiceConfidence: 0.6,
    feeOutlierPercentile: 99,
    greenQaSamplePct: 5,
  });

  // Copilot Chat State
  const [chatMessages, setChatMessages] = useState([
    {
      role: 'assistant',
      text: 'Ask ClaimLens Copilot ready. Connected to Foundry Toolbox (`claimlens-rules-mcp`) and Foundry IQ (`ncci-policy-2026`). All tools are strictly read-only.',
      toolCall: null,
      citation: null,
    },
  ]);
  const [chatInput, setChatInput] = useState('');

  const selectedClaim = useMemo(
    () => claims.find((c) => c.id === selectedClaimId) || claims[0],
    [claims, selectedClaimId]
  );

  const triggerToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4500);
  };

  // --- HELPER: Navigate to a specific claim ---
  const openClaim = (claim) => {
    setSelectedClaimId(claim.id);
    if (claim.status === 'NEEDS_FIELD_VERIFICATION') {
      setVerifyUnitsInput(claim.lines[1]?.units || 8);
      setVerifyNpiInput(claim.billing_npi);
      setActiveScreen('verify');
    } else {
      setDetailTab('findings');
      setActiveScreen('detail');
    }
  };

  // --- ACTION: Complete Human Approval Point #1 (Field Verification) ---
  const handleCompleteVerification = () => {
    if (simulateStaleVersion) {
      triggerToast('409 Conflict: Stale row_version detected! Another examiner updated this claim.');
      return;
    }
    const unitsNum = parseInt(verifyUnitsInput, 10) || 1;
    const triggersMue = unitsNum > 4; // MUE for 97140 is 4 units/day

    setClaims((prev) =>
      prev.map((c) => {
        if (c.id !== selectedClaim.id) return c;
        const updatedLines = c.lines.map((l, idx) =>
          idx === 1
            ? {
                ...l,
                units: unitsNum,
                charge: unitsNum * 65.0,
                flags: triggersMue ? ['R2_MUE'] : [],
              }
            : l
        );
        const newFindings = triggersMue
          ? [
              {
                id: 'FND-042-MUE',
                check_id: 'R2_MUE',
                check_type: 'RULE',
                severity: 'HARD',
                line_nos: [2],
                table_version: 'MUE-Practitioner-2026Q4',
                overridden: false,
                details: {
                  code: '97140',
                  mue_value: 4,
                  mai: 2,
                  summed_units_on_dos: unitsNum,
                },
              },
            ]
          : [];

        return {
          ...c,
          billing_npi: verifyNpiInput,
          status: 'READY_FOR_REVIEW',
          bucket: triggersMue ? 'RED' : 'GREEN',
          dollars_at_risk: triggersMue ? unitsNum * 65.0 : 0,
          total_charge: 160.0 + unitsNum * 65.0,
          top_finding: triggersMue ? 'R2_MUE (Units > 4)' : 'NONE (Verified Clean)',
          row_version: c.row_version + 1,
          lines: updatedLines,
          findings: [
            ...newFindings,
            {
              id: 'FND-042-AI',
              check_id: 'AI_DECISION_1',
              check_type: 'AI',
              severity: 'INFO',
              line_nos: [1, 2],
              model_deployment: 'decision1-claimlens',
              question_set_version: 'qset-v1.2',
              details: {
                note_documents_all_services: {
                  type: 'noul',
                  p_true: unitsNum === 2 ? 0.95 : 0.22,
                  status: unitsNum === 2 ? 'GREEN' : 'RED',
                },
                diagnosis_supports_services: {
                  type: 'choice',
                  choice: 'supports',
                  probabilities: { supports: 0.94, does_not_support: 0.03, cannot_tell: 0.03 },
                  status: 'GREEN',
                },
                em_level_consistent: {
                  type: 'choice',
                  choice: 'no_em_service',
                  probabilities: {
                    no_em_service: 0.99,
                    consistent: 0.01,
                    likely_overcoded: 0,
                    likely_undercoded: 0,
                  },
                  status: 'GREEN',
                },
              },
            },
          ],
          memo: {
            model_deployment: triggersMue ? 'chat-claimlens (gpt-5.2)' : 'TEMPLATE (0 LLM Tokens)',
            prompt_version: triggersMue ? 'memo-rag-v1.1' : 'template-green-v1.0',
            validation_passed: true,
            suggested_action: triggersMue ? 'recommend_denial' : 'approve',
            summary: triggersMue
              ? `Examiner verified Line 2 units=${unitsNum}, which exceeds the NCCI MUE limit of 4 units/day for CPT 97140 and conflicts with the 2 units documented in the note.`
              : 'TEMPLATE SUMMARY: Examiner corrected OCR unit count on Line 2 from 8 to 2. All NCCI PTP/MUE rules and Decision-1 documentation checks passed.',
            explanations: [],
          },
          audit_events: [
            ...c.audit_events,
            {
              seq: 1050,
              timestamp: '2026-10-15 09:01:12',
              actor: `examiner:${currentUser.oid.slice(0, 8)} (${currentUser.name})`,
              event_type: 'FIELDS_VERIFIED_RESUMED',
              details: `PATCH /claims/${c.id}/fields (row_version=${c.row_version}->${c.row_version + 1}). Updated Line 2 units to ${unitsNum}. Pipeline completed -> READY_FOR_REVIEW.`,
              prev_hash: c.audit_events[c.audit_events.length - 1]?.hash || '3c9909afec25354d',
              hash: '9e1122bc89f011a4',
            },
          ],
        };
      })
    );

    triggerToast(
      `Fields verified (Line 2 units = ${unitsNum}). Pipeline ran Rules + Decision-1 -> READY_FOR_REVIEW.`
    );
    setActiveScreen('detail');
  };

  // --- ACTION: Examiner Review Decision (Human Approval Point #2) ---
  const handleExaminerReview = (actionType) => {
    if (simulateStaleVersion) {
      triggerToast('409 Conflict: row_version mismatch! Reload claim before submitting review.');
      return;
    }
    if (actionType === 'recommend_denial' && !selectedReasonCode) {
      triggerToast('Error: A standardized Reason Code is required to recommend denial.');
      return;
    }

    const nextStatus =
      actionType === 'approve'
        ? 'APPROVED'
        : actionType === 'request_records'
          ? 'RECORDS_REQUESTED'
          : 'DENIAL_RECOMMENDED';

    setClaims((prev) =>
      prev.map((c) => {
        if (c.id !== selectedClaim.id) return c;
        const lastHash = c.audit_events[c.audit_events.length - 1]?.hash || '00000000';
        return {
          ...c,
          status: nextStatus,
          row_version: c.row_version + 1,
          recommended_by_oid: actionType === 'recommend_denial' ? currentUser.oid : c.recommended_by_oid,
          recommended_by_name:
            actionType === 'recommend_denial'
              ? `${currentUser.name} (${currentUser.role})`
              : c.recommended_by_name,
          recommended_reason: actionType === 'recommend_denial' ? selectedReasonCode : c.recommended_reason,
          recommended_comment: actionComment || `Examiner executed ${actionType}.`,
          audit_events: [
            ...c.audit_events,
            {
              seq: Math.floor(1055 + Math.random() * 900),
              timestamp: '2026-10-15 09:04:30',
              actor: `${currentUser.role.toLowerCase()}:${currentUser.oid.slice(0, 8)} (${currentUser.name})`,
              event_type: nextStatus,
              details: `POST /claims/${c.id}/review -> action=${actionType}${
                actionType === 'recommend_denial' ? `, reason_code=${selectedReasonCode}` : ''
              }. Comment: "${actionComment || 'Standard review completed'}"`,
              prev_hash: lastHash,
              hash: Math.random().toString(16).substring(2, 18),
            },
          ],
        };
      })
    );

    setActionComment('');
    triggerToast(
      nextStatus === 'DENIAL_RECOMMENDED'
        ? `Claim ${selectedClaim.id} moved to DENIAL_RECOMMENDED and routed to Supervisor Inbox.`
        : `Claim ${selectedClaim.id} transitioned to ${nextStatus}.`
    );
  };

  // --- ACTION: Override Individual Finding ---
  const handleToggleOverrideFinding = (findingId) => {
    setClaims((prev) =>
      prev.map((c) => {
        if (c.id !== selectedClaim.id) return c;
        const updatedFindings = c.findings.map((f) =>
          f.id === findingId
            ? {
                ...f,
                overridden: !f.overridden,
                override_reason: !f.overridden
                  ? 'Examiner verified distinct anatomical/clinical documentation'
                  : null,
              }
            : f
        );
        return {
          ...c,
          findings: updatedFindings,
          row_version: c.row_version + 1,
          audit_events: [
            ...c.audit_events,
            {
              seq: Math.floor(1100 + Math.random() * 900),
              timestamp: '2026-10-15 09:05:10',
              actor: `${currentUser.role.toLowerCase()}:${currentUser.oid.slice(0, 8)}`,
              event_type: 'FINDING_OVERRIDE_TOGGLED',
              details: `Toggled override on finding ${findingId}. Logged for disagreement eval set.`,
              prev_hash: c.audit_events[c.audit_events.length - 1]?.hash || '00000000',
              hash: Math.random().toString(16).substring(2, 18),
            },
          ],
        };
      })
    );
    triggerToast(`Finding ${findingId} override recorded in audit trail and added to disagreement eval set.`);
  };

  // --- ACTION: Supervisor Sign-Off (Human Approval Point #3) ---
  const handleSupervisorDecision = (claim, decision) => {
    if (currentUser.role !== 'Supervisor') {
      triggerToast('403 Forbidden: Only users with the Supervisor Entra role can execute sign-off.');
      return;
    }
    if (claim.recommended_by_oid === currentUser.oid) {
      triggerToast('403 Four-Eyes Violation: Supervisor actor_oid cannot equal the Examiner actor_oid.');
      return;
    }

    const nextStatus = decision === 'confirm' ? 'DENIAL_CONFIRMED' : 'READY_FOR_REVIEW';
    setClaims((prev) =>
      prev.map((c) => {
        if (c.id !== claim.id) return c;
        return {
          ...c,
          status: nextStatus,
          row_version: c.row_version + 1,
          audit_events: [
            ...c.audit_events,
            {
              seq: Math.floor(1200 + Math.random() * 900),
              timestamp: '2026-10-15 09:08:00',
              actor: `supervisor:${currentUser.oid.slice(0, 8)} (${currentUser.name})`,
              event_type: nextStatus,
              details:
                decision === 'confirm'
                  ? `Four-eyes check passed (Supervisor ${currentUser.oid.slice(0, 6)} != Examiner ${claim.recommended_by_oid?.slice(0, 6)}). Denial recommendation confirmed.`
                  : 'Supervisor returned claim to READY_FOR_REVIEW queue for additional documentation check.',
              prev_hash: c.audit_events[c.audit_events.length - 1]?.hash || '00000000',
              hash: Math.random().toString(16).substring(2, 18),
            },
          ],
        };
      })
    );

    triggerToast(
      decision === 'confirm'
        ? `Four-eyes check passed! Claim ${claim.id} status -> DENIAL_CONFIRMED.`
        : `Claim ${claim.id} returned to Examiner Queue (READY_FOR_REVIEW).`
    );
  };

  // --- ACTION: Submit New Claim (PDF / JSON / Batch) ---
  const handleCreateClaim = () => {
    const newId = `CLM-2026-00${Math.floor(200 + Math.random() * 700)}`;
    if (submitTab === 'pdf') {
      const isNoisy = pdfScanMode === 'noisy';
      const newClaim = {
        ...CLAIMS_BY_ID['CLM-2026-00042'],
        id: newId,
        external_ref: `CMS1500-PDF-${newId.slice(-3)}`,
        source: 'pdf',
        status: isNoisy ? 'NEEDS_FIELD_VERIFICATION' : 'READY_FOR_REVIEW',
        bucket: isNoisy ? 'PENDING' : 'GREEN',
        top_finding: isNoisy ? 'LOW_CONFIDENCE_EXTRACTION (Box 24G)' : 'NONE (PDF Extracted Clean)',
        created_at: 'Just now',
        age: '1m',
      };
      setClaims([newClaim, ...claims]);
      setSelectedClaimId(newId);
      triggerToast(`202 Accepted: ${newId} uploaded to Blob bills/ and processed by claimlens-cms1500.`);
      setActiveScreen(isNoisy ? 'verify' : 'detail');
    } else if (submitTab === 'json') {
      const template =
        jsonPreset === 'invalid_npi' ? CLAIMS_BY_ID['CLM-2026-00055'] : CLAIMS_BY_ID['CLM-2026-00104'];
      const newClaim = {
        ...template,
        id: newId,
        external_ref: `837P-API-${newId.slice(-3)}`,
        source: 'json',
        created_at: 'Just now',
        age: '1m',
      };
      setClaims([newClaim, ...claims]);
      setSelectedClaimId(newId);
      triggerToast(`202 Accepted: ${newId} normalized to canonical Claim model -> ${newClaim.status}.`);
      setActiveScreen('detail');
    } else {
      triggerToast(
        '202 Accepted { batch_id: "BATCH-GOLD-1000" }: Enqueued 1,000 JSONL claims into PostgreSQL jobs table (SKIP LOCKED).'
      );
      setActiveScreen('dashboard');
    }
  };

  // --- ACTION: Ask ClaimLens Copilot ---
  const handleSendCopilot = (promptText) => {
    const q = promptText || chatInput;
    if (!q.trim()) return;

    const userMsg = { role: 'user', text: q };
    let reply = {
      role: 'assistant',
      text: `For claim ${selectedClaim.id}, I checked the active NCCI v32.3 tables and 2026 Policy Manual. All findings are grounded in versioned reference rows.`,
      toolCall: `get_claim_findings(claim_id="${selectedClaim.id}")`,
      citation: 'NCCI Policy Manual 2026, Ch. I, Sec. A (p. 6)',
    };

    if (q.toLowerCase().includes('97140') || q.toLowerCase().includes('97530')) {
      reply = {
        role: 'assistant',
        text: 'CPT 97530 (Column 1) and CPT 97140 (Column 2) form an active NCCI practitioner PTP edit in v32.3 (effective 2026-10-01) with Modifier Indicator 1. They may only be billed together on the same date of service if performed in separate, distinct 15-minute time increments and reported with an NCCI-associated modifier (such as 59, XE, XS, XP, or XU).',
        toolCall:
          'check_ptp_pair(code1="97530", code2="97140", dos="2026-10-12", modifiers=[]) -> {edit_active: true, indicator: "1", bypassed: false}',
        citation: 'NCCI Policy Manual 2026, Ch. XI, Sec. M (p. 112) [chunk_id: ncci-2026-ch11-secM-p112]',
      };
    } else if (q.toLowerCase().includes('indicator 0') || q.toLowerCase().includes('29881')) {
      reply = {
        role: 'assistant',
        text: 'CPT 29881 (Column 1) and CPT 29877 (Column 2) carry Modifier Indicator 0 in NCCI PTP v32.3. Even though Modifier 59 was submitted on Line 2, NCCI rules strictly prohibit any modifier from bypassing a Column 1/Column 2 edit when the modifier indicator is 0.',
        toolCall:
          'check_ptp_pair(code1="29881", code2="29877", dos="2026-10-12", modifiers=["59","RT"]) -> {edit_active: true, indicator: "0", bypassed: false}',
        citation: 'NCCI Policy Manual 2026, Ch. I, Sec. E (p. 18) & Ch. IV, Sec. F (p. 44)',
      };
    } else if (q.toLowerCase().includes('mue') || q.toLowerCase().includes('11721')) {
      reply = {
        role: 'assistant',
        text: 'CPT 11721 has a Practitioner MUE limit of 1 unit per day with MAI = 2 (Date of Service Edit: Policy). Because MAI is 2, the worker sums units across all claim lines on the same date of service for the same patient and rendering NPI.',
        toolCall: 'get_mue(code="11721") -> {mue_value: 1, mai: 2, table_version: "MUE-Practitioner-2026Q4"}',
        citation: 'NCCI Policy Manual 2026, Ch. III, Sec. C (p. 31)',
      };
    }

    setChatMessages((prev) => [...prev, userMsg, reply]);
    setChatInput('');
  };

  // Derived data
  const filteredClaims = useMemo(
    () => filterClaims(claims, { bucketFilter, statusFilter, checkFilter, searchQuery }),
    [claims, bucketFilter, statusFilter, checkFilter, searchQuery]
  );

  const supervisorQueue = useMemo(() => claims.filter((c) => c.status === 'DENIAL_RECOMMENDED'), [claims]);

  const value = {
    // auth / navigation
    isLoggedIn,
    setIsLoggedIn,
    currentRole,
    setCurrentRole,
    currentUser,
    activeScreen,
    setActiveScreen,
    // claims
    claims,
    setClaims,
    selectedClaimId,
    setSelectedClaimId,
    selectedClaim,
    filteredClaims,
    supervisorQueue,
    // ui chrome
    copilotOpen,
    setCopilotOpen,
    showDemoBar,
    setShowDemoBar,
    toastMessage,
    setToastMessage,
    triggerToast,
    // queue filters
    bucketFilter,
    setBucketFilter,
    statusFilter,
    setStatusFilter,
    checkFilter,
    setCheckFilter,
    searchQuery,
    setSearchQuery,
    // claim detail
    detailTab,
    setDetailTab,
    selectedReasonCode,
    setSelectedReasonCode,
    actionComment,
    setActionComment,
    simulateStaleVersion,
    setSimulateStaleVersion,
    // field verification
    verifyUnitsInput,
    setVerifyUnitsInput,
    verifyNpiInput,
    setVerifyNpiInput,
    // submit
    submitTab,
    setSubmitTab,
    pdfScanMode,
    setPdfScanMode,
    jsonPreset,
    setJsonPreset,
    // dashboard thresholds
    thresholds,
    setThresholds,
    // copilot chat
    chatMessages,
    setChatMessages,
    chatInput,
    setChatInput,
    // actions
    openClaim,
    handleCompleteVerification,
    handleExaminerReview,
    handleToggleOverrideFinding,
    handleSupervisorDecision,
    handleCreateClaim,
    handleSendCopilot,
  };

  return <ClaimLensContext.Provider value={value}>{children}</ClaimLensContext.Provider>;
}
