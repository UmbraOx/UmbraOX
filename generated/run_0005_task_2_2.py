import subprocess

def count_passing_tests():
    # Run pytest and capture the output
    result = subprocess.run(['pytest', '-v'], capture_output=True, text=True)
    
    # Parse the output to count passing tests
    lines = result.stdout.splitlines()
    passing_count = 0
    
    for line in lines:
        if 'PASSED' in line:
            passing_count += 1
    
    return passing_count

# Run the function and print the number of passing tests
passing_tests = count_passing_tests()
print(f"Number of passing tests: {passing_tests}")
