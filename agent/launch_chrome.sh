#!/bin/bash
# Script to launch Chrome with remote debugging enabled

echo "Launching Chrome with remote debugging on port 9222..."
echo ""

# Detect OS and launch Chrome
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    google-chrome --remote-debugging-port=9222 \
                  --user-data-dir=/tmp/chrome-profile \
                  --disable-blink-features=AutomationControlled &
    echo "✓ Chrome launched (Linux)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
        --remote-debugging-port=9222 \
        --user-data-dir=/tmp/chrome-profile \
        --disable-blink-features=AutomationControlled &
    echo "✓ Chrome launched (macOS)"
else
    echo "⚠ Unknown OS. Please launch Chrome manually with:"
    echo "  chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile"
    exit 1
fi

echo ""
echo "Chrome DevTools available at: http://127.0.0.1:9222"
echo ""
echo "Next steps:"
echo "1. Log in to LeetCode in the Chrome window that just opened"
echo "2. Run: python main.py <leetcode_problem_url>"
echo ""
echo "To stop Chrome: pkill -f 'remote-debugging-port=9222'"
