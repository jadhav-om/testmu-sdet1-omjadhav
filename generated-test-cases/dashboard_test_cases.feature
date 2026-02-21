Feature: Dashboard Module Regression

  @smoke @regression
  Scenario: Dashboard widgets load successfully
    Given an authorized user is on the dashboard
    When dashboard data calls complete
    Then all mandatory widgets should render
    And each widget should show a non-error state

  @regression
  Scenario: Dashboard data matches backend source
    Given an authorized user is on the dashboard
    When the dashboard displays KPIs and counts
    Then the values should match the latest backend response
    And currency/number formatting should follow product rules

  @regression
  Scenario: Filter and sort controls return expected ordering
    Given an authorized user is viewing dashboard data
    When the user applies a filter and sort combination
    Then visible rows/cards should reflect only filtered data
    And sort order should remain stable across refresh

  @regression
  Scenario: Responsive layout adapts to mobile viewport
    Given an authorized user opens the dashboard on 390x844 viewport
    Then primary navigation should remain usable
    And dashboard content should not overlap or clip
    And horizontal scrolling should be avoided for core widgets

  @regression @security
  Scenario: Permission-based visibility hides restricted widgets
    Given a user with limited role permissions is logged in
    When the dashboard loads
    Then restricted widgets should not be visible
    And direct URL access to restricted dashboard sections should be denied