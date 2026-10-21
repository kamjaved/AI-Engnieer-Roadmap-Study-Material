import { useClaimLens } from '../../context/useClaimLens';

export default function JsonPasteTab() {
  const { jsonPreset, setJsonPreset } = useClaimLens();

  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-semibold text-slate-700">
          POST /claims (Canonical Pydantic v2 Claim Schema):
        </span>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setJsonPreset('ptp_error')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-xl border transition cursor-pointer ${
              jsonPreset === 'ptp_error'
                ? 'bg-indigo-600 text-white border-indigo-600'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            Preset 1: Valid Schema + Planted E1 PTP Error
          </button>
          <button
            onClick={() => setJsonPreset('invalid_npi')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-xl border transition cursor-pointer ${
              jsonPreset === 'invalid_npi'
                ? 'bg-indigo-600 text-white border-indigo-600'
                : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
            }`}
          >
            Preset 2: Invalid Luhn NPI + Future Date (REJECTED_INVALID)
          </button>
        </div>
      </div>

      <textarea
        readOnly
        rows={12}
        value={
          jsonPreset === 'ptp_error'
            ? JSON.stringify(
                {
                  external_ref: '837P-SYN-00291',
                  patient_token: 'SYN-PT-44219',
                  billing_npi: '1457392815',
                  dos_from: '2026-10-12',
                  dos_to: '2026-10-12',
                  total_charge: 700.0,
                  lines: [
                    {
                      line_no: 1,
                      dos: '2026-10-12',
                      place_of_service: '11',
                      code: '29881',
                      modifiers: ['RT'],
                      units: 1,
                      charge: 390.0,
                      dx_codes: ['M23.211'],
                      rendering_npi: '1457392815',
                    },
                    {
                      line_no: 2,
                      dos: '2026-10-12',
                      place_of_service: '11',
                      code: '29877',
                      modifiers: ['59', 'RT'],
                      units: 1,
                      charge: 310.0,
                      dx_codes: ['M23.211'],
                      rendering_npi: '1457392815',
                    },
                  ],
                  encounter_note:
                    'Right knee arthroscopy with medial meniscectomy and articular cartilage shaving in same compartment.',
                },
                null,
                2
              )
            : JSON.stringify(
                {
                  external_ref: '837P-BAD-00055',
                  patient_token: 'SYN-PT-00491',
                  billing_npi: '1234567890',
                  dos_from: '2026-11-05',
                  dos_to: '2026-11-05',
                  total_charge: 210.0,
                  lines: [
                    {
                      line_no: 1,
                      dos: '2026-11-05',
                      place_of_service: '11',
                      code: '99213',
                      modifiers: [],
                      units: 1,
                      charge: 210.0,
                      dx_codes: ['Z99.999'],
                      rendering_npi: '1234567890',
                    },
                  ],
                },
                null,
                2
              )
        }
        className="w-full font-mono text-xs p-4 bg-slate-950 text-emerald-400 border border-slate-800 rounded-2xl shadow-inner"
      />
    </>
  );
}
