# Databricks notebook source
# MAGIC %md
# MAGIC # 🧞 Deploy SouthernLink Network Intelligence Genie Space
# MAGIC 
# MAGIC This notebook deploys the Genie Space using the Databricks REST API.
# MAGIC 
# MAGIC **Prerequisites:**
# MAGIC 1. Run `01_generate_synthetic_data.py` to create the tables
# MAGIC 2. Have a SQL Warehouse available

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1: Configure Your SQL Warehouse ID
# MAGIC 
# MAGIC Get your warehouse ID from: SQL Warehouses → Select your warehouse → Copy the ID from the URL

# COMMAND ----------

# Add your SQL warehouse ID here
warehouse_id = '<YOUR_WAREHOUSE_ID>'  # e.g., '9e81d8837e3e52b4'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Define the Genie Space Configuration

# COMMAND ----------

import requests
import json

# Define the workspace URL and API endpoint
workspace_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
api_endpoint = "/api/2.0/genie/spaces"

# Retrieve Databricks token
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

# Set up authentication headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# COMMAND ----------

# Define the Genie space configuration inline
genie_config = {
    "title": "SouthernLink Network Intelligence",
    "description": "AI-powered network analytics for SouthernLink Networks. Ask questions about network health, congestion, customer experience, and capacity planning in plain English.",
    "warehouse_id": warehouse_id,
    "tables": [
        {
            "table_name": "zivile.telco.network_telemetry",
            "description": "Real-time and historical network performance metrics collected hourly from each POI. Contains 30 days of hourly data. Peak hours are 18:00-21:00."
        },
        {
            "table_name": "zivile.telco.capacity_forecasts",
            "description": "ML model predictions for network capacity over the next 6 months. Use for capacity planning. High-growth suburbs like Werribee, Cranbourne show highest risk."
        },
        {
            "table_name": "zivile.telco.incidents",
            "description": "Network incidents, outages, and maintenance events. Contains 12 months of incident history."
        },
        {
            "table_name": "zivile.telco.customers",
            "description": "Customer accounts and broadband plans. Use for customer experience analysis and churn prediction."
        },
        {
            "table_name": "zivile.telco.customer_usage",
            "description": "Daily aggregated usage data per customer. Contains 90 days of daily data."
        },
        {
            "table_name": "zivile.telco.poi_infrastructure",
            "description": "Network Points of Interconnect (POIs) - physical network nodes that aggregate customer connections."
        },
        {
            "table_name": "zivile.telco.premises",
            "description": "Physical customer locations that can be connected to the network."
        }
    ],
    "instructions": """You are an AI assistant for SouthernLink Networks, one of Australia's largest broadband providers.

DOMAIN KNOWLEDGE:
- SouthernLink operates a multi-technology network: FTTP (Fiber to Premises), FTTN (Fiber to Node), HFC (Hybrid Fiber Coaxial), Fixed Wireless
- A POI (Point of Interconnect) is a network aggregation point serving multiple customer premises
- Peak hours are 6 PM to 9 PM (hours 18-21) when residential usage is highest
- Congestion: utilization >70% = Warning, >85% = Critical
- FTTN typically has lower speeds and higher congestion than FTTP

TERMINOLOGY:
- Utilization = percentage of maximum capacity being used
- Speed achievement = actual speed as percentage of plan speed
- Premises = customer locations (homes or businesses)
- Churn risk = likelihood of customer cancellation (0-1 score)

RESPONSE GUIDELINES:
- Always include relevant metrics (counts, percentages, averages)
- When showing POIs or suburbs, include the state for context
- For forecasts, mention the confidence score
- Round percentages to 1 decimal place
- Format currency in AUD with $ symbol
- For 'high risk' suburbs, filter for risk_score IN ('Critical', 'High')""",
    "curated_questions": [
        {"question": "Which POIs are currently in Critical congestion status?"},
        {"question": "What is the average latency by technology type?"},
        {"question": "Which suburbs in Melbourne have the highest risk of congestion over the next 6 months?"},
        {"question": "How many customers were affected by Critical incidents last month?"},
        {"question": "What percentage of customers are achieving their plan speeds?"},
        {"question": "Which technology type has the worst performance during evening peak?"},
        {"question": "What's the total estimated cost to upgrade all high-risk POIs?"},
        {"question": "Give me a summary of network health by state"}
    ]
}

print(f"✅ Genie space config ready: {genie_config['title']}")
print(f"   Tables: {len(genie_config['tables'])}")
print(f"   Sample questions: {len(genie_config['curated_questions'])}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Create the Genie Space via API

# COMMAND ----------

# Make POST request to create the Genie space
response = requests.post(
    f"{workspace_url}{api_endpoint}",
    headers=headers,
    json=genie_config
)

# Check response status
if response.status_code == 200:
    result = response.json()
    space_id = result.get('space_id', result.get('id', 'N/A'))
    print("✅ Genie space created successfully!")
    print(f"\n📍 Genie Space ID: {space_id}")
    print(f"🔗 Access URL: {workspace_url}/genie/spaces/{space_id}")
elif response.status_code == 409:
    print("⚠️ A Genie space with this name already exists.")
    print("You can either:")
    print("  1. Delete the existing space and re-run this notebook")
    print("  2. Change the 'title' in the config above")
else:
    print(f"❌ Failed to create Genie space: {response.status_code}")
    print(f"   Error: {response.text}")
    print("\n📋 Request body sent:")
    print(json.dumps(genie_config, indent=2)[:1000] + "...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Alternative: Create via UI
# MAGIC 
# MAGIC If the API doesn't work, create the Genie Space manually:
# MAGIC 
# MAGIC 1. **Navigate to:** Workspace → Click **"+"** → Select **"Genie space"**
# MAGIC 
# MAGIC 2. **Configure:**
# MAGIC    - **Name:** `SouthernLink Network Intelligence`
# MAGIC    - **Description:** AI-powered network analytics
# MAGIC    - **Warehouse:** Select your SQL warehouse
# MAGIC 
# MAGIC 3. **Add Tables:** 
# MAGIC    - `zivile.telco.network_telemetry`
# MAGIC    - `zivile.telco.capacity_forecasts`
# MAGIC    - `zivile.telco.incidents`
# MAGIC    - `zivile.telco.customers`
# MAGIC    - `zivile.telco.customer_usage`
# MAGIC    - `zivile.telco.poi_infrastructure`
# MAGIC    - `zivile.telco.premises`
# MAGIC 
# MAGIC 4. **Add Instructions:** Copy from the `instructions` field above
# MAGIC 
# MAGIC 5. **Add Sample Questions:** Copy from `curated_questions` above

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: List Existing Genie Spaces

# COMMAND ----------

# List all Genie spaces
list_response = requests.get(
    f"{workspace_url}{api_endpoint}",
    headers=headers
)

if list_response.status_code == 200:
    result = list_response.json()
    spaces = result.get('spaces', result.get('genie_spaces', []))
    if spaces:
        print(f"📋 Found {len(spaces)} Genie space(s):\n")
        for space in spaces:
            title = space.get('title', space.get('name', 'Untitled'))
            space_id = space.get('space_id', space.get('id', 'N/A'))
            print(f"  • {title}")
            print(f"    ID: {space_id}")
            print(f"    URL: {workspace_url}/genie/spaces/{space_id}")
            print()
    else:
        print("No Genie spaces found")
else:
    print(f"Could not list Genie spaces: {list_response.status_code}")
    print(f"Response: {list_response.text[:500]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧹 Cleanup: Delete Genie Space (Optional)

# COMMAND ----------

# Uncomment and run to delete a Genie space
# space_id_to_delete = "<SPACE_ID>"
# 
# delete_response = requests.delete(
#     f"{workspace_url}{api_endpoint}/{space_id_to_delete}",
#     headers=headers
# )
# 
# if delete_response.status_code == 200:
#     print(f"✅ Genie space deleted")
# else:
#     print(f"❌ Failed: {delete_response.status_code} - {delete_response.text}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Demo Questions for Genie
# MAGIC 
# MAGIC **Simple:**
# MAGIC - "Which POIs are currently in Critical congestion status?"
# MAGIC - "What is the average latency by technology type?"
# MAGIC 
# MAGIC **Medium:**
# MAGIC - "How many customers were affected by Critical incidents last month?"
# MAGIC - "Compare speed achievement between FTTN and FTTP customers"
# MAGIC 
# MAGIC **Deep Research:**
# MAGIC - "Which suburbs in Melbourne have the highest risk of congestion during evening peak hours over the next 6 months, and what's driving the growth? Include recommendations for capacity upgrades."
