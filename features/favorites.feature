Feature: Favorites

  Scenario: Add first sofa to favorites
    Given open sofas catalog
    When user adds the first sofa to favorites
    And user opens favorites page
    Then selected sofa should appear in favorites