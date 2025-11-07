#!/usr/bin/env python3
"""
Test Runner Script
Allows selection of target environment and runs test scripts against it.

Usage:
    Interactive mode:
        python run-tests.py
    
    Direct mode with arguments:
        python run-tests.py --env <1-4> --api-key <test|demo|none> --test <api|html|both>
        
    Examples:
        python run-tests.py --env 2 --api-key test --test both
        python run-tests.py -e 1 -k demo -t api
"""

import argparse
import os
import subprocess
import sys
import re

# Set UTF-8 encoding for stdout to handle emoji and special characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration: Available environments
ENVIRONMENTS = [
    {"name": "Production From TailNet", "ip": "10.0.0.101", "port": "30080"},
    {"name": "Development From TailNet", "ip": "10.0.0.101", "port": "30081"},
    {"name": "Production From Lab PC", "ip": "192.168.20.27", "port": "980"},
    {"name": "Development From Lab PC", "ip": "192.168.20.27", "port": "981"},
]


def display_menu():
    """Display the environment selection menu."""
    print("\n" + "="*60)
    print("TropoMetrics Test Runner")
    print("="*60)
    print("\nAvailable Environments:")
    print("-"*60)
    for idx, env in enumerate(ENVIRONMENTS, 1):
        print(f"{idx}. {env['name']:<25} http://{env['ip']}:{env['port']}")
    print("-"*60)


def get_user_selection():
    """Get and validate user's environment selection."""
    while True:
        try:
            choice = input(f"\nSelect environment (1-{len(ENVIRONMENTS)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("Exiting...")
                sys.exit(0)
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(ENVIRONMENTS):
                return ENVIRONMENTS[choice_num - 1]
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(ENVIRONMENTS)}.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")


def run_test_script(script_name, base_url, api_key):
    """Run a test script with the specified base URL and API key."""
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"Target: {base_url}")
    print(f"API Key: {api_key}")
    print(f"{'='*60}\n")
    
    try:
        # Run the test script and pass the base URL and API key as environment variables
        result = subprocess.run(
            [sys.executable, script_name],
            env={**os.environ, "TEST_BASE_URL": base_url, "TEST_API_KEY": api_key},
            cwd=os.path.dirname(__file__) or ".",
            check=False,
            capture_output=True,
            text=True
        )
        
        # Print the output in real-time
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode == 0:
            print(f"\n✓ {script_name} completed successfully")
        else:
            print(f"\n✗ {script_name} failed with exit code {result.returncode}")
        
        # Parse statistics from output
        stats = parse_test_statistics(result.stdout)
        
        return result.returncode, stats
    except Exception as e:
        print(f"\n✗ Error running {script_name}: {e}")
        return 1, {}


def parse_test_statistics(output):
    """Parse test statistics from test script output."""
    stats = {}
    
    # Extract total requests
    match = re.search(r'Total requests:\s+(\d+)', output)
    if match:
        stats['total'] = int(match.group(1))
    
    # Extract successful requests
    match = re.search(r'Successful:\s+(\d+)', output)
    if match:
        stats['successful'] = int(match.group(1))
    
    # Extract failed requests
    match = re.search(r'Failed:\s+(\d+)', output)
    if match:
        stats['failed'] = int(match.group(1))
    
    # Extract success rate
    match = re.search(r'Success rate:\s+([\d.]+)%', output)
    if match:
        stats['success_rate'] = float(match.group(1))
    
    # Extract average latency
    match = re.search(r'Average:\s+([\d.]+)s', output)
    if match:
        stats['avg_latency'] = float(match.group(1))
    
    # Extract min latency
    match = re.search(r'Min:\s+([\d.]+)s', output)
    if match:
        stats['min_latency'] = float(match.group(1))
    
    # Extract max latency
    match = re.search(r'Max:\s+([\d.]+)s', output)
    if match:
        stats['max_latency'] = float(match.group(1))
    
    return stats


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="TropoMetrics Test Runner - Test web application across different environments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python run-tests.py
  
  # Run both tests on dev environment with local data
  python run-tests.py --env 2 --api-key test --test both
  
  # Run API test on production with demo API key
  python run-tests.py -e 1 -k demo -t api
  
  # Run HTML test with no API key
  python run-tests.py --env 3 --api-key none --test html

Environment Options:
  1 - Production From TailNet (10.0.0.101:30080)
  2 - Development From TailNet (10.0.0.101:30081)
  3 - Production From Lab PC (192.168.20.27:980)
  4 - Development From Lab PC (192.168.20.27:981)
        """
    )
    
    parser.add_argument(
        '-e', '--env',
        type=int,
        choices=[1, 2, 3, 4],
        help='Environment number (1-4)'
    )
    
    parser.add_argument(
        '-k', '--api-key',
        type=str,
        choices=['test', 'demo', 'none'],
        help='API key to use: test (local data), demo (API data), or none (no parameter)'
    )
    
    parser.add_argument(
        '-t', '--test',
        type=str,
        choices=['api', 'html', 'both'],
        help='Which test(s) to run: api, html, or both'
    )
    
    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()
    
    # Check if running in direct mode (all arguments provided)
    if args.env and args.api_key and args.test:
        # Direct mode - use provided arguments
        selected_env = ENVIRONMENTS[args.env - 1]
        
        # Set API key based on argument
        if args.api_key == 'test':
            api_key = "test"
            data_source = "Local Data"
        elif args.api_key == 'demo':
            api_key = "demo"
            data_source = "API Data"
        else:  # none
            api_key = ""
            data_source = "No API Key"
        
        # Set test choice
        if args.test == 'api':
            test_choice = '1'
        elif args.test == 'html':
            test_choice = '2'
        else:  # both
            test_choice = '3'
        
        # Display configuration
        print("\n" + "="*60)
        print("TropoMetrics Test Runner - Direct Mode")
        print("="*60)
        base_url = f"http://{selected_env['ip']}:{selected_env['port']}"
        print(f"\nEnvironment: {selected_env['name']}")
        print(f"URL: {base_url}")
        if api_key:
            print(f"Data Source: {data_source} (api_key={api_key})")
        else:
            print(f"Data Source: {data_source} (no API parameter)")
        print(f"Test(s): {args.test.upper()}")
        print("="*60)
        
    else:
        # Interactive mode - show menus
        if args.env or args.api_key or args.test:
            print("Warning: Some arguments provided but not all. Use --help for usage.")
            print("Switching to interactive mode...\n")
        
        display_menu()
        selected_env = get_user_selection()
        
        base_url = f"http://{selected_env['ip']}:{selected_env['port']}"
        
        print(f"\n{'='*60}")
        print(f"Selected: {selected_env['name']}")
        print(f"URL: {base_url}")
        print(f"{'='*60}")
        
        # Ask for data source selection
        print("\nWhich data source would you like to test?")
        print("1. Local Data (?api_key=test)")
        print("2. API Data (?api_key=demo)")
        print("3. No API Key (no parameter)")
        
        while True:
            data_choice = input("\nSelect data source (1-3): ").strip()
            if data_choice in ['1', '2', '3']:
                break
            print("Invalid choice. Please enter 1, 2, or 3.")
        
        # Set the API key based on selection
        if data_choice == '1':
            api_key = "test"
            data_source = "Local Data"
        elif data_choice == '2':
            api_key = "demo"
            data_source = "API Data"
        else:
            api_key = ""
            data_source = "No API Key"
        
        print(f"\n{'='*60}")
        if api_key:
            print(f"Data Source: {data_source} (api_key={api_key})")
        else:
            print(f"Data Source: {data_source} (no API parameter)")
        print(f"{'='*60}")
        
        # Ask which tests to run
        print("\nWhich tests would you like to run?")
        print("1. API Test (test_API.py)")
        print("2. HTML Test (test_html.py)")
        print("3. Both tests")
        
        while True:
            test_choice = input("\nSelect test(s) to run (1-3): ").strip()
            if test_choice in ['1', '2', '3']:
                break
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    # Get base_url for direct mode (already set in interactive mode)
    if args.env and args.api_key and args.test:
        base_url = f"http://{selected_env['ip']}:{selected_env['port']}"
    
    # Run tests based on selection
    results = []
    test_stats = {}
    
    if test_choice in ['1', '3']:
        code, stats = run_test_script("test_API.py", base_url, api_key)
        results.append(("test_API.py", code))
        test_stats["test_API.py"] = stats
    
    if test_choice in ['2', '3']:
        code, stats = run_test_script("test_html.py", base_url, api_key)
        results.append(("test_html.py", code))
        test_stats["test_html.py"] = stats
    
    # Display summary with detailed statistics
    print(f"\n{'='*60}")
    print("COMBINED TEST SUMMARY")
    print(f"{'='*60}\n")
    
    for script, code in results:
        status = "✓ PASSED" if code == 0 else "✗ FAILED"
        print(f"{script} - {status}")
        print("-" * 60)
        
        if script in test_stats and test_stats[script]:
            stats = test_stats[script]
            
            # Display request statistics
            if 'total' in stats:
                print(f"  Total requests:     {stats['total']}")
            if 'successful' in stats:
                print(f"  Successful:         {stats['successful']}")
            if 'failed' in stats:
                print(f"  Failed:             {stats['failed']}")
            if 'success_rate' in stats:
                print(f"  Success rate:       {stats['success_rate']}%")
            
            # Display latency statistics
            if 'avg_latency' in stats or 'min_latency' in stats or 'max_latency' in stats:
                print(f"\n  Latency Statistics:")
                if 'avg_latency' in stats:
                    print(f"    Average:          {stats['avg_latency']:.3f}s")
                if 'min_latency' in stats:
                    print(f"    Minimum:          {stats['min_latency']:.3f}s")
                if 'max_latency' in stats:
                    print(f"    Maximum:          {stats['max_latency']:.3f}s")
        else:
            print("  No statistics available")
        
        print()
    
    print(f"{'='*60}\n")
    
    # Exit with error if any test failed
    sys.exit(max([code for _, code in results]) if results else 0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user.")
        sys.exit(130)