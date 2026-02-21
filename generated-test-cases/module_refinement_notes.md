# Module Refinement Notes

## Login (what failed first, and what changed)
1. Initial prompt was too broad and returned only happy-path scenarios.
2. Added explicit required coverage items (forgot password, lockout, session expiry).
3. Required structured output fields (priority, preconditions, test data) to improve automation readiness.
4. Forced deterministic expectations to avoid ambiguous assertions.

## Dashboard (what failed first, and what changed)
1. First output mixed UI checks with implementation details (CSS selectors in Gherkin).
2. Refined prompt to request implementation-agnostic steps with measurable outcomes.
3. Added explicit edge-case constraints (empty state, delayed data, role restrictions).
4. Added tagging requirements so smoke/regression separation was immediately usable.

## REST API (what failed first, and what changed)
1. Initial output under-covered non-functional checks, especially rate limiting.
2. Added required metadata fields (method, endpoint pattern, payload, expected status, schema).
3. Added negative and boundary language for each coverage area.
4. Result became directly mappable to pytest + requests automation.