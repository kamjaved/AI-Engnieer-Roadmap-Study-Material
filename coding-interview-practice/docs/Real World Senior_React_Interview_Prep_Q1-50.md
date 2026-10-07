# Senior React / Front-End Interview Prep — Answered Questions

**Complete edition · All 50 questions answered · Research notes and sources at the end**

Target: 4–<8 YOE Senior / Senior 1 / Senior 2 React and Front-End roles at service, Big Four, consulting and large-tech companies (TCS, Infosys, Accenture, Capgemini, Cognizant, EY, Deloitte, IBM, LTIMindtree, KPMG, Microsoft). Every question comes from first-hand candidate reports (Glassdoor, GeeksforGeeks, LeetCode Discuss, Medium write-ups, Fishbowl, FrontendLead, Naukri). Sources are listed at the end.

---

## How to use this document

**Priority legend**

| Label | Meaning |
|---|---|
| 🔥 Very High | 5+ independent reports, high confidence — expect it in almost every screen |
| ⭐ High | 3–4+ reports or high confidence — very likely |
| 🟡 Medium | 1–3 reports, often a senior-depth follow-up or company-specific |
| ⚪ Low | single weak source |

**Answer style.** Each answer is written the way I would say it to the interviewer — first person, definition first, then the practical detail and the trade-off that signals seniority. "Likely follow-ups" lists what interviewers pushed on in the source reports or what naturally comes next.

**What the research says interviewers reward at 4–<8 YOE**

- A crisp definition in one or two sentences, then a real use case — not a recited textbook paragraph.
- Follow-up depth: "what is caching?", "is caching always beneficial?", "what if `flat()` isn't available?", "how do you prevent a race condition?". This is where senior candidates separate themselves.
- Output-prediction fluency (hoisting, closures, event loop) — service companies use these as fast filters.
- Clean live code for small tasks: fetch-and-render, debounced search, counter, flatten, string manipulation.

**Typical round structure (service / Big Four):** Round 1 is 45–60 minutes of JS theory + React theory + output snippets + one or two small coding problems. Later rounds add scenario, managerial and architecture questions. Microsoft-tier companies lean on live machine-coding instead.

---

## Quick index (Q1–50)

| # | Question | Priority | Area |
|---|---|---|---|
| 1 | What is a closure? | 🔥 Very High | JavaScript |
| 2 | Deep copy vs shallow copy | 🔥 Very High | JavaScript |
| 3 | useMemo vs useCallback (+ caching follow-ups) | 🔥 Very High | React hooks |
| 4 | Prevent an API call on every keystroke / debounce | ⭐ High | React practical |
| 5 | Prop drilling and Context API | ⭐ High | React state |
| 6 | Hoisting, var/let/const, TDZ | ⭐ High | JavaScript |
| 7 | Promises, Promise.all / race / allSettled | ⭐ High | JavaScript async |
| 8 | React performance optimization techniques | ⭐ High | React performance |
| 9 | useEffect, cleanup, dependency array | ⭐ High | React hooks |
| 10 | useState vs useRef | 🟡 Medium | React hooks |
| 11 | Fetch API data and display it in a table | ⭐ High | Live coding |
| 12 | Controlled vs uncontrolled components | 🟡 Medium | React forms |
| 13 | Higher-Order Components and PureComponent | 🟡 Medium | React patterns |
| 14 | Redux: why, flow, useSelector/useDispatch, Saga | ⭐ High | State management |
| 15 | Functional vs class components, lifecycle | 🟡 Medium | React fundamentals |
| 16 | Lazy loading and code splitting | ⭐ High | React performance |
| 17 | Event loop, microtasks vs macrotasks | ⭐ High | JavaScript async |
| 18 | null vs undefined vs not defined, typeof null | 🟡 Medium | JavaScript |
| 19 | Custom hooks | 🟡 Medium | React hooks |
| 20 | Cancel an API call (AbortController) | 🟡 Medium | React / JS practical |
| 21 | Parallel API calls; dynamic endpoint from user input | 🟡 Medium | Scenario |
| 22 | Flatten a nested array (without flat()) | 🟡 Medium | Coding |
| 23 | Reverse a string / words; remove duplicates | ⭐ High | Coding |
| 24 | Auto-increment / increment–decrement counter | 🟡 Medium | Live coding |
| 25 | Spread vs rest operator | 🟡 Medium | JavaScript |
| 26 | Prototype inheritance and lexical scoping | 🟡 Medium | JavaScript |
| 27 | Throttling (+ debounce/throttle polyfill) | 🟡 Medium | JavaScript performance |
| 28 | useEffect vs useLayoutEffect; useImperativeHandle | 🟡 Medium | React hooks |
| 29 | Nested routes, Outlet, query params | 🟡 Medium | Routing |
| 30 | type vs interface, typing objects, generics, null vs unknown | 🟡 Medium | TypeScript |
| 31 | Access a child's state from the parent | 🟡 Medium | React data flow |
| 32 | Stale closures and race conditions in useEffect | 🟡 Medium | React hooks |
| 33 | Strict Mode double effects, batching, flushSync | 🟡 Medium | React 18 |
| 34 | Virtual DOM, diffing, reconciliation, Fiber | 🟡 Medium | React internals |
| 35 | Core Web Vitals; Web Components | 🟡 Medium | Browser / performance |
| 36 | Focus an input on first render without onFocus | 🟡 Medium | React practical |
| 37 | CSR vs SSR vs SSG, hydration | 🟡 Medium | Rendering architecture |
| 38 | Design a loan-management dashboard | 🟡 Medium | Scenario / design |
| 39 | Micro-frontends; reuse payment logic in mobile | 🟡 Medium | Architecture |
| 40 | Implement reduce() from scratch | 🟡 Medium | Coding |
| 41 | Live machine-coding: Todo, newsfeed, number pad, nav | ⭐ High | Machine coding |
| 42 | Tell me about yourself / current project | 🔥 Very High | Behavioral |
| 43 | setState in render; setState callback | 🟡 Medium | React fundamentals |
| 44 | Error boundaries | ⚪ Low–Medium | React fundamentals |
| 45 | React Portals | 🟡 Medium | React patterns |
| 46 | Currying: sum(3)(5)(7)(3)() | 🟡 Medium | Coding |
| 47 | Unique elements without Set; 2nd & 3rd largest | 🟡 Medium | Coding |
| 48 | Redux createStore syntax; store and routes | 🟡 Medium | State management |
| 49 | map, filter, reduce; copying objects | 🟡 Medium | JavaScript |
| 50 | Center a div with flex and grid | 🟡 Medium | CSS |

---

## Answers

### Q1. "What is a closure?" (often followed by "give a practical use case of closures")

> **Priority:** 🔥 Very High · 6+ independent reports · Confidence: High
> **Where asked:** Round 1 JS fundamentals at IBM/Coforge/LTIMindtree (5+ YOE), Capgemini Senior FE, Accenture, Cognizant, Deloitte, TCS. Capgemini followed up with "practical use case"; a live code example is usually requested.

**My answer**

A closure is a function bundled together with the lexical scope it was created in. When I define a function inside another function, the inner function keeps a live reference to the outer function's variables — not a copy — even after the outer function has returned. That works because JavaScript is lexically scoped: what a function can see is decided by where it is written, not where it is called.

```js
function createCounter() {
  let count = 0; // private: nothing outside can touch it directly

  return {
    increment: () => ++count,
    getValue: () => count,
  };
}

const counter = createCounter();
counter.increment();
counter.increment();
counter.getValue(); // 2
```

Where I actually use closures:

- **Encapsulation / private state** — factory functions and the module pattern, as above.
- **Debounce and throttle** — the timer ID lives in the closure between calls (see Q4).
- **Memoization** — the cache object is closed over by the memoized function.
- **Function factories and partial application** — `const logAuth = createLogger('auth')`.
- **React itself** — every event handler and effect closes over the props and state of the render that created it.

Two points I'd add to show depth:

1. **Closures capture variables by reference.** That is why this classic snippet prints `3 3 3` with `var` (one shared binding) but `0 1 2` with `let` (a new binding per iteration):

   ```js
   for (var i = 0; i < 3; i++) setTimeout(() => console.log(i), 0); // 3 3 3
   for (let j = 0; j < 3; j++) setTimeout(() => console.log(j), 0); // 0 1 2
   ```

2. **Stale closures in React.** A `setInterval` inside `useEffect(..., [])` keeps seeing the first render's state forever. I fix it with functional updates (`setCount(c => c + 1)`), correct dependencies, or a ref holding the latest value.

There's also a memory angle: a closure keeps its outer scope alive, so a long-lived listener that closes over a large object prevents garbage collection. That's one reason effect cleanup matters.

**Likely follow-ups:** "Fix the `var` loop without `let`" (wrap in an IIFE that receives `i`). "What is a stale closure in React?" (Q32). "Implement memoize / debounce using closures."

---

### Q2. "Difference between deep copy and shallow copy?" (+ "how do you achieve a deep copy?")

> **Priority:** 🔥 Very High · 5+ reports · Confidence: High
> **Where asked:** Round 1 JS theory at Capgemini Senior FE, EY FE (verbatim, including "how can we achieve deep copy"), IBM/Coforge/LTIMindtree (5+ YOE), Cognizant.

**My answer**

A shallow copy creates a new top-level container, but nested objects are still shared references. A deep copy recursively copies everything, so the copy shares nothing with the original.

```js
const user = { name: 'Asha', address: { city: 'Pune' } };

const shallow = { ...user };
shallow.address.city = 'Delhi';
console.log(user.address.city); // 'Delhi' — nested object is shared

const deep = structuredClone(user);
deep.address.city = 'Mumbai';
console.log(user.address.city); // still 'Delhi'
```

How I create each, and the catches:

| Technique | Depth | Caveats |
|---|---|---|
| `{ ...obj }`, `[...arr]`, `Object.assign`, `arr.slice()`, `Array.from` | Shallow | Only the top level is new |
| `JSON.parse(JSON.stringify(x))` | Deep | Drops `undefined` and functions, turns `Date` into a string, `NaN`/`Infinity` into `null`, `Map`/`Set` into `{}`, throws on circular references |
| `structuredClone(x)` | Deep | Native; handles `Date`, `Map`, `Set`, typed arrays and circular references. Throws `DataCloneError` on functions and DOM nodes; class instances lose their prototype |
| `lodash.cloneDeep` | Deep | Handles most cases, but adds a dependency |
| Custom recursive function | Deep | Must handle cycles (`WeakMap`) and special types yourself |

If asked to write one:

```js
function deepClone(value, seen = new WeakMap()) {
  if (value === null || typeof value !== 'object') return value; // primitives
  if (seen.has(value)) return seen.get(value);                   // circular refs
  if (value instanceof Date) return new Date(value.getTime());

  const copy = Array.isArray(value) ? [] : {};
  seen.set(value, copy);
  for (const key of Object.keys(value)) {
    copy[key] = deepClone(value[key], seen);
  }
  return copy;
}
```

The senior point: in React and Redux I almost never deep-clone state. I do **immutable updates with structural sharing** — copy only the path that changed — so unchanged subtrees keep their reference identity and `React.memo` and memoized selectors can skip work. Deep-cloning the whole state is slower and defeats those optimizations. For deeply nested updates I use Immer (built into Redux Toolkit).

```js
setUser(prev => ({ ...prev, address: { ...prev.address, city: 'Mumbai' } }));
```

**Likely follow-ups:** "Is spread a deep copy?" (no). "Why does mutating state not re-render?" (same reference, React bails out). "What does JSON clone lose?"

---

### Q3. "Difference between useMemo and useCallback?" (+ "what is caching?", "is caching always beneficial?")

> **Priority:** 🔥 Very High · 5+ reports · Confidence: High
> **Where asked:** React section of the technical round at Capgemini Senior FE (with layered caching follow-ups), EY (two separate reports), IBM. Variant: "React.memo vs useMemo".

**My answer**

Both cache something between renders and recompute only when a dependency changes (compared with `Object.is`). `useMemo` caches the **result** of a function; `useCallback` caches the **function itself**. In fact `useCallback(fn, deps)` is the same as `useMemo(() => fn, deps)`.

```tsx
const visibleTodos = useMemo(
  () => filterTodos(todos, filter), // expensive derivation
  [todos, filter],
);

const handleToggle = useCallback((id: string) => {
  setTodos(prev => prev.map(t => (t.id === id ? { ...t, done: !t.done } : t)));
}, []); // functional update means no dependency on `todos`

return <TodoList items={visibleTodos} onToggle={handleToggle} />; // TodoList is React.memo'd
```

When I reach for them:

- **useMemo** — a genuinely expensive computation (sorting or filtering thousands of rows), or when I need a stable object/array reference for a memoized child, a context value, or another hook's dependency list.
- **useCallback** — a callback passed to a `React.memo` child, or a function used as a dependency of `useEffect` or another hook.
- **React.memo vs useMemo** — `React.memo` memoizes a *component* (skips re-render when props are shallowly equal); `useMemo` memoizes a *value* inside a component. They work as a team: `useMemo`/`useCallback` mostly exist so `React.memo`'s shallow comparison succeeds.

**"What is caching?"** — Storing the result of an expensive operation keyed by its inputs, so a later request with the same inputs is served without redoing the work. Memoization is caching function results by arguments. `useMemo` is effectively a cache of size one per component instance, keyed on the dependency array.

**"Is caching always beneficial?"** — No:

- It costs memory plus a dependency comparison every render. For cheap work, memoizing is slower than recomputing.
- `useCallback` without a memoized consumer does nothing useful — the child re-renders anyway.
- Unstable dependencies (an inline object) mean the cache misses every time — pure overhead. Missing dependencies are worse: stale data, a correctness bug.
- Invalidation is the hard part at every layer — HTTP cache, CDN, query cache — serving stale data is a real failure mode.
- React treats `useMemo` as a performance hint, not a semantic guarantee; it may discard the cache.

So I profile with React DevTools first and memoize where it measurably helps. On codebases that adopt the React Compiler (v1.0 released in 2025), memoization is inserted automatically at build time, so manual `useMemo`/`useCallback` becomes mostly unnecessary — but I still need to understand it for existing code.

**Likely follow-ups:** "Why does a memoized child still re-render?" (new inline props or context change). "What is referential equality?"

---

### Q4. "How do you prevent an API call on every keystroke?" / "How to debounce?"

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** Accenture (exact scenario: typing "Apple" fires an API call per keystroke), Infosys, echoed in EY and TCS-tier reports. Usually leads to live coding with `useEffect` + `setTimeout`.

**My answer**

Typing "Apple" fires five requests, and they can resolve out of order, so a slow response for "App" may overwrite the results for "Apple". I solve it with two things: **debounce** the input so the request fires only after the user pauses (around 300 ms), and **cancel stale requests** so only the latest response can update the UI.

A reusable hook that debounces a value:

```tsx
import { useEffect, useState } from 'react';

export function useDebouncedValue<T>(value: T, delayMs = 300): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timerId = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(timerId); // every keystroke resets the timer
  }, [value, delayMs]);

  return debouncedValue;
}
```

Using it with request cancellation:

```tsx
const MIN_QUERY_LENGTH = 2;
const SEARCH_DEBOUNCE_MS = 300;

function ProductSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);
  const debouncedQuery = useDebouncedValue(query.trim(), SEARCH_DEBOUNCE_MS);

  useEffect(() => {
    if (debouncedQuery.length < MIN_QUERY_LENGTH) {
      setResults([]);
      return;
    }
    const controller = new AbortController();
    const params = new URLSearchParams({ q: debouncedQuery });

    fetch(`/api/products?${params}`, { signal: controller.signal })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<Product[]>;
      })
      .then(data => { setResults(data); setError(null); })
      .catch(err => {
        if (err.name !== 'AbortError') setError(err.message);
      });

    return () => controller.abort(); // a newer query cancels the older request
  }, [debouncedQuery]);

  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} aria-label="Search products" />
      {error && <p role="alert">{error}</p>}
      <ul>{results.map(p => <li key={p.id}>{p.name}</li>)}</ul>
    </>
  );
}
```

If they want plain JavaScript:

```js
function debounce(fn, delayMs) {
  let timerId;
  return function (...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => fn.apply(this, args), delayMs);
  };
}
```

Common mistake I call out: writing `const debouncedSearch = debounce(search, 300)` directly in the component body. It's recreated on every render, so the timer is lost and nothing is debounced. It must be stable (`useMemo`/`useRef`) — or debounce the value as I did above.

Trade-offs and production touches:

- Delay: too long feels laggy, too short doesn't help. 250–400 ms is typical.
- **Debounce vs throttle:** debounce fires after a quiet period (search, autosave, resize end); throttle fires at most once per interval (scroll, mousemove).
- Minimum query length and trimming avoid useless requests.
- In production I'd use TanStack Query with `queryKey: ['products', debouncedQuery]`: it caches results (backspacing to "App" is instant), dedupes, and passes an abort `signal` automatically. The backend should still rate-limit.
- `useDeferredValue` keeps typing responsive when *rendering* results is expensive, but on its own it does not reduce network calls.

**Likely follow-ups:** "Implement throttle" (Q27). "How do you handle out-of-order responses?" (abort, or ignore with a flag). "How would you cache results?"

---

### Q5. "What is prop drilling and how do you avoid it?" / "What is the Context API?"

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** Accenture (both parts), EY ("what problems does it create?"), Cognizant, EY ("What is ContextAPI?"). Context is the expected answer; Redux/Zustand is the scale follow-up.

**My answer**

Prop drilling is passing data through intermediate components that don't use it, just so a deeply nested descendant can get it. The problems: tight coupling (every intermediate component's API changes when the leaf needs something new), noisy code, harder refactors, and it's hard to see where data actually comes from. That said, two or three levels of explicit props is fine — it's explicit and easy to trace.

How I avoid it, in the order I reach for options:

1. **Component composition.** Pass `children` or elements as props so the component that owns the data renders the leaf directly. This often removes drilling with no global state at all.
2. **Context API** for low-frequency, widely-needed data: auth user, theme, locale, feature flags.
3. **A state library** (Redux Toolkit, Zustand) for frequently updated, complex shared client state that needs selectors.
4. **Server data** belongs in TanStack Query or RTK Query, not in Context.

Context is three pieces: create it, provide a value high in the tree, consume it anywhere below. I always wrap it in a custom hook:

```tsx
type AuthContextValue = { user: User | null; logout: () => void };

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const logout = useCallback(() => setUser(null), []);
  const value = useMemo(() => ({ user, logout }), [user, logout]); // stable identity

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used inside <AuthProvider>');
  return context;
}
```

Senior caveats I mention:

- Context is a **dependency-injection mechanism, not a state manager**. Every consumer re-renders when the value changes, and there are no selectors. One giant `AppContext` holding fast-changing values re-renders half the app.
- Mitigations: split contexts by concern and update frequency (e.g. separate state and dispatch contexts), memoize the provider value, keep providers as low as possible.
- React 19 lets you render `<AuthContext value={value}>` directly instead of `.Provider`, and the `use(AuthContext)` API can be called conditionally.

**Likely follow-ups:** "Context vs Redux — when which?" "Why do all consumers re-render?" "Lifting state up — when and why?" (Q31).

---

### Q6. "What is hoisting?" (+ output prediction with var/let/const, Temporal Dead Zone)

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** Capgemini Senior FE ("var, let, const, TDZ"), Accenture (three output questions), Deloitte, EY (two output questions). Expect code-output prediction.

**My answer**

Before executing a scope, the engine runs a creation phase that registers all declarations in that scope. That's what we call hoisting. Declarations are registered but not moved, and different declaration types are initialized differently:

| Declaration | Scope | Initialized at creation to | Access before the line |
|---|---|---|---|
| `var` | Function | `undefined` | Returns `undefined` |
| `let` / `const` | Block | Nothing — in the TDZ | `ReferenceError` |
| Function declaration | Function | The full function | Works |
| `var fn = function () {}` / arrow | Function | `undefined` (only the var) | `TypeError: fn is not a function` |
| `class` | Block | Nothing — in the TDZ | `ReferenceError` |

The **Temporal Dead Zone** is the span from the start of the block until the `let`/`const`/`class` line executes. The binding exists — it's hoisted — but can't be read yet. This snippet proves `let` is hoisted: if it weren't, the inner `console.log` would read the outer `x`.

```js
let x = 1;
(function () {
  console.log(x); // ReferenceError: Cannot access 'x' before initialization
  let x = 2;
})();
```

Typical output questions (all verified):

```js
console.log(a);   // undefined
var a = 5;

greet();          // works — function declarations are fully hoisted
function greet() { console.log('hi'); }

bar();            // TypeError: bar is not a function
var bar = function () {};

console.log(typeof f); // 'function' — the declaration wins at creation time;
var f = 1;             // the assignment only happens when this line runs
function f() {}
```

Beyond hoisting, the other `var`/`let`/`const` differences: `var` allows redeclaration and, at the top level of a classic script, becomes a property of `window`; `let`/`const` don't. `const` prevents reassignment, not mutation — `const arr = []; arr.push(1)` is fine. And the loop + `setTimeout` difference from Q1.

In practice I use `const` by default, `let` only when I reassign, and never `var`, enforced with ESLint `no-var` and `prefer-const`.

**Likely follow-ups:** "Is `let` hoisted?" (yes, but in the TDZ). "Are arrow functions hoisted?" "What does `const` actually freeze?"

---

### Q7. "Explain promises" / "Difference between Promise.all(), Promise.race() and Promise.allSettled()"

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** Capgemini (`all` vs `race`), EY (`allSettled` vs `race`, plus "what is a Promise? give pseudocode"), Accenture ("how promises work"), TCS-tier.

**My answer**

A Promise is an object representing the eventual result of an asynchronous operation. It starts `pending` and settles exactly once to `fulfilled` (with a value) or `rejected` (with a reason) — after that it's immutable. `.then`/`.catch`/`.finally` register reactions, which run as **microtasks**. `async/await` is syntax on top of promises.

Pseudocode for creating one:

```js
function fetchUser(userId) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    request.open('GET', `/api/users/${userId}`);
    request.onload = () =>
      request.status === 200
        ? resolve(JSON.parse(request.responseText))
        : reject(new Error(`HTTP ${request.status}`));
    request.onerror = () => reject(new Error('Network error'));
    request.send();
  });
}

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
```

The combinators:

| Method | Fulfills when | Rejects when | Where I use it |
|---|---|---|---|
| `Promise.all` | All fulfill → values in input order | First rejection (fail-fast) | Everything is required: a page needs user, permissions and config |
| `Promise.allSettled` | All settle → `{ status, value \| reason }[]` | Never | Independent widgets on a dashboard; batch jobs with partial-failure reporting |
| `Promise.race` | First promise to settle, either way | If the first to settle rejects | Timeouts |
| `Promise.any` | First fulfillment | All reject → `AggregateError` | Fastest of several mirrors |

```js
// Independent dashboard widgets: render what succeeded, show errors for the rest
const [salesResult, ordersResult] = await Promise.allSettled([fetchSales(), fetchOrders()]);
if (salesResult.status === 'fulfilled') renderSales(salesResult.value);
else showWidgetError('sales', salesResult.reason);

// Timeout with race
const timeout = ms => new Promise((_, reject) => setTimeout(() => reject(new Error('Request timed out')), ms));
const data = await Promise.race([fetchReport(), timeout(5000)]);
```

The point I make about `race` and `all`: **they don't cancel the losers**. The slower requests keep running. For real cancellation I use `AbortController`, and for timeouts specifically `fetch(url, { signal: AbortSignal.timeout(5000) })`.

Common mistakes: forgetting to `return` inside a `.then` chain, `await` inside a loop for independent calls (serializes them), `async` callbacks in `forEach` (it doesn't wait), and unhandled rejections.

**Likely follow-ups:** "Promise vs callback" (inversion of control, chaining, error propagation). "Implement `Promise.all`." "Output order of promise vs setTimeout" (Q17).

---

### Q8. "What are the performance optimization techniques in React?"

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** Accenture (full list expected), Infosys, EY ("how to prevent unnecessary re-rendering?"), IBM.

**My answer**

I always start with **measure, then fix**: React DevTools Profiler (with "why did this render"), the Chrome Performance panel, Lighthouse and Core Web Vitals (LCP, INP, CLS), and a bundle analyzer. Then I group fixes by what's actually slow.

**1. Load performance — how fast it shows up**
- Route-level code splitting with `React.lazy` + `Suspense`; dynamic `import()` for heavy libraries such as charts or rich-text editors (Q16).
- Bundle hygiene: tree-shaking, avoiding barrel-file imports, replacing heavy dependencies.
- Images: correct sizes, WebP/AVIF, `loading="lazy"` below the fold, explicit width/height to avoid layout shift.
- SSR/SSG or Server Components (e.g. Next.js) to improve LCP; CDN caching and compression.

**2. Render performance — how much work each update does**
- **State colocation** — keep state as low in the tree as possible. Most "unnecessary re-render" problems are state placed too high.
- `React.memo` on expensive children, with stable props via `useCallback`/`useMemo`.
- Stable, unique keys — not array indexes for lists that reorder.
- **Virtualization** for long lists and tables (TanStack Virtual, react-window): render only visible rows.
- Compute derived data during render instead of syncing it into state with an effect (avoids an extra render).
- Split contexts so a fast-changing value doesn't re-render every consumer.
- `useTransition` / `useDeferredValue` to keep input responsive while a heavy update renders.

**3. Interaction and runtime**
- Debounce/throttle high-frequency events (Q4).
- Move CPU-heavy work to a Web Worker; break up long tasks so the main thread can respond.

**4. Data**
- A query cache (TanStack Query / RTK Query) for deduping and caching, plus pagination and prefetching.

For "how do you prevent unnecessary re-rendering?" I first explain **why** a component re-renders: its own state changed, its parent re-rendered, or a context it reads changed. Props changing isn't the trigger by itself — the parent re-rendering is. Then the fixes follow: move state down, lift content up via `children`, memoize the child and stabilize its props, split context.

> **Prepare one real story** (replace with your own): "A 5,000-row table re-rendered on every keystroke in its filter. I moved the filter state into the toolbar, memoized the filtered rows, and virtualized the table; the Profiler showed render time dropping from X ms to Y ms."

**Likely follow-ups:** "What is React.memo / is memo always good?" (Q3). "What is virtualization?" "How do you measure?" "What are Core Web Vitals?" (Q35).

---

### Q9. "What is useEffect?" / "useEffect cleanup" / "the dependency array and how it affects rendering"

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** EY ("what is useEffect", "syntax of cleanup"), Capgemini ("dependency array"), TCS, Infosys (lifecycle mapping).

**My answer**

`useEffect` lets a component **synchronize with something outside React**: network requests, subscriptions, timers, browser APIs, third-party widgets. It runs after React commits the update and the browser paints, so it doesn't block rendering.

The dependency array controls when it re-runs (compared with `Object.is`):

| Dependencies | Runs |
|---|---|
| Omitted | After every render |
| `[]` | After the first mount only; cleanup on unmount |
| `[a, b]` | After mount, and again whenever `a` or `b` changes |

Cleanup is the function returned from the effect. It runs **before the effect re-runs** (with the old values) and **on unmount**:

```tsx
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

The lifecycle mapping interviewers expect:

| Class component | Hooks |
|---|---|
| `componentDidMount` | `useEffect(fn, [])` |
| `componentDidUpdate` | `useEffect(fn, [deps])` |
| `componentWillUnmount` | Cleanup returned from `useEffect` |

But I add that I think in terms of synchronization, not lifecycles: "keep this subscription in sync with `roomId`" naturally covers mount, update and unmount.

How dependencies affect rendering: the effect itself doesn't render, but setting state inside it triggers another render. If a dependency is an object, array or function created during render, its identity changes every render, so the effect runs every time — and if it also sets state, that's an infinite loop.

Mistakes I watch for:
- Missing dependencies → stale values. I keep `react-hooks/exhaustive-deps` on.
- Passing an `async` function directly — it returns a Promise, not a cleanup. Define the async function inside and call it.
- Using effects for derived state or event logic ("You Might Not Need an Effect") — compute during render or handle in the event handler.
- Not cleaning up timers or subscriptions → leaks.
- Fetching without abort → race conditions (Q20).
- In development, React 18+ Strict Mode mounts, unmounts and remounts once, so effects run twice. That's deliberate, to expose missing cleanup; production runs once.

**Likely follow-ups:** "useEffect vs useLayoutEffect" (Q28). "Why does my effect run twice?" (Q33). "Race conditions in useEffect" (Q32).

---

### Q10. "Difference between useState and useRef?" / "useRef practical use cases"

> **Priority:** 🟡 Medium · 2–3 reports · Confidence: Medium
> **Where asked:** Accenture (direct comparison), EY ("practical use cases").

**My answer**

Both persist a value across renders. The difference is whether changing it re-renders the component.

| | `useState` | `useRef` |
|---|---|---|
| Persists across renders | Yes | Yes |
| Updating triggers re-render | Yes | No |
| Update timing | Scheduled; the new value appears on the next render (each render sees a snapshot) | `ref.current` is mutated immediately |
| Use for | Data the UI displays | Values that don't affect output |

Practical `useRef` cases:

```tsx
// 1. DOM access: focus, scroll, measure
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => { inputRef.current?.focus(); }, []);

// 2. Mutable instance values: timer IDs, AbortControllers, WebSocket instances
const intervalIdRef = useRef<number | null>(null);

// 3. Previous value
const previousValueRef = useRef(value);
useEffect(() => { previousValueRef.current = value; }, [value]);

// 4. Latest callback for long-lived listeners (avoids stale closures without re-subscribing)
const onMessageRef = useRef(onMessage);
useEffect(() => { onMessageRef.current = onMessage; });
```

My rule: if the UI needs to reflect the value, it's state. I also avoid reading or writing `ref.current` during render (except lazy initialization) because it makes rendering impure and unpredictable.

A related state trap I mention: calling `setCount(count + 1)` three times in one handler adds 1, not 3, because each call uses the same render snapshot. `setCount(c => c + 1)` fixes it.

**Likely follow-ups:** "Focus an input on first render without onFocus" (Q36). "Can you use a ref to store previous props?" "What is forwardRef?" (in React 19, `ref` is a regular prop for function components).

---

### Q11. "Fetch data from an API and display it (in a table/list) using hooks"

> **Priority:** ⭐ High · 3+ reports · Confidence: High
> **Where asked:** Live coding at IBM/Coforge/LTIMindtree ("print user JSON in a React table from an external API"), Infosys ("fetch or Axios with useEffect and useState"), Accenture.

**My answer**

I'd model the three async states explicitly — loading, error, success — handle the empty case, abort on unmount, and render a semantic table with stable keys.

```tsx
import { useEffect, useState } from 'react';

type User = { id: number; name: string; email: string; company: { name: string } };

type FetchState =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'success'; users: User[] };

const USERS_URL = 'https://jsonplaceholder.typicode.com/users';

export function UsersTable() {
  const [state, setState] = useState<FetchState>({ status: 'loading' });

  useEffect(() => {
    const controller = new AbortController();

    async function loadUsers() {
      try {
        const response = await fetch(USERS_URL, { signal: controller.signal });
        if (!response.ok) throw new Error(`Request failed: ${response.status}`);
        const users: User[] = await response.json();
        setState({ status: 'success', users });
      } catch (error) {
        if ((error as Error).name === 'AbortError') return; // unmounted — ignore
        setState({ status: 'error', message: (error as Error).message });
      }
    }

    loadUsers();
    return () => controller.abort();
  }, []);

  if (state.status === 'loading') return <p>Loading users…</p>;
  if (state.status === 'error') return <p role="alert">Could not load users: {state.message}</p>;
  if (state.users.length === 0) return <p>No users found.</p>;

  return (
    <table>
      <caption>Users</caption>
      <thead>
        <tr><th scope="col">Name</th><th scope="col">Email</th><th scope="col">Company</th></tr>
      </thead>
      <tbody>
        {state.users.map(user => (
          <tr key={user.id}>
            <td>{user.name}</td>
            <td>{user.email}</td>
            <td>{user.company.name}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

Decisions I'd explain while coding:

- **A discriminated union** instead of three booleans makes impossible states (loading *and* error) unrepresentable.
- **`response.ok` check** — `fetch` only rejects on network failure, not on 404/500. Axios rejects on non-2xx, which is one reason teams pick it.
- **AbortController** prevents setting state after unmount and avoids races.
- **`user.id` as key**, never the index.

How I'd take it to production: move fetching into a custom hook or, better, TanStack Query (caching, retries, background refetch, dedup); validate the response at the boundary (e.g. Zod) because the API is untrusted input; add pagination or virtualization for large data; wrap in an error boundary.

**Likely follow-ups:** "Add search/sort/pagination." "fetch vs Axios." "How would you cache this?" "What if the component unmounts mid-request?"

---

### Q12. "Controlled vs uncontrolled components"

> **Priority:** 🟡 Medium · 3 reports · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree, Cognizant, EY-tier React theory.

**My answer**

It's about who owns the form value. In a **controlled** component, React state is the single source of truth: the input gets `value` and updates through `onChange`. In an **uncontrolled** component, the DOM keeps the value; I set an initial `defaultValue` and read it when needed through a ref or `FormData`.

```tsx
// Controlled
function EmailFieldControlled() {
  const [email, setEmail] = useState('');
  const isValid = email.includes('@');
  return (
    <>
      <input value={email} onChange={e => setEmail(e.target.value)} />
      {!isValid && email && <span>Enter a valid email</span>}
    </>
  );
}

// Uncontrolled
function EmailFieldUncontrolled() {
  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    submitEmail(String(formData.get('email')));
  }
  return (
    <form onSubmit={handleSubmit}>
      <input name="email" defaultValue="" />
      <button type="submit">Save</button>
    </form>
  );
}
```

When I choose which:

- **Controlled** when the UI depends on the value while typing: live validation, input masking/formatting, enabling a button, dependent fields.
- **Uncontrolled** for simple forms, file inputs (always uncontrolled), integrating non-React widgets, and large forms where re-rendering on every keystroke is costly. React Hook Form is built on uncontrolled inputs plus refs for exactly that reason, and React 19 form Actions (`<form action={fn}>`) work naturally with `FormData`.

A classic bug: initializing state as `undefined` and later setting a string gives the warning "a component is changing an uncontrolled input to be controlled". I initialize with `''`.

**Likely follow-ups:** "Which form library do you use and why?" "How would you validate a large form efficiently?"

---

### Q13. "What are Higher-Order Components (HOC)?" / "What is a pure component?"

> **Priority:** 🟡 Medium · 3 reports · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree (both), Cognizant (both), Deloitte (HOC). Experienced candidates are expected to know older patterns.

**My answer**

A **Higher-Order Component** is a function that takes a component and returns a new component with added behavior. It's the component version of a higher-order function and was the main way to reuse cross-cutting logic before hooks — `connect()` from react-redux is the best-known example.

```tsx
function withAuth<P extends object>(WrappedComponent: React.ComponentType<P>) {
  function WithAuth(props: P) {
    const { user } = useAuth();
    if (!user) return <Navigate to="/login" replace />;
    return <WrappedComponent {...props} />;
  }
  WithAuth.displayName = `withAuth(${WrappedComponent.displayName ?? WrappedComponent.name})`;
  return WithAuth;
}

export default withAuth(Dashboard);
```

Why hooks replaced most HOCs: deeply nested "wrapper hell" in DevTools, prop-name collisions between HOCs, implicit props that are hard to trace, refs not forwarded (needed `forwardRef` before React 19), static methods not hoisted, and awkward TypeScript. Today I use **custom hooks for logic reuse** and keep HOCs for wrapping rendering — route guards, error boundaries, analytics or feature-flag wrappers.

A **PureComponent** is a class component that implements `shouldComponentUpdate` with a **shallow comparison** of props and state, skipping re-renders when nothing changed by reference. The function-component equivalent is `React.memo` (which compares props only).

Pitfalls of both: mutating an object or array keeps the same reference, so the shallow check sees "no change" and the UI doesn't update — a bug. And inline objects or functions as props are new every render, so the optimization never kicks in.

**Likely follow-ups:** "HOC vs render props vs custom hooks." "PureComponent vs React.memo." "Can a HOC be used with hooks?" (yes — the HOC itself is a function component).

---

### Q14. "Why Redux? Explain the Redux flow / useDispatch & useSelector / Redux-Saga"

> **Priority:** ⭐ High · 4+ reports · Confidence: High
> **Where asked:** TCS ("flow of Redux"), Accenture ("useDispatch and useSelector"), IBM/Coforge/LTIMindtree ("why Saga", "why generator functions in Saga"), Cognizant ("why Redux is needed").

**My answer**

**Why Redux:** it gives predictable, centralized management of client state that many distant components read and update. All changes go through dispatched actions and pure reducers, so state transitions are traceable, testable, and debuggable with Redux DevTools (time travel), and middleware gives one place for side effects and logging.

I'm also clear about when I *don't* need it: local UI state stays in components, and server data goes in a query cache (RTK Query / TanStack Query), not hand-written Redux slices.

**The flow:**

```
UI event
  → dispatch(action)                { type: 'cart/itemAdded', payload }
  → middleware (thunk / saga / logger)
  → reducer(previousState, action) → new state   (pure, immutable)
  → store notifies subscribers
  → useSelector re-runs; component re-renders only if its selected value changed
```

The modern Redux Toolkit setup (`createStore` is deprecated in favor of `configureStore`):

```ts
const cartSlice = createSlice({
  name: 'cart',
  initialState: { items: [] as CartItem[] },
  reducers: {
    itemAdded(state, action: PayloadAction<CartItem>) {
      state.items.push(action.payload); // Immer turns this into an immutable update
    },
  },
});

export const store = configureStore({ reducer: { cart: cartSlice.reducer } });
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export const { itemAdded } = cartSlice.actions;
```

```tsx
const itemCount = useSelector((state: RootState) => state.cart.items.length);
const dispatch = useDispatch<AppDispatch>();
dispatch(itemAdded(product));
```

- **`useSelector`** subscribes to the store and re-renders the component when its selected value changes by strict reference (`===`). Pitfall: returning a new object or array (`state => ({ a, b })`, `.filter(...)`) re-renders on every action. Fix with memoized selectors (`createSelector`) or `shallowEqual`.
- **`useDispatch`** returns the store's `dispatch`.

**Redux-Saga** is middleware for complex async workflows written as generator functions. **Why generators:** a saga `yield`s plain effect descriptions (`call`, `put`, `take`), and the middleware executes them. That makes flows pausable and cancellable (`takeLatest` cancels the previous run automatically) and very testable — you step through the generator and assert on the yielded objects without mocking the network.

```ts
function* fetchUserSaga(action: PayloadAction<string>) {
  try {
    const user: User = yield call(api.fetchUser, action.payload);
    yield put(userLoaded(user));
  } catch (error) {
    yield put(userFailed((error as Error).message));
  }
}

export function* userRootSaga() {
  yield takeLatest('user/fetchRequested', fetchUserSaga);
}
```

Saga shines for orchestration — WebSockets, polling, retries, races, multi-step workflows. For ordinary data fetching I'd prefer RTK Query or `createAsyncThunk`; Saga is heavier and less common in new code.

**Likely follow-ups:** "Thunk vs Saga." "Redux vs Context" (Q5). "Write createStore syntax" (Q48). "What are pure functions and why must reducers be pure?"

---

### Q15. "Difference between functional and class components" (+ React lifecycle)

> **Priority:** 🟡 Medium · 3 reports · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree, Cognizant ("why functional components are better"), TCS-tier.

**My answer**

| | Class component | Function component |
|---|---|---|
| Definition | `class X extends React.Component` with `render()` | A function returning JSX |
| State | `this.state` / `this.setState` (merges) | `useState` / `useReducer` (replaces) |
| Side effects | Lifecycle methods | `useEffect` and related hooks |
| `this` | Required; handlers need binding | None |
| Logic reuse | HOCs, render props | Custom hooks |
| Error boundaries | Supported | Not yet — still need a class (or `react-error-boundary`) |

Why I prefer function components: less boilerplate, no `this`-binding bugs, logic reuse through custom hooks without wrapper nesting, and effects organized **by concern** rather than split across lifecycle methods (in a class, one subscription's setup and teardown live in two different methods next to unrelated code). All new React features — concurrent rendering, the React Compiler, Server Components — are designed around function components.

The class lifecycle, since it's usually asked alongside:

- **Mounting:** `constructor` → `getDerivedStateFromProps` → `render` → `componentDidMount`
- **Updating:** `getDerivedStateFromProps` → `shouldComponentUpdate` → `render` → `getSnapshotBeforeUpdate` → `componentDidUpdate`
- **Unmounting:** `componentWillUnmount`
- **Errors:** `getDerivedStateFromError`, `componentDidCatch`
- Legacy `componentWillMount`, `componentWillReceiveProps` and `componentWillUpdate` are now `UNSAFE_` because they're unreliable under concurrent rendering.

Hook equivalents: the effect mappings from Q9; `shouldComponentUpdate` → `React.memo`; `getSnapshotBeforeUpdate` has no direct hook (closest is `useLayoutEffect`).

**Likely follow-ups:** "Write an error boundary" (Q44). "Can you use hooks in class components?" (no).

---

### Q16. "What is lazy loading / code splitting?" (+ pseudocode)

> **Priority:** ⭐ High · 3 reports · Confidence: High
> **Where asked:** Infosys, EY ("write pseudocode for lazy loading"), Accenture (as part of performance).

**My answer**

**Code splitting** is having the bundler split the app into multiple chunks at dynamic `import()` boundaries, so the initial bundle only contains what the first screen needs. **Lazy loading** is loading a resource only when it's actually needed — a route, a heavy component, an image.

Route-level splitting is the highest-value place to start:

```tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));

export function AppRoutes() {
  return (
    <ErrorBoundary fallback={<ChunkLoadError />}>
      <Suspense fallback={<PageSpinner />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
}
```

Other patterns I use:
- Load heavy features on interaction — `const { exportToPdf } = await import('./pdfExport')` inside a click handler.
- Preload on hover or idle so the click feels instant.
- Images below the fold: `loading="lazy"`, or `IntersectionObserver` for custom cases.
- In Next.js, routes are split automatically and `next/dynamic` handles components.

Trade-offs I mention:
- Too many tiny chunks create request waterfalls; split at meaningful boundaries.
- Don't lazy-load above-the-fold content — it hurts LCP.
- After a deploy, old chunk hashes may 404 for users on a stale tab, so I wrap lazy routes in an error boundary with a retry/reload.
- `React.lazy` expects a default export; for named exports: `lazy(() => import('./X').then(m => ({ default: m.X })))`.

**Likely follow-ups:** "How does Suspense work?" "How do you verify bundle size?" (bundle analyzer). "Lazy loading vs prefetching."

---

### Q17. "What is the event loop?" (+ output ordering of setTimeout vs Promise / microtask vs macrotask)

> **Priority:** ⭐ High · 3 reports · Confidence: High
> **Where asked:** EY, TCS-tier, and common in senior FE screens — usually with an output-ordering snippet.

**My answer**

JavaScript runs on a single thread with one call stack. Async work — timers, network, I/O — is handled by the host environment (browser Web APIs, or libuv in Node), and when it completes, a callback is queued. The event loop coordinates that:

1. Run the current task until the call stack is empty.
2. **Drain the entire microtask queue** — promise reactions, `await` continuations, `queueMicrotask`, `MutationObserver`. Microtasks queued during this step also run now.
3. The browser may render (requestAnimationFrame callbacks, style, layout, paint).
4. Take **one** macrotask — `setTimeout`/`setInterval`, I/O, UI events, `MessageChannel` — and repeat.

The classic output question (verified):

```js
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
queueMicrotask(() => console.log('4'));
(async () => {
  console.log('5');
  await null;
  console.log('6');
})();
console.log('7');

// Output: 1 5 7 3 4 6 2
```

How I explain it: `1`, `5` and `7` are synchronous — note an `async` function runs synchronously until its first `await`. Then microtasks run in the order they were queued: `3`, `4`, then `6` (the code after `await`). The `setTimeout` callback is a macrotask, so `2` is last even with a 0 ms delay.

Why it matters in real work:
- A long synchronous task blocks both rendering and input, which shows up as poor INP. I break up work (yield back via `setTimeout`, or `scheduler.yield()` where supported) or move it to a Web Worker.
- An endless chain of microtasks starves rendering, because the queue is always drained before paint.
- `setTimeout(fn, 0)` means "no earlier than", not "immediately" — browsers clamp nested timers to about 4 ms and it waits behind other tasks.

**Likely follow-ups:** "Where does requestAnimationFrame fit?" "Is `await` a microtask?" (yes). "Node vs browser event loop differences" (`process.nextTick`, `setImmediate`).

---

### Q18. "Difference between null, undefined and not defined" / "typeof null"

> **Priority:** 🟡 Medium · 2–3 reports · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree (explicit "typeof null"), Wipro. Often a quick trap question.

**My answer**

- **`undefined`** means a variable was declared but has no value assigned. It's also what you get for missing function arguments, missing object properties, and functions without a `return`.
- **`null`** is an intentional "no value" that a developer assigns explicitly.
- **"not defined"** means the identifier was never declared at all; reading it throws `ReferenceError: x is not defined`. The one exception: `typeof undeclaredVar` returns `'undefined'` without throwing.

**`typeof null === 'object'`** is a bug from the first JavaScript implementation — values carried a type tag, objects used tag 0, and `null` was the null pointer, which also read as 0. It was never fixed because changing it would break the web. So to check for a real object I use `value !== null && typeof value === 'object'`.

Comparison behavior (verified):

```js
null == undefined;   // true  — special rule in loose equality
null === undefined;  // false — different types
null + 1;            // 1     — null converts to 0
undefined + 1;       // NaN
null >= 0;           // true  — relational operators convert to number
null == 0;           // false — == doesn't convert null that way
```

Practical consequences:
- `??` and `?.` treat both as nullish; `value == null` is the one place I use loose equality, because it catches both.
- **Default parameters only apply for `undefined`, not `null`** — `f(null)` keeps `null`. That's a common API bug.
- JSON has `null` but no `undefined`; `JSON.stringify` drops `undefined` properties.
- In TypeScript with `strictNullChecks`, I pick a convention: `undefined` for optional/absent, `null` for an explicit "empty" value in API contracts.

**Likely follow-ups:** "`typeof NaN`?" (`'number'`). "`==` vs `===`." "What is the TDZ?" (Q6).

---

### Q19. "What are custom hooks — why and how to create them?"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** EY (explicit), Capgemini ("basic custom hook implementations" as a follow-up). Senior-depth hooks question.

**My answer**

A custom hook is a function whose name starts with `use` and that calls other hooks. It extracts reusable **stateful logic** — not UI. An important detail: it shares logic, not state; each component that calls it gets its own isolated state.

Why I write them:
- **Reuse** — data fetching, debouncing (the `useDebouncedValue` in Q4), media queries, local storage, online status.
- **Separation of concerns** — the component reads as "what it renders", the hook holds "how it works".
- **Testability** — I can test the hook in isolation with `renderHook`.
- They replace HOCs and render props without wrapper nesting.

Example: a typed fetch hook with cancellation.

```tsx
type AsyncState<T> =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: T };

export function useFetch<T>(url: string | null): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({ status: 'loading' });

  useEffect(() => {
    if (!url) return;
    const controller = new AbortController();
    setState({ status: 'loading' });

    fetch(url, { signal: controller.signal })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<T>;
      })
      .then(data => setState({ status: 'success', data }))
      .catch((error: Error) => {
        if (error.name !== 'AbortError') setState({ status: 'error', error });
      });

    return () => controller.abort();
  }, [url]);

  return state;
}

// Usage
const usersState = useFetch<User[]>('/api/users');
```

Guidelines I follow:
- The `use` prefix is required for the Rules of Hooks linting to apply.
- Return a tuple when there are two values like `useState` (`[value, setValue]`), an object when there are more.
- Don't abstract prematurely — extract when logic is duplicated or the component is hard to read.
- For server data in production I'd use TanStack Query rather than a hand-rolled `useFetch`; it adds caching, deduplication, retries and refetching that are hard to get right.

**Likely follow-ups:** "Rules of hooks and why they exist" (hooks are tracked by call order). "Do two components using the same hook share state?" (no). "Write useLocalStorage / useDebounce."

---

### Q20. "How do you cancel an API call? (AbortController)"

> **Priority:** 🟡 Medium · 1 detailed report + echoes · Confidence: Medium
> **Where asked:** Capgemini Senior FE (the candidate said it "caught me off guard"); related to EY's parallel-API question. A good senior differentiator.

**My answer**

I use `AbortController`. I create a controller, pass its `signal` to the request, and call `abort()` when the result is no longer wanted. `fetch` then rejects with a `DOMException` named `AbortError`, which I ignore rather than show as an error. Axios supports the same `signal` option; its old `CancelToken` API is deprecated.

Why I cancel:
- **Race conditions** — an older, slower response overwriting a newer one (search, filters, fast tab switching).
- **Unmount or navigation** — no wasted work or state updates on a component that's gone.
- Bandwidth and server load on rapid interactions.

```tsx
// Cancel on dependency change or unmount
useEffect(() => {
  const controller = new AbortController();
  fetch(`/api/orders?status=${status}`, { signal: controller.signal })
    .then(res => res.json())
    .then(setOrders)
    .catch(err => { if (err.name !== 'AbortError') setError(err); });
  return () => controller.abort();
}, [status]);

// User-triggered cancel, e.g. a long export
const exportControllerRef = useRef<AbortController | null>(null);

async function startExport() {
  exportControllerRef.current = new AbortController();
  await fetch('/api/export', { method: 'POST', signal: exportControllerRef.current.signal });
}
const cancelExport = () => exportControllerRef.current?.abort();

// Timeout without manual timers
fetch('/api/report', { signal: AbortSignal.timeout(5000) });
```

`AbortSignal.any([userSignal, AbortSignal.timeout(5000)])` combines a user cancel with a timeout.

The caveat that shows seniority: **aborting only stops the client from waiting — the server may have already processed the request.** For non-idempotent operations like payments or order submission, cancel isn't undo. I'd disable double submission, use idempotency keys, and confirm the final state from the server.

**Likely follow-ups:** "How else can you avoid race conditions?" (an `ignore` flag in the effect cleanup, or a request ID). "How does TanStack Query cancel?" (it passes `signal` into the query function).

---

### Q21. "Given multiple APIs to call in parallel, what will you do?" / "dynamically change an API endpoint based on user input"

> **Priority:** 🟡 Medium · 1–2 reports · Confidence: Medium
> **Where asked:** EY (both, 3.5 YOE), React practical/scenario round.

**My answer — parallel calls**

My first question is whether the calls are **independent or dependent**. Independent calls run in parallel; only genuinely dependent steps are sequenced. Then I pick the combinator based on how failure should behave:

- **`Promise.all`** — when every response is required; fails fast.
- **`Promise.allSettled`** — when sections are independent, so one failing widget doesn't blank the whole page.

```ts
const [profileResult, ordersResult, notificationsResult] = await Promise.allSettled([
  api.getProfile(userId),
  api.getOrders(userId),
  api.getNotifications(userId),
]);
```

At scale, a few more considerations:

- **Concurrency limits.** Firing 50 requests at once can overwhelm the server, and HTTP/1.1 browsers allow only about 6 connections per origin. I'd use a small pool:

  ```ts
  async function mapWithConcurrency<T, R>(
    items: T[], limit: number, worker: (item: T, index: number) => Promise<R>,
  ): Promise<R[]> {
    const results = new Array<R>(items.length);
    let nextIndex = 0;
    async function runWorker() {
      while (nextIndex < items.length) {
        const index = nextIndex++;
        results[index] = await worker(items[index], index);
      }
    }
    await Promise.all(Array.from({ length: Math.min(limit, items.length) }, runWorker));
    return results;
  }
  ```

- **Progressive rendering.** In React I let each section own its query (TanStack `useQueries`, or separate Suspense boundaries) so each widget shows as soon as its data arrives.
- **Avoid waterfalls.** Start requests early — in a route loader or a parent — rather than in nested child effects that only start after the parent renders.
- **Architecture.** If a screen always needs the same six calls, a BFF (Backend-for-Frontend) or GraphQL layer can aggregate them into one round trip, which matters most on mobile networks.

**My answer — endpoint driven by user input**

The endpoint is just derived from state, so I put the inputs in the effect's (or query key's) dependencies, abort the previous request, and build URLs safely:

```tsx
const RESOURCE_ENDPOINTS = { users: '/api/users', orders: '/api/orders' } as const;
type Resource = keyof typeof RESOURCE_ENDPOINTS;

useEffect(() => {
  const controller = new AbortController();
  const params = new URLSearchParams({ page: String(page), search });
  fetch(`${RESOURCE_ENDPOINTS[resource]}?${params}`, { signal: controller.signal })
    .then(res => res.json())
    .then(setRows)
    .catch(err => { if (err.name !== 'AbortError') setError(err); });
  return () => controller.abort();
}, [resource, page, search]);
```

Security point: user input selects from an **allow-list** of endpoints and is encoded with `URLSearchParams`/`encodeURIComponent`. I never concatenate raw input into a URL or let it choose a host — that risks injection and leaking auth tokens to an attacker-controlled server.

**Likely follow-ups:** "allSettled vs all" (Q7). "How would you show partial failures?" "How do you avoid request waterfalls?"

---

### Q22. "Flatten a nested array" (+ "what if flat() is not available?")

> **Priority:** 🟡 Medium · 1 detailed report · Confidence: Medium
> **Where asked:** Capgemini Senior FE logical round, verbatim, with the "no `flat()`" follow-up pushing toward recursion.

**My answer**

With the built-in: `arr.flat(Infinity)`. Without it, I'd write a recursive version that supports a depth like the native method, using an accumulator so I don't create intermediate arrays:

```js
function flatten(arr, depth = Infinity, result = []) {
  for (const item of arr) {
    if (Array.isArray(item) && depth > 0) {
      flatten(item, depth - 1, result);
    } else {
      result.push(item);
    }
  }
  return result;
}

flatten([1, [2, [3, [4, 5]]], 6]);    // [1, 2, 3, 4, 5, 6]
flatten([1, [2, [3, [4, 5]]], 6], 1); // [1, 2, [3, [4, 5]], 6]
```

A shorter `reduce` version they often expect:

```js
const flattenDeep = arr =>
  arr.reduce((acc, item) => acc.concat(Array.isArray(item) ? flattenDeep(item) : item), []);
```

If they ask about extremely deep nesting (recursion depth limits), an iterative version with an explicit stack:

```js
function flattenIterative(arr) {
  const stack = [...arr];
  const result = [];
  while (stack.length > 0) {
    const next = stack.pop();
    if (Array.isArray(next)) stack.push(...next);
    else result.push(next);
  }
  return result.reverse(); // popping from the end reverses order
}
```

Complexity: O(n) time over the total number of elements, O(n) space for the output. The `reduce` + `concat` version is the most readable but allocates a new array per level, so the accumulator version is better for large inputs.

**Likely follow-ups:** "Flatten a nested object into dot-notation keys." "Implement `Array.prototype.flat` as a polyfill." "Handle depth."

---

### Q23. "Reverse a string / reverse the characters of words in a sentence" / "remove duplicates from a string"

> **Priority:** ⭐ High · 3 reports · Confidence: High
> **Where asked:** EY (both), Deloitte ("reverse a string in 3 ways"), LTIMindtree ("reverse words", "remove duplicates"). Coding round warm-ups.

**My answer**

Three ways to reverse a string:

```js
const text = 'hello world';

// 1. Built-ins
text.split('').reverse().join('');                 // 'dlrow olleh'

// 2. Loop from the end
let reversed = '';
for (let i = text.length - 1; i >= 0; i--) reversed += text[i];

// 3. reduce
[...text].reduce((acc, char) => char + acc, '');
```

Edge case I mention: `split('')` splits by UTF-16 code units, so it breaks emoji and other surrogate pairs. `[...text]` iterates by code point, which is safer: `[...'a😀b'].reverse().join('')` gives `'b😀a'`, while the `split('')` version corrupts the emoji.

Reverse the characters **within each word** vs reverse the **word order**:

```js
'hello world'.split(' ').map(word => [...word].reverse().join('')).join(' '); // 'olleh dlrow'
'hello world'.split(' ').reverse().join(' ');                                // 'world hello'

// Robust to extra spaces
'  hello   world  '.trim().split(/\s+/).reverse().join(' ');                 // 'world hello'
```

Remove duplicate characters, keeping first occurrence order:

```js
[...new Set('programming')].join('');  // 'progamin'

// Without Set, if they ask
function removeDuplicateChars(str) {
  const seen = {};
  let output = '';
  for (const char of str) {
    if (!seen[char]) {
      seen[char] = true;
      output += char;
    }
  }
  return output;
}
```

All of these are O(n). I'd confirm requirements before coding: case sensitivity, whether spaces count, and whether punctuation stays attached to words.

**Likely follow-ups:** "Check for a palindrome." "Count character frequency." "Without built-in methods."

---

### Q24. "Write an auto-increment counter / increment–decrement counter in React"

> **Priority:** 🟡 Medium · 1 detailed report · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree live coding — both variants, using `setInterval`/`clearInterval`.

**My answer**

The increment/decrement version is about functional updates; the auto-increment version is about effect cleanup and stale closures. I'd do both in one component:

```tsx
import { useEffect, useState } from 'react';

const TICK_INTERVAL_MS = 1000;
const STEP = 1;

export function Counter() {
  const [count, setCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;
    const intervalId = setInterval(() => {
      setCount(previous => previous + STEP); // functional update: never stale
    }, TICK_INTERVAL_MS);
    return () => clearInterval(intervalId); // runs on stop, on unmount, and in Strict Mode re-runs
  }, [isRunning]);

  return (
    <div>
      <output aria-live="polite">{count}</output>
      <button onClick={() => setCount(c => c - STEP)}>−</button>
      <button onClick={() => setCount(c => c + STEP)}>+</button>
      <button onClick={() => setIsRunning(running => !running)}>
        {isRunning ? 'Stop' : 'Start'}
      </button>
      <button onClick={() => { setIsRunning(false); setCount(0); }}>Reset</button>
    </div>
  );
}
```

Points I'd explain while writing it:

- **The stale closure bug** they're usually probing for: `setInterval(() => setCount(count + 1), 1000)` with `[]` dependencies gets stuck at 1, because the callback forever sees the initial `count`. The functional updater fixes it.
- **Cleanup** prevents leaked intervals. Without it, React 18+ Strict Mode (which runs effects twice in development) would create two intervals and the counter would jump by 2.
- **Declarative control**: the interval is driven by `isRunning` state, instead of storing the interval ID in a ref and starting/stopping it imperatively. The ref approach also works; this one is easier to reason about.
- **Accuracy**: `setInterval` drifts and is throttled in background tabs. For a real timer (countdowns, session timeouts) I'd compute elapsed time from a start timestamp (`Date.now()` / `performance.now()`) instead of counting ticks.

**Likely follow-ups:** "Add a min/max bound." "Why does it jump by 2 in development?" "Build a stopwatch/countdown."

---

### Q25. "Difference between spread and rest operator"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** TCS ("spread vs rest"), IBM/Coforge/LTIMindtree. JS fundamentals.

**My answer**

Same `...` syntax, opposite jobs. **Spread expands** an iterable or object into individual elements or properties. **Rest collects** remaining elements or properties into one array or object. My rule of thumb: spread appears where values are *used* (call sites, array/object literals); rest appears where values are *received* (parameter lists, destructuring).

```js
// Spread — expanding
const merged = [...frontendSkills, ...backendSkills];
const updatedUser = { ...user, city: 'Pune' };  // later keys override earlier ones
Math.max(...scores);

// Rest — collecting
function logAll(level, ...messages) {           // messages is a real array
  messages.forEach(message => console.log(`[${level}]`, message));
}
const [first, ...remaining] = [10, 20, 30];      // remaining = [20, 30]
const { password, ...safeUser } = user;          // strip a field without mutating
```

Details worth mentioning:
- Spread creates a **shallow** copy (ties back to Q2).
- Object spread copies only own, enumerable properties; the "later key wins" behavior is how I apply defaults: `{ ...defaults, ...options }`.
- A rest parameter must be last, and there can be only one. It replaced the old `arguments` object, which isn't a real array and doesn't exist in arrow functions.
- In React I use both constantly: `const { className, ...rest } = props` then `<button className={cx('btn', className)} {...rest} />` to forward props without passing unknown ones twice.
- Spreading a huge array into a function call (`Math.max(...hugeArray)`) can exceed the engine's argument limit; a loop or `reduce` is safer there.

**Likely follow-ups:** "Is spread a deep copy?" (no). "Difference between rest parameters and `arguments`." "Merge two objects with nested keys."

---
### Q26. "What is prototype inheritance / lexical scoping?"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** JS internals at Cognizant (both parts) and IBM/Coforge/LTIMindtree (prototype inheritance).

**My answer — prototype inheritance**

Every JavaScript object has an internal link, `[[Prototype]]`, to another object. When I read a property, the engine checks the object itself first, then walks up that chain until it finds the property or reaches `null`. That chain is how objects share behavior — JavaScript has no classes underneath; `class` is syntax over prototypes.

When I call a function with `new`, the new object's `[[Prototype]]` is set to that function's `.prototype` object. So methods defined on a class live once on the prototype and are shared by every instance, instead of being copied into each object.

```js
class Animal {
  constructor(name) { this.name = name; }
  speak() { return `${this.name} makes a sound`; }
}
class Dog extends Animal {
  speak() { return `${this.name} barks`; } // overrides — found first on the chain
}

const rex = new Dog('Rex');
rex.speak();                                                   // 'Rex barks'
Object.getPrototypeOf(rex) === Dog.prototype;                  // true
Object.getPrototypeOf(Dog.prototype) === Animal.prototype;     // true
rex.hasOwnProperty('speak');                                   // false — it's inherited

// Without classes
const greeter = { greet() { return `Hi ${this.name}`; } };
const user = Object.create(greeter); // user's prototype is greeter
user.name = 'Asha';
user.greet(); // 'Hi Asha'
```

Points I add:
- Use `Object.getPrototypeOf` / `Object.create`; `__proto__` is legacy, and changing a prototype after creation (`Object.setPrototypeOf`) de-optimizes the object.
- `hasOwnProperty` / `Object.hasOwn` distinguishes own vs inherited properties; `for...in` also walks inherited enumerable properties.
- **Security — prototype pollution.** A naive deep-merge of untrusted JSON containing a `"__proto__"` key can write onto `Object.prototype`, and then every object in the app "has" that property (e.g. `isAdmin: true`). I guard merges by skipping `__proto__`, `constructor` and `prototype` keys, or use `Object.create(null)` / `Map` for lookup tables.

**My answer — lexical scoping**

Lexical scoping means a variable's scope is determined by **where the code is written**, not where it's called. Each function or block creates a scope; an inner scope can read variables from enclosing scopes, and lookup walks outward through the scope chain to the global scope.

```js
const appName = 'Portal';
function outer() {
  const section = 'Reports';
  function inner() {
    return `${appName} / ${section}`; // resolved by where inner is defined
  }
  return inner;
}
outer()(); // 'Portal / Reports' — still works after outer returned: that's a closure (Q1)
```

The contrast interviewers like: **scope is lexical, but `this` is dynamic** — it depends on how a function is called. Arrow functions are the exception: they take `this` lexically from the surrounding code, which is why they're convenient for callbacks.

**Likely follow-ups:** "Difference between `__proto__` and `prototype`." "How does `class` differ from constructor functions?" "What is `this` in different call styles?"

---

### Q27. "What is throttling?" (+ implement a debounce/throttle polyfill)

> **Priority:** 🟡 Medium · 1 detailed report + echoes · Confidence: Medium
> **Where asked:** Capgemini Senior FE, through a real-world scenario, with a polyfill expected. Natural follow-up to the debounce question (Q4).

**My answer**

Throttling guarantees a function runs **at most once per interval**, no matter how often the event fires. Debouncing waits until events **stop** for a period and then runs once.

| | Debounce | Throttle |
|---|---|---|
| Runs | Once, after a quiet period | Regularly, at most every N ms |
| Good for | Search input, autosave, resize end, form validation | Scroll position, mousemove/drag, window resize while resizing, rate-limited analytics |
| Under continuous input | Never fires until input stops | Keeps firing at a steady rate |

A throttle with leading and trailing calls, so the **last** event is never lost (important for things like final scroll position):

```js
function throttle(fn, intervalMs) {
  let lastRunTime = 0;
  let trailingTimerId = null;
  let lastArgs = null;

  return function throttled(...args) {
    const now = Date.now();
    const remaining = intervalMs - (now - lastRunTime);
    lastArgs = args;

    if (remaining <= 0) {
      clearTimeout(trailingTimerId);
      trailingTimerId = null;
      lastRunTime = now;
      fn.apply(this, args);                 // leading call
    } else if (trailingTimerId === null) {
      trailingTimerId = setTimeout(() => {  // trailing call with the latest args
        lastRunTime = Date.now();
        trailingTimerId = null;
        fn.apply(this, lastArgs);
      }, remaining);
    }
  };
}

window.addEventListener('scroll', throttle(updateScrollProgress, 100), { passive: true });
```

Calling it every 25 ms for 250 ms with a 100 ms interval runs it four times (verified): immediately, twice more at the interval, and once trailing with the final value.

The debounce polyfill is in Q4; in an interview I'd add a `cancel()` method to both so React effects can clean up on unmount.

Production notes:
- In React, the throttled function must be stable (`useMemo` or `useRef`) and cancelled in cleanup.
- For visual updates tied to scroll, `requestAnimationFrame` is often better than a fixed interval — it syncs with the display's frame rate.
- Often the best throttle is not needing one: `IntersectionObserver` for infinite scroll, lazy loading and "is visible" checks replaces scroll listeners entirely; `ResizeObserver` for element size.
- `{ passive: true }` on scroll and touch listeners lets the browser scroll without waiting for JS.

**Likely follow-ups:** "Debounce vs throttle — pick one for search / infinite scroll." "Add leading/trailing options like lodash."

---

### Q28. "Difference between useEffect and useLayoutEffect" / "What is useImperativeHandle?"

> **Priority:** 🟡 Medium · 2 reports (both EY) · Confidence: Medium
> **Where asked:** EY, as senior-depth hooks questions.

**My answer — useEffect vs useLayoutEffect**

They have the same API; the difference is **timing**.

| | `useEffect` | `useLayoutEffect` |
|---|---|---|
| Runs | After the browser paints | After DOM mutations, **before** the browser paints |
| Blocks paint | No | Yes — runs synchronously |
| Use for | Almost everything: data fetching, subscriptions, logging | Measuring layout and synchronously correcting it to avoid a visible flicker |

The classic case is positioning a tooltip: I need its rendered height to decide whether it goes above or below the anchor. With `useEffect`, the user briefly sees it in the wrong place and then it jumps.

```tsx
function Tooltip({ anchorRect, children }: TooltipProps) {
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [top, setTop] = useState(0);

  useLayoutEffect(() => {
    const height = tooltipRef.current?.getBoundingClientRect().height ?? 0;
    const fitsAbove = anchorRect.top - height > 0;
    setTop(fitsAbove ? anchorRect.top - height : anchorRect.bottom);
  }, [anchorRect]); // re-render happens before paint — no flicker

  return <div ref={tooltipRef} style={{ position: 'fixed', top }}>{children}</div>;
}
```

I default to `useEffect` because `useLayoutEffect` delays paint and hurts responsiveness if overused. It also doesn't run during server rendering. There's a third one, `useInsertionEffect`, which is only for CSS-in-JS libraries injecting styles.

**My answer — useImperativeHandle**

It customizes what a parent receives through a `ref`. Instead of exposing the raw DOM node, a component exposes a small, deliberate imperative API — `focus()`, `clear()`, `scrollToTop()`, `validate()`.

```tsx
type SearchInputHandle = { focus: () => void; clear: () => void };

// React 19: ref is a regular prop on function components (React ≤ 18 needs forwardRef)
function SearchInput({ ref }: { ref?: React.Ref<SearchInputHandle> }) {
  const inputRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    clear: () => { if (inputRef.current) inputRef.current.value = ''; },
  }), []);

  return <input ref={inputRef} type="search" />;
}

// Parent
const searchRef = useRef<SearchInputHandle>(null);
<SearchInput ref={searchRef} />;
searchRef.current?.focus();
```

I use it sparingly — for actions that are inherently imperative (focus, scroll, play/pause, triggering validation in a form library). If something can be expressed as props and state, it should be; refs bypass React's data flow.

**Likely follow-ups:** "What is forwardRef?" "When would useLayoutEffect hurt performance?" "How do you call a child's method from a parent?" (Q31).

---

### Q29. "What are nested routes / what is an Outlet in React Router?" / "How to access query params (useLocation)?"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** EY ("nested routes… pseudocode", "what is an Outlet?"), Accenture ("access query params… useLocation").

**My answer**

Nested routes let the route tree mirror the UI layout. A parent route renders a shared layout — header, sidebar, tabs — and **`<Outlet />` is the placeholder where the matched child route renders**. The layout stays mounted (and keeps its state) while only the child area changes on navigation.

```tsx
// React Router v6 imports from 'react-router-dom'; v7 imports from 'react-router'
const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,              // header + sidebar + <Outlet />
    errorElement: <RouteError />,
    children: [
      { index: true, element: <Home /> }, // renders at '/'
      {
        path: 'loans',
        element: <LoansLayout />,         // tabs + <Outlet />
        children: [
          { index: true, element: <LoanList /> },
          { path: ':loanId', element: <LoanDetail /> },
        ],
      },
    ],
  },
]);

function AppLayout() {
  return (
    <>
      <Header />
      <Sidebar />
      <main><Outlet /></main>
    </>
  );
}
```

Reading URL data:

```tsx
const { loanId } = useParams();                       // path params: /loans/42
const [searchParams, setSearchParams] = useSearchParams();
const status = searchParams.get('status') ?? 'all';   // query params: ?status=open&page=2
setSearchParams(prev => { prev.set('page', '2'); return prev; });

const location = useLocation();                       // { pathname, search, hash, state, key }
```

On the `useLocation` question: it does give me `location.search`, and I can parse it with `new URLSearchParams(location.search)`. But for query parameters I prefer `useSearchParams`, which parses and updates them for me. I use `useLocation` for the pathname (active links, analytics on route change) and for navigation `state`, like the page to return to after login.

Why I put filters, pagination and tabs in the URL rather than component state: the view becomes shareable and bookmarkable, it survives refresh, and the back button works as users expect.

**Likely follow-ups:** "How do you protect routes?" (a layout route that checks auth and renders `<Navigate>` or `<Outlet />`). "How do you lazy-load routes?" (Q16). "useNavigate vs `<Link>`."

---

### Q30. "Types vs interface in TypeScript" / "how do you type an object?" / "null vs unknown"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** Accenture (types vs interface, typing an object, generics for any datatype; "null vs unknown" in the second part of that write-up). TypeScript is increasingly expected for senior FE.

**My answer — type vs interface**

For plain object shapes they're mostly interchangeable. The differences:

| | `interface` | `type` alias |
|---|---|---|
| Object shapes | Yes | Yes |
| Extending | `extends` | Intersection `&` |
| Declaration merging (re-declaring adds fields) | Yes — useful for augmenting library types like `Window` | No — duplicate name is an error |
| Unions, tuples, primitives, function types | No | Yes: `type Status = 'idle' \| 'loading'` |
| Mapped and conditional types | No | Yes: `Partial<T>`, `Record<K, V>`, `T extends U ? X : Y` |

My convention: `interface` for public object contracts and component props when a team prefers it, `type` for unions, discriminated unions, and anything computed. Consistency within the codebase matters more than the choice.

**Typing an object**

```ts
interface Address { city: string; pinCode: string }

interface User {
  readonly id: string;              // can't be reassigned
  name: string;
  email?: string;                   // optional
  address: Address;                 // nested type
  roles: Array<'admin' | 'viewer'>; // union of literals
  metadata: Record<string, string>; // dictionary
}
```

**Generics for any data type** — instead of `any`, I keep the type information flowing:

```ts
function firstOrNull<T>(items: readonly T[]): T | null {
  return items.length > 0 ? items[0] : null;
}
firstOrNull([1, 2]);       // number | null
firstOrNull(['a']);        // string | null

interface ApiResponse<TData> { data: TData; error: string | null }
type UserResponse = ApiResponse<User>;
```

**null vs unknown (and any)**

- **`null`** is a *value* type meaning "intentionally empty". With `strictNullChecks`, `string` doesn't include `null`; I write `string | null` explicitly.
- **`unknown`** is the type-safe "could be anything". I can assign anything to it, but I **must narrow** before using it. That's what I use for API responses, `JSON.parse` results and `catch` errors.
- **`any`** turns type checking off for that value and spreads silently. I avoid it.

```ts
function getErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === 'string') return error;
  return 'Unknown error';
}
```

For data crossing a trust boundary, narrowing alone isn't enough at runtime — I validate with a schema library like Zod and infer the type from the schema.

**Likely follow-ups:** "`never` — where is it useful?" (exhaustive `switch` checks). "Utility types you use" (`Partial`, `Pick`, `Omit`, `ReturnType`). "How do you type props with children?"

---

### Q31. "How can you access a child component's state in the parent?" (lifting state / refs / global state)

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** Accenture (verbatim), EY ("lifting state up – when and why").

**My answer**

In React, data flows down, so a parent shouldn't reach into a child to read its state. If the parent needs the value, the parent should **own** it. My options, in order:

**1. Lift state up (preferred).** Move the state to the closest common parent and pass the value plus a change handler down. The child becomes controlled, and there's a single source of truth.

```tsx
function FilterPanel() {
  const [status, setStatus] = useState<LoanStatus>('open');
  return (
    <>
      <StatusSelect value={status} onChange={setStatus} />
      <LoanTable status={status} />
    </>
  );
}

function StatusSelect({ value, onChange }: { value: LoanStatus; onChange: (s: LoanStatus) => void }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value as LoanStatus)}>
      <option value="open">Open</option>
      <option value="closed">Closed</option>
    </select>
  );
}
```

**2. Child notifies the parent through a callback** (`onChange`, `onSubmit`) when the parent only needs to react to events, not own the value. I avoid copying the child's state into parent state on every change — that creates two sources of truth that drift.

**3. Ref + `useImperativeHandle`** (Q28) for imperative actions such as `reset()`, `focus()` or `validate()` — not as a routine way to read state.

**4. Context or a store** when the components are far apart or many components need the value.

**When to lift and when not to:** I lift when two siblings need the same data or the parent needs to coordinate them. Otherwise I keep state as low as possible (colocation), because lifting too high makes more components re-render.

**Likely follow-ups:** "What is a single source of truth?" "How do siblings communicate?" "What problems does lifting state cause?" (prop drilling — Q5).

---

### Q32. "What is a stale closure / a race condition in useEffect and how do you prevent it?"

> **Priority:** 🟡 Medium · 1 report (EY) · Confidence: Medium
> **Where asked:** EY, as senior-depth React internals. Builds directly on Q1, Q9 and Q20.

**My answer — stale closures**

Every render creates new functions that capture that render's props and state (a closure, Q1). If a function outlives its render — an interval, a subscription, a memoized callback with missing dependencies — it keeps reading **old values**.

```tsx
// Bug: always logs and sets based on the first render's count
useEffect(() => {
  const intervalId = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(intervalId);
}, []); // count is captured once — the counter gets stuck at 1
```

Fixes, depending on the case:
- **Functional updates**: `setCount(c => c + 1)` — no need to read `count` at all.
- **Correct dependencies**, enforced by `react-hooks/exhaustive-deps`, so the effect re-subscribes with fresh values.
- **A ref holding the latest value** when re-subscribing is expensive (WebSockets, third-party listeners):

  ```tsx
  const onMessageRef = useRef(onMessage);
  useEffect(() => { onMessageRef.current = onMessage; });
  useEffect(() => {
    const socket = connect(roomId);
    socket.on('message', msg => onMessageRef.current(msg)); // always the latest handler
    return () => socket.disconnect();
  }, [roomId]);
  ```

  React 19.2 provides `useEffectEvent` for exactly this pattern.

**My answer — race conditions in useEffect**

When an effect fetches based on a changing value, requests can resolve out of order. If the user switches from user 1 to user 2 and user 1's slower response arrives last, it overwrites user 2's data.

```tsx
useEffect(() => {
  let ignore = false; // or use an AbortController (Q20)
  fetchUser(userId).then(user => {
    if (!ignore) setUser(user); // only the latest effect's result is applied
  });
  return () => { ignore = true; }; // cleanup runs when userId changes
}, [userId]);
```

Options: an `ignore` flag in cleanup, `AbortController` (also stops the network work), comparing a request ID, or a data library such as TanStack Query, which keys results by query and handles this for me.

**Likely follow-ups:** "Why does the interval get stuck?" "AbortController vs ignore flag?" (abort also saves bandwidth; the flag works for any promise).

---

### Q33. "Why does useEffect run twice in React 18 (Strict Mode)?" / "Batching in React 18" / "What is flushSync?"

> **Priority:** 🟡 Medium · 1 report (EY) · Confidence: Medium
> **Where asked:** EY, all three as React 18 internals.

**My answer — effects running twice**

In development with `<StrictMode>`, React 18+ deliberately **mounts, unmounts and re-mounts** each component once on first render, so every effect runs setup → cleanup → setup. It also double-invokes render functions, state initializers and reducers. The point is to surface bugs: effects without proper cleanup (duplicate subscriptions, leaked intervals, double event listeners) and impure rendering. It's preparation for features like preserving state when components are hidden and shown again.

**It only happens in development** — production runs effects once. The right response is to fix the cleanup, not to disable Strict Mode or add "ran already" refs. For something that should truly happen once per app load (analytics init), I put it at module level outside components.

**My answer — automatic batching**

Batching means React groups multiple state updates into **one re-render**. In React 17, that only happened inside React event handlers; updates inside `setTimeout`, promises or native listeners each caused a separate render. React 18, with `createRoot`, batches updates **everywhere** automatically.

```tsx
fetchOrders().then(orders => {
  setOrders(orders);
  setIsLoading(false);
  setLastUpdated(Date.now());
  // React 17: three renders. React 18+: one render.
});
```

**My answer — flushSync**

`flushSync` from `react-dom` opts out of batching: React applies the updates inside the callback and updates the DOM **synchronously** before the next line runs. I use it when I must read or act on the updated DOM immediately — for example scrolling a newly added message into view, or integrating with third-party code that expects the DOM to be current.

```tsx
import { flushSync } from 'react-dom';

function handleSend(message: Message) {
  flushSync(() => setMessages(prev => [...prev, message]));
  listEndRef.current?.scrollIntoView({ behavior: 'smooth' }); // the new item is already in the DOM
}
```

It's expensive and defeats batching and concurrent rendering, so it's rare in my code.

**Likely follow-ups:** "What else changed in React 18?" (concurrent rendering, `useTransition`, `useDeferredValue`, Suspense on the server, `createRoot`). "How do you stop double API calls in development?" (you don't — abort in cleanup, or use a query cache that dedupes).

---

### Q34. "What is the virtual DOM / diffing algorithm / reconciliation (React Fiber)?"

> **Priority:** 🟡 Medium · 3 reports · Confidence: Medium
> **Where asked:** EY ("what is the diffing algorithm?"), Cognizant (Fiber/reconciliation), Microsoft.

**My answer**

The **virtual DOM** is a lightweight JavaScript tree of React elements describing what the UI should look like. On each update, React renders a new tree, compares it to the previous one — that comparison is **reconciliation** — and then applies only the necessary changes to the real DOM in the **commit** phase.

I'm careful not to say "the virtual DOM is faster than the DOM". The benefit is a declarative programming model — I describe the UI for a given state and React works out the updates — with performance that's good enough by default.

**The diffing algorithm.** A general tree diff is O(n³), so React uses heuristics that make it O(n):

1. **Different element types** (`<div>` → `<section>`, or `ComponentA` → `ComponentB`): React tears down the old subtree, including its state, and builds a new one.
2. **Same DOM element type:** keep the node, update only changed attributes.
3. **Same component type:** keep the instance and its state, pass new props, re-render it.
4. **Lists use `key`s** to match children between renders.

Practical consequences:
- Using the **array index as a key** in a list that reorders, inserts or deletes attaches state to the wrong rows (e.g. an input's text jumps to another item). I use stable IDs.
- **Changing a `key` intentionally resets** a component's state: `<ProfileForm key={userId} />`.
- Defining a component inside another component creates a new type every render, so its state is reset every time.

**Fiber** (React 16) is the rewritten reconciler. Each element gets a fiber node — a unit of work linked to its parent, child and sibling. Because work is split into units, the **render phase can be paused, prioritized, resumed or discarded**, while the commit phase stays synchronous so the DOM never shows a half-updated UI. React keeps a current tree and a work-in-progress tree and swaps them on commit. Fiber is what enables concurrent features: `useTransition`, `useDeferredValue`, Suspense, and prioritizing urgent updates like typing over expensive re-renders.

**Likely follow-ups:** "Render phase vs commit phase." "Why are keys needed?" "Is re-rendering the same as updating the DOM?" (no — a render can produce no DOM changes).

---

### Q35. "What are Web Vitals / Core Web Vitals?" / "What are Web Components?"

> **Priority:** 🟡 Medium · 1–2 reports · Confidence: Medium
> **Where asked:** EY FE (both, 3.5 YOE), corroborated by a second EY breakdown.

**My answer — Core Web Vitals**

They're Google's user-centric metrics for real-world page experience, assessed at the 75th percentile of real user visits:

| Metric | Measures | "Good" threshold | Common fixes |
|---|---|---|---|
| **LCP** — Largest Contentful Paint | Loading: when the main content appears | ≤ 2.5 s | Preload the hero image and use `fetchpriority="high"`, don't lazy-load it, SSR/SSG, CDN, smaller JS |
| **INP** — Interaction to Next Paint | Responsiveness to clicks, taps and keys across the visit (replaced FID in March 2024) | ≤ 200 ms | Break up long tasks, ship less JS, debounce, `useTransition`, move heavy work to workers |
| **CLS** — Cumulative Layout Shift | Visual stability | ≤ 0.1 | Width/height on images and embeds, reserve space for ads and late content, font loading strategy |

Supporting metrics: TTFB and FCP.

I distinguish **lab data** (Lighthouse, DevTools — reproducible, good for debugging) from **field data** (real users: CrUX, Search Console, or my own RUM). Field data is what counts, so I collect it:

```ts
import { onCLS, onINP, onLCP } from 'web-vitals';

const sendToAnalytics = (metric: { name: string; value: number; id: string }) =>
  navigator.sendBeacon('/analytics/vitals', JSON.stringify(metric));

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

**My answer — Web Components**

Web Components are browser-native standards for building reusable, encapsulated custom elements that work in any framework or none:

- **Custom Elements** — define your own tag with lifecycle callbacks.
- **Shadow DOM** — encapsulated DOM and styles that don't leak in or out.
- **`<template>` and `<slot>`** — reusable markup and content projection.

```js
class StatusBadge extends HTMLElement {
  connectedCallback() {
    const root = this.attachShadow({ mode: 'open' });
    root.innerHTML = `<style>span{padding:2px 8px;border-radius:999px;background:#e6f4ea}</style>
                      <span><slot></slot></span>`;
  }
}
customElements.define('status-badge', StatusBadge);
// <status-badge>Approved</status-badge>
```

Where they fit: framework-agnostic design systems shared across React, Angular and plain-HTML apps — common in large enterprises and micro-frontends (Q39). Trade-offs: server rendering is harder (Declarative Shadow DOM helps), styling across the shadow boundary needs CSS custom properties or `::part`, and form integration takes extra work. React 19 added full support for custom elements (passing properties and handling custom events), which removed a long-standing friction point.

**Likely follow-ups:** "How did you improve LCP/INP on a project?" "Shadow DOM vs CSS Modules." "Lighthouse score vs field data — which matters?"

---

### Q36. "How do you focus an input field on first render without onFocus (useRef)?"

> **Priority:** 🟡 Medium · 1 report · Confidence: Medium
> **Where asked:** EY, verbatim, as a React practical.

**My answer**

I attach a ref to the input and call `focus()` in an effect after it mounts:

```tsx
function LoginForm() {
  const emailInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    emailInputRef.current?.focus();
  }, []); // after the first render, once the DOM node exists

  return <input ref={emailInputRef} type="email" name="email" aria-label="Email" />;
}
```

Alternatives I'd mention:
- **`autoFocus`** — `<input autoFocus />` does the same thing declaratively; React calls `focus()` on mount.
- **A callback ref** for inputs that appear conditionally later (inside a modal or after a toggle), because a `useEffect` with `[]` would have run before the input existed:

  ```tsx
  <input ref={node => node?.focus()} />
  ```

The accessibility point that shows judgment: auto-focusing moves screen-reader users and can skip content before the input, so I only do it when the input is clearly the purpose of the screen (search page, login, a dialog's first field). For dialogs, I also return focus to the triggering button on close.

**Likely follow-ups:** "Why doesn't `useEffect` + `[]` work for a modal input?" "useRef vs useState" (Q10).

---

### Q37. "Explain CSR vs SSR / hydration" (+ SSG)

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** EY ("CSR vs SSR"), Cognizant ("do you know server-side rendering").

**My answer**

| Strategy | Where HTML is produced | Strengths | Weaknesses | Good fit |
|---|---|---|---|---|
| **CSR** — Client-Side Rendering | In the browser, after JS downloads and runs | Simple hosting (static files), rich interactivity, cheap servers | Blank screen until JS loads, weaker SEO, slower LCP on slow devices | Dashboards and internal tools behind login |
| **SSR** — Server-Side Rendering | On the server, per request | Fast first content, SEO, fresh data | Server cost and complexity, TTFB depends on data fetching | Product pages, personalized or frequently changing public pages |
| **SSG** — Static Site Generation | At build time | Fastest delivery from a CDN, cheap, robust | Data is as old as the last build | Marketing pages, docs, blogs |
| **ISR** — Incremental Static Regeneration | Static, re-generated in the background after a time or on demand | Static speed with periodic freshness | Briefly stale content | Catalogs, content sites |

**Hydration** is the step after SSR/SSG where React runs on the client, builds its tree, and **attaches event handlers and state to the existing server HTML** instead of recreating it. Until hydration finishes, the page looks ready but buttons don't respond.

Hydration requires the client's first render to match the server HTML. **Hydration mismatches** come from rendering things that differ between server and client: `Date.now()`, `Math.random()`, `window`/`localStorage` checks, locale-dependent formatting. I fix them by rendering browser-only content after mount (in an effect) or making the values deterministic.

Modern refinements:
- **Streaming SSR with Suspense** (React 18) sends HTML in chunks as data resolves, and **selective hydration** makes the part the user interacts with hydrate first.
- **React Server Components** (e.g. Next.js App Router) run only on the server and send no JavaScript for those parts; only interactive "client components" hydrate.

How I'd choose: by page, not by app. Next.js lets a marketing page be static, a product page SSR/ISR, and the logged-in dashboard mostly client-side.

**Likely follow-ups:** "What causes hydration errors?" "How does SSR affect Core Web Vitals?" (improves LCP; heavy hydration can hurt INP). "Server Components vs SSR."

---

### Q38. Scenario/design: "Design the screen layout for [loan-management system / dashboard]; how would you set up the components and fetch the data?"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** TCS (loan-management scenario, 3–6 YOE), Infosys managerial round. Evaluates structured thinking more than code.

**My answer**

I'd spend the first couple of minutes on requirements, because they drive every decision:
- **Who uses it?** Loan officers, approvers, or customers — each needs different views and permissions.
- **Key screens:** loan list with filters, loan detail (borrower, EMI schedule, documents, history), new application form, approval queue.
- **Data scale and freshness:** thousands of loans means server-side pagination; does status need to update in real time?
- **Non-functional:** roles and permissions, audit, accessibility, mobile support, and handling financial and personal data.

**Layout and component structure**

```
<AppShell>                       header (user, notifications) + role-based sidebar
 └─ <Outlet>                     nested routes (Q29)
     ├─ /dashboard   <DashboardPage>
     │                ├─ <KpiCards/>          (portfolio value, overdue count…)
     │                ├─ <ApplicationsChart/>
     │                └─ <OverdueLoansTable/>  each widget loads and fails independently
     ├─ /loans       <LoanListPage>
     │                ├─ <LoanFilters/>        state lives in the URL query string
     │                └─ <LoanTable/>          server pagination, sorting, virtualization
     ├─ /loans/:id   <LoanDetailPage>  tabs: Overview | EMI Schedule | Documents | Audit log
     └─ /apply       <LoanApplicationWizard>  multi-step form
```

I'd organize code by feature rather than by file type:

```
src/
  app/            routing, providers, layout shell
  features/
    loans/        api.ts · hooks.ts · components/ · types.ts
    applications/
    customers/
  shared/         ui components (design system), utils, api client, auth
```

**Data fetching and state**
- A typed API client in one place (base URL, auth, error normalization).
- **Server state in TanStack Query** (or RTK Query): query keys like `['loans', filters]`, caching, background refetch, request dedup, and invalidation after mutations (approving a loan refreshes the list and detail).
- **URL state** for filters, sort and page, so views are shareable and survive refresh.
- **Minimal global state** — auth user, permissions, theme — in Context or a small store. No copying server data into Redux.
- Independent dashboard widgets fetch in parallel, with per-widget loading skeletons and error boundaries (`allSettled` semantics, Q21), so one failed API doesn't blank the page.

**Forms** — React Hook Form + Zod for the multi-step application: per-step validation, draft autosave, and server-side validation as the real authority.

**Cross-cutting concerns**
- **Security:** role-based UI, but enforcement on the server; tokens in httpOnly cookies, not `localStorage`; mask account and ID numbers; no personal data in logs or analytics.
- **Performance:** route-level code splitting, virtualized tables, skeletons instead of spinners.
- **Accessibility and formatting:** keyboard-navigable tables and forms; currency via `Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })`.
- **Quality:** unit tests for EMI and eligibility logic, integration tests for key flows, error monitoring.

**Trade-offs I'd call out:** server-side vs client-side filtering (server for large data), polling vs WebSockets for status updates (polling is simpler and usually enough for loans), and how much to put in a shared design system early.

**Likely follow-ups:** "How would you handle role-based access?" "How do you keep the list and detail views in sync after an approval?" "How would you handle 100k rows?"

---

### Q39. "Explain micro-frontend architecture" (+ "how would you reuse React payment logic in a mobile app?")

> **Priority:** 🟡 Medium · 3 reports · Confidence: Medium
> **Where asked:** IBM ("React architecture — micro frontend"), Deloitte (2nd round), Infosys managerial (reusing payment logic in a mobile app). Architecture round for senior candidates.

**My answer — micro-frontends**

Micro-frontends apply the microservices idea to the UI: a large frontend is split into **independently developed and deployed applications**, usually owned by different teams along business domains (catalog, checkout, account), and composed into one product for the user.

**Why organizations adopt them:** team autonomy and independent release cycles, incremental migration of a legacy app (an old Angular app migrated screen by screen to React), and isolating failures and ownership in very large codebases.

**Composition approaches:**

| Approach | How | Trade-off |
|---|---|---|
| Route-based split | Each app owns URL paths behind a reverse proxy | Simplest and most isolated; full page reload between apps |
| Run-time integration — Module Federation (webpack/Rspack, Vite plugins) or single-spa | A shell app loads remote bundles at run time | Seamless SPA experience; needs careful dependency sharing and versioning |
| Web Components | Each team ships custom elements (Q35) | Framework-agnostic; SSR and styling are harder |
| iframes | Each app in a frame | Strong isolation; poor UX, accessibility and performance |
| Build-time packages | Apps published as npm packages | Easy, but deploys are coupled — not truly independent |

**The hard parts I'd raise:**
- **Shared dependencies:** React must be a singleton, or hooks break; version drift across teams.
- **Consistency:** a shared design system and tokens, or the product looks stitched together.
- **Communication:** keep it minimal and explicit — URL, custom browser events, or a small typed event bus. A shared global store re-couples everything.
- **Cross-cutting concerns:** auth/session, routing ownership, shared observability and error tracking.
- **Performance:** duplicate libraries in multiple bundles.
- **Contracts and testing:** integration tests at the shell level.

When **not** to use them: a single team or a modest codebase — the operational overhead outweighs the benefit, and you risk a "distributed monolith". A well-structured modular monolith (a monorepo with clear feature boundaries, Nx or Turborepo) gives most of the organizational benefit with far less complexity.

**My answer — reusing React payment logic in a mobile app**

The key is to **separate business logic from UI**:
- Extract the pure TypeScript logic — validation, fee calculation, the payment state machine — and the API client into a shared package in a monorepo. Expose it to React through headless hooks (`usePaymentFlow`).
- **React Native** can reuse those packages and hooks directly; only the UI components differ (no DOM).
- If the mobile app is fully native (Swift/Kotlin), shared JavaScript isn't an option, so I'd move the rules to the backend or a BFF so both clients call the same API. A WebView-embedded payment flow is the fastest route, with UX and security trade-offs.
- For payments specifically: use the payment provider's SDK and tokenization so raw card data never touches our code (PCI DSS scope), and make payment submission idempotent.

**Likely follow-ups:** "How do micro-frontends share state?" "How would you handle a shared header?" "Module Federation — how does dependency sharing work?"

---

### Q40. "Implement reduce() (or another array method) from scratch" / array-manipulation problem

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** IBM ("implement reduce for a given array"), Accenture ("array manipulation in vanilla JavaScript").

**My answer**

`reduce` walks the array, passing an accumulator and each element to the callback, and returns the final accumulator. The edge cases interviewers look for: the optional initial value, the empty-array error, and skipping holes in sparse arrays.

```js
Array.prototype.myReduce = function (callback, ...initialValue) {
  if (typeof callback !== 'function') throw new TypeError(`${callback} is not a function`);

  const array = Object(this);
  const length = array.length >>> 0;
  let index = 0;
  let accumulator;

  if (initialValue.length > 0) {
    accumulator = initialValue[0];
  } else {
    while (index < length && !(index in array)) index++; // skip leading holes
    if (index >= length) throw new TypeError('Reduce of empty array with no initial value');
    accumulator = array[index++];                        // first element becomes the accumulator
  }

  for (; index < length; index++) {
    if (index in array) accumulator = callback(accumulator, array[index], index, array);
  }
  return accumulator;
};

[1, 2, 3, 4].myReduce((sum, n) => sum + n);     // 10
[1, 2, 3].myReduce((sum, n) => sum + n, 10);    // 16
[1, , 3].myReduce((sum, n) => sum + n);         // 4 — the hole is skipped
```

Why `...initialValue` instead of `initialValue = undefined`: `reduce(fn, undefined)` is a valid explicit initial value, so I check whether the argument was **passed**, not whether it's undefined.

I'd mention that in production code I never patch built-in prototypes — it's done here only because the question asks for a polyfill. In real code I'd write a standalone function.

A typical "array manipulation" follow-up — group orders by status and total the paid ones (verified):

```js
const orders = [
  { status: 'paid', amount: 100 },
  { status: 'failed', amount: 50 },
  { status: 'paid', amount: 25 },
];

const ordersByStatus = orders.reduce((groups, order) => {
  (groups[order.status] ??= []).push(order);
  return groups;
}, {});
// Modern alternative: Object.groupBy(orders, order => order.status)

const paidTotal = orders
  .filter(order => order.status === 'paid')
  .reduce((sum, order) => sum + order.amount, 0); // 125
```

**Likely follow-ups:** "Implement map and filter using reduce." "Polyfill `Promise.all` / `bind`." "Why is `reduce` without an initial value risky?"

---

### Q41. "Live machine-coding in React" — build a Todo app / newsfeed card / number-pad / responsive nav menu

> **Priority:** ⭐ High · 3+ reports · Confidence: High
> **Where asked:** Microsoft Senior FE (newsfeed card at 5 YOE, number-pad, Todo app), Razorpay (responsive nav menu). Product and big-tech machine-coding rounds.

**My approach (what I say at the start)**

"I'll take two minutes to confirm requirements, sketch the component and state shape, get a working version first, then handle edge cases, accessibility and polish, and explain my choices as I go." Evaluators score working code, sensible state design, clean component boundaries, edge cases, accessibility and communication — not CSS perfection.

**Todo app** — `useReducer` keeps every state transition in one testable place:

```tsx
import { useReducer, useState } from 'react';

type Todo = { id: string; title: string; done: boolean };
type Filter = 'all' | 'active' | 'done';
type Action =
  | { type: 'added'; title: string }
  | { type: 'toggled'; id: string }
  | { type: 'deleted'; id: string };

function todosReducer(todos: Todo[], action: Action): Todo[] {
  switch (action.type) {
    case 'added':
      return [...todos, { id: crypto.randomUUID(), title: action.title, done: false }];
    case 'toggled':
      return todos.map(t => (t.id === action.id ? { ...t, done: !t.done } : t));
    case 'deleted':
      return todos.filter(t => t.id !== action.id);
  }
}

const FILTERS: Filter[] = ['all', 'active', 'done'];

export function TodoApp() {
  const [todos, dispatch] = useReducer(todosReducer, []);
  const [draft, setDraft] = useState('');
  const [filter, setFilter] = useState<Filter>('all');

  const visibleTodos = todos.filter(t =>
    filter === 'all' ? true : filter === 'done' ? t.done : !t.done,
  ); // derived during render, not stored in state
  const remainingCount = todos.filter(t => !t.done).length;

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const title = draft.trim();
    if (!title) return;
    dispatch({ type: 'added', title });
    setDraft('');
  }

  return (
    <section aria-labelledby="todo-heading">
      <h2 id="todo-heading">Todos ({remainingCount} left)</h2>
      <form onSubmit={handleSubmit}>
        <input value={draft} onChange={e => setDraft(e.target.value)} aria-label="New todo" />
        <button type="submit">Add</button>
      </form>

      <div role="group" aria-label="Filter todos">
        {FILTERS.map(f => (
          <button key={f} aria-pressed={filter === f} onClick={() => setFilter(f)}>{f}</button>
        ))}
      </div>

      {visibleTodos.length === 0 ? (
        <p>Nothing here.</p>
      ) : (
        <ul>
          {visibleTodos.map(todo => (
            <li key={todo.id}>
              <label>
                <input
                  type="checkbox"
                  checked={todo.done}
                  onChange={() => dispatch({ type: 'toggled', id: todo.id })}
                />
                {todo.title}
              </label>
              <button onClick={() => dispatch({ type: 'deleted', id: todo.id })} aria-label={`Delete ${todo.title}`}>
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
```

Things I'd point out: a real `<form>` so Enter works, trimming empty input, stable IDs as keys, derived filtering, and accessible labels.

**What I'd focus on for the other common prompts:**

- **Newsfeed card:** a typed `Post` prop (author, avatar, timestamp, text, image, like count); "See more" truncation for long text; relative time with `Intl.RelativeTimeFormat`; a like button with an **optimistic update** that rolls back if the API fails; lazy-loaded images with fixed dimensions to avoid layout shift; semantic `<article>`.
- **Number pad:** render digits from an array into a CSS grid; a controlled value with a max length; backspace and clear; **also support the physical keyboard** with a `keydown` listener cleaned up in the effect; `aria-label`s for icon buttons; disabled states at the limits.
- **Responsive nav menu:** CSS media queries for the layout (not JS); a hamburger button with `aria-expanded` and `aria-controls`; close on Escape, outside click and route change; move focus into the menu when it opens and back to the button when it closes; avoid layout jumps.

**Likely follow-ups:** "Persist todos" (`localStorage` with a lazy initializer, wrapped in try/catch). "Add edit-in-place." "How would you test this?" (React Testing Library: user-centric queries and interactions).

---

### Q42. "Tell me about yourself / your current project and role / your responsibilities"

> **Priority:** 🔥 Very High · 8+ reports · Confidence: High
> **Where asked:** The opening of essentially every round at TCS, Infosys, Deloitte, IBM, Accenture and Cognizant. It sets the interviewer's agenda for the rest of the round.

**How I structure it (60–90 seconds): present → proof → strengths → why this role**

1. **Present:** role, years of experience, core stack, type of domain.
2. **Proof:** one or two projects with *my* ownership and a measurable result.
3. **How I work:** the senior signals — design decisions, performance work, code reviews, mentoring, working with backend/product.
4. **Why this role:** one line connecting my experience to what they need.

**Template, written for a frontend-heavy full-stack profile** (replace every bracket with real details — interviewers will dig into whatever you mention):

> "I'm a frontend-focused full-stack engineer with about 7 years of experience, mostly with React, Next.js and TypeScript, plus Node.js, Express, PostgreSQL and both REST and GraphQL APIs. I've worked in large service organizations on [domain, e.g. banking / insurance / retail] applications for enterprise clients.
>
> On my current project, [project in one line — what it does and who uses it], I own [specific area, e.g. the customer onboarding module] end to end — from working out the API contract with the backend team to building the UI, writing tests, and supporting releases. One thing I'm proud of: [concrete improvement, e.g. 'I reduced the dashboard's load time from X to Y seconds by splitting the bundle by route and virtualizing a large table'].
>
> Beyond feature work, I [review pull requests / mentor two junior developers / set up our component library / improved our testing approach]. I'm looking for a senior role where I can take more ownership of frontend architecture and technical decisions, which is why this position interests me."

**For "your current project and responsibilities"** I describe: the business problem; the architecture at a high level (frontend stack, state and data fetching, how it talks to the backend, deployment); team size and my position in it; then two or three responsibilities phrased as ownership ("I designed…", "I decided…", "I led…") with outcomes.

Mistakes to avoid:
- Reciting the resume chronologically, or going past two minutes.
- Saying "we" for everything — interviewers need to hear what **I** did.
- No numbers. Even rough ones ("cut build time by about half") are far stronger than adjectives.
- Mentioning technologies I can't go deep on — each one becomes a follow-up question.
- Framing work as "I was assigned tickets". Describe the same work in terms of the features I owned, the problems I solved, and the decisions I influenced.

**Likely follow-ups:** "What was the biggest technical challenge on that project?" "Describe the architecture." "What would you do differently?" "Why are you leaving?"

---

### Q43. "What happens if you call setState in the render method?" / "What is the second parameter of setState (callback)?"

> **Priority:** 🟡 Medium · 1 report · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree (both), as tricky React theory.

**My answer — setState during render**

Rendering must be pure: given the same props and state, return the same JSX with no side effects. Calling `setState` unconditionally during render schedules another render, which calls `setState` again — an **infinite loop**. React stops it: function components throw **"Too many re-renders"**, and class components warn that you can't update during an existing state transition and loop.

```tsx
function Broken() {
  const [count, setCount] = useState(0);
  setCount(count + 1); // infinite loop → "Too many re-renders"
  return <p>{count}</p>;
}
```

A common accidental version: `onClick={setOpen(true)}` instead of `onClick={() => setOpen(true)}` — the setter is *called* during render.

The one documented exception in function components: a **conditional** update during render to adjust state when a prop changes. React re-renders the component immediately, before rendering children.

```tsx
function ItemList({ items }: { items: Item[] }) {
  const [previousItems, setPreviousItems] = useState(items);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  if (items !== previousItems) {   // guarded — runs once per change
    setPreviousItems(items);
    setSelectedId(null);           // reset selection when the list changes
  }
  // ...
}
```

Usually there's a simpler option: derive the value during render, or reset the component with a `key`.

**My answer — setState's second parameter**

In class components, `this.setState(updater, callback)` takes an optional callback that runs **after the state update has been applied and the component has re-rendered** (after `componentDidUpdate`). It exists because `setState` is asynchronous and batched, so reading `this.state` on the next line still gives the old value.

```jsx
this.setState(
  prev => ({ count: prev.count + 1 }),
  () => console.log('Updated count:', this.state.count), // the new value
);
```

Hooks have no callback parameter. If I need to act after an update, I either use the value I already computed (I know what I'm setting it to), or run the logic in a `useEffect` that depends on that state when it's genuinely a reaction to the state change.

**Likely follow-ups:** "Is setState synchronous?" "Why does `console.log(state)` right after `setState` show the old value?" (each render sees a snapshot).

---

### Q44. "What is an error boundary?"

> **Priority:** ⚪ Low–Medium · 1 report · Confidence: Low–Medium
> **Where asked:** Deloitte React-developer prep thread. Also a natural follow-up to Q15 and Q16.

**My answer**

An error boundary is a component that **catches JavaScript errors thrown while rendering its child tree** — in render, lifecycle methods and constructors — logs them, and shows a fallback UI instead of letting the whole app unmount to a blank screen.

It must be a class component, because it relies on two lifecycle methods with no hook equivalent:
- `static getDerivedStateFromError(error)` — update state to render the fallback.
- `componentDidCatch(error, info)` — side effects such as logging to Sentry.

```tsx
type ErrorBoundaryProps = { fallback: React.ReactNode; children: React.ReactNode };
type ErrorBoundaryState = { hasError: boolean };

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    reportError(error, info.componentStack); // monitoring service
  }

  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}
```

What it does **not** catch:
- Errors in **event handlers** — they don't happen during rendering; I use try/catch there.
- **Async code** — `setTimeout`, promise rejections, fetch failures.
- Server-side rendering errors, and errors in the boundary itself.

To route an async error into a boundary, I set state that throws during the next render, or use `react-error-boundary`'s `showBoundary`. That library also gives `resetKeys` and a "try again" button, which is what I use in practice.

**Placement:** granular, not one global boundary. An app-level boundary as a last resort, one per route, and one around independent widgets, so a broken chart doesn't take down the whole dashboard. Next.js App Router provides this through `error.tsx` files per route segment.

**Likely follow-ups:** "Why can't a function component be an error boundary?" "How do you reset an error boundary?" "How do you handle errors from API calls?"

---

### Q45. "What are React Portals — what are they and when do you use them?"

> **Priority:** 🟡 Medium · 1 report · Confidence: Medium
> **Where asked:** Capgemini Senior FE, verbatim, with the discussion going into modals, tooltips and z-index.

**My answer**

A portal renders children into a **different DOM node** — usually one directly under `<body>` — while keeping them in the **same place in the React tree**. So the content escapes its parent's CSS constraints, but context, state and event handling still behave as if it were rendered in place.

```tsx
import { createPortal } from 'react-dom';

function Modal({ isOpen, onClose, title, children }: ModalProps) {
  if (!isOpen) return null;
  return createPortal(
    <div className="modal-backdrop" onClick={onClose}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        onClick={e => e.stopPropagation()} // clicks inside shouldn't close it
      >
        <h2 id="modal-title">{title}</h2>
        {children}
      </div>
    </div>,
    document.body,
  );
}
```

**When I use them:** modals, tooltips, popovers, dropdown menus, toasts — anything that must visually escape a parent with `overflow: hidden`, a `transform`, or a lower stacking context that traps `z-index`.

**The gotcha interviewers like:** events bubble through the **React tree**, not the DOM tree. A click inside the portaled modal triggers `onClick` handlers on the React ancestors of `<Modal>`, even though the modal's DOM is under `<body>`. Context also flows through, which is usually what you want.

Senior considerations:
- **Accessibility:** trap focus inside the dialog, close on Escape, return focus to the trigger, make background content inert, and use proper dialog roles.
- The native `<dialog>` element with `showModal()` renders in the browser's **top layer**, which solves z-index and gives Escape handling and inert background for free; the Popover API does the same for popovers. For new work I consider these first.
- **SSR:** `document` doesn't exist on the server, so portals render after mount on the client.

**Likely follow-ups:** "How does event bubbling work with portals?" "How do you trap focus in a modal?" "Why not just raise z-index?" (stacking contexts can make it impossible).

---

### Q46. "Currying: implement sum(3)(5)(7)(3)() = 18" / "sum(a)(b)(c)()"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** KPMG (Glassdoor frontend set), IBM/Coforge/LTIMindtree (`sum = a => b => b ? sum(a+b) : a`).

**My answer**

Currying transforms a function that takes several arguments into a chain of functions that each take one: `f(a, b, c)` becomes `f(a)(b)(c)`. It relies on closures (Q1): each call remembers the running total.

For `sum(3)(5)(7)(3)()`, each call with a value returns a new function; the empty call ends the chain and returns the total:

```js
function sum(a) {
  return function next(b) {
    return b === undefined ? a : sum(a + b);
  };
}

sum(3)(5)(7)(3)(); // 18
sum(5)();          // 5
sum(1)(0)(2)();    // 3
```

I check `b === undefined` deliberately. The commonly shared one-liner `const sum = a => b => b ? sum(a + b) : a` uses a truthiness check, so **passing `0` ends the chain early** — `sum(1)(0)` returns the number 1, and the next call throws "is not a function" (verified). Pointing that out is a good senior signal.

A generic `curry` utility, based on the function's declared parameter count:

```js
function curry(fn) {
  return function curried(...args) {
    return args.length >= fn.length
      ? fn.apply(this, args)
      : (...nextArgs) => curried.apply(this, [...args, ...nextArgs]);
  };
}

const addThree = curry((a, b, c) => a + b + c);
addThree(1)(2)(3);  // 6
addThree(1, 2)(3);  // 6
addThree(1)(2, 3);  // 6
```

Variant without the final `()`: make the returned function convertible to a number.

```js
function infiniteSum(a) {
  const next = b => infiniteSum(a + b);
  next[Symbol.toPrimitive] = () => a;
  return next;
}
+infiniteSum(1)(2)(3); // 6
```

Where currying is useful in real code: partial application and configuration-first functions (`const logError = log('error')`), and React handler factories like `const handleFieldChange = field => event => setForm(f => ({ ...f, [field]: event.target.value }))`.

**Likely follow-ups:** "Currying vs partial application." "Implement `curry` for variadic functions." "Why does `fn.length` matter?" (it ignores default and rest parameters).

---

### Q47. "Get unique elements from an array without using Set" / "find the 2nd & 3rd largest"

> **Priority:** 🟡 Medium · 1 report · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree, explicit coding questions.

**My answer — unique elements without Set**

```js
// O(n) with a Map — keeps first-occurrence order and distinguishes 1 from '1'
function uniqueWithoutSet(items) {
  const seen = new Map();
  const result = [];
  for (const item of items) {
    if (!seen.has(item)) {
      seen.set(item, true);
      result.push(item);
    }
  }
  return result;
}
uniqueWithoutSet([1, '1', 2, 1, 3, 2]); // [1, '1', 2, 3]

// O(n²) but short — fine for small arrays
[1, 2, 1, 3].filter((item, index, arr) => arr.indexOf(item) === index); // [1, 2, 3]
```

The trade-offs I mention:
- Using a **plain object** as the lookup converts keys to strings, so `1` and `'1'` collide (verified: `[1, '1', 2]` becomes `[1, 2]`). `Map` keeps types.
- `filter` + `indexOf` is O(n²) — fine for tens of items, not thousands.
- Sorting first and comparing neighbors is O(n log n) but loses the original order.
- For objects, I dedupe by a key: track `seen` IDs rather than object references.

**My answer — second and third largest**

One pass, tracking the top three distinct values — O(n) time, O(1) space:

```js
function secondAndThirdLargest(numbers) {
  let first = -Infinity;
  let second = -Infinity;
  let third = -Infinity;

  for (const n of numbers) {
    if (n === first || n === second || n === third) continue; // distinct values only
    if (n > first) {
      [third, second, first] = [second, first, n];
    } else if (n > second) {
      [third, second] = [second, n];
    } else if (n > third) {
      third = n;
    }
  }
  const valueOrNull = value => (value === -Infinity ? null : value);
  return { second: valueOrNull(second), third: valueOrNull(third) };
}

secondAndThirdLargest([10, 5, 20, 20, 8, 15]); // { second: 15, third: 10 }
secondAndThirdLargest([4, 4]);                 // { second: null, third: null }
```

The simpler O(n log n) version is fine if they allow it — with the trap called out:

```js
[...new Set(numbers)].sort((a, b) => b - a).slice(1, 3); // [15, 10]
// Without a comparator, sort() compares as strings: [10, 9, 1, 100].sort() → [1, 10, 100, 9]
```

I'd clarify up front whether duplicates count ("is the second largest of [20, 20, 15] 20 or 15?") and what to return when there aren't enough values.

**Likely follow-ups:** "Find the k-th largest" (sort, or a min-heap of size k for O(n log k)). "Remove duplicates from an array of objects."

---

### Q48. "Write Redux createStore syntax" / "how is the store connected to routes?"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** LTIMindtree ("write redux createStore syntax", 2025), IBM/Coforge/LTIMindtree ("how the store is connected to React routes").

**My answer — createStore syntax**

The classic API is `createStore(reducer, preloadedState?, enhancer?)`:

```js
import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import { thunk } from 'redux-thunk';

const rootReducer = combineReducers({ auth: authReducer, loans: loansReducer });

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
  rootReducer,
  undefined,                                      // optional preloaded state
  composeEnhancers(applyMiddleware(thunk)),
);
```

I'd add that `createStore` is now **deprecated** in favor of Redux Toolkit's `configureStore`, which sets up thunk, DevTools, and development checks for accidental mutation and non-serializable values in one call:

```ts
import { configureStore } from '@reduxjs/toolkit';

export const store = configureStore({
  reducer: { auth: authReducer, loans: loansReducer },
});
```

**My answer — connecting the store and routes**

The store and the router are independent; both are providers near the root, and any component rendered by a route reads the store with `useSelector`:

```tsx
createRoot(document.getElementById('root')!).render(
  <Provider store={store}>
    <RouterProvider router={router} />
  </Provider>,
);
```

Common integration points:
- **Protected routes** read auth state from the store and redirect:

  ```tsx
  function RequireAuth() {
    const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
    const location = useLocation();
    return isAuthenticated ? <Outlet /> : <Navigate to="/login" state={{ from: location }} replace />;
  }
  ```

- **Route loaders** (React Router data APIs) can import the store and dispatch or prefetch — for example `store.dispatch(api.endpoints.getLoan.initiate(params.loanId))` with RTK Query — so data starts loading before the component renders.

Older apps used `connected-react-router` to mirror the location into Redux. I'd avoid that now: the **URL should be the source of truth** for route state, read through the router's own hooks; duplicating it in Redux creates two sources that can disagree.

**Likely follow-ups:** "What does `applyMiddleware` do?" "What is an enhancer?" "combineReducers — how does it work?"

---

### Q49. "map, filter, reduce in JS" / "how can objects be copied (shallow/deep)?"

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** IBM/Coforge/LTIMindtree, Cognizant. JS fundamentals.

**My answer**

All three are non-mutating array methods that take a callback `(item, index, array)` and return something new:

| Method | Returns | Use it to |
|---|---|---|
| `map` | New array, **same length** | Transform each element |
| `filter` | New array, **subset** | Keep elements that pass a test |
| `reduce` | **Any single value** (number, object, array) | Fold the array into a result — totals, grouping, lookup maps |

```js
const loans = [
  { id: 1, amount: 50000, status: 'approved' },
  { id: 2, amount: 20000, status: 'rejected' },
  { id: 3, amount: 80000, status: 'approved' },
];

const approvedAmounts = loans.filter(l => l.status === 'approved').map(l => l.amount); // [50000, 80000]
const totalApproved = approvedAmounts.reduce((sum, amount) => sum + amount, 0);       // 130000
const loansById = loans.reduce((map, loan) => ({ ...map, [loan.id]: loan }), {});
```

Points that show experience:
- **`map` vs `forEach`:** `map` returns a new array; `forEach` returns `undefined` and is for side effects. Using `map` and ignoring the result, or forgetting `return` in a block-bodied callback (giving `[undefined, …]`), are common mistakes.
- **The classic trap:** `['1', '2', '3'].map(parseInt)` gives `[1, NaN, NaN]`, because `map` passes the index as `parseInt`'s radix argument (verified). Use `map(Number)` or `map(s => parseInt(s, 10))`.
- **Performance:** chaining loops over the array several times. That's fine for typical UI data and more readable; for very large arrays in hot paths, one `reduce` or a `for` loop avoids intermediate arrays. Also, spreading the accumulator inside `reduce` (as in `loansById`) is O(n²) — for big inputs I mutate a local accumulator instead.
- `reduce` without an initial value throws on an empty array — I always pass one.
- In React state updates I also use the ES2023 non-mutating methods: `toSorted`, `toReversed`, `toSpliced` and `with`, instead of `sort()`/`reverse()`, which mutate the original array.

**Copying objects** is covered in Q2: spread and `Object.assign` are shallow; `structuredClone` is the standard deep copy (with its limits); `JSON.parse(JSON.stringify())` loses types; in React I use structural sharing rather than deep copies.

**Likely follow-ups:** "Implement map/filter/reduce from scratch" (Q40). "find vs filter." "some vs every."

---

### Q50. "Center a div using flex and grid" (CSS)

> **Priority:** 🟡 Medium · 2 reports · Confidence: Medium
> **Where asked:** TCS-tier and general senior FE screens — a quick CSS check, sometimes with follow-ups about the axes.

**My answer**

```css
/* Flexbox */
.flex-center {
  display: flex;
  justify-content: center; /* main axis (horizontal by default) */
  align-items: center;     /* cross axis (vertical by default) */
  min-height: 100dvh;      /* the container needs height to center vertically */
}

/* Grid — the shortest version */
.grid-center {
  display: grid;
  place-items: center;     /* shorthand for align-items + justify-items */
  min-height: 100dvh;
}

/* Child-side alternative inside a flex or grid container */
.child { margin: auto; }
```

Other approaches if asked:

```css
/* Absolute positioning — when the element must overlay its container */
.overlay-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Horizontal centering only, for a block with a width */
.block-center { width: 600px; margin-inline: auto; }
```

Modern browsers also support `align-content: center` on a normal block container, which centers content vertically without flex or grid.

Explanations that go beyond the snippet:
- **Axes:** `justify-content` works on the main axis and `align-items` on the cross axis. With `flex-direction: column`, they swap — a common source of "why isn't it centering?".
- The most common bug is the container having no height, so there's nothing to center within vertically.
- `100dvh` instead of `100vh` avoids the mobile browser address bar causing overflow.
- `translate(-50%, -50%)` can produce blurry text at half-pixel positions; flex or grid avoids that.
- **Flex vs grid:** flexbox is one-dimensional and content-driven (toolbars, rows of items); grid is two-dimensional and layout-driven (page layouts, card grids). For centering a single element, both are fine; grid is shorter.

**Likely follow-ups:** "Center text inside a button." "Difference between `align-items` and `align-content`." "Build a responsive card grid" (`grid-template-columns: repeat(auto-fill, minmax(240px, 1fr))`).

---

# Research Notes (from the original research)

### Notable company-specific first-hand sources used
- **EY (Ernst & Young):** LeetCode Discuss "EY India | Frontend Developer | August 2025 | 3.5 YOE" (full verbatim question list); Anil's Medium "EY React Interview Questions" (3+ YOE); Enginebogie EY Frontend Developer breakdown; JavaScript-in-Plain-English EY React.js engineer write-up.
- **Accenture:** Richa Gautam's three-part "React Interview Experience (August 2025): Accenture" (Medium/CodeToDeploy); Glassdoor Accenture Front-End (Chennai, May 2024 — custom hooks, side effects, large component trees); Naukri "4.5-years experienced Frontend developer interview in Accenture" (YouTube).
- **Capgemini:** Mohnish Sharma's "Capgemini Frontend Developer Interview Experience (20 LPA)" (Medium, Senior FE role, verbatim JS+React+logic questions).
- **TCS:** GeeksforGeeks "TCS Interview Experience for ReactJS Developer (3–6 Years Experienced)"; CodeReacher's "TCS Interview Experience — Java + React (4–6 Years)"; Fishbowl TCS React 6-YOE thread.
- **Infosys:** GeeksforGeeks "Infosys Interview Experience for React frontend developer"; Richa Gautam's "Infosys (August 2025)"; DEV Community "Infosys Frontend Developer (React) — Pune (3 YOE)".
- **IBM / Coforge / Valuelabs / LTIMindtree:** Pakki Prasanna's "Senior-Front End Engineer (5+ years) Interview Questions (IBM, Coforge, Valuelabs, LTI Mindtree)" (Medium); IBM Glassdoor (Feb 2025 — micro-frontend, React.memo vs useMemo, implement reduce); LTIMindtree Glassdoor (2025 — redux createStore syntax) and Naukri.
- **Cognizant:** Sona's "FrontEnd Developer Interview in Cognizant (2–4 yrs)" (Medium); Hrusikesh Swain's "React Native Interview experience with Cognizant" (Medium).
- **Deloitte / KPMG:** Deloitte UI Developer Glassdoor (vanilla-JS live coding — loops, objects, keys, closures, scopes, output prediction); Deloitte Frontend Developer Glassdoor (hoisting, reverse-a-string); Fishbowl Deloitte React threads (hooks, HOC, micro-frontend, error boundary); KPMG Glassdoor frontend set (closures, react-redux, ES5/ES6, currying).
- **Microsoft:** FrontendLead / Front End Interview Handbook Microsoft threads (Senior FE 5 YOE — newsfeed card; number-pad; Todo app); Glassdoor Microsoft Frontend Developer (3 technical rounds, live coding, React task).

## Recommendations
- **Prioritize the top 9** (closures; deep vs shallow copy; useMemo vs useCallback; debounce; prop drilling/Context; hoisting + output prediction; promises; React performance; useEffect). These appear in nearly every 4–<8 YOE report across all target companies and are the highest-ROI preparation.
- **Prepare follow-up depth, not just definitions.** The senior signal in these reports is the second/third question ("what is caching?", "is caching always beneficial?", "what if flat() isn't available?", "how do you prevent a race condition in useEffect?"). Practice explaining trade-offs aloud rather than reciting definitions.
- **Rehearse ~6 small coding tasks live:** fetch-and-render-table, debounced search, auto-increment counter, flatten nested array, reverse string/words, and one machine-coding component (Todo / newsfeed / nav menu). Service companies typically want one; Microsoft-tier wants a full component built end to end.
- **Tailor by company type:**
  - *TCS / Infosys / Wipro / Cognizant / LTIMindtree:* theory + output snippets + one small task + a managerial/scenario round.
  - *EY / Deloitte / Capgemini:* deeper JS internals plus React-18 and TypeScript follow-ups; Deloitte often opens with a vanilla-JS live-coding filter.
  - *IBM / Deloitte senior rounds:* expect micro-frontend architecture.
  - *Microsoft:* live React machine-coding + a system/API design discussion.
- **Benchmarks that should change your prep:** If targeting 6+ YOE, "Senior 2"/architect rounds, or product companies, add frontend system design (scalable dashboard, autocomplete component), micro-frontends, SSR/hydration, and React-18 concurrency — these surface more as YOE rises. If targeting the lower edge (4 YOE) or pure service-company screens, weight prep toward JS fundamentals and hooks theory over architecture.

## Caveats
- **Reddit gap:** No qualifying r/developersIndia or r/reactjs thread listing a specific senior candidate's actually-asked React/JS questions was found despite targeted searches; Teamblind, Fishbowl, LeetCode Discuss, and FrontendLead threads were used as first-hand community substitutes.
- **YOE precision:** Several Glassdoor / AmbitionBox / Fishbowl entries do not state exact years. Where a report was explicitly senior/experienced (e.g., Capgemini "Senior Frontend Developer, ~20 LPA"; EY 3.5 YOE; Microsoft Senior FE 5 YOE; IBM/Coforge/LTI "5+ years"; TCS 3–6 / 4–6 YOE) it is noted. A few entries at the 3–4 YOE edge were included because they sit at the lower boundary of the target band and matched senior/experienced role postings.
- **Frequency counts are the author's own approximate tally** of how often a question or close variant surfaced across the specific independent first-hand sources reviewed here — not a statistical survey. Some counts combine one strongly-worded detailed report with lighter corroboration.
- **Attribution risk:** A few items (e.g., the KPMG currying set on Glassdoor's aggregated frontend page) are candidate-submitted but sit on aggregated pages; treat single-source, single-company attributions (Confidence Medium/Low) with appropriate caution.
- **Answers were deliberately excluded** per the task scope — this is a question-collection deliverable only. Generic "top 50" listicles and AI-generated question banks were excluded from the ranking and used, at most, only to confirm that a question also circulates widely.

## Sources

1. [Infosys Interview Experience for React frontend developer - GeeksforGeeks](https://www.geeksforgeeks.org/infosys-interview-experience-for-react-frontend-developer/)
2. [EY React Interview Questions (Frontend Developer) | by Anil | Medium](https://medium.com/@anil-singh/ey-react-interview-questions-frontend-developer-68f7d5659ccb)
3. [FrontEnd Developer Interview in Cognizant(2–4 yrs) | by Sona | Frontend Weekly | Medium](https://medium.com/front-end-weekly/frontend-developer-interview-in-cognizant-2-4-yrs-c7bbb6c2b4cb)
4. [EY India | Frontend Developer | August 2025 | 3.5 YOE - Discuss - LeetCode](https://leetcode.com/discuss/post/7142108/)
5. [🚀 React Interview Experience (August 2025): Accenture (Part-1)](https://medium.com/codetodeploy/react-interview-experience-august-2025-accenture-part-1-03e4e95c66ac)
6. [Deloitte Frontend Developer Interview Experience & Questions](https://www.glassdoor.com/Interview/Deloitte-Frontend-Developer-Interview-Questions-EI_IE2763.0,8_KO9,27.htm)
7. [🚀 React Interview Experience (August 2025): Accenture (Part -2)](https://medium.com/codetodeploy/react-interview-experience-august-2025-accenture-part-2-0252d9b12f6e)
8. [IBM React Developer Interview Questions | Glassdoor](https://www.glassdoor.co.in/Interview/IBM-React-Developer-Interview-Questions-EI_IE354.0,3_KO4,19.htm)
9. [TCS Interview Experience for ReactJS Developer ( 3-6 Years Experienced) - GeeksforGeeks](https://www.geeksforgeeks.org/interview-experiences/tcs-interview-experience-for-reactjs-developer-3-6-years-experienced/)
10. [Senior-Front End Engineer(5+ years experience)Interview Questions(IBM,Coforge,Valuelabs,LTI…](https://medium.com/@prasannaaudi5/senior-front-end-engineer-5-years-experience-interview-questions-ibm-coforge-valuelabs-lti-c50893d62cb8)
11. [LTIMindtree interview experience Real time questions & tips from candidates to crack your interview](https://www.naukri.com/code360/interview-experiences/ltimindtree/interview-experience-frontend-developer-jan-2024-exp-0-2-years-2)
12. [🚀 React Interview Experience (August 2025): Accenture (Part -3)](https://medium.com/codetodeploy/react-interview-experience-august-2025-accenture-part-3-91ea17f83b40)
13. [Cognizant React JS Interview Questions - Credo Systemz](https://www.credosystemz.com/cognizant-react-js-interview-questions/)
14. [Accenture Front End Developer Interview Questions | Glassdoor](https://www.glassdoor.co.in/Interview/Accenture-Front-End-Developer-Interview-Questions-EI_IE4138.0,9_KO10,29.htm)
15. [LTIMindtree Full Stack Developer Interview Experience & Questions | Glassdoor](https://www.glassdoor.com/Interview/LTIMindtree-Full-Stack-Developer-Interview-Questions-EI_IE8441464.0,11_KO12,32.htm)
