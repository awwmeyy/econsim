**Task:** Generate 5 options for new industries that the country can set up, based on the country's current schema.

---

**Instructions:**

1. **Input Data:**

   - You are provided with the country's current schema, which includes:
     - **Existing Industries**: Details about current industries, their inputs, and outputs.
     - **Resources**: Information on natural resources, stockpiles, and available goods.
     - **Workforce**: Number of skilled and unskilled workers available.
     - **Government Capital Pool**: The amount of capital the country currently has.
   - **Note:** Use only the provided data for your analysis.

2. **Objective:**

   - Generate **5 options** for new industries that the country can potentially set up.
   - For each industry, provide:
     - **Industry ID**: Unique identifier (e.g., "IND6").
     - **Type**: Primary, Secondary, or Tertiary.
     - **Sub-Type**: Specific industry type (e.g., "Automobile Manufacturing").
     - **Inputs Required**: List of resources and goods needed per production cycle.
     - **Outputs Produced**: Goods or resources produced per production cycle.
     - **Setup Cost**: Capital required to establish the industry.
     - **Skilled Workers Required**: Number needed to operate the industry.
     - **Unskilled Workers Required**: Number needed to operate the industry.
     - **Production Level**: Initial production capacity level.
     - **Technology Level**: Initial technology sophistication level.
     - **Justification**: Brief explanation of why this industry suits the country based on current resources and industries.

3. **Guidelines:**

   - **Realism and Feasibility:**
     - Ensure proposed industries are realistic, considering the country's current resources, industries, and workforce.
     - On average, **half of the industries** should be ones the country can set up **immediately** with current capital and workforce.
     - The other half can be industries that are **more expensive or require more resources** than currently available, requiring future progress.
   - **Resource Utilization:**
     - Prefer industries that utilize existing resources, stockpiles, or outputs from current industries.
     - Introduce industries that add value by processing raw materials into higher-value goods.
   - **Diversity:**
     - Provide a mix of industry types (Primary, Secondary, Tertiary) for varied options.
   - **Consistency:**
     - Ensure costs, workforce requirements, and outputs align with industry type and scale.
     - Costs and worker needs should be proportional to industry complexity and size.
   - **Avoid Overlaps:**
     - Do not propose industries identical to existing ones unless strategically justified.

4. **Output Format:**

   - Provide the industries in a structured JSON format as shown below.
   - **Do not** include any additional text or explanations.

```json
{
  "NewIndustries": [
    {
      "Industry ID": "IND6",
      "Type": "Secondary",
      "Sub-Type": "Automobile Manufacturing",
      "Inputs Required": {
        "Steel": 100,
        "Electronics": 50,
        "Rubber": 30
      },
      "Outputs Produced": {
        "Automobiles": 20
      },
      "Setup Cost": 500000,
      "Skilled Workers Required": 200,
      "Unskilled Workers Required": 800,
      "Production Level": 1,
      "Technology Level": 2,
      "Justification": "The country has abundant steel and electronics production, making automobile manufacturing feasible."
    },
    {
      "Industry ID": "IND7",
      "Type": "Tertiary",
      "Sub-Type": "Software Development",
      "Inputs Required": {
        "Skilled Labor Hours": 1000
      },
      "Outputs Produced": {
        "Software Products": 50
      },
      "Setup Cost": 150000,
      "Skilled Workers Required": 50,
      "Unskilled Workers Required": 0,
      "Production Level": 1,
      "Technology Level": 3,
      "Justification": "With a surplus of skilled workers, expanding into software development leverages existing human capital."
    },
    {
      "Industry ID": "IND8",
      "Type": "Primary",
      "Sub-Type": "Gold Mining",
      "Inputs Required": {},
      "Outputs Produced": {
        "Gold Ore": 10
      },
      "Setup Cost": 800000,
      "Skilled Workers Required": 100,
      "Unskilled Workers Required": 400,
      "Production Level": 1,
      "Technology Level": 1,
      "Justification": "The country has unexplored gold reserves, offering high-value resource extraction opportunities."
    },
    {
      "Industry ID": "IND9",
      "Type": "Secondary",
      "Sub-Type": "Pharmaceutical Manufacturing",
      "Inputs Required": {
        "Chemicals": 200,
        "Herbs": 100
      },
      "Outputs Produced": {
        "Medicines": 150
      },
      "Setup Cost": 300000,
      "Skilled Workers Required": 150,
      "Unskilled Workers Required": 200,
      "Production Level": 1,
      "Technology Level": 2,
      "Justification": "Leveraging existing chemical stockpiles to produce medicines meets domestic needs and export potential."
    },
    {
      "Industry ID": "IND10",
      "Type": "Tertiary",
      "Sub-Type": "Financial Services",
      "Inputs Required": {
        "Capital": 200000
      },
      "Outputs Produced": {
        "Financial Products": 100
      },
      "Setup Cost": 250000,
      "Skilled Workers Required": 80,
      "Unskilled Workers Required": 20,
      "Production Level": 1,
      "Technology Level": 2,
      "Justification": "Developing financial services diversifies the economy and utilizes the skilled workforce."
    }
  ]
}
```

5. **Additional Notes:**

   - **Financial Constraints:**
     - At least **two or three** industries have setup costs and workforce requirements within current capacities.
   - **Worker Availability:**
     - Consider available skilled and unskilled workers when proposing requirements.
   - **Resource Constraints:**
     - Immediate options use resources currently accessible; future options may require trade or resource development.

---

**Remember:** Provide only the JSON output as specified, without additional commentary.
