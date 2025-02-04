import os
from docx import Document
import requests
from urllib.parse import urlparse
from tqdm import tqdm

def extract_pdf_links(docx_path):
    """Extract all links from the DOCX file."""
    document = Document(docx_path)
    links = []
    
    # Method 1: Extract links from relationships
    rels = document.part.rels
    for rel in rels:
        if rels[rel].reltype == 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink':
            links.append(rels[rel]._target)
    
    # Method 2: Extract from paragraphs
    for paragraph in document.paragraphs:
        # Get the paragraph XML
        xml = paragraph._p.xml
        # Look for hyperlinks
        if '<w:hyperlink' in xml:
            # Parse the XML to get the relationship ID
            import re
            rel_ids = re.findall(r'r:id="(.*?)"', xml)
            for rel_id in rel_ids:
                if rel_id in document.part.rels:
                    url = document.part.rels[rel_id]._target
                    links.append(url)
    
    # Remove duplicates while preserving order
    links = list(dict.fromkeys(links))
    
    # Print all found links
    print("\nFound links in document:")
    print("-" * 50)
    if links:
        for i, url in enumerate(links, 1):
            print(f"{i}. {url}")
    else:
        print("No links found!")
    print("-" * 50)
    
    return links

def download_pdf(url, output_dir):
    """Download a file from the given URL."""
    try:
        # Get filename from URL
        filename = os.path.basename(urlparse(url).path)
        if not filename:  # If no filename in URL, use the last part of the path
            filename = url.split('/')[-1]
        if not filename:  # If still no filename, use the full URL hash
            import hashlib
            filename = hashlib.md5(url.encode()).hexdigest()
            
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nCreated output directory: {os.path.abspath(output_dir)}")
        
        # Full path for saving the file
        output_path = os.path.join(output_dir, filename)
        
        # Download the file with progress bar
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get content type and update filename if needed
        content_type = response.headers.get('content-type', '')
        if 'pdf' in content_type.lower() and not filename.lower().endswith('.pdf'):
            filename += '.pdf'
            output_path = os.path.join(output_dir, filename)
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
                
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def list_folder_contents(folder_path):
    """List all files in the folder."""
    print("\nFiles in the same folder:")
    print("-" * 50)
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path) / (1024 * 1024)  # Convert to MB
            print(f"{item:<40} {size:.2f} MB")
    print("-" * 50)

def main():
    # Input DOCX file path
    docx_path = input("Enter the path to your DOCX file: ")
    
    # List files in the same folder as the DOCX file
    folder_path = os.path.dirname(os.path.abspath(docx_path))
    list_folder_contents(folder_path)
    
    # Output directory for PDFs
    output_dir = input("Enter the output directory for PDFs (default: 'downloaded_pdfs'): ").strip()
    if not output_dir:
        output_dir = 'downloaded_pdfs'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nOutput directory: {os.path.abspath(output_dir)}")
    
    # Extract PDF links
    print("\nExtracting PDF links...")
    links = extract_pdf_links(docx_path)
    
    if not links:
        print("No links found in the document.")
        return
    
    print(f"Found {len(links)} links.")
    
    # Download PDFs
    successful_downloads = 0
    for url in links:
        print(f"\nDownloading: {url}")
        if download_pdf(url, output_dir):
            successful_downloads += 1
    
    print(f"\nDownload complete! Successfully downloaded {successful_downloads} out of {len(links)} links.")

if __name__ == "__main__":
    main() 