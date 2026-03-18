#!/usr/bin/env python3
"""
Create skill for both Claude and Antigravity platforms simultaneously.
Usage:
    python scripts/create_skill_both_platforms.py <skill-name> [--path <output-base>]
"""

import sys
import os
import shutil
import argparse
from pathlib import Path

# Default paths
CLAUDE_SKILLS_PATH = Path(".claude/skills")
ANTIGRAVITY_SKILLS_PATH = Path(".agent/skills")


def init_skill_for_platform(skill_name: str, platform: str, base_path: Path) -> Path:
    """
    Initialize skill for a specific platform using init_skill.py.

    Args:
        skill_name: Name of the skill
        platform: Platform name (claude or antigravity)
        base_path: Base path for skills

    Returns:
        Path to created skill directory
    """
    script_dir = Path(__file__).parent
    init_script = script_dir / "init_skill.py"

    # Platform-specific output path
    output_path = base_path / skill_name

    # Run init_skill.py
    import subprocess
    result = subprocess.run(
        [sys.executable, str(init_script), skill_name, "--path", str(base_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error initializing skill for {platform}:")
        print(result.stderr)
        sys.exit(1)

    print(f"✓ Created {platform} skill at: {output_path}")
    return output_path


def update_platform_specific_content(skill_dir: Path, platform: str):
    """
    Update platform-specific content in SKILL.md.

    Args:
        skill_dir: Path to skill directory
        platform: Platform name (claude or antigravity)
    """
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return

    # Read current content
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add platform-specific note at the end
    platform_note = f"\n\n---\n\n**Platform**: This skill is for {platform.title()}.\n"
    platform_note += f"**Path**: `{skill_dir.relative_to(Path.cwd())}`\n"

    if platform == "antigravity":
        platform_note += "\n**Compatible with**: Antigravity, Claude Code, GitHub Copilot, VS Code, Cursor, OpenCode\n"
    elif platform == "claude":
        platform_note += "\n**Compatible with**: Claude Code, Antigravity (copy to .agent/skills/), GitHub Copilot\n"

    # Append if not already present
    if platform_note not in content:
        with open(skill_md, 'a', encoding='utf-8') as f:
            f.write(platform_note)


def copy_to_other_platforms(source_dir: Path, skill_name: str):
    """
    Copy skill to other platform directories.

    Args:
        source_dir: Source skill directory (from init_skill.py)
        skill_name: Name of the skill
    """
    # Define target platforms
    platforms = []

    # Check if source is in .claude/skills
    if ".claude/skills" in str(source_dir):
        targets = [
            (ANTIGRAVITY_SKILLS_PATH / skill_name, "Antigravity"),
        ]
    # Check if source is in .agent/skills
    elif ".agent/skills" in str(source_dir):
        targets = [
            (CLAUDE_SKILLS_PATH / skill_name, "Claude Code"),
        ]
    else:
        # Source is custom path, copy to both
        targets = [
            (CLAUDE_SKILLS_PATH / skill_name, "Claude Code"),
            (ANTIGRAVITY_SKILLS_PATH / skill_name, "Antigravity"),
        ]

    # Copy to each target
    for target_path, platform_name in targets:
        if target_path.exists():
            response = input(f"Target {target_path} already exists. Overwrite? [y/N]: ")
            if response.lower() != 'y':
                print(f"⊗ Skipped {platform_name}")
                continue

        # Create parent directory if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy directory
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(source_dir, target_path)

        # Update platform-specific content
        update_platform_specific_content(target_path, platform_name.lower())

        print(f"✓ Copied to {platform_name}: {target_path}")


def create_skill_both_platforms(skill_name: str, base_path: Path = None):
    """
    Create skill for both Claude and Antigravity platforms.

    Args:
        skill_name: Name of the skill (kebab-case)
        base_path: Optional base path (defaults to both .claude/skills and .agent/skills)
    """
    print(f"Creating skill '{skill_name}' for both platforms...")
    print("-" * 60)

    # If custom base path provided, use it and copy to both platforms
    if base_path:
        # Initialize at custom location
        custom_dir = base_path / skill_name
        custom_dir.mkdir(parents=True, exist_ok=True)

        # Run init_skill.py for custom location
        script_dir = Path(__file__).parent
        init_script = script_dir / "init_skill.py"

        import subprocess
        result = subprocess.run(
            [sys.executable, str(init_script), skill_name, "--path", str(base_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error initializing skill:")
            print(result.stderr)
            sys.exit(1)

        print(f"✓ Created skill at: {custom_dir}")

        # Copy to both platforms
        copy_to_other_platforms(custom_dir, skill_name)

    else:
        # Create directly in both platform directories
        print("\n1. Creating for Claude Code...")
        claude_dir = init_skill_for_platform(skill_name, "claude", CLAUDE_SKILLS_PATH)
        update_platform_specific_content(claude_dir, "claude")

        print("\n2. Creating for Antigravity...")
        antigravity_dir = init_skill_for_platform(skill_name, "antigravity", ANTIGRAVITY_SKILLS_PATH)
        update_platform_specific_content(antigravity_dir, "antigravity")

    print("-" * 60)
    print("Skill creation complete!")
    print(f"\nNext steps:")
    print(f"  1. Edit SKILL.md in both platforms:")
    print(f"     - {CLAUDE_SKILLS_PATH / skill_name / 'SKILL.md'}")
    print(f"     - {ANTIGRAVITY_SKILLS_PATH / skill_name / 'SKILL.md'}")
    print(f"  2. Add scripts/, references/, examples/ as needed")
    print(f"  3. Validate: python scripts/quick_validate.py {skill_name}")


def main():
    parser = argparse.ArgumentParser(
        description="Create skill for both Claude and Antigravity platforms"
    )
    parser.add_argument(
        "skill_name",
        help="Name of the skill (use kebab-case, e.g., 'my-skill')"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Optional base path (if provided, copies to both platforms from this location)"
    )

    args = parser.parse_args()

    # Validate skill name format
    if not args.skill_name.replace("-", "").replace("_", "").isalnum():
        print("Error: Skill name should be kebab-case (letters, numbers, hyphens only)")
        print("Example: 'my-skill', 'database-query', 'json-formatter'")
        sys.exit(1)

    create_skill_both_platforms(args.skill_name, args.path)


if __name__ == "__main__":
    main()
