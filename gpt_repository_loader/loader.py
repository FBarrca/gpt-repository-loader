import os
import sys
import fnmatch

def get_ignore_list(ignore_file_paths):
    """Reads the ignore files and returns a combined list of patterns."""
    ignore_list = []
    for ignore_file_path in ignore_file_paths:
        if os.path.exists(ignore_file_path):
            with open(ignore_file_path, 'r') as ignore_file:
                # Filter out empty lines and comments
                patterns = [
                    line.strip() 
                    for line in ignore_file 
                    if line.strip() and not line.startswith('#')
                ]
                ignore_list.extend(patterns)
    return ignore_list

def should_ignore(file_path, ignore_list):
    """Determines whether a file should be ignored based on the ignore list."""
    return any(fnmatch.fnmatch(file_path, pattern) for pattern in ignore_list)

def process_repository(repo_path, ignore_list, output_file):
    """Processes the repository files, ignoring those specified in the ignore list."""
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)

            if not should_ignore(relative_file_path, ignore_list):
                with open(file_path, 'r', errors='ignore') as file_content:
                    contents = file_content.read()
                output_file.write("-" * 4 + "\n")
                output_file.write(f"{relative_file_path}\n")
                output_file.write(f"{contents}\n")

def main(repo_path, output_file_path, preamble_file=None):
    """Main function that processes the repository while respecting both .gitignore and .gptignore."""
    
    # Check for ignore files in both current directory and repo path
    cwd_gpt_ignore = os.path.join(os.getcwd(), ".gptignore")
    repo_gpt_ignore = os.path.join(repo_path, ".gptignore")
    cwd_git_ignore = os.path.join(os.getcwd(), ".gitignore")
    repo_git_ignore = os.path.join(repo_path, ".gitignore")

    # Use ignore files from current working directory if available, else from repo_path
    gpt_ignore_path = cwd_gpt_ignore if os.path.exists(cwd_gpt_ignore) else repo_gpt_ignore
    git_ignore_path = cwd_git_ignore if os.path.exists(cwd_git_ignore) else repo_git_ignore

    # Combine patterns from both ignore files
    ignore_list = get_ignore_list([gpt_ignore_path, git_ignore_path])
    
    with open(output_file_path, 'w') as output_file:
        if preamble_file:
            with open(preamble_file, 'r') as pf:
                output_file.write(f"{pf.read()}\n")
        process_repository(repo_path, ignore_list, output_file)
    
    with open(output_file_path, 'a') as output_file:
        output_file.write("--END--")

    print(f"Repository contents written to {output_file_path}.")
