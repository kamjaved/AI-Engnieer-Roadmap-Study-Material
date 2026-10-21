// Pure filter used by the Work Queue (moved out of the original App component, logic unchanged).
export function filterClaims(claims, { bucketFilter, statusFilter, checkFilter, searchQuery }) {
  return claims.filter((c) => {
    if (bucketFilter !== 'ALL' && c.bucket !== bucketFilter) return false;
    if (statusFilter !== 'ALL' && c.status !== statusFilter) return false;
    if (checkFilter !== 'ALL') {
      const hasCheck =
        c.findings.some((f) => f.check_id === checkFilter) || c.top_finding.includes(checkFilter);
      if (!hasCheck) return false;
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const match =
        c.id.toLowerCase().includes(q) ||
        c.patient_token.toLowerCase().includes(q) ||
        c.billing_npi.includes(q) ||
        c.top_finding.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });
}
