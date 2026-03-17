#!/usr/bin/env python3
"""Convert markdown deliverables to styled HTML pages for GitHub Pages."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / "public"

NAV = """<nav>
  <div class="inner">
    <span class="brand">Kit's Take-Home Submission</span>
    <div class="links">
      <a href="./">Demo</a>
      <a href="blog.html">Blog</a>
      <a href="video.html">Video</a>
      <a href="social.html">Social</a>
      <a href="campaign.html">Campaign</a>
      <a href="process.html">Process</a>
      <a href="https://github.com/KitTheRevenueCat/revenuecat-growth-brief">Repo</a>
    </div>
  </div>
</nav>"""

STYLE = """<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #09090b; color: #fafafa; font-family: system-ui, -apple-system, sans-serif; line-height: 1.7; }
nav { position: sticky; top: 0; z-index: 50; border-bottom: 1px solid #27272a; background: rgba(9,9,11,0.9); backdrop-filter: blur(8px); }
nav .inner { max-width: 800px; margin: 0 auto; padding: 0.75rem 1.5rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; }
nav .brand { font-size: 0.875rem; font-weight: 600; color: #2dd4bf; }
nav .links { display: flex; gap: 0.75rem; font-size: 0.8rem; flex-wrap: wrap; }
nav .links a { color: #a1a1aa; text-decoration: none; transition: color 0.15s; }
@media (max-width: 640px) {
  nav .inner { flex-direction: column; align-items: flex-start; gap: 0.5rem; }
  nav .links { gap: 0.6rem; }
  h1 { font-size: 1.5rem; }
  h2 { font-size: 1.25rem; }
  .container { padding: 2rem 1rem; }
}
nav .links a:hover { color: #2dd4bf; }
.container { max-width: 800px; margin: 0 auto; padding: 3rem 1.5rem; }
h1 { font-size: 2rem; font-weight: 700; line-height: 1.3; margin-bottom: 1.5rem; }
h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2.5rem; margin-bottom: 1rem; color: #fafafa; border-bottom: 1px solid #27272a; padding-bottom: 0.5rem; }
h3 { font-size: 1.15rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
h4 { font-size: 1rem; font-weight: 600; margin-top: 1.25rem; margin-bottom: 0.4rem; color: #d4d4d8; }
p { margin-bottom: 1rem; color: #d4d4d8; }
a { color: #2dd4bf; text-decoration: none; }
a:hover { text-decoration: underline; }
blockquote { border-left: 3px solid #2dd4bf; padding: 1rem 1.5rem; margin: 1.5rem 0; background: rgba(45,212,191,0.05); border-radius: 0 8px 8px 0; }
code { background: #18181b; padding: 0.15em 0.4em; border-radius: 4px; font-size: 0.9em; color: #2dd4bf; }
pre { background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 1.25rem; overflow-x: auto; margin: 1rem 0 1.5rem; }
pre code { background: none; padding: 0; color: #e4e4e7; }
ul, ol { margin: 0.5rem 0 1rem 1.5rem; color: #d4d4d8; }
li { margin-bottom: 0.35rem; }
table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
th, td { border: 1px solid #27272a; padding: 0.6rem 0.8rem; text-align: left; font-size: 0.9rem; }
th { background: #18181b; color: #fafafa; font-weight: 600; }
td { color: #d4d4d8; }
hr { border: none; border-top: 1px solid #27272a; margin: 2rem 0; }
strong { color: #fafafa; }
em { color: #a1a1aa; }
img { width: 100%; max-width: 100%; border-radius: 8px; margin: 1rem 0; display: block; }
.label { color: #2dd4bf; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.5rem; }
</style>"""


def md_to_html(md_text):
    """Very simple markdown to HTML converter for our deliverables."""
    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    in_ol = False
    in_code = False
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        
        # Code blocks
        if stripped.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = stripped[3:].strip()
                html_lines.append(f"<pre><code>")
                in_code = True
            continue
        
        if in_code:
            html_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue
        
        # Close lists if needed
        if in_list and not stripped.startswith("- ") and not stripped.startswith("* "):
            html_lines.append("</ul>")
            in_list = False
        if in_ol and not re.match(r"^\d+\.", stripped):
            html_lines.append("</ol>")
            in_ol = False
        
        # Table
        if stripped.startswith("|") and not in_table:
            in_table = True
            html_lines.append("<table>")
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            html_lines.append("<tr>" + "".join(f"<th>{inline_md(c)}</th>" for c in cells) + "</tr>")
            continue
        elif in_table and stripped.startswith("|"):
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                continue  # separator row
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            html_lines.append("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in cells) + "</tr>")
            continue
        elif in_table and not stripped.startswith("|"):
            html_lines.append("</table>")
            in_table = False
        
        # Headers
        if stripped.startswith("#### "):
            html_lines.append(f"<h4>{inline_md(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{inline_md(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{inline_md(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html_lines.append(f"<h1>{inline_md(stripped[2:])}</h1>")
        elif stripped.startswith("---"):
            html_lines.append("<hr>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{inline_md(stripped[2:])}</li>")
        elif re.match(r"^\d+\.\s", stripped):
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            text = re.sub(r"^\d+\.\s*", "", stripped)
            html_lines.append(f"<li>{inline_md(text)}</li>")
        elif stripped.startswith("> "):
            html_lines.append(f"<blockquote><p>{inline_md(stripped[2:])}</p></blockquote>")
        elif stripped == "":
            pass
        else:
            html_lines.append(f"<p>{inline_md(stripped)}</p>")
    
    if in_list:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")
    if in_table:
        html_lines.append("</table>")
    if in_code:
        html_lines.append("</code></pre>")
    
    return "\n".join(html_lines)


def inline_md(text):
    """Handle inline markdown: bold, italic, code, links, images."""
    # Images
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def build_page(title, label, md_file, out_file):
    md_text = (ROOT / md_file).read_text()
    body = md_to_html(md_text)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {STYLE}
</head>
<body>
  {NAV}
  <div class="container">
    <p class="label">{label}</p>
    {body}
  </div>
</body>
</html>"""
    
    (PUBLIC / out_file).write_text(html)
    print(f"  ✅ {out_file}")


if __name__ == "__main__":
    print("Building deliverable pages...\n")
    build_page("Social Posts — RevenueCat Growth Brief", "Social Launch Pack", "SOCIAL_POSTS.md", "social.html")
    build_page("Growth Campaign — RevenueCat Growth Brief", "Growth Campaign Report", "GROWTH_CAMPAIGN.md", "campaign.html")
    build_page("Process Log — RevenueCat Growth Brief", "Process Log", "PROCESS_LOG.md", "process.html")
    print("\nDone.")
