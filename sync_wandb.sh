#!/bin/bash
# Script to sync offline W&B runs to cloud

cd /teamspace/studios/this_studio/medical-I2I-benchmark

echo "🔄 Syncing W&B runs to cloud..."
echo ""

# Find all offline runs
for run_dir in wandb/offline-run-*; do
    if [ -d "$run_dir" ]; then
        echo "Syncing: $run_dir"
        wandb sync "$run_dir"
        echo ""
    fi
done

echo "✅ All runs synced!"

