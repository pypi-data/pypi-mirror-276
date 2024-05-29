import sys  , os 
from mkdocsi import generate_site

def main():
    docs = os.path.join(os.getcwd(),"docs")
    generate_site(docs)

if __name__ == "__main__":
    main()
