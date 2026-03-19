Feature: Cart

  Scenario: Add first sofa to cart and verify price
    Given open sofas catalog
    When user adds first product to cart and dismisses dialog
    And user opens cart from header
    Then added product should be displayed in cart
    And cart price should match catalog price