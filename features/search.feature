Feature: Search

  Scenario: Search sofa by name
    Given open sofas catalog
    When user searches for "Бостон"
    Then search results page should be loaded
    And first search result should contain "Бостон"