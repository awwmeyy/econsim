**Task:** Generate options for technology upgrades for existing industries based on the country's current schema.

---

**Instructions:**

1. **Input Data:**

   - You are provided with the country's current schema, which includes:
     - **Existing Industries**: Details about current industries, their production levels, technology levels, inputs, outputs, etc.
     - **Government Capital Pool**: The amount of capital the country currently has.
   - **Note:** Use only the provided data for your analysis.

2. **Objective:**

   - Generate **5 options** for technology upgrades for existing industries that the country can potentially undertake.
   - For each technology upgrade option, provide:
     - **Industry ID**: The identifier of the existing industry to be upgraded (e.g., "IND2").
     - **Current Technology Level**: The industry's current technology level.
     - **New Technology Level**: The proposed new technology level after the upgrade.
     - **Upgrade Cost**: Capital required to perform the technology upgrade.
     - **Time to Complete**: Number of turns required to complete the upgrade.
     - **Benefits**: Expected benefits from the upgrade, provided as a structured JSON object. The benefits should include the following categories (expressed as percentages without the "%" symbol; if there's no change, set to 0):
       - **Unskilled Labor Reduction**
       - **Skilled Labor Reduction**
       - **Output Increase**
       - **Input Decrease**
     - **Justification**: Brief explanation of why upgrading this industry's technology is beneficial based on the country's current situation.

3. **Guidelines:**

   - **Feasibility:**
     - Ensure that the proposed upgrades are realistic, considering the country's current capital and the existing technology level of the industry.
     - At least **half of the options** should be upgrades that can be started **immediately** with current capital.
     - The other options can be more expensive, requiring future capital accumulation.
   - **Strategic Impact:**
     - Prioritize upgrades that offer significant benefits, such as substantial efficiency gains, cost reductions, or output improvements.
     - Consider industries that are critical to the country's economy or that have high potential for growth.
   - **Consistency:**
     - Upgrade costs and time to complete should be proportional to the increase in technology level and the complexity of the industry.
     - Higher technology levels should provide greater benefits.

4. **Output Format:**

   - Provide the technology upgrade options in a structured JSON format as shown below.
   - **Do not** include any additional text or explanations.

```json
{
  "TechnologyUpgrades": [
    {
      "Industry ID": "IND2",
      "Current Technology Level": 2,
      "New Technology Level": 3,
      "Upgrade Cost": 75000,
      "Time to Complete": 2,
      "Benefits": {
        "Unskilled Labor Reduction": 10,
        "Skilled Labor Reduction": 5,
        "Output Increase": 20,
        "Input Decrease": 15
      },
      "Justification": "Upgrading the electronics manufacturing industry will boost output and efficiency, capitalizing on its role in the economy."
    },
    {
      "Industry ID": "IND1",
      "Current Technology Level": 1,
      "New Technology Level": 2,
      "Upgrade Cost": 50000,
      "Time to Complete": 1,
      "Benefits": {
        "Unskilled Labor Reduction": 5,
        "Skilled Labor Reduction": 0,
        "Output Increase": 25,
        "Input Decrease": 0
      },
      "Justification": "Enhancing mining technology increases copper ore output, supporting related industries."
    },
    {
      "Industry ID": "IND3",
      "Current Technology Level": 2,
      "New Technology Level": 3,
      "Upgrade Cost": 90000,
      "Time to Complete": 2,
      "Benefits": {
        "Unskilled Labor Reduction": 15,
        "Skilled Labor Reduction": 10,
        "Output Increase": 30,
        "Input Decrease": 20
      },
      "Justification": "Advancing steel production technology reduces costs and enhances competitiveness."
    },
    {
      "Industry ID": "IND4",
      "Current Technology Level": 1,
      "New Technology Level": 3,
      "Upgrade Cost": 130000,
      "Time to Complete": 3,
      "Benefits": {
        "Unskilled Labor Reduction": 20,
        "Skilled Labor Reduction": 15,
        "Output Increase": 35,
        "Input Decrease": 25
      },
      "Justification": "A significant upgrade in chemical production can position the country as an industry leader."
    },
    {
      "Industry ID": "IND5",
      "Current Technology Level": 2,
      "New Technology Level": 4,
      "Upgrade Cost": 210000,
      "Time to Complete": 5,
      "Benefits": {
        "Unskilled Labor Reduction": 25,
        "Skilled Labor Reduction": 20,
        "Output Increase": 50,
        "Input Decrease": 30
      },
      "Justification": "Investing in software development maximizes high-tech potential and skilled workforce utilization."
    }
  ]
}
```

5. **Additional Notes:**

   - **Financial Constraints:**
     - At least **two or three** upgrade options have costs within current capital availability.
   - **Time Constraints:**
     - Consider the game's timeline; longer upgrades should offer proportionally greater benefits.
   - **Strategic Priorities:**
     - Focus on industries that will significantly impact the country's economic metrics.

---

**Remember:** Provide only the JSON output as specified, without additional commentary.
