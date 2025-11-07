#!/usr/bin/env python3
import os
import re

def get_persian_ordinal(num):
    """Convert number to Persian ordinal"""
    persian_ordinals = {
        1: 'اول',
        2: 'دوم',
        3: 'سوم',
        4: 'چهارم',
        5: 'پنجم',
        6: 'ششم',
        7: 'هفتم',
        8: 'هشتم',
        9: 'نهم',
        10: 'دهم',
        11: 'یازدهم',
        12: 'دوازدهم',
        13: 'سیزدهم',
        14: 'چهاردهم',
        15: 'پانزدهم',
        16: 'شانزدهم',
        17: 'هفدهم',
        18: 'هجدهم',
        19: 'نوزدهم',
        20: 'بیستم'
    }
    return persian_ordinals.get(num, f'{num}')

def get_directories():
    """Scan for directories that contain index.html files"""
    directories = []

    # Get all items in the current directory
    # Sort numerically for digit-only names, alphabetically for others
    def sort_key(item):
        if item.isdigit():
            return (0, int(item))  # Numbers first, sorted numerically
        else:
            return (1, item)  # Then strings, sorted alphabetically

    for item in sorted(os.listdir('.'), key=sort_key):
        # Skip hidden files/folders and .github
        if item.startswith('.'):
            continue

        # Check if it's a directory
        if os.path.isdir(item):
            # Check if it has an index.html file
            index_path = os.path.join(item, 'index.html')
            if os.path.exists(index_path):
                # If it's a number, create Persian lesson name
                if item.isdigit():
                    lesson_num = int(item)
                    name = f'درس {get_persian_ordinal(lesson_num)}'
                else:
                    # For non-numeric directories, use the name as-is
                    name = item.replace('_', ' ').replace('-', ' ')

                directories.append({
                    'name': name,
                    'path': item
                })

    return directories

def generate_html(directories):
    """Generate the HTML content"""

    # Generate directory items for JavaScript
    dir_items = []
    for d in directories:
        dir_items.append(f"            {{ name: '{d['name']}', path: '{d['path']}' }}")

    directories_js = ',\n'.join(dir_items)

    html = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>فهرست دروس</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: Tahoma, 'Iranian Sans', 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }}

        header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}

        header p {{
            opacity: 0.9;
            font-size: 1rem;
        }}

        .directory-list {{
            padding: 2rem;
        }}

        .directory-item {{
            display: block;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            text-decoration: none;
            color: #495057;
            transition: all 0.3s ease;
            font-size: 1.2rem;
            font-weight: 500;
        }}

        .directory-item:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateX(-10px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}

        .directory-item::after {{
            content: "📁";
            margin-left: 1rem;
            font-size: 1.3rem;
        }}

        .directory-item:hover::after {{
            content: "📂";
        }}

        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: #6c757d;
        }}

        footer {{
            text-align: center;
            padding: 1.5rem;
            color: #6c757d;
            font-size: 0.9rem;
            border-top: 1px solid #e9ecef;
        }}

        .badge {{
            background: #667eea;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            margin-right: 0.5rem;
        }}

        @media (max-width: 600px) {{
            body {{
                padding: 1rem;
            }}

            header h1 {{
                font-size: 1.5rem;
            }}

            .directory-list {{
                padding: 1rem;
            }}

            .directory-item {{
                padding: 1rem;
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 فهرست دروس</h1>
            <p>یک درس را برای مشاهده انتخاب کنید</p>
        </header>

        <div class="directory-list" id="directoryList">
            <!-- Directories will be listed here -->
        </div>

        <footer>
            <p>تولید شده توسط <span class="badge">زینب محمودی فر</span></p>
        </footer>
    </div>

    <script>
        // Automatically generated directory list
        const directories = [
{directories_js}
        ];

        const directoryList = document.getElementById('directoryList');

        if (directories.length === 0) {{
            directoryList.innerHTML = `
                <div class="empty-state">
                    <p>هیچ درسی یافت نشد</p>
                </div>
            `;
        }} else {{
            directories.forEach(dir => {{
                const link = document.createElement('a');
                link.href = `${{dir.path}}/index.html`;
                link.className = 'directory-item';
                link.textContent = dir.name;
                directoryList.appendChild(link);
            }});
        }}
    </script>
</body>
</html>"""

    return html

def main():
    print("Scanning for directories with index.html...")
    directories = get_directories()

    print(f"Found {len(directories)} directories:")
    for d in directories:
        print(f"  - {d['name']} ({d['path']})")

    print("\nGenerating index.html...")
    html_content = generate_html(directories)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✓ index.html generated successfully!")

if __name__ == '__main__':
    main()
