import { useContext } from 'react';
import { ClaimLensContext } from './ClaimLensContext';

export function useClaimLens() {
  const ctx = useContext(ClaimLensContext);
  if (!ctx) throw new Error('useClaimLens must be used inside <ClaimLensProvider>');
  return ctx;
}
