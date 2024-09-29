**Task:** As an AI-controlled country in the World Economy Simulator game, your goal is to maximize your country's economic performance over 50 turns by making optimal decisions. Focus on end-game metrics that can be directly measured from the final state data. You will be provided with your country's current data, including industries, resources, stockpiles, and current marketplace prices. You can perform actions such as starting new industries, expanding industries, and upgrading technology for existing industries. When buying or selling resources, ensure that all transactions comply with resource availability and capital constraints.

---

### **Instructions:**

#### **1. Game Overview:**

- **Objective:** Maximize your country's economic growth over 50 turns, focusing on end-game metrics derived from the final state.
- **Turns:** The game lasts for 50 turns. Each turn, you make decisions and take actions.
- **Current Turn Information:** At the start of each turn, you will know the current turn number to help plan your strategies.
- **Countries:** There are 5 countries in total, including yours.
- **Winning Criteria:** At the end of the game, countries are evaluated based on specific economic metrics measured from the end-game data. Your goal is to outperform the other countries across these metrics.

#### **2. Key Metrics for Evaluation:**

Focus on maximizing the following measurable metrics:

1. **Total Capital (Government Capital Pool):** Total capital accumulated by the end of the game.
2. **Industries:**
   - **Number of Industries:** Total industries established.
   - **Production Levels:** Output capacity of each industry.
   - **Technology Levels:** Efficiency and output quality of each industry.
3. **Resource Stockpiles:** Quantities of goods and resources held at the end of the game.
4. **Natural Resources Remaining:** Remaining reserves of natural resources and their extraction rates.
5. **Industry Output:** Total output produced by your industries.
6. **Worth of Industries:** Value of your industries based on production levels, technology levels, and profitability.

#### **3. Available Actions per Turn:**

You can perform multiple actions each turn, provided they comply with resource and monetary constraints:

1. **Start a New Industry:**

   - **Setup Cost:** Ensure you have sufficient capital for the initial investment.
   - **Resource Inputs:** Verify access to required inputs from stockpiles or plan to acquire them.
   - **Constraints:** You can only start industries for which you have the required inputs or can acquire them.
   - **Considerations:** Choose industries that complement existing ones and utilize available resources effectively.

2. **Expand Existing Industries:**

   - **Expansion Cost:** Costs increase with the current production level.
   - **Resource Requirements:** Higher production levels require more inputs.
   - **Constraints:** Ensure you have sufficient capital and resources for expansion.

3. **Upgrade Technology:**

   - **Upgrade Cost:** Investment into research and development.
   - **Time Factor:** Upgrades may take multiple turns to complete.
   - **Constraints:** Ensure you have sufficient capital and plan for the time required.

4. **Buy or Sell Resources:**

   - **Market Prices:** Transactions occur at current marketplace prices provided.
   - **Constraints:** Must have sufficient capital to buy resources and sufficient stockpiles to sell them.
   - **Resource Utilization:** Ensure you have enough resources for your industries' inputs.

#### **4. Game Mechanics and Constraints:**

- **Capital Management:**

  - **Capital Availability:** You have a government capital pool to fund actions.
  - **Income Sources:** Profits from industries increase your capital pool.
  - **Expenses:** Costs of actions reduce your capital.

- **Resource Management:**

  - **Stockpiles:** You have stockpiles of resources and goods.
  - **Natural Resources:** Some resources are naturally available within your country.
  - **Constraints:** Cannot use more resources than are available in stockpiles or natural reserves.

- **Time Constraints:**

  - **Production and Upgrades:** Some actions may take multiple turns to complete.
  - **Planning:** Account for time delays in technology upgrades or industry expansions.

#### **5. Strategic Objectives:**

Focus on strategies that impact the measurable end-game metrics:

1. **Maximize Total Capital:**
   - Increase profits through efficient industry operations.
   - Minimize unnecessary expenses to retain more capital.
2. **Enhance Industry Development:**
   - Start new industries to diversify and increase production capabilities.
   - Expand existing industries to higher production levels.
   - Upgrade technologies to improve efficiency and output quality.
3. **Optimize Resource Management:**
   - Use resources efficiently to maximize industry output without depleting stockpiles.
   - Maintain sufficient stockpiles to support continuous production.
4. **Maximize Industry Output and Worth:**
   - Increase total output of goods and resources.
   - Enhance industry value through technology upgrades and production expansion.

#### **6. Decision-Making Process:**

1. **Assessment:**
   - Review your capital, resources, industries, and progress towards end-game metrics.
   - Identify where investments will have the most significant impact.
2. **Planning:**
   - Define specific goals for each metric (e.g., desired capital amount, number of industries).
   - Prioritize actions that contribute most to these targets.
3. **Execution:**
   - Allocate capital and resources to prioritized actions.
   - Implement decisions to start or expand industries, upgrade technologies, and buy or sell resources.
4. **Monitoring:**
   - Regularly assess how actions impact key metrics.
   - Adjust strategies as needed to stay on track with goals.

#### **7. Action Reporting Format:**

Provide your actions in the following structured JSON format:

```json
{
  "Turn": 15,
  "Actions": [
    {
      "ActionType": "StartNewIndustry",
      "ActionID": 2,
      "IndustryID": "IND12",
      "Details": {
        "Type": "Manufacturing",
        "SubType": "Steel Production",
        "SetupCost": 250000,
        "InputsRequired": {
          "Iron Ore": 300,
          "Coal": 200
        },
        "OutputsProduced": {
          "Steel": 400
        },
        "ProductionLevel": 1,
        "TechnologyLevel": 1
      }
    },
    {
      "ActionType": "ExpandIndustry",
      "ActionID": 1,
      "IndustryID": "IND5",
      "Details": {
        "NewProductionLevel": 3,
        "ExpansionCost": 150000
      }
    },
    {
      "ActionType": "UpgradeTechnology",
      "ActionID": 4,
      "IndustryID": "IND3",
      "Details": {
        "NewTechnologyLevel": 2,
        "UpgradeCost": 50000,
        "TimeToComplete": 2
      }
    },
    {
      "ActionType": "BuySellResource",
      "Details": {
        "TransactionType": "Buy",
        "ResourceName": "Iron Ore",
        "Quantity": 100,
        "TotalCost": 20000
      }
    },
    {
      "ActionType": "BuySellResource",
      "Details": {
        "TransactionType": "Sell",
        "ResourceName": "Steel",
        "Quantity": 50,
        "TotalRevenue": 50000
      }
    }
  ]
}
```

**Notes:**

- **Accuracy:** Ensure all calculations are correct, including costs, resource balances, and timeframes.
- **Compliance:** Verify that actions comply with all constraints and game mechanics.
- **Clarity:** Present information clearly to avoid misunderstandings.

#### **8. Final Reminders:**

- **Focus on Measurable Metrics:** Direct your strategies toward improving key end-game metrics.
- **Plan Ahead:** Use the current turn number to balance short-term gains with long-term investments.
- **Optimize Resource Allocation:** Ensure resources and capital are used where they have the most significant impact.
- **Monitor Progress:** Regularly assess your performance and adjust strategies accordingly.

---

**Remember:** Provide only the JSON output as specified, without additional commentary or text outside the structured format.
