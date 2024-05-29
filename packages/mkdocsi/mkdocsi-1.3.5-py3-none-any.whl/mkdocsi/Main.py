import sys  , os , argparse
import mkdocsi 





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index',  type = str , default= None  , required = False )
    parser.add_argument('--docs',  type = str , default= os.path.join(os.getcwd() , "docs")  , required = False )
    parser.add_argument('--mkdocs', type = str , default= None   , required = False )
    parser.add_argument('--site_name',  type = str , default= os.path.basename(os.getcwd())   , required = False)

    args = parser.parse_args()
    Template_mkdocs = mkdocsi.DEFAULT_MKDOCS
    if args.mkdocs is not None  : 
        with open(args.mkdocs) as buff  : 
            Template_mkdocs = buff.read()

    if args.index is not None  : 
        with open(args.index,"r") as buff : 
            print(buff.read() , file = open(os.path.join(args.docs ,"index.md"),"w"))

    _MkdocsUtils = mkdocsi.MkdocsUtils(docs_folder = args.docs  , Template_mkdocs = Template_mkdocs  ,site_name = args.site_name 
    _MkdocsUtils.buildTree()

if __name__ == "__main__":
    main()
