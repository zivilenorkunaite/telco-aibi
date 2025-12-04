# 🌐 SouthernLink Network Intelligence Demo

Databricks AI/BI demo showcasing network health monitoring, Genie, and Deep Research capabilities.

## 📁 Project Structure

```
telco-aibi/
├── databricks.yml                    # DAB bundle configuration
├── src/
│   └── dashboards/
│       └── network_intelligence.lvdash.json  # AI/BI Dashboard
├── notebooks/
│   ├── 01_generate_synthetic_data.py # Generate demo data
│   ├── 02_deploy_aibi_dashboard.py   # Dashboard SQL queries
│   └── 03_deploy_genie_space.py      # Genie configuration
└── SouthernLink_Databricks_Demo_Storyline.md # Demo script
```

## 🚀 Quick Start

### Prerequisites

1. **Databricks CLI v0.200+** installed and configured
2. **Databricks workspace** with Unity Catalog enabled
3. **SQL Warehouse** available for dashboard queries

### Step 1: Configure Authentication

```bash
# Set your Databricks host
export DATABRICKS_HOST=https://your-workspace.cloud.databricks.com

# Authenticate (choose one method)
databricks auth login --host $DATABRICKS_HOST
# OR use a token
export DATABRICKS_TOKEN=your-token
```

### Step 2: Get Your SQL Warehouse ID

```bash
# List available warehouses
databricks warehouses list

# Note the warehouse ID (looks like: abc123def456)
```

### Step 3: Validate the Bundle

```bash
cd telco-aibi

# Validate configuration
databricks bundle validate -t dev

# If you get errors about warehouse_id, set it:
databricks bundle validate -t dev --var warehouse_id=YOUR_WAREHOUSE_ID
```

### Step 4: Generate Sample Data

Before deploying the dashboard, run the data generation notebook:

1. Import `notebooks/01_generate_synthetic_data.py` to your workspace
2. Run on serverless compute
3. Verify tables exist in `zivile.telco`

### Step 5: Deploy the Dashboard

```bash
# Deploy to dev environment
databricks bundle deploy -t dev --var warehouse_id=YOUR_WAREHOUSE_ID

# Check deployment status
databricks bundle summary -t dev
```

### Step 6: Access the Dashboard

After deployment, find your dashboard:
1. Go to **Dashboards** in Databricks workspace
2. Search for "SouthernLink Network Intelligence"
3. Click to open and publish

## 🧪 Local Development

### Validate Changes

```bash
# Check YAML syntax and configuration
databricks bundle validate -t dev --var warehouse_id=YOUR_WAREHOUSE_ID
```

### Preview Deployment

```bash
# See what will be deployed without actually deploying
databricks bundle deploy -t dev --var warehouse_id=YOUR_WAREHOUSE_ID --dry-run
```

### Destroy Resources

```bash
# Remove deployed resources
databricks bundle destroy -t dev
```

## 📊 Dashboard Pages

1. **Network Overview** - KPI cards, state/technology charts, peak trends
2. **Capacity Planning** - Risk forecast table for 6-month projections
3. **Incidents** - Recent network incidents and alerts
4. **Customer Experience** - Speed achievement metrics

## 🧞 Genie Space Setup

After deploying the dashboard, create a Genie Space manually:

1. Go to **Workspace** → **Create** → **Genie space**
2. Name: `SouthernLink Network Intelligence`
3. Add tables from `zivile.telco`:
   - `network_telemetry`
   - `capacity_forecasts`
   - `incidents`
   - `customers`
   - `customer_usage`
   - `poi_infrastructure`
   - `premises`
4. Copy instructions from `notebooks/03_deploy_genie_space.py`

## 🎯 Demo Script

See `SouthernLink_Databricks_Demo_Storyline.md` for the full 15-minute demo script including:
- Talking points
- Sample Genie questions
- Deep Research example

## ⚠️ Troubleshooting

### "warehouse_id is required"
Set the warehouse ID variable:
```bash
databricks bundle deploy -t dev --var warehouse_id=YOUR_WAREHOUSE_ID
```

### "Cannot connect to tables"
Ensure you've run `01_generate_synthetic_data.py` to create the tables in `zivile.telco`.

### Dashboard import fails
The dashboard JSON format may need adjustment. Try creating a simple dashboard in the UI first, then export it to see the expected format.

## 📝 License

Internal demo use only.

