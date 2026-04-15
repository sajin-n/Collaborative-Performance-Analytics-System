#!/bin/bash

# Continuous monitoring and committing script
# Monitors for changes and commits/pushes them to GitHub

cd "$(dirname "$0")"

echo "🚀 Starting Git change monitor and auto-commit..."
echo "Monitoring for changes every 10 seconds..."
echo "Press Ctrl+C to stop"
echo ""

LAST_STATUS=""
consecutive_stable=0

retry_push() {
    local max_attempts=5
    local delay=5
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if git push origin main &>/dev/null; then
            echo "🎯 Successfully pushed to GitHub"
            return 0
        fi

        if [ $attempt -lt $max_attempts ]; then
            echo "⚠️  Push failed (attempt $attempt/$max_attempts). Retrying in ${delay}s..."
            sleep $delay
            delay=$((delay * 2))
        else
            echo "❌ Push failed after $max_attempts attempts. Will retry on next change cycle."
        fi

        attempt=$((attempt + 1))
    done

    return 1
}

while true; do
    # Get current git status
    CURRENT_STATUS=$(git status --porcelain)
    
    if [ "$CURRENT_STATUS" != "" ]; then
        consecutive_stable=0
        
        # Only commit if status changed or first time seeing changes
        if [ "$CURRENT_STATUS" != "$LAST_STATUS" ]; then
            LAST_STATUS="$CURRENT_STATUS"
            
            echo "---"
            echo "📝 Changes detected at $(date '+%H:%M:%S')"
            echo ""
            
            # Categorize changes and commit accordingly
            MODIFIED=$(git status --porcelain | grep '^ M' | awk '{print $2}' | tr '\n' ' ')
            ADDED=$(git status --porcelain | grep '^??' | awk '{print $2}' | tr '\n' ' ')
            DELETED=$(git status --porcelain | grep '^ D' | awk '{print $2}' | tr '\n' ' ')
            DID_COMMIT=0
            
            if [ ! -z "$MODIFIED" ]; then
                echo "📋 Modified files: $MODIFIED"
                git add $MODIFIED 2>/dev/null
                MODIFIED_FILES=$(echo $MODIFIED | tr ' ' ', ')
                if git commit -m "update: Modify $MODIFIED_FILES" 2>/dev/null; then
                    DID_COMMIT=1
                    echo "✅ Committed modifications"
                fi
            fi
            
            if [ ! -z "$ADDED" ]; then
                echo "🆕 New files: $ADDED"
                git add $ADDED 2>/dev/null
                if git commit -m "feat: Add new files - $ADDED" 2>/dev/null; then
                    DID_COMMIT=1
                    echo "✅ Committed new files"
                fi
            fi
            
            if [ ! -z "$DELETED" ]; then
                echo "🗑️  Deleted files: $DELETED"
                git add -A 2>/dev/null
                if git commit -m "refactor: Remove $DELETED" 2>/dev/null; then
                    DID_COMMIT=1
                    echo "✅ Committed deletions"
                fi
            fi
            
            # Push to GitHub
            if [ "$DID_COMMIT" -eq 1 ]; then
                echo "⬆️  Pushing to GitHub..."
                retry_push
            else
                echo "ℹ️  No new commit created in this cycle."
            fi
            echo ""
        fi
    else
        # If no changes, increment counter
        consecutive_stable=$((consecutive_stable + 1))
        
        # Show status every 30 seconds
        if [ $((consecutive_stable % 3)) -eq 0 ]; then
            echo "✨ No changes detected at $(date '+%H:%M:%S') - monitoring..."
        fi
    fi
    
    sleep 10
done
