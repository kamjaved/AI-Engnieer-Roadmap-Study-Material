import StateMachineStepper from './StateMachineStepper';
import ClaimHeaderCard from './ClaimHeaderCard';
import ValidationErrorsBanner from './ValidationErrorsBanner';
import PromptShieldAlert from './PromptShieldAlert';
import ServiceLinesTable from './ServiceLinesTable';
import EncounterNotePanel from './EncounterNotePanel';
import AnalysisPanel from './AnalysisPanel';
import ExaminerActionBar from './ExaminerActionBar';

/** Claim review (§3.5 #5, F9, F10, F11 - HITL Point #2). */
export default function ClaimDetailScreen() {
  return (
    <div className="max-w-7xl mx-auto space-y-5">
      <StateMachineStepper />
      <ClaimHeaderCard />
      <ValidationErrorsBanner />
      <PromptShieldAlert />
      <ServiceLinesTable />

      {/* Lower split: left = encounter note, right = findings / memo / audit tabs */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <EncounterNotePanel />
        <AnalysisPanel />
      </div>

      <ExaminerActionBar />
    </div>
  );
}
