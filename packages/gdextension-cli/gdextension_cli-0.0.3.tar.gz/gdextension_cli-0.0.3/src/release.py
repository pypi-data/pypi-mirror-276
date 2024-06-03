"""
Simple script to create a new tag that triggers a release.
"""

import subprocess

from gdextension_cli import __version__

if __name__ == "__main__":
    YES = "yes"
    VERSION = __version__.__version__

    PRODUCTION_RELEASE = False
    if input("Create a production release? (yes/no): ") == YES:
        PRODUCTION_RELEASE = True

    TAG_MESSAGE = input(f"Tag message (default: '{VERSION}'): ")
    if TAG_MESSAGE.strip() == "":
        TAG_MESSAGE = VERSION

    # tags starting with 'release-' will trigger production release
    tag_name = f"release-{VERSION}"
    if not PRODUCTION_RELEASE:
        # starting with 'test-release-' trigger test release to test.pypi
        tag_name = f"test-{tag_name}"

    print(f"Creating release {VERSION}")
    print(f"With tag: {tag_name}")
    print(f"With tag message: '{TAG_MESSAGE}'")

    if (confirm := input("Are you sure? (yes/no): ")) == YES:
        subprocess.run(["git", "tag", "-a", tag_name, "-m", TAG_MESSAGE], check=True)
        subprocess.run(["git", "push", "--follow-tags"], check=True)
