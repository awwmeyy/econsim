**Task:** Generate options for expanding existing industries based on the country's current schema.

---

**Instructions:**

1. **Input Data:**

   - You are provided with the country's current schema, which includes:
     - **Existing Industries**: Details about current industries, their production levels, inputs, outputs, etc.
     - **Government Capital Pool**: The amount of capital the country currently has.
     - **Workforce**: Number of skilled and unskilled workers available.
   - **Note:** Use only the provided data for your analysis.

2. **Objective:**

   - Generate **5 options** for expanding existing industries that the country can potentially undertake.
   - For each expansion option, provide:
     - **Industry ID**: The identifier of the existing industry to be expanded (e.g., "IND3").
     - **Current Production Level**: The industry's current production level.
     - **New Production Level**: The proposed new production level after expansion.
     - **Expansion Cost**: Capital required to expand the industry.
     - **Additional Skilled Workers Required**: Number of additional skilled workers needed due to expansion.
     - **Additional Unskilled Workers Required**: Number of additional unskilled workers needed due to expansion.
     - **Increase in Outputs**: Expected increase in outputs per production cycle.
     - **Additional Inputs Required**: Additional inputs needed per production cycle due to expansion.
     - **Justification**: Brief explanation of why expanding this industry is beneficial based on the country's current situation.

3. **Guidelines:**

   - **Feasibility:**
     - Ensure that the proposed expansions are realistic, considering the country's current capital and available workforce.
     - At least **half of the options** should be expansions that can be started **immediately** with current capital and workforce.
     - The other options can be more ambitious, requiring future capital or workforce growth.
   - **Strategic Impact:**
     - Prioritize expansions that significantly increase output and contribute to the country's economic goals.
     - Consider industries that are highly profitable or critical to the economy.
   - **Consistency:**
     - Expansion costs and worker requirements should be proportional to the increase in production level and industry complexity.
     - Higher production levels should yield proportionally higher outputs.

4. **Output Format:**

   - Provide the expansion options in a structured JSON format as shown below.
   - **Do not** include any additional text or explanations.

```json
{
  "IndustryExpansions": [
    {
      "Industry ID": "IND1",
      "Current Production Level": 2,
      "New Production Level": 3,
      "Expansion Cost": 100000,
      "Additional Skilled Workers Required": 20,
      "Additional Unskilled Workers Required": 80,
      "Increase in Outputs": {
        "Copper Ore": 200
      },
      "Additional Inputs Required": {},
      "Justification": "Expanding copper mining increases resource supply for domestic use and export."
    },
    {
      "Industry ID": "IND2",
      "Current Production Level": 1,
      "New Production Level": 2,
      "Expansion Cost": 150000,
      "Additional Skilled Workers Required": 30,
      "Additional Unskilled Workers Required": 120,
      "Increase in Outputs": {
        "Electronics": 100
      },
      "Additional Inputs Required": {
        "Copper Ore": 100,
        "Silicon": 50
      },
      "Justification": "Increasing electronics production meets growing demand and boosts exports."
    },
    {
      "Industry ID": "IND3",
      "Current Production Level": 2,
      "New Production Level": 4,
      "Expansion Cost": 300000,
      "Additional Skilled Workers Required": 50,
      "Additional Unskilled Workers Required": 200,
      "Increase in Outputs": {
        "Steel": 400
      },
      "Additional Inputs Required": {
        "Iron Ore": 200,
        "Coal": 150
      },
      "Justification": "Significant expansion in steel manufacturing supports construction and manufacturing sectors."
    },
    {
      "Industry ID": "IND4",
      "Current Production Level": 1,
      "New Production Level": 3,
      "Expansion Cost": 250000,
      "Additional Skilled Workers Required": 40,
      "Additional Unskilled Workers Required": 160,
      "Increase in Outputs": {
        "Chemicals": 300
      },
      "Additional Inputs Required": {
        "Oil": 100,
        "Natural Gas": 80
      },
      "Justification": "Expanding chemical production enhances capabilities in pharmaceuticals and manufacturing."
    },
    {
      "Industry ID": "IND5",
      "Current Production Level": 2,
      "New Production Level": 5,
      "Expansion Cost": 500000,
      "Additional Skilled Workers Required": 70,
      "Additional Unskilled Workers Required": 0,
      "Increase in Outputs": {
        "Software Products": 200
      },
      "Additional Inputs Required": {
        "Skilled Labor Hours": 2000
      },
      "Justification": "Aggressive expansion in software development capitalizes on the skilled workforce and high-value outputs."
    }
  ]
}
```

5. **Additional Notes:**

   - **Financial Constraints:**
     - At least **two or three** expansion options have costs within current capital availability.
   - **Workforce Availability:**
     - Ensure that additional worker requirements can be met with current or projected workforce.
   - **Resource Availability:**
     - Verify that additional inputs required are available or can be acquired.
   - **Strategic Priorities:**
     - Focus on industries that will significantly impact the country's economic metrics.

---

**Remember:** Provide only the JSON output as specified, without additional commentary.
