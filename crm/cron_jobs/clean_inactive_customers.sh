#!/bin/bash

# Absolute path to project root (adjust if needed)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# Activate virtual environment if you use one
# source /path/to/venv/bin/activate

# Run Django shell command
DELETED_COUNT=$(
  python3 "$PROJECT_ROOT/manage.py" shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
)

count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Log result with timestamp
echo "\$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: \$DELETED_COUNT" >> /tmp/customer_cleanup_log.txt
