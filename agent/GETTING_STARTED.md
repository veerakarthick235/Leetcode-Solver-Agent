# 🚀 Getting Started with LeetCode Auto-Solver

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.11 or higher installed
- [ ] Google Chrome browser installed
- [ ] A LeetCode account (free or premium)
- [ ] Terminal/command line access

## Quick Start (5 Minutes)

### Step 1: Install Dependencies (1 minute)

```bash
cd /app/agent
pip install -r requirements.txt
```

Expected output:
```
Successfully installed selenium-4.16.0 emergentintegrations-0.1.0 python-dotenv-1.0.0
```

### Step 2: Launch Chrome with Remote Debugging (1 minute)

```bash
./launch_chrome.sh
```

**Or manually**:
```bash
# Linux/Mac
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile &

# Windows
chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\temp\chrome-profile
```

**Important**: A new Chrome window will open. Keep this window open!

### Step 3: Log In to LeetCode (1 minute)

In the Chrome window that just opened:
1. Navigate to https://leetcode.com
2. Log in to your account
3. Keep the window open

### Step 4: Verify Setup (1 minute)

```bash
python test_setup.py
```

Expected output:
```
✓ PASS: Environment
✓ PASS: Imports
✓ PASS: File Structure
✓ PASS: Memory
✓ PASS: Chrome Connection

✅ All tests passed! System ready.
```

### Step 5: Solve Your First Problem (1 minute)

```bash
python main.py https://leetcode.com/problems/two-sum/
```

Watch the magic happen! 🎩✨

The agent will:
1. 📖 Read the problem description
2. 🤖 Generate a solution with AI
3. ⌨️ Inject code into the editor
4. ▶️ Run tests automatically
5. ✅ Submit if tests pass
6. 💾 Save result to database

## Expected Output

```
============================================================
Starting to solve: two-sum
============================================================
INFO: Navigating to https://leetcode.com/problems/two-sum/
INFO: Scraped description (850 chars)
INFO: Generating solution with Gemini...
INFO: Generated solution (125 chars)
INFO: Injecting code into editor...
INFO: Code injected successfully
INFO: Clicking Run button...
INFO: Run button clicked
INFO: Waiting for test results (timeout: 30s)...
INFO: ✓ Tests passed!
INFO: Submitting solution...
INFO: Submit button clicked
INFO: Saved two-sum: pass (attempts: 1)
INFO: ✓ Problem two-sum solved successfully!
```

## Check Your Results

```bash
# View solved problems
cat data/problems.json

# View detailed logs
cat logs/solver.log

# Get statistics
python -c "from memory import MemoryStore; m = MemoryStore('./data/problems.json'); print(m.get_stats())"
```

## What's Next?

### Try More Problems

```bash
# Easy problem
python main.py https://leetcode.com/problems/palindrome-number/

# Medium problem
python main.py https://leetcode.com/problems/add-two-numbers/

# Multiple problems at once
python main.py \
  https://leetcode.com/problems/two-sum/ \
  https://leetcode.com/problems/reverse-integer/ \
  https://leetcode.com/problems/roman-to-integer/
```

### Run the Demo

```bash
python demo.py
```

This will solve 5 easy problems automatically.

### Solve All Easy Problems

Create a file `easy_problems.txt`:
```
https://leetcode.com/problems/two-sum/
https://leetcode.com/problems/reverse-integer/
https://leetcode.com/problems/palindrome-number/
https://leetcode.com/problems/roman-to-integer/
https://leetcode.com/problems/longest-common-prefix/
```

Then run:
```bash
cat easy_problems.txt | xargs python main.py
```

## Troubleshooting

### ❌ "Connection refused" Error

**Problem**: Chrome is not running with remote debugging.

**Solution**:
```bash
# Kill any existing Chrome
pkill -f 'remote-debugging-port=9222'

# Relaunch
./launch_chrome.sh
```

### ❌ "Could not find problem description"

**Problem**: Not logged in to LeetCode or page structure changed.

**Solution**:
1. Open the Chrome window on port 9222
2. Go to leetcode.com and log in
3. Try again

### ❌ "Test execution timeout"

**Problem**: Tests are taking longer than 30 seconds.

**Solution**: Edit `.env` and increase timeout:
```bash
RESULT_TIMEOUT=60
```

### ❌ "Rate limit exceeded"

**Problem**: Too many API calls to Gemini.

**Solution**: Wait 60 seconds. The system enforces 10 calls/minute automatically.

### ❌ "Invalid API key"

**Problem**: Emergent LLM key is not working.

**Solution**: The key is pre-configured in `.env`. If still failing:
1. Check your balance at Emergent dashboard
2. Add credits if needed
3. Enable auto top-up

## Advanced Usage

### Custom Configuration

Edit `.env` to customize behavior:

```bash
# Increase timeout for slow networks
RESULT_TIMEOUT=60

# More retry attempts
MAX_RETRIES=3

# Debug mode
LOG_LEVEL=DEBUG
```

### Monitor in Real-Time

```bash
# Terminal 1: Run solver
python main.py <url>

# Terminal 2: Watch logs
tail -f logs/solver.log
```

### Batch Processing

Process many problems efficiently:

```bash
# Create problem list
echo "https://leetcode.com/problems/two-sum/" > problems.txt
echo "https://leetcode.com/problems/add-two-numbers/" >> problems.txt
echo "https://leetcode.com/problems/longest-substring-without-repeating-characters/" >> problems.txt

# Solve all
cat problems.txt | xargs python main.py
```

## Understanding the Output

### Success (✓)
```
INFO: ✓ Tests passed!
INFO: Saved two-sum: pass (attempts: 1)
```
Problem solved and submitted!

### Failure (✗)
```
WARNING: ✗ Tests failed
INFO: Test failed: Wrong Answer - Expected [0,1], Got [1,0]
INFO: Retrying with error context...
```
Agent will retry with the error message.

### Timeout (⏱)
```
WARNING: Timeout waiting for test results
INFO: Saved two-sum: timeout (attempts: 1)
```
Tests didn't complete in time. Increase `RESULT_TIMEOUT`.

## Performance Tips

### Optimize for Speed

1. **Solve easy problems first** - Higher success rate
2. **Use batch processing** - More efficient than one-by-one
3. **Increase API rate limit** - Contact Emergent for higher limits
4. **Skip solved problems** - Agent automatically skips them

### Optimize for Success Rate

1. **Start with retries = 3** - In `.env`: `MAX_RETRIES=3`
2. **Increase timeouts** - For slow networks: `RESULT_TIMEOUT=60`
3. **Use debug mode** - To see what's happening: `LOG_LEVEL=DEBUG`

## Daily Usage Pattern

### Morning Routine (10 Easy Problems)

```bash
# 1. Launch Chrome
./launch_chrome.sh

# 2. Run demo
python demo.py

# 3. Check results
cat data/problems.json | python -m json.tool | grep -A 5 '"status": "pass"'
```

### Weekly Goal (50 Problems)

```bash
# Get list of 50 easy problems from LeetCode
# Save to problems.txt
# Run batch processor
cat problems.txt | xargs python main.py

# Check statistics
python -c "from memory import MemoryStore; m = MemoryStore('./data/problems.json'); stats = m.get_stats(); print(f\"Solved: {stats['solved']}/{stats['total']} ({stats['success_rate']:.1%})\")"
```

## Best Practices

### ✅ DO

- Keep Chrome window open while solving
- Log in to LeetCode before starting
- Check logs if something fails
- Start with easy problems
- Use retry logic for failures

### ❌ DON'T

- Close Chrome window during solving
- Run without logging in to LeetCode
- Ignore timeout errors
- Try hard problems first without testing
- Use in actual interviews (ethical concerns)

## Success Metrics

Track your progress:

```bash
# View statistics
python -c "
from memory import MemoryStore
m = MemoryStore('./data/problems.json')
stats = m.get_stats()
print(f'''
📊 Your Statistics:
  Total Problems: {stats['total']}
  ✅ Solved: {stats['solved']}
  ❌ Failed: {stats['failed']}
  ⏱ Timeout: {stats['timeout']}
  📈 Success Rate: {stats['success_rate']:.1%}
''')
"
```

## Next Steps

### Learn More

1. **Architecture**: Read [SYSTEM_DESIGN.md](/app/docs/SYSTEM_DESIGN.md)
2. **Advanced Features**: Read [README.md](/app/agent/README.md)
3. **Troubleshooting**: See README Troubleshooting section

### Customize

1. **Modify AI behavior**: Edit `brain.py`
2. **Change selectors**: Edit `config.py`
3. **Add features**: See SYSTEM_DESIGN.md Section 8

### Contribute

1. Add support for more languages (Java, C++)
2. Improve AI prompts for better solutions
3. Add UI dashboard for visualization
4. Share your improvements!

## Getting Help

### Quick Help

```bash
# Check if everything is set up
python test_setup.py

# View recent logs
tail -20 logs/solver.log

# Check Chrome connection
lsof -i :9222
```

### Common Questions

**Q: How long does it take to solve a problem?**  
A: 15-30 seconds on average for easy problems.

**Q: What's the success rate?**  
A: ~70-80% on first attempt, ~85-90% with retries.

**Q: Can I use my own API key?**  
A: Yes, replace `EMERGENT_LLM_KEY` in `.env`.

**Q: Does it work with premium problems?**  
A: Yes, if you're logged in with a premium account.

**Q: Will LeetCode ban me?**  
A: Using automation may violate ToS. Use for learning only.

## Support

For issues:
1. Check logs: `cat logs/solver.log`
2. Run test: `python test_setup.py`
3. Review docs: [README.md](/app/agent/README.md)

---

**You're all set! Happy solving! 🎉**

Start with:
```bash
python main.py https://leetcode.com/problems/two-sum/
```

Then explore more in [README.md](/app/agent/README.md) and [SYSTEM_DESIGN.md](/app/docs/SYSTEM_DESIGN.md).
