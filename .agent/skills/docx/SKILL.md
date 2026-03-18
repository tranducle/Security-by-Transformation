---
name: docx
description: Comprehensive Microsoft Word (.docx) document creation, editing, and analysis with tracked changes, comments, and formatting preservation. Use when Claude needs to create new Word documents, edit existing documents with tracked changes (redlining), add comments, extract content, or convert documents. Supports legal contracts, business reports, academic papers, and government documents with professional OOXML manipulation.
license: See LICENSE.txt for terms
version: 1.0.0
---

# DOCX Document Processing

Professional Microsoft Word document manipulation with full support for tracked changes, comments, formatting, and content extraction.

## When to Use

- **Creating new Word documents** - Generate .docx files with proper formatting
- **Editing existing documents** - Modify content with or without tracked changes
- **Legal/business documents** - Redlining workflow for contract review
- **Content extraction** - Read and analyze document contents
- **Document conversion** - Convert to markdown, PDF, or images
- **Adding comments** - Annotate documents with review notes
- **Tracked changes** - Professional redlining with insertions/deletions

## Capabilities

### Document Creation
- Generate new .docx files using docx-js library
- Professional formatting with styles, tables, lists, headers/footers
- Images, hyperlinks, table of contents, page breaks

### Document Editing
- **Tracked changes (redlining)** - Professional review workflow
- **Comments** - Add annotations and replies
- **Content modification** - Insert, delete, replace text
- **Formatting preservation** - Maintain document structure

### Content Analysis
- Extract text content to markdown
- Read document structure and metadata
- Analyze tracked changes and comments
- View embedded media

### Document Conversion
- DOCX → Markdown (with tracked changes)
- DOCX → PDF → Images (for visual review)

## Workflow Decision Tree

### Reading/Analyzing Content
→ Use "Text extraction" or "Raw XML access" sections

### Creating New Document
→ Use "Creating a new Word document" workflow

### Editing Existing Document
- **Your own document + simple changes** → Use "Basic OOXML editing"
- **Someone else's document** → Use "Redlining workflow"
- **Legal/academic/business docs** → Use "Redlining workflow" (required)

## Prerequisites

**Required dependencies:**

```bash
# For text extraction
sudo apt-get install pandoc

# For creating new documents
npm install -g docx

# For PDF conversion
sudo apt-get install libreoffice

# For PDF to images
sudo apt-get install poppler-utils

# For XML manipulation
pip install defusedxml Pillow
```

## Quick Start Examples

### Example 1: Extract Text Content

```bash
# Convert to markdown with tracked changes visible
pandoc --track-changes=all document.docx -o output.md
```

### Example 2: Create New Document

**MANDATORY:** Read `references/docx-js.md` completely (~350 lines) for detailed syntax and best practices.

```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun("My Document")]
      }),
      new Paragraph({
        children: [new TextRun("Document content here")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer =>
  fs.writeFileSync("output.docx", buffer)
);
```

### Example 3: Edit with Tracked Changes

**MANDATORY:** Read `references/ooxml.md` completely (~600 lines) for Document library API and XML patterns.

```bash
# 1. Unpack document
python scripts/unpack.py document.docx unpacked

# 2. Create Python script using Document library
# See references/ooxml.md "Document Library" section

# 3. Pack modified document
python scripts/pack.py unpacked edited.docx
```

## Detailed Workflows

### Creating a New Word Document

**When to use:** Starting from scratch, generating reports, creating templates

**Steps:**

1. **MANDATORY - READ ENTIRE FILE:** Read `references/docx-js.md` (~350 lines) completely from start to finish. **NEVER set range limits.** This file contains critical formatting rules and common pitfalls.

2. Create JavaScript/TypeScript file:
   ```javascript
   const { Document, Packer, Paragraph, TextRun, Table, AlignmentType } = require('docx');

   const doc = new Document({
     styles: {
       default: {
         document: {
           run: { font: "Arial", size: 24 }  // 12pt default
         }
       },
       paragraphStyles: [
         { id: "Heading1", name: "Heading 1", basedOn: "Normal",
           run: { size: 32, bold: true },  // 16pt
           paragraph: { spacing: { before: 240, after: 240 } } }
       ]
     },
     sections: [{
       properties: {
         page: {
           margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
         }
       },
       children: [
         new Paragraph({
           heading: HeadingLevel.HEADING_1,
           children: [new TextRun("Document Title")]
         }),
         new Paragraph({
           children: [new TextRun("Regular paragraph text")]
         })
       ]
     }]
   });

   Packer.toBuffer(doc).then(buffer =>
     fs.writeFileSync("output.docx", buffer)
   );
   ```

3. **Critical Formatting Rules:**
   - **NEVER use `\n` for line breaks** - always use separate Paragraph elements
   - **ALWAYS use ShadingType.CLEAR** for table cell shading
   - **ALWAYS set columnWidths array** for tables
   - **ALWAYS use proper numbering config** for lists (not unicode bullets)
   - **ImageRun REQUIRES type parameter** - "png", "jpg", etc.

### Editing Existing Document - Redlining Workflow

**When to use:** Reviewing documents from others, legal contracts, collaborative editing

**Principle: Minimal, Precise Edits**
Only mark text that actually changes. Preserve unchanged text to make reviews professional.

**Example - GOOD:**
```xml
<!-- Changing "30 days" to "60 days" - only marks what changed -->
<w:r><w:t>The term is </w:t></w:r>
<w:del><w:r><w:delText>30</w:delText></w:r></w:del>
<w:ins><w:r><w:t>60</w:t></w:r></w:ins>
<w:r><w:t> days.</w:t></w:r>
```

**Example - BAD:**
```xml
<!-- Replaces entire sentence - unprofessional -->
<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del>
<w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>
```

**Steps:**

1. **Get markdown representation:**
   ```bash
   pandoc --track-changes=all document.docx -o current.md
   ```

2. **Identify and group changes:**
   - **Location methods:** Section numbers, headings, unique text patterns
   - **DO NOT use markdown line numbers** - they don't map to XML
   - **Batch organization:** Group 3-10 related changes per batch
   - **Batch by:** Section, change type, proximity, or complexity

3. **MANDATORY - READ ENTIRE FILE:** Read `references/ooxml.md` (~600 lines) completely. Focus on:
   - "Document Library" section for API
   - "Tracked Change Patterns" for XML structure
   - "Method Selection Guide" for when to use each approach

4. **Unpack the document:**
   ```bash
   python scripts/unpack.py document.docx unpacked

   # Note the suggested RSID from output
   # Example: "Suggested RSID: 07DC5ECB"
   ```

5. **Implement changes in batches:**

   For each batch:

   **a. Map text to XML:**
   ```bash
   grep -n "specific text" unpacked/word/document.xml
   ```

   **b. Create and run script:**
   ```python
   # Find the docx skill root
   import sys
   sys.path.insert(0, r'd:\APPS\BUILDSKILLFORANTIGRAVITY\.agent\skills\docx')

   from scripts.document import Document

   # Initialize with suggested RSID
   doc = Document('unpacked', rsid="07DC5ECB", track_revisions=True)

   # Find node and make changes
   node = doc["word/document.xml"].get_node(
       tag="w:r",
       contains="specific text",
       line_number=range(100, 150)
   )

   # Minimal edit - preserve formatting
   rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
   replacement = f'<w:r>{rpr}<w:t>unchanged </w:t></w:r><w:del><w:r>{rpr}<w:delText>old</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>new</w:t></w:r></w:ins>'
   doc["word/document.xml"].replace_node(node, replacement)

   # Save
   doc.save()
   ```

6. **Pack the document:**
   ```bash
   python scripts/pack.py unpacked reviewed-document.docx
   ```

7. **Final verification:**
   ```bash
   # Convert to markdown
   pandoc --track-changes=all reviewed-document.docx -o verification.md

   # Verify changes
   grep "original phrase" verification.md  # Should NOT find
   grep "replacement phrase" verification.md  # Should find
   ```

### Adding Comments

```python
import sys
sys.path.insert(0, r'd:\APPS\BUILDSKILLFORANTIGRAVITY\.agent\skills\docx')

from scripts.document import Document

doc = Document('unpacked')

# Add comment on tracked change
start_node = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "1"})
end_node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "2"})
doc.add_comment(start=start_node, end=end_node, text="Explanation of this change")

# Reply to existing comment
doc.reply_to_comment(parent_comment_id=0, text="I agree with this change")

doc.save()
```

### Converting Documents to Images

For visual analysis of Word documents:

```bash
# Step 1: Convert DOCX to PDF
soffice --headless --convert-to pdf document.docx

# Step 2: Convert PDF to JPEG images
pdftoppm -jpeg -r 150 document.pdf page

# Creates: page-1.jpg, page-2.jpg, etc.

# For specific page range:
pdftoppm -jpeg -r 150 -f 2 -l 5 document.pdf page  # Pages 2-5 only
```

## Critical Rules

### Tracked Changes

1. **NEVER modify content inside another author's `<w:ins>` or `<w:del>` tags**
2. **ALWAYS use nested deletions** to remove another author's insertions
3. **Preserve original `<w:r>` elements** for unchanged text (maintains RSIDs)
4. **Every edit must be properly tracked** with `<w:ins>` or `<w:del>` tags

### XML Structure

1. **Place `<w:del>` and `<w:ins>` at paragraph level** containing complete `<w:r>` elements
2. **NEVER nest inside `<w:r>` elements** - creates invalid XML
3. **RSIDs must be 8-digit hex** - use values like `00AB1234` (only 0-9, A-F)
4. **Whitespace handling** - add `xml:space='preserve'` to `<w:t>` with leading/trailing spaces

### Document Creation

1. **NEVER use `\n` for line breaks** - always use separate Paragraph elements
2. **ALWAYS use proper Word lists** - never unicode bullets
3. **ALWAYS set columnWidths array** for table compatibility
4. **ALWAYS use ShadingType.CLEAR** for table cell shading
5. **ImageRun REQUIRES type parameter** - "png", "jpg", "jpeg", "gif", "bmp", "svg"

## Document Library API Reference

The Document class (`scripts/document.py`) provides:

### Initialization
```python
from scripts.document import Document

# Basic
doc = Document('unpacked')

# Custom author
doc = Document('unpacked', author="John Doe", initials="JD")

# Track revisions mode
doc = Document('unpacked', track_revisions=True)

# Custom RSID
doc = Document('unpacked', rsid="07DC5ECB")
```

### Core Methods

**Finding nodes:**
```python
# By text content
node = doc["word/document.xml"].get_node(tag="w:p", contains="specific text")

# By line range
para = doc["word/document.xml"].get_node(tag="w:p", line_number=range(100, 150))

# By attributes
node = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "1"})

# Combine filters
node = doc["word/document.xml"].get_node(
    tag="w:r",
    line_number=range(40, 60),
    contains="text"
)
```

**Making changes:**
```python
# Replace node
doc["word/document.xml"].replace_node(node, replacement_xml)

# Insert after
nodes = doc["word/document.xml"].insert_after(node, new_xml)

# Suggest deletion (entire run/paragraph)
doc["word/document.xml"].suggest_deletion(node)

# Reject insertion
nodes = doc["word/document.xml"].revert_insertion(ins_node)

# Reject deletion (restore)
nodes = doc["word/document.xml"].revert_deletion(del_node)
```

**Comments:**
```python
# Add comment
doc.add_comment(start=start_node, end=end_node, text="Comment text")

# Reply to comment
doc.reply_to_comment(parent_comment_id=0, text="Reply text")
```

**Saving:**
```python
# Save with validation (default)
doc.save()

# Save to different location
doc.save('modified-unpacked')

# Skip validation (debugging only)
doc.save(validate=False)
```

## Method Selection Guide

### For Adding Your Own Changes

- **To regular text**: Use `replace_node()` with `<w:del>`/`<w:ins>` tags
- **To delete entire `<w:r>` or `<w:p>`**: Use `suggest_deletion()`

### For Modifying Another Author's Changes

- **Partially modify**: Use `replace_node()` to nest your changes inside their `<w:ins>`/`<w:del>`
- **Completely reject insertion**: Use `revert_insertion()` (NOT `suggest_deletion()`)
- **Completely reject deletion**: Use `revert_deletion()` to restore with tracked changes

## Common Patterns

### Minimal Text Replacement

```python
# Change "30 days" to "60 days"
node = doc["word/document.xml"].get_node(tag="w:r", contains="30 days")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:r>{rpr}<w:t>within </w:t></w:r><w:del><w:r>{rpr}<w:delText>30</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>60</w:t></w:r></w:ins><w:r>{rpr}<w:t> days</w:t></w:r>'
doc["word/document.xml"].replace_node(node, replacement)
```

### Partially Delete Another Author's Insertion

```python
# Original: <w:ins w:author="Jane"><w:r><w:t>quarterly report</w:t></w:r></w:ins>
# Goal: Delete "financial" to make it "quarterly report"
node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "5"})
replacement = '''<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:r><w:t>quarterly </w:t></w:r>
  <w:del><w:r><w:delText>financial </w:delText></w:r></w:del>
  <w:r><w:t>report</w:t></w:r>
</w:ins>'''
doc["word/document.xml"].replace_node(node, replacement)
```

### Complete Replacement with Formatting Preserved

```python
# Replace "apple" with "banana orange" while preserving formatting
node = doc["word/document.xml"].get_node(tag="w:r", contains="apple")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:del><w:r>{rpr}<w:delText>apple</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>banana orange</w:t></w:r></w:ins>'
doc["word/document.xml"].replace_node(node, replacement)
```

## Troubleshooting

### Script Not Found Error

**Error:** `ModuleNotFoundError: No module named 'scripts.document'`

**Solution:**
```python
# Add skill root to path before importing
import sys
sys.path.insert(0, r'd:\APPS\BUILDSKILLFORANTIGRAVITY\.agent\skills\docx')
```

### Validation Failed

**Error:** `Validation error: ...`

**Solution:**
- Check XML structure matches patterns in `references/ooxml.md`
- Verify RSIDs are 8-digit hex
- Ensure `<w:ins>` and `<w:del>` tags are properly closed
- Check that tracked changes don't modify another author's changes directly

### Changes Not Appearing

**Possible causes:**
1. Text split across multiple `<w:r>` elements - grep to verify structure
2. Line numbers changed after previous edits - re-grep before each script
3. Using markdown line numbers instead of XML line numbers

**Solution:**
```bash
# Always grep immediately before writing script
grep -n "target text" unpacked/word/document.xml
```

### Document Won't Open

**Possible causes:**
1. Invalid XML structure
2. PageBreak not inside Paragraph
3. Malformed tracked changes

**Solution:**
- Read `references/docx-js.md` for creation rules
- Read `references/ooxml.md` for tracked change patterns
- Validate XML before packing

## References

- `references/ooxml.md` - Document library API and XML patterns (~600 lines)
- `references/docx-js.md` - Document creation tutorial (~350 lines)
- `scripts/document.py` - Main Document class
- `scripts/unpack.py` - Unpack .docx to XML
- `scripts/pack.py` - Pack XML to .docx
- `LICENSE.txt` - License terms

## Best Practices

1. **Read reference files completely** - Never skip sections or set range limits
2. **Batch changes logically** - Group 3-10 related changes per batch
3. **Test each batch** - Verify before moving to next batch
4. **Grep before scripting** - Always verify text location in XML
5. **Use minimal edits** - Only mark text that actually changes
6. **Preserve formatting** - Extract and reuse original `<w:rPr>` elements
7. **Validate output** - Convert to markdown and verify changes
8. **Follow patterns** - Use established patterns from reference files

## Code Style

When generating code for DOCX operations:
- Write concise code
- Avoid verbose variable names
- Avoid unnecessary print statements
- Focus on clarity and brevity

## License

See LICENSE.txt for complete license terms.
