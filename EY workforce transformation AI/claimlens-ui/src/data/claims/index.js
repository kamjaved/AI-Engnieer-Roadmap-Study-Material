import { claim00042 } from './claim00042';
import { claim00104 } from './claim00104';
import { claim00108 } from './claim00108';
import { claim00112 } from './claim00112';
import { claim00119 } from './claim00119';
import { claim00089 } from './claim00089';
import { claim00055 } from './claim00055';

// One synthetic claim per scenario in the blueprint. The order is the order shown in the queue.
// When the real FastAPI backend exists, replace this module with an API call (see README, "Next steps").
export const INITIAL_CLAIMS = [
  claim00042,
  claim00104,
  claim00108,
  claim00112,
  claim00119,
  claim00089,
  claim00055,
];

// Look claims up by id instead of array position, so re-ordering the array cannot break the presets.
export const CLAIMS_BY_ID = Object.fromEntries(INITIAL_CLAIMS.map((c) => [c.id, c]));
