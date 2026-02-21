# Prompt Engineering Log (Raw Prompts)

## Login Module Prompt (Iteration 1)
You are a senior QA engineer. Generate login test cases.

## Login Module Prompt (Iteration 2)
You are a senior SDET creating regression assets for a web test management product.
Generate exhaustive test cases for the Login module in Gherkin format.
Include: valid login, invalid credentials, forgot password, session expiry, brute-force lockout.
For each scenario, include priority (P0/P1/P2), test data, preconditions, and expected outcome.
Keep steps implementation-agnostic and deterministic.

## Dashboard Module Prompt (Iteration 1)
Generate dashboard tests.

## Dashboard Module Prompt (Iteration 2)
You are a QA lead. Produce Dashboard module regression scenarios in Gherkin.
Coverage required: widget loading, data accuracy, filter/sort behavior, responsive layout, permission-based visibility.
Add edge cases for empty widgets, delayed API responses, and role-based restrictions.
Include tags (@smoke, @regression, @negative) and measurable assertions.

## REST API Module Prompt (Iteration 1)
Give me API test cases.

## REST API Module Prompt (Iteration 2)
You are an SDET specializing in API automation.
Generate REST API test cases in Gherkin for:
- auth token validation
- CRUD operations
- error handling (4xx/5xx)
- rate limiting
- schema validation
For each test case, include endpoint pattern, HTTP method, sample payload, expected status, and schema expectation.
Also include negative and boundary cases.