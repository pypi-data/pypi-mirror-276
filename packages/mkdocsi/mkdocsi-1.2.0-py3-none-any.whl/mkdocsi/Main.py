import sys  , os 
from mkdocsi import generate_site

def main():
    docs_folder = os.path.join(os.getcwd() , "docs")
    Template_mkdocs   = None
    site_name = os.path.dirname(os.getcwd())
    generate_site(docs_folder = docs_folder , Template_mkdocs = Template_mkdocs , site_name = site_name )

if __name__ == "__main__":
    main()
