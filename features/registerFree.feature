Feature: Freelancer registration and profile editing

  Scenario: Successful registration and profile completion
    Given the user is on the Django freelancer registration page
    When the user registers with valid freelancer credentials
    And the user fills the freelancer profile information
    Then the user should be redirected to the freelancer home page

  Scenario: Unsuccessful registration with invalid freelancer credentials
    Given the user is on the Django freelancer registration page
    When the user registers with invalid freelancer credentials
    Then an error message for freelancer registration should be displayed
