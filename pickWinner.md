### **Prompt for Determining the Game Winner**

---

**Task:** Evaluate the final states of all countries after 50 turns and determine the winner based on specified economic metrics.

---

**Instructions:**

1. **Input Data:**

   - You will be provided with the end-state data for all countries after 50 turns. This data includes:
     - **Country Name**
     - **Government Capital Pool**: Total capital at the end of the game.
     - **Industries**: Detailed information on all industries, including production levels, technology levels, outputs, and inputs.
     - **Workforce**: Number of employed and unemployed skilled and unskilled workers.
     - **Stockpiles**: Quantities of all goods and resources held.
     - **Natural Resources**: Remaining reserves and extraction rates.
     - **Trade Records**: Summary of trade activities, including exports and imports.
     - **Economic Indicators**: Any additional data such as GDP, economic growth rates, technological advancements, and standard of living indices.

2. **Objective:**

   - Analyze the provided data for each country.
   - Determine which country performed the best over the 50 turns.
   - Provide a detailed justification for your choice based on the economic metrics.

3. **Metrics to Consider:**

   Evaluate each country based on the following criteria:

   - **Total Wealth (Government Capital Pool):**
     - Assess the total capital accumulated.
   - **Economic Growth:**
     - Evaluate the growth rate of the economy over the 50 turns.
   - **Industrial Development:**
     - Consider the number and levels of industries, including production and technology levels.
   - **Technological Advancement:**
     - Analyze advancements in technology levels across industries.
   - **Resource Utilization:**
     - Evaluate how effectively natural resources were managed and utilized.
   - **Trade Performance:**
     - Assess the trade balance, export volumes, and import dependencies.
   - **Workforce Employment:**
     - Consider employment rates of skilled and unskilled workers.
   - **Standard of Living:**
     - Infer based on factors like unemployment rates, availability of goods, and economic prosperity.
   - **Diversification:**
     - Evaluate the diversity of industries and economic resilience.
   - **Strategic Achievements:**
     - Consider any significant achievements, such as monopolizing a resource or technology.

4. **Evaluation Process:**

   - **Data Analysis:**
     - Carefully analyze the data for each country against each metric.
   - **Scoring:**
     - Assign a score to each country for each metric on a scale of 1 to 10 (10 being the highest).
     - You may provide a total score for each country by summing up individual metric scores.
   - **Comparison:**
     - Compare the scores to determine which country outperformed the others overall.
   - **Tie-Breakers:**
     - In case of a tie, consider qualitative factors such as strategic moves or long-term sustainability.

5. **Output Format:**

   - Provide your evaluation in a structured JSON format as shown below.
   - Include a ranking of the countries, their scores, and detailed justifications.
   - **Do not** include any additional text or explanations outside the JSON structure.

```json
{
  "Results": [
    {
      "Country Name": "Country A",
      "Total Score": total_score_numeric_value,
      "Rank": 1,
      "Scores": {
        "Total Wealth": numeric_value,
        "Economic Growth": numeric_value,
        "Industrial Development": numeric_value,
        "Technological Advancement": numeric_value,
        "Resource Utilization": numeric_value,
        "Trade Performance": numeric_value,
        "Workforce Employment": numeric_value,
        "Standard of Living": numeric_value,
        "Diversification": numeric_value,
        "Strategic Achievements": numeric_value
      },
      "Justification": "Detailed justification for why Country A is ranked first, citing specific data and achievements."
    },
    {
      "Country Name": "Country B",
      "Total Score": total_score_numeric_value,
      "Rank": 2,
      "Scores": {
        "Total Wealth": numeric_value,
        "...": "..."
      },
      "Justification": "Detailed justification for Country B."
    },
    {
      "Country Name": "Country C",
      "Total Score": total_score_numeric_value,
      "Rank": 3,
      "Scores": {
        "...": "..."
      },
      "Justification": "Detailed justification for Country C."
    }
    // Include all countries in the same format
  ],
  "Winner": "Country A"
}
```

6. **Guidelines:**

   - **Fairness and Objectivity:**
     - Ensure that your evaluation is unbiased and based solely on the provided data.
   - **Data Citation:**
     - Reference specific data points in your justification (e.g., "Country A achieved a total capital of 2,000,000, the highest among all countries").
   - **Consistency:**
     - Apply the same evaluation criteria and scoring methodology to all countries.
   - **Clarity:**
     - Make sure your justifications are clear and concise, highlighting key reasons for the rankings.
   - **Avoid Assumptions:**
     - Do not make assumptions beyond the provided data.
   - **No External Information:**
     - Use only the information given in the end-state data.

---

**Note:** The purpose of this evaluation is to determine which country performed the best economically over the course of the game. The winner should be the country that demonstrates superior performance across the majority of the metrics, showing overall economic strength and strategic success.

---

**Remember:** Provide only the JSON output as specified, without additional commentary or text outside the structured format.
