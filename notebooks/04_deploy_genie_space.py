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
import uuid

def generate_id():
    """Generate a 32-char hex ID like Databricks uses"""
    return uuid.uuid4().hex

# The serialized_space contains the internal configuration as a JSON string
serialized_space_config = {
    "version": 1,
    "config": {
        "sample_questions": [
            {"id": generate_id(), "question": ["Which POIs are currently in Critical congestion status?"]},
            {"id": generate_id(), "question": ["What is the average latency by technology type?"]},
            {"id": generate_id(), "question": ["Which suburbs have the highest risk of congestion over the next 6 months?"]},
            {"id": generate_id(), "question": ["How many customers were affected by Critical incidents last month?"]},
            {"id": generate_id(), "question": ["What percentage of customers are achieving their plan speeds?"]},
            {"id": generate_id(), "question": ["What is the total estimated cost to upgrade all high-risk POIs?"]},
            {"id": generate_id(), "question": ["Give me a summary of network health by state"]}
        ]
    },
    "data_sources": {
        "tables": [
            {"identifier": "zivile.telco.capacity_forecasts"},
            {"identifier": "zivile.telco.customer_usage"},
            {"identifier": "zivile.telco.customers"},
            {"identifier": "zivile.telco.incidents"},
            {"identifier": "zivile.telco.network_telemetry"},
            {"identifier": "zivile.telco.poi_infrastructure"}
        ]
    },
    "instructions": {
        "text_instructions": [
            {
                "id": generate_id(),
                "content": [
                    "You are an AI assistant for SouthernLink Networks, an Australian broadband provider.\n",
                    "Technologies: FTTP (Fiber to Premises - best), FTTN (Fiber to Node), HFC (Hybrid Fiber Coaxial), Fixed Wireless\n",
                    "POI = Point of Interconnect, aggregates customer connections\n",
                    "Peak hours = 6-9 PM (hours 18-21)\n",
                    "Congestion: >70% utilization = Warning, >85% = Critical\n",
                    "FTTN typically has higher congestion than FTTP\n",
                    "Round percentages to 1 decimal place\n",
                    "Format currency as AUD with $ symbol\n",
                    "For high risk analysis, filter risk_score IN ('Critical', 'High')"
                ]
            }
        ]
    }
}

# Get the current user's workspace path for parent_path
username = spark.sql("SELECT current_user()").collect()[0][0]
parent_path = f"/Workspace/Users/{username}"

# Full API request payload
genie_space_config = {
    "title": "SouthernLink Network Intelligence",
    "description": "AI-powered network analytics for SouthernLink Networks. Ask questions about network health, congestion, customer experience, and capacity planning in plain English.",
    "warehouse_id": warehouse_id,
    "parent_path": parent_path,
    "serialized_space": json.dumps(serialized_space_config)
}

print(f"Genie Space: {genie_space_config['title']}")
print(f"Parent Path: {genie_space_config['parent_path']}")
print(f"Tables: {len(serialized_space_config['data_sources']['tables'])}")
print(f"Sample Questions: {len(serialized_space_config['config']['sample_questions'])}")
print(f"\n📦 Payload preview:")
print(json.dumps(genie_space_config, indent=2))

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
