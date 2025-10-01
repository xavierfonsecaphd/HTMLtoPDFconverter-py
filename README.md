# HTML to PDF Converter

Convert HTML files to PDF with **clickable hyperlinks** and **automatic SVG-to-PNG conversion**.

## Features

- ✓ Preserves clickable hyperlinks in the PDF
- ✓ Automatically converts SVG images to PNG for better PDF compatibility
- ✓ Maintains CSS styling and formatting
- ✓ Supports local images and resources
- ✓ Works on Windows with minimal setup

## Prerequisites

### 1. Python 3.7 or higher

Check if Python is installed:
```bash
python --version
```

If not installed, download from: https://www.python.org/downloads/

### 2. Required Python Packages

Install the following packages:

```bash
pip install pdfkit
```

Optional (for SVG conversion, but Inkscape is preferred):
```bash
pip install svglib reportlab
```

### 3. wkhtmltopdf

**Download and install wkhtmltopdf:**
- Visit: https://wkhtmltopdf.org/downloads.html
- Download: **Windows (MSVC 2015) 64-bit installer**
- Install to the default location: `C:\Program Files\wkhtmltopdf`

**Verify installation:**
After installation, check if the executable exists at:
```
C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
```

### 4. Inkscape (Required for SVG conversion)

**Download and install Inkscape:**
- Visit: https://inkscape.org/release/
- Download the latest Windows installer (`.msi` file)
- Example: `Inkscape-1.3.2_2023-11-25_091e20e-x64.msi`
- Install to the default location: `C:\Program Files\Inkscape`

**Direct download link:**
https://inkscape.org/release/inkscape-1.3.2/windows/64-bit/msi/

**Installation steps:**
1. Run the downloaded `.msi` installer
2. Accept the default installation path: `C:\Program Files\Inkscape`
3. Click through the installer (Next → Next → Install)
4. Wait for installation to complete (1-2 minutes)

**Verify installation:**
After installation, check if the executable exists at:
```
C:\Program Files\Inkscape\bin\inkscape.exe
```

## Installation

1. **Save the script** as `HTMLtoPDFconverter.py`

2. **Ensure all prerequisites are installed** (see above)

3. **Test the installation:**
```bash
python HTMLtoPDFconverter.py --help
```

## Usage

### Basic Usage

Convert an HTML file to PDF using default names:

```bash
python HTMLtoPDFconverter.py
```

This will:
- Look for `Pagina.html` in the current directory
- Create `README.pdf` as output

### Custom Input/Output

Specify custom HTML input and PDF output files:

```bash
python HTMLtoPDFconverter.py input.html output.pdf
```

### Examples

**Example 1: Convert documentation to PDF**
```bash
python HTMLtoPDFconverter.py documentation.html docs.pdf
```

**Example 2: Convert a report**
```bash
python HTMLtoPDFconverter.py quarterly-report.html Q3-2024-Report.pdf
```

**Example 3: Convert with images in subdirectories**
```bash
# Your HTML references images like: <img src="images/diagram.svg">
# The script will automatically convert SVGs and include all images
python HTMLtoPDFconverter.py report.html report.pdf
```

## How It Works

### SVG Conversion Process

The script automatically handles SVG images in your HTML:

1. **Scans** the HTML for any `<img src="*.svg">` references
2. **Converts** each SVG to PNG using Inkscape
3. **Updates** the HTML to reference the PNG files
4. **Generates** the PDF with all images properly embedded

**Example:**
```html
<!-- Original HTML -->
<img src="diagrams/flowchart.svg">

<!-- Automatically becomes -->
<img src="diagrams/flowchart.png">
```

The PNG files are saved alongside the original SVG files, so you'll have both versions.

### Link Preservation

All hyperlinks in the HTML are preserved as clickable links in the PDF:
- External links (https://example.com)
- Internal links (#section-anchor)
- Email links (mailto:user@example.com)

## File Structure

Make sure your files are organized correctly:

```
your-project/
├── HTMLtoPDFconverter.py
├── your-file.html
└── images/
    ├── diagram.svg
    ├── photo.png
    └── screenshot.jpg
```

The HTML file should be in the same directory where you run the script, or provide the full path.

## Troubleshooting

### Error: "wkhtmltopdf not found"

**Solution:**
- Install wkhtmltopdf from: https://wkhtmltopdf.org/downloads.html
- Ensure it's installed at: `C:\Program Files\wkhtmltopdf`
- If installed elsewhere, update line 120 in the script:
  ```python
  wkhtmltopdf_path = r'C:\Your\Custom\Path\wkhtmltopdf.exe'
  ```

### Error: "Inkscape conversion failed"

**Solution:**
- Install Inkscape from: https://inkscape.org/release/
- Ensure it's installed at: `C:\Program Files\Inkscape`
- Restart your terminal/command prompt after installation
- If installed elsewhere, update line 33 in the script to add your path

### SVG not converting

**Manual workaround:**
1. Open the SVG file in Chrome or Firefox
2. Right-click → "Save Page As..."
3. Save as PNG with the same name (e.g., `diagram.svg` → `diagram.png`)
4. Run the script again

### Images not appearing in PDF

**Cause:** Images must be accessible via relative or absolute paths.

**Solution:**
- Ensure image files exist at the paths specified in the HTML
- Use relative paths from the HTML file location
- Run the script from the same directory as the HTML file

### PDF file size is very large

**Causes:**
- High-resolution images
- Many SVG conversions (PNG files can be large)

**Solutions:**
- Compress images before converting to PDF
- Reduce SVG export width (edit line 56 in script): `'--export-width=800'`
- Use image optimization tools

## Advanced Configuration

### Customize PDF Margins

Edit the `options` dictionary in the script (lines 147-157):

```python
options = {
    'margin-top': '10mm',      # Change from 20mm to 10mm
    'margin-right': '15mm',    # Change from 20mm to 15mm
    'margin-bottom': '10mm',   # Change from 20mm to 10mm
    'margin-left': '15mm',     # Change from 20mm to 15mm
}
```

### Change Page Size

```python
options = {
    'page-size': 'Letter',  # Instead of 'A4'
    # Other options: 'Legal', 'A3', 'A5'
}
```

### Adjust SVG Resolution

Higher resolution = larger file size but better quality

Edit line 56 in the script:
```python
'--export-width=1200'  # Change to 800, 1600, 2400, etc.
```

## Output

### Success Message

```
Converting your-file.html to PDF...

Found 2 SVG file(s) to convert:
  Processing: images/diagram.svg
  ✓ Converted images/diagram.svg to images/diagram.png (using Inkscape)
  Processing: charts/graph.svg
  ✓ Converted charts/graph.svg to charts/graph.png (using Inkscape)

✓ PDF created successfully: output.pdf
✓ All hyperlinks are clickable in the PDF!
  File size: 1.23 MB
```

### Generated Files

After running the script, you'll have:
- **output.pdf** - The final PDF with clickable links
- **images/diagram.png** - Converted from SVG (kept alongside original)
- **temp_for_pdf.html** - Temporary file (automatically deleted)

## Command Line Arguments

```bash
python HTMLtoPDFconverter.py [HTML_FILE] [OUTPUT_PDF]
```

**Arguments:**
- `HTML_FILE` (optional) - Path to HTML file. Default: `Pagina.html`
- `OUTPUT_PDF` (optional) - Path to output PDF. Default: `README.pdf`

**Examples:**
```bash
# Use defaults
python HTMLtoPDFconverter.py

# Custom input only
python HTMLtoPDFconverter.py my-document.html

# Custom input and output
python HTMLtoPDFconverter.py my-document.html my-output.pdf

# With full paths
python HTMLtoPDFconverter.py C:\Users\User\Documents\file.html C:\Output\file.pdf
```

## Tips for Best Results

1. **Test your HTML first** - Open the HTML in a browser to ensure it looks correct
2. **Use relative paths** - For images and resources, use paths relative to the HTML file
3. **Optimize images** - Compress large images before conversion
4. **Check links** - Verify all hyperlinks work in the HTML before converting
5. **Keep files organized** - Maintain a clear directory structure for assets

## License

This script uses:
- **pdfkit** - MIT License
- **wkhtmltopdf** - LGPLv3 License
- **Inkscape** - GPL License

## Support

For issues with:
- **The script**: Check the troubleshooting section above
- **wkhtmltopdf**: Visit https://wkhtmltopdf.org/
- **Inkscape**: Visit https://inkscape.org/

## Version History

- **v1.0** - Initial release with SVG conversion support
  - Clickable hyperlinks preserved
  - Automatic SVG to PNG conversion
  - Support for local images and resources