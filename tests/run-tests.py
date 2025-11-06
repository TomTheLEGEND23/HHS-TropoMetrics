#!/usr/bin/env python3
"""
Test Runner Script
Allows selection of target environment and runs test scripts against it.
"""

import os
import subprocess
import sys

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
            check=False
        )
        
        if result.returncode == 0:
            print(f"\n✓ {script_name} completed successfully")
        else:
            print(f"\n✗ {script_name} failed with exit code {result.returncode}")
        
        return result.returncode
    except Exception as e:
        print(f"\n✗ Error running {script_name}: {e}")
        return 1


def main():
    """Main execution function."""
    display_menu()
    selected_env = get_user_selection()
    
    base_url = f"http://{selected_env['ip']}:{selected_env['port']}"
    
    print(f"\n{'='*60}")
    print(f"Selected: {selected_env['name']}")
    print(f"URL: {base_url}")
    print(f"{'='*60}")
    
    # Ask for data source selection
    print("\nWhich data source would you like to test?")
    print("1. Local Data (uses ?api_key=test)")
    print("2. API Data (uses ?api_key=demo)")
    
    while True:
        data_choice = input("\nSelect data source (1-2): ").strip()
        if data_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    # Set the API key based on selection
    if data_choice == '1':
        api_key = "test"
        data_source = "Local Data"
    else:
        api_key = "demo"
        data_source = "API Data"
    
    print(f"\n{'='*60}")
    print(f"Data Source: {data_source} (api_key={api_key})")
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
    
    results = []
    
    if test_choice in ['1', '3']:
        results.append(("test_API.py", run_test_script("test_API.py", base_url, api_key)))
    
    if test_choice in ['2', '3']:
        results.append(("test_html.py", run_test_script("test_html.py", base_url, api_key)))
    
    # Display summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    for script, code in results:
        status = "✓ PASSED" if code == 0 else "✗ FAILED"
        print(f"{script:<20} {status}")
    print(f"{'='*60}\n")
    
    # Exit with error if any test failed
    sys.exit(max([code for _, code in results]) if results else 0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user.")
        sys.exit(130)