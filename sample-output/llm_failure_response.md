# Sample LLM Failure Output

This is a sample of what gets written under `reports/llm/*.md` when a test fails and `OPENAI_API_KEY` is configured.

## Example

**Test**: `tests/ui/test_login.py::test_invalid_credentials`

1) What failed  
The test expected successful navigation to `/inventory.html`, but the page stayed on login and displayed an authentication error.

2) Most likely root cause  
The provided password does not match the expected value for `standard_user`, so authentication failed as designed.

3) Suggested fix  
Update test data to use valid credentials for positive-path tests, or change assertion to validate the error banner for negative-path tests.

4) Confidence (High/Medium/Low)  
High