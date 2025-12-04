# Databricks notebook source
# MAGIC %md
# MAGIC # 🧞 Deploy SouthernLink Network Intelligence Genie Space
# MAGIC 
# MAGIC This notebook deploys the Genie Space using the Databricks REST API.
# MAGIC 
# MAGIC **Prerequisites:**
# MAGIC 1. Run `01_generate_synthetic_data.py` to create the tables
# MAGIC 2. Have a SQL Warehouse available
# MAGIC 3. Upload the Genie JSON file to the workspace

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
# MAGIC ## Step 2: Import and Deploy the Genie Space

# COMMAND ----------

import requests
import json
import os

# Define the workspace URL and API endpoint for creating a Genie space
workspace_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().get()
api_endpoint = "/api/2.0/genie/spaces"

# Retrieve Databricks token
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

# Path to the Genie space JSON file
# Update this path based on where you uploaded the file
json_file_path = "/Workspace/Users/{}/telco-aibi/src/genie/southernlink_network_genie_space.json".format(
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
)

# Alternative: If using Repos
# json_file_path = "/Workspace/Repos/{}/telco-aibi/src/genie/southernlink_network_genie_space.json".format(
#     dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
# )

print(f"Looking for Genie JSON at: {json_file_path}")

# COMMAND ----------

# Load and configure the Genie space JSON
try:
    with open(json_file_path, "r") as f:
        genie_data = json.load(f)
        # Add your warehouse ID
        genie_data['warehouse_id'] = warehouse_id
        print(f"✅ Loaded Genie space: {genie_data['title']}")
        print(f"   Tables: {len(genie_data['tables'])}")
        print(f"   Sample questions: {len(genie_data['curated_questions'])}")
except FileNotFoundError:
    print(f"❌ File not found: {json_file_path}")
    print("\nPlease upload the Genie JSON file to your workspace.")
    print("You can find it at: src/genie/southernlink_network_genie_space.json")
    raise

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Create the Genie Space via API

# COMMAND ----------

# Set up authentication headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Make POST request to create the Genie space
response = requests.post(
    f"{workspace_url}{api_endpoint}",
    headers=headers,
    json=genie_data
)

# Check response status
if response.status_code == 200:
    result = response.json()
    print("✅ Genie space created successfully!")
    print(f"\n📍 Genie Space ID: {result.get('space_id', 'N/A')}")
    print(f"🔗 Access URL: {workspace_url}/genie/spaces/{result.get('space_id', '')}")
elif response.status_code == 409:
    print("⚠️ A Genie space with this name already exists.")
    print("You can either:")
    print("  1. Delete the existing space and re-run this notebook")
    print("  2. Update the 'title' field in the JSON file to create a new space")
else:
    print(f"❌ Failed to create Genie space: {response.status_code}")
    print(f"   Error: {response.text}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: List Existing Genie Spaces (Optional)

# COMMAND ----------

# List all Genie spaces to verify
list_response = requests.get(
    f"{workspace_url}{api_endpoint}",
    headers=headers
)

if list_response.status_code == 200:
    spaces = list_response.json().get('spaces', [])
    print(f"📋 Found {len(spaces)} Genie space(s):\n")
    for space in spaces:
        print(f"  • {space.get('title', 'Untitled')}")
        print(f"    ID: {space.get('space_id', 'N/A')}")
        print(f"    URL: {workspace_url}/genie/spaces/{space.get('space_id', '')}")
        print()
else:
    print(f"Could not list Genie spaces: {list_response.status_code}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧹 Cleanup: Delete Genie Space (Optional)
# MAGIC 
# MAGIC Run this cell only if you need to delete the Genie space

# COMMAND ----------

# Uncomment and run to delete a Genie space
# space_id_to_delete = "<SPACE_ID>"  # Get this from the list above
# 
# delete_response = requests.delete(
#     f"{workspace_url}{api_endpoint}/{space_id_to_delete}",
#     headers=headers
# )
# 
# if delete_response.status_code == 200:
#     print(f"✅ Genie space {space_id_to_delete} deleted successfully")
# else:
#     print(f"❌ Failed to delete: {delete_response.status_code} - {delete_response.text}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Demo: Sample Questions to Ask Genie
# MAGIC 
# MAGIC After creating the Genie space, try these questions:
# MAGIC 
# MAGIC **Simple Queries:**
# MAGIC - "Which POIs are currently in Critical congestion status?"
# MAGIC - "What is the average latency by technology type?"
# MAGIC 
# MAGIC **Medium Complexity:**
# MAGIC - "How many customers were affected by Critical incidents last month?"
# MAGIC - "What percentage of customers are achieving their plan speeds?"
# MAGIC 
# MAGIC **Deep Research (Complex Analysis):**
# MAGIC - "Which suburbs in Melbourne have the highest risk of congestion during evening peak hours over the next 6 months, and what's driving the growth? Include recommendations for capacity upgrades."
# MAGIC 
# MAGIC **Executive Summary:**
# MAGIC - "Give me a summary of network health by state for the board meeting"

