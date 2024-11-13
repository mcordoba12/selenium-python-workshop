Feature: Django Login Feature

  Scenario: Successful login with valid credentials
    Given the user is on the Django login page
    When the user logs in with valid credentials
    Then the user should be redirected to the dashboard page

  Scenario: Unsuccessful login with invalid credentials
    Given the user is on the Django login page
    When the user logs in with invalid credentials
    Then an error message should be displayed


