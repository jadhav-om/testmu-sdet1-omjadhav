Feature: REST API Regression

  @smoke @regression @security
  Scenario: Valid token grants access to protected endpoint
    Given a valid user credential payload
    When the client requests an auth token
    And calls a protected endpoint using that token
    Then the API should return HTTP 200
    And the response body should contain authorized user context

  @regression @security @negative
  Scenario: Invalid token is rejected
    Given an invalid or tampered bearer token
    When the token is used on a protected endpoint
    Then the API should return HTTP 401 or 403
    And the error response should describe token validation failure

  @regression
  Scenario: CRUD lifecycle succeeds for a resource
    Given a valid create payload for a resource
    When the client performs create, read, update, and delete operations
    Then each operation should return expected HTTP status codes
    And the updated representation should match submitted values

  @regression @negative
  Scenario: API returns correct 4xx and 5xx error contracts
    Given a malformed request and an unavailable service condition
    When the client calls target endpoints
    Then 4xx errors should include actionable validation details
    And 5xx errors should return standardized server error schema

  @regression
  Scenario: Rate limiting policy is enforced
    Given a client exceeds configured request threshold
    When additional requests are sent within the same window
    Then the API should return HTTP 429
    And rate-limit headers should include limit, remaining, and reset fields

  @regression
  Scenario: Response schema validation for core entities
    Given a successful GET request for a core entity
    When the response is received
    Then the body should conform to the agreed JSON schema
    And no undocumented fields should violate strict schema rules