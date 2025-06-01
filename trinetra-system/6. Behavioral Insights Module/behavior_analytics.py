from datetime import datetime, timedelta
import random
import pprint

# Simulated visit log
visit_log = {}

# Step 1: Log entry time
def log_entry(customer_id):
    visit_log[customer_id] = {
        "entry_time": datetime.now(),
        "items": [],
        "total_value": 0,
        "staff": None,
        "exit_time": None
    }

# Step 2: Log billing data
def log_billing(customer_id, order_items, value, staff):
    if customer_id not in visit_log:
        log_entry(customer_id)  # fallback
    visit_log[customer_id]["items"].extend(order_items)
    visit_log[customer_id]["total_value"] += value
    visit_log[customer_id]["staff"] = staff

# Step 3: Log exit time
def log_exit(customer_id):
    if customer_id in visit_log:
        visit_log[customer_id]["exit_time"] = datetime.now()

# Step 4: Compute behavior insights
def compute_behavior(customer_id):
    data = visit_log.get(customer_id)
    if not data:
        return None

    entry = data["entry_time"]
    exit_ = data["exit_time"] or datetime.now()
    duration = (exit_ - entry).total_seconds() / 60.0  # in minutes

    # Simulate waiting time
    waiting_time = random.uniform(1, 5)

    return {
        "time_spent": f"{duration:.2f} minutes",
        "waiting_time": f"{waiting_time:.1f} minutes",
        "favorite_items": list(set(data["items"])),
        "order_value": data["total_value"],
        "staff_served": data["staff"]
    }

# 🔍 Simulate session
customer_id = "john_doe"

log_entry(customer_id)
log_billing(customer_id, ["Latte", "Pastry"], 320, "Ritika")
log_exit(customer_id)

# Report
insights = compute_behavior(customer_id)
print("\n[TRINETRA - Behavioral Summary]")
pprint.pprint(insights)