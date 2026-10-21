import { useClaimLens } from './context/useClaimLens';
import LoginScreen from './screens/LoginScreen';
import SyntheticBanner from './components/layout/SyntheticBanner';
import DemoWalkthroughBar from './components/layout/DemoWalkthroughBar';
import Header from './components/layout/Header';
import Toast from './components/layout/Toast';
import QueueScreen from './screens/queue/QueueScreen';
import SubmitScreen from './screens/submit/SubmitScreen';
import VerifyScreen from './screens/verify/VerifyScreen';
import ClaimDetailScreen from './screens/detail/ClaimDetailScreen';
import SupervisorScreen from './screens/supervisor/SupervisorScreen';
import DashboardScreen from './screens/dashboard/DashboardScreen';
import CopilotDrawer from './features/copilot/CopilotDrawer';

// Screen registry: the single place that maps `activeScreen` to a component.
const SCREENS = {
  queue: QueueScreen,
  submit: SubmitScreen,
  verify: VerifyScreen,
  detail: ClaimDetailScreen,
  supervisor: SupervisorScreen,
  dashboard: DashboardScreen,
};

export default function AppShell() {
  const { isLoggedIn, activeScreen } = useClaimLens();

  if (!isLoggedIn || activeScreen === 'login') return <LoginScreen />;

  const Screen = SCREENS[activeScreen] ?? QueueScreen;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      <SyntheticBanner />
      <DemoWalkthroughBar />
      <Header />
      <Toast />
      <div className="flex-1 flex overflow-hidden">
        <main className="flex-1 overflow-y-auto p-6">
          <Screen />
        </main>
        <CopilotDrawer />
      </div>
    </div>
  );
}
