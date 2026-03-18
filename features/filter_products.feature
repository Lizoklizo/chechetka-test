Feature: Filter sofas by price

Scenario: Filter sofas between 10000 and 15000 rubles
    Given open sofas catalog
    When apply price filter
    Then sofa with name should appear in results