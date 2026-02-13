#!/usr/bin/env python3
"""Demo script showing how to use the LeetCode Auto-Solver"""

import asyncio
import sys
from main import solve_all_problems

# Sample easy LeetCode problems for testing
EASY_PROBLEMS = [
    "https://leetcode.com/problems/two-sum/",
    "https://leetcode.com/problems/palindrome-number/",
    "https://leetcode.com/problems/roman-to-integer/",
    "https://leetcode.com/problems/valid-parentheses/",
    "https://leetcode.com/problems/merge-two-sorted-lists/",
]


async def demo():
    """Run demo with sample problems"""
    print("="*60)
    print("LeetCode Auto-Solver - Demo")
    print("="*60)
    print("\nThis demo will attempt to solve 5 easy LeetCode problems.")
    print("Make sure:")
    print("  1. Chrome is running with remote debugging (port 9222)")
    print("  2. You're logged in to LeetCode in that Chrome instance")
    print("\nPress Ctrl+C at any time to stop.\n")
    
    input("Press Enter to continue...")
    
    results = await solve_all_problems(EASY_PROBLEMS)
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print(f"\nResults saved to: ./data/problems.json")
    print(f"Logs saved to: ./logs/solver.log")
    print("\nTo solve more problems, run:")
    print("  python main.py <problem_url>")
    
    return results


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
