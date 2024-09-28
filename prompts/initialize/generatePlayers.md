- Please generate a country for a world economy simulation game using the updated schema provided below. The country should be balanced yet unique, with specific industries and resources that encourage strategic gameplay. Ensure diversity to promote interdependence among countries.
- ## **Country Schema**
- **Country Name**: _[Unique Country Name]_
- **Government Capital Pool**:
  - The initial capital should be approximately **1,000,000 currency units**, with slight variations (+/- 10%) allowed.
- **Industries**:
  - Each industry should include:
    - **Industry ID**: Unique identifier (e.g., "IND1").
    - **Type**: Primary, Secondary, or Tertiary.
    - **Sub-Type**: Specific industry type (e.g., "Iron Mining", "Steel Manufacturing").
    - **Production Level**: Numeric level indicating production capacity.
      - **Production Level** determines the **quantity of output produced per turn**.
    - **Technology Level**: Numeric level affecting efficiency and labor needs.
    - **Inputs**: List input resources/goods required per turn with quantities based on production level.
    - **Outputs**: List output goods produced per turn with quantities.
    - **Skilled Workers Employed**: Number employed after accounting for technology level reductions.
    - **Unskilled Workers Employed**: Number employed after accounting for technology level reductions.
- **Workforce**:
  - **Unemployed Skilled Workers**: Remaining skilled workers available after assigning employed workers.
  - **Unemployed Unskilled Workers**: Remaining unskilled workers available after assigning employed workers.
- **Stockpiles**:
  - List the initial quantities of goods/resources the country has in stock.
  - _Ensure enough resources to run industries for at least **2 turns** without additional purchases._
- **Natural Resources**: List resources available for extraction.

  - For each resource, specify:
    - **Total Reserves**: _[Total units available in the country]_
    - **Extraction Rate**: _[Maximum units that can be extracted per turn]_

- **Instructions**:

  - Use the above schema to generate a unique country.
  - Pay attention to the **labor reductions** due to technology levels.
    - **Higher Technology Levels** decrease labor requirements:
      - **Skilled Workers**: Reduced by **10% per tech level**.
      - **Unskilled Workers**: Reduced by **20% per tech level**.
  - Provide **concrete numerical values** for resource reserves and extraction rates.
  - Ensure the **country's industries are aligned with its available resources**.
  - **Stockpiles** should be sufficient to sustain industries for at least **2 turns**.
  - Provide the data in **JSON format** for easy parsing.

- ## **Example of Generated Country**

  ```json
  {
    "Country Name": "Eldoria",
    "Government Capital Pool": 1020000,
    "Industries": [
      {
        "Industry ID": "IND1",
        "Type": "Primary",
        "Sub-Type": "Copper Mining",
        "Production Level": 2,
        "Technology Level": 1,
        "Inputs": {},
        "Outputs": {
          "Copper Ore": 400
        },
        "Skilled Workers Employed": 90,
        "Unskilled Workers Employed": 360
      },
      {
        "Industry ID": "IND2",
        "Type": "Secondary",
        "Sub-Type": "Electronics Manufacturing",
        "Production Level": 1,
        "Technology Level": 2,
        "Inputs": {
          "Copper Ore": 200,
          "Silicon": 100
        },
        "Outputs": {
          "Electronics": 150
        },
        "Skilled Workers Employed": 72,
        "Unskilled Workers Employed": 288
      }
    ],
    "Workforce": {
      "Unemployed Skilled Workers": 338,
      "Unemployed Unskilled Workers": 1352
    },
    "Stockpiles": {
      "Copper Ore": 800,
      "Silicon": 200,
      "Electronics": 100
    },
    "Natural Resources": {
      "Copper Ore": {
        "Total Reserves": 25000,
        "Extraction Rate": 500
      }
    }
  }
  ```

**Reminder: Provide only the JSON output as specified, without additional commentary.**
