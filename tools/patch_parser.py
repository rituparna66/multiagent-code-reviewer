import re


def extract_patch_metadata(filename: str, patch: str):
    """
    Extract approximate starting line and added lines from unified diff patch.
    """

    # Find the @@ header
    header_match = re.search(r"@@ -\d+,\d+ \+(\d+),\d+ @@", patch)

    if header_match:
        new_start_line = int(header_match.group(1))
    else:
        new_start_line = None

    # Extract added lines (lines starting with + but not +++)
    added_lines = [
        line[1:]
        for line in patch.split("\n")
        if line.startswith("+") and not line.startswith("+++")
    ]

    return {
        "file": filename,
        "start_line": new_start_line,
        "added_lines": added_lines,
    }
