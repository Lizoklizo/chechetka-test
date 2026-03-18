Feature: Product details

  Scenario: Check sofa details in product card
    Given open sofas catalog
    When user opens sofa card by name "Диван Шенилл"
    Then opened product title should contain "Шенилл"
    When user opens the "Характеристики" tab
    Then product width should be the same as in catalog
    And product depth should be the same as in catalog