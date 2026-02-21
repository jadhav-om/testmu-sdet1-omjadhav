Feature: Login Module Regression

  @smoke @regression
  Scenario: Successful login with valid credentials
    Given the user is on the login page
    When the user enters valid username and valid password
    And clicks the Sign In button
    Then the user should be redirected to the dashboard
    And an active authenticated session should be created

  @regression @negative
  Scenario: Login fails with invalid password
    Given the user is on the login page
    When the user enters a valid username and invalid password
    And clicks the Sign In button
    Then the system should display an authentication error message
    And the user should remain unauthenticated

  @regression
  Scenario: Forgot password sends reset instructions for registered email
    Given the user is on the forgot password screen
    When the user submits a registered email address
    Then the system should confirm that reset instructions were sent
    And a reset token should be generated with expiry metadata

  @regression @security
  Scenario: Session expires after inactivity threshold
    Given the user is logged in
    And no activity occurs for the configured inactivity timeout
    When the user performs a protected action
    Then the user should be redirected to login
    And the session token should be invalidated

  @regression @security @negative
  Scenario: Account lockout after repeated failed logins
    Given the account exists and lockout policy is enabled
    When 5 consecutive login attempts fail within the lockout window
    Then the account should be temporarily locked
    And further attempts should return a lockout message