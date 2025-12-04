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

print(f"Workspace URL: {workspace_url}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Create the Genie Space

# COMMAND ----------

# Genie Space configuration
genie_space_config = {
    "title": "SouthernLink Network Intelligence",
    "description": "AI-powered network analytics for SouthernLink Networks. Ask questions about network health, congestion, customer experience, and capacity planning in plain English.",
    "warehouse_id": warehouse_id,
    "tables": [
        {
            "table_name": "zivile.telco.network_telemetry",
            "description": "Real-time and historical network performance metrics collected hourly from each POI. Contains 30 days of data. Peak hours are 18:00-21:00.",
            "columns": [
                {"name": "poi_id", "description": "Unique POI identifier (STATE-XXXX format)"},
                {"name": "suburb", "description": "Suburb name"},
                {"name": "state", "description": "Australian state code"},
                {"name": "technology_type", "description": "FTTP, FTTN, HFC, or Fixed Wireless"},
                {"name": "timestamp", "description": "Measurement timestamp"},
                {"name": "hour", "description": "Hour of day (0-23)"},
                {"name": "utilization_pct", "description": "Capacity utilization (0-100). >70=Warning, >85=Critical"},
                {"name": "avg_latency_ms", "description": "Average latency in milliseconds"},
                {"name": "congestion_status", "description": "Normal, Warning, or Critical"},
                {"name": "active_connections", "description": "Active customer connections"}
            ]
        },
        {
            "table_name": "zivile.telco.capacity_forecasts",
            "description": "ML predictions for capacity over 6 months. Use for planning.",
            "columns": [
                {"name": "poi_id", "description": "POI identifier"},
                {"name": "suburb", "description": "Suburb name"},
                {"name": "state", "description": "State code"},
                {"name": "technology_type", "description": "Technology type"},
                {"name": "months_ahead", "description": "Months into future (1-6)"},
                {"name": "projected_utilization_pct", "description": "Predicted utilization"},
                {"name": "risk_score", "description": "Critical, High, Medium, or Low"},
                {"name": "estimated_upgrade_cost_aud", "description": "Upgrade cost in AUD"}
            ]
        },
        {
            "table_name": "zivile.telco.incidents",
            "description": "Network incidents and outages. 12 months of history.",
            "columns": [
                {"name": "incident_id", "description": "Incident identifier"},
                {"name": "poi_id", "description": "Affected POI"},
                {"name": "suburb", "description": "Suburb"},
                {"name": "incident_type", "description": "Type of incident"},
                {"name": "severity", "description": "Critical, High, Medium, Low"},
                {"name": "incident_time", "description": "When incident occurred"},
                {"name": "duration_hours", "description": "Duration in hours"},
                {"name": "customers_affected", "description": "Number of affected customers"}
            ]
        },
        {
            "table_name": "zivile.telco.customers",
            "description": "Customer accounts and plans.",
            "columns": [
                {"name": "customer_id", "description": "Customer identifier"},
                {"name": "poi_id", "description": "Serving POI"},
                {"name": "technology_type", "description": "Connection technology"},
                {"name": "plan_tier", "description": "Plan name"},
                {"name": "download_speed_mbps", "description": "Plan download speed"},
                {"name": "churn_risk_score", "description": "Churn probability (0-1)"},
                {"name": "is_active", "description": "Account active status"}
            ]
        },
        {
            "table_name": "zivile.telco.customer_usage",
            "description": "Daily customer usage data. 90 days of history.",
            "columns": [
                {"name": "customer_id", "description": "Customer identifier"},
                {"name": "usage_date", "description": "Date"},
                {"name": "download_gb", "description": "Daily download in GB"},
                {"name": "speed_achievement_pct", "description": "Actual speed vs plan speed %"},
                {"name": "streaming_hours", "description": "Streaming hours"},
                {"name": "gaming_hours", "description": "Gaming hours"}
            ]
        },
        {
            "table_name": "zivile.telco.poi_infrastructure",
            "description": "Network POI infrastructure details.",
            "columns": [
                {"name": "poi_id", "description": "POI identifier"},
                {"name": "suburb", "description": "Suburb"},
                {"name": "state", "description": "State"},
                {"name": "technology_type", "description": "Technology"},
                {"name": "premises_served", "description": "Connected premises"},
                {"name": "max_capacity_gbps", "description": "Maximum capacity"}
            ]
        }
    ],
    "instructions": """You are an AI assistant for SouthernLink Networks, an Australian broadband provider.

DOMAIN KNOWLEDGE:
- Technologies: FTTP (Fiber to Premises - best), FTTN (Fiber to Node), HFC (Hybrid Fiber Coaxial), Fixed Wireless
- POI = Point of Interconnect, aggregates customer connections
- Peak hours = 6-9 PM (hours 18-21)
- Congestion: >70% = Warning, >85% = Critical
- FTTN typically has higher congestion than FTTP

RESPONSE GUIDELINES:
- Include relevant metrics (counts, percentages, averages)
- Round percentages to 1 decimal place
- Format currency as AUD with $ symbol
- For high risk analysis, filter risk_score IN ('Critical', 'High')
- Peak hour analysis should focus on hours 18-21""",
    "curated_questions": [
        {"question": "Which POIs are currently in Critical congestion status?"},
        {"question": "What is the average latency by technology type?"},
        {"question": "Which suburbs have the highest risk of congestion over the next 6 months?"},
        {"question": "How many customers were affected by Critical incidents last month?"},
        {"question": "What percentage of customers are achieving their plan speeds?"},
        {"question": "What's the total estimated cost to upgrade all high-risk POIs?"},
        {"question": "Give me a summary of network health by state"}
    ]
}

print(f"Genie Space: {genie_space_config['title']}")
print(f"Tables: {len(genie_space_config['tables'])}")
print(f"Sample Questions: {len(genie_space_config['curated_questions'])}")

# COMMAND ----------

# Create the Genie space
response = requests.post(
    f"{workspace_url}{api_endpoint}",
    headers=headers,
    json=genie_space_config
)

if response.status_code == 200:
    result = response.json()
    space_id = result.get('space_id', result.get('id', 'N/A'))
    print("✅ Genie space created successfully!")
    print(f"\n📍 Genie Space ID: {space_id}")
    print(f"🔗 Access URL: {workspace_url}/genie/spaces/{space_id}")
elif response.status_code == 409:
    print("⚠️ A Genie space with this name already exists.")
else:
    print(f"❌ Failed to create Genie space: {response.status_code}")
    print(f"   Error: {response.text}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: List Existing Genie Spaces (Optional)

# COMMAND ----------

# List all Genie spaces
list_response = requests.get(
    f"{workspace_url}{api_endpoint}",
    headers=headers
)

if list_response.status_code == 200:
    spaces = list_response.json().get('spaces', list_response.json().get('genie_spaces', []))
    print(f"📋 Found {len(spaces)} Genie space(s):\n")
    for space in spaces:
        title = space.get('title', space.get('name', 'Untitled'))
        space_id = space.get('space_id', space.get('id', 'N/A'))
        print(f"  • {title}")
        print(f"    ID: {space_id}")
        print(f"    URL: {workspace_url}/genie/spaces/{space_id}")
        print()
else:
    print(f"Could not list Genie spaces: {list_response.status_code}")
    print(list_response.text)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧹 Cleanup: Delete Genie Space (Optional)

# COMMAND ----------

# Uncomment to delete a Genie space
# space_id_to_delete = "<SPACE_ID>"
# 
# delete_response = requests.delete(
#     f"{workspace_url}{api_endpoint}/{space_id_to_delete}",
#     headers=headers
# )
# 
# if delete_response.status_code in [200, 204]:
#     print(f"✅ Genie space deleted")
# else:
#     print(f"❌ Failed: {delete_response.status_code} - {delete_response.text}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Sample Questions for Demo
# MAGIC 
# MAGIC **Simple:**
# MAGIC - "Which POIs are currently Critical?"
# MAGIC - "What is the average latency by technology type?"
# MAGIC 
# MAGIC **Medium:**
# MAGIC - "How many customers were affected by Critical incidents last month?"
# MAGIC 
# MAGIC **Deep Research:**
# MAGIC - "Which suburbs in Melbourne have the highest risk of congestion during evening peak hours over the next 6 months? Include recommendations."
