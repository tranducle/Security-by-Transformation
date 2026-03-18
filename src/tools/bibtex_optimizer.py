#!/usr/bin/env python3
"""
BibTeX Optimizer Script
-----------------------
Optimizes references.bib by finding missing DOIs and retrieving accurate BibTeX entries.

Features:
- Parses existing .bib file and preserves original keys
- Searches for DOIs via Semantic Scholar and CrossRef APIs
- Retrieves accurate BibTeX from DOI.org (same method as doi2bib)
- Creates backup before modification
- Generates optimization report

Usage:
    python bibtex_optimizer.py references.bib
    python bibtex_optimizer.py references.bib --output optimized.bib
"""

import re
import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

# Check for required libraries
try:
    import requests
except ImportError:
    print("Please install requests: pip install requests")
    sys.exit(1)

try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter
except ImportError:
    print("Please install bibtexparser: pip install bibtexparser")
    sys.exit(1)


class BibTeXOptimizer:
    """Optimizes BibTeX entries by finding DOIs and getting accurate entries."""
    
    def __init__(self, bib_file: str, output_file: Optional[str] = None):
        self.bib_file = bib_file
        self.output_file = output_file or bib_file
        self.entries: List[Dict] = []
        self.report: Dict = {
            "total_entries": 0,
            "dois_found": [],
            "dois_already_present": [],
            "dois_not_found": [],
            "entries_updated": [],
            "errors": []
        }
        
        # API rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds between API calls
    
    def _rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def load_bib_file(self) -> bool:
        """Load and parse the BibTeX file."""
        try:
            with open(self.bib_file, 'r', encoding='utf-8') as f:
                parser = BibTexParser(common_strings=True)
                bib_db = bibtexparser.load(f, parser=parser)
                self.entries = bib_db.entries
                self.report["total_entries"] = len(self.entries)
                print(f"✓ Loaded {len(self.entries)} entries from {self.bib_file}")
                return True
        except Exception as e:
            print(f"✗ Error loading {self.bib_file}: {e}")
            self.report["errors"].append(f"Load error: {e}")
            return False
    
    def create_backup(self) -> str:
        """Create a backup of the original file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{os.path.splitext(self.bib_file)[0]}_backup_{timestamp}.bib"
        try:
            with open(self.bib_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"✓ Backup created: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"✗ Backup failed: {e}")
            return ""
    
    def search_doi_semantic_scholar(self, title: str, authors: str = "") -> Optional[str]:
        """Search for DOI using Semantic Scholar API."""
        self._rate_limit()
        
        # Clean title for search
        clean_title = re.sub(r'[{}\\]', '', title)
        
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": clean_title,
            "limit": 3,
            "fields": "externalIds,title,authors,year"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    for paper in data["data"]:
                        # Check if title matches closely
                        if self._title_similarity(clean_title, paper.get("title", "")) > 0.8:
                            external_ids = paper.get("externalIds", {})
                            if external_ids and external_ids.get("DOI"):
                                return external_ids["DOI"]
            return None
        except Exception as e:
            print(f"  Semantic Scholar error: {e}")
            return None
    
    def search_doi_crossref(self, title: str, authors: str = "") -> Optional[str]:
        """Search for DOI using CrossRef API."""
        self._rate_limit()
        
        # Clean title for search
        clean_title = re.sub(r'[{}\\]', '', title)
        
        url = "https://api.crossref.org/works"
        params = {
            "query.title": clean_title,
            "rows": 3
        }
        if authors:
            first_author = authors.split(" and ")[0].split(",")[0].strip()
            params["query.author"] = first_author
        
        headers = {
            "User-Agent": "BibTeXOptimizer/1.0 (mailto:research@example.com)"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data.get("message", {}).get("items", [])
                for item in items:
                    item_title = " ".join(item.get("title", []))
                    if self._title_similarity(clean_title, item_title) > 0.8:
                        return item.get("DOI")
            return None
        except Exception as e:
            print(f"  CrossRef error: {e}")
            return None
    
    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate simple title similarity (case-insensitive)."""
        t1 = set(title1.lower().split())
        t2 = set(title2.lower().split())
        if not t1 or not t2:
            return 0.0
        intersection = len(t1 & t2)
        union = len(t1 | t2)
        return intersection / union if union > 0 else 0.0
    
    def get_bibtex_from_doi(self, doi: str) -> Optional[str]:
        """Get BibTeX entry from DOI using DOI.org (same as doi2bib method)."""
        self._rate_limit()
        
        url = f"https://doi.org/{doi}"
        headers = {
            "Accept": "application/x-bibtex; charset=utf-8"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return response.text
            return None
        except Exception as e:
            print(f"  DOI.org error: {e}")
            return None
    
    def parse_bibtex_entry(self, bibtex_str: str) -> Optional[Dict]:
        """Parse a single BibTeX entry string."""
        try:
            parser = BibTexParser(common_strings=True)
            bib_db = bibtexparser.loads(bibtex_str, parser=parser)
            if bib_db.entries:
                return bib_db.entries[0]
            return None
        except Exception:
            return None
    
    def merge_entry(self, original: Dict, new_entry: Dict) -> Dict:
        """Merge new entry data into original, preserving the original key."""
        merged = original.copy()
        
        # Preserve original ID (key) - CRITICAL!
        original_id = original.get("ID")
        
        # Update fields from new entry (except ID)
        for key, value in new_entry.items():
            if key.lower() != "id":
                # Only update if the new value is more complete
                if key not in merged or (value and not merged.get(key)):
                    merged[key] = value
                # Always update DOI if found
                if key.lower() == "doi":
                    merged[key] = value
        
        # Restore original ID
        merged["ID"] = original_id
        
        return merged
    
    def optimize_entry(self, entry: Dict) -> Tuple[Dict, bool]:
        """Optimize a single BibTeX entry."""
        entry_id = entry.get("ID", "unknown")
        title = entry.get("title", "")
        authors = entry.get("author", "")
        existing_doi = entry.get("doi", "")
        
        print(f"\nProcessing: {entry_id}")
        
        # If DOI already exists, try to get better BibTeX
        if existing_doi:
            print(f"  DOI already present: {existing_doi}")
            self.report["dois_already_present"].append({
                "id": entry_id,
                "doi": existing_doi
            })
            
            # Try to get more complete BibTeX from DOI
            new_bibtex = self.get_bibtex_from_doi(existing_doi)
            if new_bibtex:
                new_entry = self.parse_bibtex_entry(new_bibtex)
                if new_entry:
                    merged = self.merge_entry(entry, new_entry)
                    print(f"  ✓ Entry enriched from DOI.org")
                    return merged, True
            
            return entry, False
        
        # Search for DOI
        print(f"  Searching for DOI...")
        
        # Try Semantic Scholar first
        doi = self.search_doi_semantic_scholar(title, authors)
        source = "Semantic Scholar"
        
        # If not found, try CrossRef
        if not doi:
            doi = self.search_doi_crossref(title, authors)
            source = "CrossRef"
        
        if doi:
            print(f"  ✓ DOI found via {source}: {doi}")
            self.report["dois_found"].append({
                "id": entry_id,
                "title": title[:50] + "..." if len(title) > 50 else title,
                "doi": doi,
                "source": source
            })
            
            # Get accurate BibTeX from DOI
            new_bibtex = self.get_bibtex_from_doi(doi)
            if new_bibtex:
                new_entry = self.parse_bibtex_entry(new_bibtex)
                if new_entry:
                    merged = self.merge_entry(entry, new_entry)
                    self.report["entries_updated"].append(entry_id)
                    print(f"  ✓ Entry updated with accurate BibTeX")
                    return merged, True
            
            # If BibTeX retrieval failed, at least add the DOI
            entry["doi"] = doi
            self.report["entries_updated"].append(entry_id)
            print(f"  ✓ DOI added to entry")
            return entry, True
        else:
            print(f"  ✗ DOI not found (keeping original)")
            self.report["dois_not_found"].append({
                "id": entry_id,
                "title": title[:50] + "..." if len(title) > 50 else title
            })
            return entry, False
    
    def optimize_all(self):
        """Optimize all entries."""
        optimized_entries = []
        updated_count = 0
        
        for entry in self.entries:
            optimized, was_updated = self.optimize_entry(entry)
            optimized_entries.append(optimized)
            if was_updated:
                updated_count += 1
        
        self.entries = optimized_entries
        print(f"\n{'='*50}")
        print(f"Optimization complete: {updated_count}/{len(self.entries)} entries updated")
        return updated_count
    
    def save_bib_file(self):
        """Save optimized entries to output file."""
        try:
            db = bibtexparser.bibdatabase.BibDatabase()
            db.entries = self.entries
            
            writer = BibTexWriter()
            writer.indent = '  '
            writer.order_entries_by = None  # Preserve original order
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(writer.write(db))
            
            print(f"✓ Saved optimized BibTeX to: {self.output_file}")
            return True
        except Exception as e:
            print(f"✗ Error saving: {e}")
            self.report["errors"].append(f"Save error: {e}")
            return False
    
    def generate_report(self, report_file: Optional[str] = None):
        """Generate optimization report in Markdown format."""
        if not report_file:
            report_file = os.path.splitext(self.bib_file)[0] + "_optimization_report.md"
        
        report = f"""# BibTeX Optimization Report

**File:** `{self.bib_file}`
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Output:** `{self.output_file}`

## Summary

| Metric | Count |
|--------|-------|
| Total Entries | {self.report['total_entries']} |
| DOIs Found & Added | {len(self.report['dois_found'])} |
| DOIs Already Present | {len(self.report['dois_already_present'])} |
| DOIs Not Found | {len(self.report['dois_not_found'])} |
| Entries Updated | {len(self.report['entries_updated'])} |

## DOIs Found & Added

| Key | Title | DOI | Source |
|-----|-------|-----|--------|
"""
        for item in self.report['dois_found']:
            report += f"| {item['id']} | {item['title']} | `{item['doi']}` | {item['source']} |\n"
        
        if not self.report['dois_found']:
            report += "| - | No new DOIs found | - | - |\n"
        
        report += """
## DOIs Not Found (Manual Check Recommended)

| Key | Title |
|-----|-------|
"""
        for item in self.report['dois_not_found']:
            report += f"| {item['id']} | {item['title']} |\n"
        
        if not self.report['dois_not_found']:
            report += "| - | All entries have DOIs |\n"
        
        report += """
## Important Notes

- **Original BibTeX keys preserved** - No changes to citation references needed
- Entries without DOI may be: books, theses, technical reports, or older publications
- Review entries marked as "DOI Not Found" manually if needed

"""
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✓ Report saved to: {report_file}")
        except Exception as e:
            print(f"✗ Report error: {e}")
    
    def run(self):
        """Run the full optimization process."""
        print(f"\n{'='*50}")
        print("BibTeX Optimizer")
        print(f"{'='*50}\n")
        
        # Load file
        if not self.load_bib_file():
            return False
        
        # Create backup
        backup = self.create_backup()
        if not backup:
            print("⚠ Warning: Proceeding without backup")
        
        # Optimize entries
        self.optimize_all()
        
        # Save
        if not self.save_bib_file():
            return False
        
        # Generate report
        self.generate_report()
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Optimize BibTeX file by finding DOIs and getting accurate entries"
    )
    parser.add_argument("bib_file", help="Input .bib file to optimize")
    parser.add_argument("-o", "--output", help="Output file (default: overwrite input)")
    parser.add_argument("-r", "--report", help="Report file (default: input_optimization_report.md)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.bib_file):
        print(f"Error: File not found: {args.bib_file}")
        sys.exit(1)
    
    optimizer = BibTeXOptimizer(args.bib_file, args.output)
    success = optimizer.run()
    
    if args.report:
        optimizer.generate_report(args.report)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
