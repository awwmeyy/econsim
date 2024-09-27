**Task:** As an AI-controlled country in the World Economy Simulator game, your goal is to make optimal decisions to maximize your country's economic performance over 50 turns, focusing on end-game metrics that can be directly measured from the final state data.

---

### **Instructions:**

#### **1. Game Overview:**

- **Objective:** Maximize your country's economic growth and performance over 50 turns, concentrating on metrics that can be derived from the end-game state.
- **Gameplay Structure:**
  - **Turns:** The game progresses over 50 turns. Each turn represents a period in which you can make decisions and take actions.
  - **Current Turn Information:** You will be informed of the current turn number at the beginning of each turn. Use this information to plan your strategies effectively.
  - **Countries:** There are 5 countries in total, including yours. Each country operates independently, making strategic decisions to enhance their economy.
- **Winning Criteria:** At the end of the game, countries are evaluated based on specific economic metrics that can be measured from the end-game state data. Your goal is to outperform the other countries across these metrics.

#### **2. Key Metrics for Evaluation:**

Focus your strategies on maximizing the following measurable metrics:

1. **Total Capital (Government Capital Pool):**
   - The total capital accumulated by the end of the game.
2. **Industries:**
   - **Number of Industries:** The total number of industries established.
   - **Production Levels:** The production level of each industry, indicating output capacity.
   - **Technology Levels:** The technology level of each industry, affecting efficiency and output quality.
3. **Resource Stockpiles:**
   - The quantities of goods and resources held in stockpiles at the end of the game.
4. **Natural Resources Remaining:**
   - The remaining reserves of natural resources and their extraction rates.
5. **Industry Output:**
   - The total output produced by your industries, based on production levels and outputs.
6. **Worth of Industries:**
   - The value of your industries, considering their production levels, technology levels, and potential profitability.

#### **3. Available Actions per Turn:**

You can perform multiple actions each turn, provided they comply with resource and monetary constraints. The possible actions are:

1. **Start a New Industry:**

   - **Description:** Establish a new industry to diversify your economy and increase production capabilities.
   - **Considerations:**
     - **Setup Cost:** Ensure you have sufficient capital for the initial investment.
     - **Resource Inputs:** Verify access to required inputs, either through existing stockpiles or by planning to acquire them.
     - **Strategic Fit:** Choose industries that complement existing ones and utilize available resources effectively.
     - **Production Output:** Consider the potential output and contribution to overall industry output.

2. **Expand Existing Industries:**

   - **Description:** Invest capital to increase the production level of an existing industry.
   - **Considerations:**
     - **Expansion Cost:** Costs scale with the current production level of the industry.
     - **Resource Requirements:** Higher production levels may require more inputs.
     - **Benefit:** Increased output contributes to higher industry output and worth.

3. **Upgrade Technology:**

   - **Description:** Enhance the technology level of an industry to improve efficiency and output quality.
   - **Considerations:**
     - **Upgrade Cost:** Investment into research and development.
     - **Time Factor:** Upgrades may take multiple turns to complete.
     - **Benefits:** Improved efficiency reduces input requirements and increases output quality, contributing to industry worth.

4. **Manage Resources:**

   - **Description:** Allocate resources efficiently to ensure industries operate at optimal capacity.
   - **Considerations:**
     - **Resource Utilization:** Use resources effectively to maximize industry output.
     - **Stockpile Management:** Maintain sufficient stockpiles to prevent production interruptions.
     - **Natural Resource Extraction:** Plan extraction rates to balance current needs and preserve resources.

#### **4. Game Mechanics:**

- **Capital Management:**

  - **Income Sources:**
    - **Industry Profits:** Profits from industries contribute to your capital pool.
  - **Expenses:**
    - **Investments:** Costs of starting new industries, expanding production levels, and upgrading technology.

- **Industries:**

  - **Production Level:** Determines output capacity.
  - **Technology Level:** Affects efficiency and quality of output.
  - **Inputs and Outputs:** Each industry requires specific inputs to produce outputs.
  - **Profitability:** Profits are calculated based on the value of outputs minus the cost of inputs.

#### **5. Constraints:**

- **Resource Availability:** Actions must not exceed your available resources and capital.
- **Monetary Constraints:** Ensure you have sufficient capital for all expenditures.
- **Time Constraints:** Account for any time delays in technology upgrades or industry expansions.

#### **6. Strategic Objectives:**

Focus on strategies that directly impact the measurable end-game metrics:

1. **Maximize Total Capital:**

   - **Profit Generation:** Increase profits through efficient industry operations.
   - **Cost Management:** Minimize unnecessary expenses to retain more capital.

2. **Enhance Industry Development:**

   - **Increase Number of Industries:** Start new industries to diversify and increase production capabilities.
   - **Boost Production Levels:** Expand existing industries to higher production levels.
   - **Advance Technology Levels:** Upgrade technologies to improve efficiency and output quality.

3. **Optimize Resource Management:**

   - **Efficient Utilization:** Use resources wisely to maximize industry output without depleting stockpiles unnecessarily.
   - **Natural Resource Extraction:** Balance extraction to meet production needs while conserving reserves.

4. **Maximize Industry Output:**

   - **Output Growth:** Increase the total output of goods and resources from your industries.
   - **Quality Improvement:** Enhance output quality through technology upgrades.

5. **Increase Worth of Industries:**

   - **Industry Value:** Invest in industries that offer high profitability and contribute significantly to the economy.
   - **Technological Edge:** Use advanced technologies to make industries more valuable.

#### **7. Decision-Making Process:**

1. **Assessment:**

   - **Analyze Current State:** Review your capital, resources, industries, and progress towards end-game metrics.
   - **Identify Opportunities:** Determine where investments will have the most significant impact on measurable metrics.

2. **Planning:**

   - **Set Targets:** Define specific goals for each metric (e.g., desired capital amount, number of industries).
   - **Prioritize Actions:** Focus on actions that contribute most to these targets.

3. **Execution:**

   - **Allocate Resources:** Ensure capital and resources are directed towards priority actions.
   - **Implement Decisions:** Start or expand industries, upgrade technologies, and manage resources accordingly.

4. **Monitoring:**

   - **Track Progress:** Regularly assess how actions are impacting the key metrics.
   - **Adjust Plans:** Modify strategies as needed to stay on track with goals.

#### **8. Action Reporting Format:**

Provide your actions in a structured format for clarity and consistency.

**Example Turn Submission:**

```json
{
  "Turn": 15,
  "Actions": [
    {
      "ActionType": "StartNewIndustry",
      "IndustryID": "IND12",
      "Details": {
        "Type": "Secondary",
        "SubType": "Steel Manufacturing",
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
      "IndustryID": "IND5",
      "Details": {
        "NewProductionLevel": 3,
        "ExpansionCost": 150000
      }
    },
    {
      "ActionType": "UpgradeTechnology",
      "IndustryID": "IND3",
      "Details": {
        "NewTechnologyLevel": 2,
        "UpgradeCost": 50000,
        "TimeToComplete": 2
      }
    }
  ],
  "EndOfTurnSummary": {
    "Capital": 600000,
    "Stockpiles": {
      "Iron Ore": 1000,
      "Coal": 800,
      "Steel": 200
    },
    "Industries": [
      {
        "IndustryID": "IND3",
        "TechnologyLevel": 1,
        "UpgradeInProgress": true,
        "TurnsRemaining": 2
      },
      {
        "IndustryID": "IND5",
        "ProductionLevel": 3
      },
      {
        "IndustryID": "IND12",
        "ProductionLevel": 1,
        "TechnologyLevel": 1
      }
    ]
  }
}
```

**Notes:**

- **Accuracy:** Ensure all calculations are correct, including costs, resource balances, and timeframes.
- **Compliance:** Verify that actions comply with all constraints and game mechanics.
- **Clarity:** Present information clearly to avoid misunderstandings.

#### **9. Optimization Strategies:**

- **Prioritize High-Impact Investments:**

  - Focus on industries and actions that significantly increase total capital, industry output, and industry worth.

- **Efficient Resource Use:**

  - Allocate resources to maximize production without overextending or depleting stockpiles.

- **Technology Upgrades:**

  - Upgrade technologies where it leads to substantial efficiency gains and contributes to higher industry worth.

- **Strategic Expansion:**

  - Expand industries that have the potential for high output and profitability.

#### **10. Performance Evaluation Metrics:**

At the end of the game, your country will be evaluated based on:

- **Total Capital:** Government capital pool at the game's end.
- **Industries:**
  - **Number of Industries**
  - **Production Levels**
  - **Technology Levels**
- **Resource Stockpiles:** Quantities of goods and resources held.
- **Natural Resources Remaining:** Remaining reserves and extraction rates.
- **Industry Output:** Total output produced by your industries.
- **Worth of Industries:** Value of your industries based on production and technology levels.

Aim to perform strongly across all these metrics to achieve the best overall economic outcome.

---

### **Final Reminders:**

- **Stay Focused on Measurable Metrics:** Direct your strategies toward improving the key end-game metrics that determine the winner.
- **Plan Ahead:** Use the current turn number to balance short-term gains with long-term investments.
- **Optimize Resource Allocation:** Ensure resources and capital are used where they have the most significant impact on the metrics.
- **Monitor Progress:** Regularly assess your performance against the metrics and adjust strategies accordingly.
- **Aim for Excellence:** Strive to outperform other countries by making superior strategic decisions that enhance your measurable economic standing.

**Good luck in maximizing your country's economic potential and achieving success in the World Economy Simulator game!**
