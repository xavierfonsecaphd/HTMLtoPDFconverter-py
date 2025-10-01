#!/usr/bin/env python3
"""Convert HTML to PDF with clickable links and SVG support"""

import pdfkit
import os
import sys
import re
from pathlib import Path

def convert_svg_to_png(svg_path, png_path, width=1200):
    """Convert SVG to PNG using svglib or inkscape"""
    # Try svglib first (pure Python, works on Windows)
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt='PNG')
        print(f"  ✓ Converted {svg_path} to {png_path}")
        return True
    except ImportError:
        print("  ⚠ svglib not installed. Trying inkscape...")
        return convert_svg_with_inkscape(svg_path, png_path)
    except Exception as e:
        print(f"  ⚠ svglib failed: {e}. Trying inkscape...")
        return convert_svg_with_inkscape(svg_path, png_path)

def convert_svg_with_inkscape(svg_path, png_path):
    """Convert SVG to PNG using Inkscape"""
    import subprocess
    
    # Try to find Inkscape
    inkscape_paths = [
        r'C:\Program Files\Inkscape\bin\inkscape.exe',
        r'C:\Program Files (x86)\Inkscape\bin\inkscape.exe',
        'inkscape'  # If in PATH
    ]
    
    inkscape_exe = None
    for path in inkscape_paths:
        if os.path.exists(path) or path == 'inkscape':
            inkscape_exe = path
            break
    
    if not inkscape_exe:
        print("  ✗ Neither cairosvg nor Inkscape found!")
        print("  Install one of:")
        print("    pip install cairosvg")
        print("    OR download Inkscape from: https://inkscape.org/")
        return False
    
    try:
        subprocess.run([
            inkscape_exe,
            svg_path,
            '--export-type=png',
            f'--export-filename={png_path}',
            '--export-width=1200'
        ], check=True, capture_output=True)
        print(f"  ✓ Converted {svg_path} to {png_path} (using Inkscape)")
        return True
    except Exception as e:
        print(f"  ✗ Inkscape conversion failed: {e}")
        return False

def process_html_for_pdf(html_file, temp_html_file):
    """Process HTML: convert SVG references to PNG"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find all SVG image references
    svg_pattern = r'src="([^"]+\.svg)"'
    svg_matches = re.findall(svg_pattern, html_content)
    
    if svg_matches:
        print(f"\nFound {len(svg_matches)} SVG file(s) to convert:")
        
        for svg_path in svg_matches:
            print(f"  Processing: {svg_path}")
            
            # Create PNG path
            png_path = svg_path.replace('.svg', '.png')
            
            # Convert SVG to PNG
            if os.path.exists(svg_path):
                if convert_svg_to_png(svg_path, png_path):
                    # Replace SVG reference with PNG in HTML
                    html_content = html_content.replace(
                        f'src="{svg_path}"',
                        f'src="{png_path}"'
                    )
                else:
                    print(f"  ⚠ Keeping SVG reference (conversion failed)")
            else:
                print(f"  ⚠ File not found: {svg_path}")
    
    # Write processed HTML to temp file
    with open(temp_html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return temp_html_file

def html_to_pdf(html_file='Pagina.html', output_file='README.pdf'):
    """
    Convert HTML file to PDF with clickable hyperlinks
    
    Args:
        html_file: Path to HTML file (default: Pagina.html)
        output_file: Path to output PDF (default: README.pdf)
    """
    
    # Check if HTML file exists
    if not os.path.exists(html_file):
        print(f"Error: File '{html_file}' not found!")
        sys.exit(1)
    
    # Path to wkhtmltopdf executable
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    
    # Check if wkhtmltopdf is installed
    if not os.path.exists(wkhtmltopdf_path):
        print("Error: wkhtmltopdf not found!")
        print(f"Expected location: {wkhtmltopdf_path}")
        print("\nPlease install wkhtmltopdf from:")
        print("https://wkhtmltopdf.org/downloads.html")
        sys.exit(1)
    
    print(f"Converting {html_file} to PDF...")
    
    # Process HTML: convert SVG to PNG
    temp_html = 'temp_for_pdf.html'
    processed_html = process_html_for_pdf(html_file, temp_html)
    
    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    # Get absolute path for proper image resolution
    html_abs_path = os.path.abspath(processed_html)
    
    # PDF generation options
    options = {
        'enable-local-file-access': None,
        'encoding': 'UTF-8',
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'print-media-type': None,
        'enable-internal-links': None,
        'enable-external-links': None,  # Clickable links!
    }
    
    try:
        # Convert HTML to PDF
        pdfkit.from_file(
            html_abs_path,
            output_file,
            configuration=config,
            options=options
        )
        
        print(f"\n✓ PDF created successfully: {output_file}")
        print(f"✓ All hyperlinks are clickable in the PDF!")
        
        # Check file size
        file_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"  File size: {file_size:.2f} MB")
        
        # Clean up temp file
        if os.path.exists(temp_html):
            os.remove(temp_html)
            
    except Exception as e:
        print(f"\nError during conversion: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Get file names from command line or use defaults
    html_file = sys.argv[1] if len(sys.argv) > 1 else 'Pagina.html'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'README.pdf'
    
    html_to_pdf(html_file, output_file)