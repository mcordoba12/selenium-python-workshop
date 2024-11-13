Feature: Django Cliente Registration Feature

  Scenario: Successful registration with valid credentials
    Given the user is on the Django registration page
    When the user registers with valid credentials
    Then the user should be redirected to the client home page

  Scenario: Unsuccessful registration with invalid credentials
    Given the user is on the Django registration page
    When the user registers with invalid credentials
    Then an error message for registration should be displayed
