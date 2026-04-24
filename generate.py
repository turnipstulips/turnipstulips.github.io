import os
import json
from datetime import datetime

# Config
VIDEO_FOLDER = "videos"
OUTPUT_FILE = "index.html"

def get_video_info(video_path):
    """Get file size, modified date, and name for a video"""
    stat = os.stat(video_path)
    size_bytes = stat.st_size
    size_mb = size_bytes / (1024 * 1024)
    modified_timestamp = stat.st_mtime
    modified_date = datetime.fromtimestamp(modified_timestamp).strftime("%Y-%m-%d / %H:%M:%S")
    filename = os.path.basename(video_path)
    return {
        "filename": filename,
        "size_mb": round(size_mb, 1),
        "date": modified_date,
        "path": f"{VIDEO_FOLDER}/{filename}"
    }

def generate_html(videos):
    """Generate the index.html file from video list"""
    
    # Build the video grid HTML
    video_items = []
    for video in videos:
        item = f'''  <div class="liveleak-item">
    <div class="timestamp">{video["date"]}</div>
    <video controls preload="metadata">
      <source src="{video["path"]}" type="video/mp4">
    </video>
    <div class="filename">{video["filename"]} | {video["size_mb"]}MB</div>
  </div>'''
        video_items.append(item)
    
    videos_html = "\n".join(video_items)
    
    # The full HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LIVE_ARCHIVE / UNEDITED / RAW</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="nav-wiki">
  <a href="index.html">HOME</a> | 
  <a href="directory.html">RAW_DIRECTORY</a> | 
  <a href="logs.html">LOGS</a> | 
  <a href="about.html">ABOUT_</a>
</div>

<div class="yzy-block">
  <div class="yzy-text">FILM_<br>DESIGN_<br>ARCHIVE_<br>2026</div>
  <div class="yzy-sub">UNEDITED. UNCOMPRESSED. UNFILTERED.</div>
</div>

<div class="liveleak-grid">
{videos_html}
</div>

<div class="wiki-section">
  <div class="wiki-header">Recent activity / changes</div>
  
  <div class="wiki-entry">
    <div class="wiki-date">{datetime.now().strftime("%Y-%m-%d")}</div>
    <div class="wiki-content">
      <strong>Auto-generated page</strong> — Scanned {len(videos)} video files. 
      <a href="directory.html">[view raw directory]</a> — <span class="wiki-contrib">generated: {datetime.now().strftime("%H:%M:%S")}</span>
    </div>
  </div>
</div>

<div class="arena-grid">
  <div class="arena-item"><a href="videos/">📁 /videos/</a></div>
  <div class="arena-item"><a href="logs/">📁 /logs/</a></div>
  <div class="arena-item"><a href="assets/">📁 /assets/</a></div>
  <div class="arena-item arena-file">README.txt (auto)</div>
  <div class="arena-item arena-file">manifest.md (auto)</div>
</div>

<div class="liveleak-footer">
  <span>AUTO-GENERATED — {len(videos)} video files — last scan: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
</div>

</body>
</html>'''
    
    return html_content

def generate_directory_html(videos):
    """Generate the raw directory listing page"""
    
    table_rows = []
    # Parent directory link
    table_rows.append('''  <tr>
    <td><a href="../">../</a></td>
    <td class="size">-</td>
    <td>-</td>
  </tr>''')
    
    # Videos folder
    table_rows.append('''  <tr>
    <td><a href="videos/">videos/</a></td>
    <td class="size">-</td>
    <td>-</td>
  </tr>''')
    
    # Each video file
    for video in videos:
        row = f'''  <tr>
    <td><a href="{video["path"]}">{video["filename"]}</a></td>
    <td class="size">{video["size_mb"]}MB</td>
    <td>{video["date"]}</td>
  </tr>'''
        table_rows.append(row)
    
    table_html = "\n".join(table_rows)
    
    total_size = sum(v["size_mb"] for v in videos)
    
    dir_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Index of /archive/</title>
  <style>
    body {{
      font-family: 'Courier New', monospace;
      font-size: 13px;
      background: white;
      color: black;
      margin: 20px;
    }}
    a {{
      color: blue;
      text-decoration: underline;
    }}
    a:visited {{
      color: purple;
    }}
    hr {{
      border: none;
      border-top: 1px solid #ccc;
    }}
    .dir-table {{
      border-collapse: collapse;
    }}
    .dir-table td {{
      padding: 2px 20px 2px 0;
    }}
    .size {{
      text-align: right;
      color: #666;
    }}
  </style>
</head>
<body>

<h1>Index of /archive/</h1>
<hr>

<table class="dir-table">
  <tr>
    <th>Name</th>
    <th>Size</th>
    <th>Last modified</th>
  </tr>
{table_html}
</table>

<hr>
<pre>
[DIRECTORY LISTING GENERATED] — {len(videos)} video files — {round(total_size, 1)}MB total
</pre>

</body>
</html>'''
    
    return dir_html

def main():
    # Get all video files from the videos folder
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)
        print(f"Created {VIDEO_FOLDER}/ folder. Add some videos and run again.")
        return
    
    video_files = []
    for file in os.listdir(VIDEO_FOLDER):
        if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            file_path = os.path.join(VIDEO_FOLDER, file)
            video_files.append(get_video_info(file_path))
    
    # Sort by date (newest first)
    video_files.sort(key=lambda x: x["date"], reverse=True)
    
    # Generate and save index.html
    index_html = generate_html(video_files)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(index_html)
    
    # Generate and save directory.html
    dir_html = generate_directory_html(video_files)
    with open("directory.html", "w", encoding="utf-8") as f:
        f.write(dir_html)
    
    print(f"✅ Generated index.html and directory.html")
    print(f"📹 Found {len(video_files)} video files")
    print(f"💾 Total size: {sum(v['size_mb'] for v in video_files):.1f}MB")
    print(f"\n➡️  Open index.html in your browser")

if __name__ == "__main__":
    main()