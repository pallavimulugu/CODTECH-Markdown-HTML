import re


def convert_inline(text):
    # Convert bold text
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    # Convert italic text
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)

    # Convert inline code
    text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)

    # Convert links
    text = re.sub(
        r"\[(.*?)\]\((.*?)\)",
        r'<a href="\2">\1</a>',
        text
    )

    return text


def markdown_to_html(markdown_text):
    lines = markdown_text.splitlines()
    html = []

    in_code_block = False
    in_unordered_list = False
    in_ordered_list = False

    for line in lines:

        # Code block
        if line.startswith("```"):
            if not in_code_block:
                html.append("<pre><code>")
                in_code_block = True
            else:
                html.append("</code></pre>")
                in_code_block = False
            continue

        if in_code_block:
            html.append(line)
            continue

        # Close unordered list
        if not line.startswith("- ") and in_unordered_list:
            html.append("</ul>")
            in_unordered_list = False

        # Close ordered list
        if not re.match(r"^\d+\.\s", line) and in_ordered_list:
            html.append("</ol>")
            in_ordered_list = False

        # Headings
        if line.startswith("### "):
            html.append(f"<h3>{convert_inline(line[4:])}</h3>")

        elif line.startswith("## "):
            html.append(f"<h2>{convert_inline(line[3:])}</h2>")

        elif line.startswith("# "):
            html.append(f"<h1>{convert_inline(line[2:])}</h1>")

        # Unordered list
        elif line.startswith("- "):
            if not in_unordered_list:
                html.append("<ul>")
                in_unordered_list = True

            html.append(f"<li>{convert_inline(line[2:])}</li>")

        # Ordered list
        elif re.match(r"^\d+\.\s", line):
            if not in_ordered_list:
                html.append("<ol>")
                in_ordered_list = True

            item = re.sub(r"^\d+\.\s", "", line)
            html.append(f"<li>{convert_inline(item)}</li>")

        # Empty line
        elif line.strip() == "":
            continue

        # Paragraph
        else:
            html.append(f"<p>{convert_inline(line)}</p>")

    # Close lists if still open
    if in_unordered_list:
        html.append("</ul>")

    if in_ordered_list:
        html.append("</ol>")

    return "\n".join(html)


def create_html_document(body):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Converted Page</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            color: #333;
            max-width: 900px;
            margin: 40px auto;
            padding: 30px;
        }}

        .container {{
            background: white;
            padding: 35px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            color: #2563eb;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
        }}

        h2 {{
            color: #7c3aed;
            margin-top: 30px;
        }}

        h3 {{
            color: #0891b2;
        }}

        p {{
            line-height: 1.7;
        }}

        strong {{
            color: #dc2626;
        }}

        em {{
            color: #059669;
        }}

        ul, ol {{
            padding-left: 30px;
            line-height: 1.8;
        }}

        li {{
            margin-bottom: 5px;
        }}

        a {{
            color: #2563eb;
            text-decoration: none;
            font-weight: bold;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        code {{
            background: #eef2ff;
            color: #7c3aed;
            padding: 4px 7px;
            border-radius: 5px;
            font-family: Consolas, monospace;
        }}

        pre {{
            background: #1e293b;
            color: white;
            padding: 18px;
            border-radius: 8px;
            overflow-x: auto;
        }}
    </style>
</head>

<body>
    <div class="container">
        {body}
    </div>
</body>
</html>
"""


def main():
    print("=" * 50)
    print("       MARKDOWN TO HTML CONVERTER")
    print("=" * 50)

    while True:
        print("\n1. Convert Markdown File")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")

        if choice == "1":
            filename = input("Enter Markdown file name: ").strip()

            try:
                with open(filename, "r", encoding="utf-8") as file:
                    markdown_text = file.read()

                html_body = markdown_to_html(markdown_text)
                html_document = create_html_document(html_body)

                with open("output.html", "w", encoding="utf-8") as file:
                    file.write(html_document)

                print("\nMarkdown converted successfully!")
                print("HTML file created: output.html")

            except FileNotFoundError:
                print("\nFile not found!")
                print("Please check the Markdown file name.")

            except PermissionError:
                print("\nPermission denied!")
                print("Unable to access the file.")

            except Exception as error:
                print("\nSomething went wrong.")
                print(f"Error: {error}")

        elif choice == "2":
            print("\nThank you for using Markdown to HTML Converter!")
            break

        else:
            print("\nInvalid choice! Please select 1 or 2.")


if __name__ == "__main__":
    main()