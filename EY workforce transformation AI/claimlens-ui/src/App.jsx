import { ClaimLensProvider } from './context/ClaimLensProvider';
import AppShell from './AppShell';

export default function App() {
  return (
    <ClaimLensProvider>
      <AppShell />
    </ClaimLensProvider>
  );
}
