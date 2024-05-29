import yaml  , os , json , sys , argparse
from glob import glob 

DEFAULT_MKDOCS = """
markdown_extensions:
- attr_list
- md_in_html
- pymdownx.superfences
- pymdownx.highlight:
    anchor_linenums: true
    line_spans: __span
    linenums: true
    pygments_lang_class: true
- pymdownx.inlinehilite
- pymdownx.snippets
- pymdownx.superfences


plugins:
- tags:
    listings_map:
      scoped:
        scope: true
    tags_file: Tags.md
    listings_sort_by: "!!python/name:material.plugins.tags.item_url"
    listings_sort_reverse: true
- search:
    pipeline:
    - stemmer
    - stopWordFilter
    - trimmer
site_name: Genrated Docs
theme:
  features:
  - search.share
  - content.code.copy
  - content.code.select
  name: material
  palette:
  - scheme: slate
    toggle:
      icon: material/brightness-4
      name: Switch to light mode

"""

class MkdocsUtils : 
    def __init__(self , docs_folder  ,  Template_mkdocs   = None , site_name = None ) : 
        self.site_name = site_name 
        if Template_mkdocs is not None : 
            self.Template_mkdocs = Template_mkdocs 
        else  : 
            self.Template_mkdocs = DEFAULT_MKDOCS 
        self.docs_folder = os.path.abspath(docs_folder)  
        self.new_mkdocsfile = os.path.join(self.docs_folder ,"..", "mkdocs.yml")
        self.mkdocs_data = yaml.safe_load(self.Template_mkdocs)
        if not ('nav' in self.mkdocs_data.keys()) : self.mkdocs_data['nav'] = list()



    def make_safe(self) : 
        if self.site_name is not None  : 
            self.mkdocs_data['site_name'] = self.site_name 
        Tags_md = os.path.join(self.docs_folder , "Tags.md")
        if not os.path.exists(Tags_md) : 
            print("<!-- material/tags { scope: true } -->" , file = open(Tags_md , "w"))
            self.mkdocs_data['nav'].append({"Tags" : "Tags.md"})


    def __repr__(self) : 
        return json.dumps(self.mkdocs_data , indent = 4 )

    def buildTree(self) : 
        self.make_safe()
        self.mkdocs_data['nav'].extend(self.get_md_files_tree())
        with open(self.new_mkdocsfile, 'w') as file:                                                                                                                                                       
            yaml.dump(self.mkdocs_data, file, default_flow_style=False)       
                                                                                                                                                                                          
    def to_camel_case(self , snake_str):                                                                                                                                                                  
        components = snake_str.split('_')                                                                                                                                                     
        return " ".join(components)                                                                                                                       
                                                                                                                                                                                                
    def get_md_files_tree(self):                                                                                                                                                            
        def walk_dir(folder, parent_path=''):                                                                                                                                                      
            tree = []                                                                                                                                                                              
            for item in sorted(os.listdir(folder)):                                                                                                                                                
                path = os.path.join(folder, item)                                                                                                                                             
                relative_path = os.path.join(parent_path, item)
                if os.path.isdir(path):  
                    # path = os.path.relpath(path, self.docs_folder)                                                                                                                                                         
                    subtree = walk_dir(path, relative_path)                                                                                                                                        
                    if subtree:  # Only include non-empty directories                                                                                                                              
                        tree.append({item: subtree})                                                                                                                                               
                elif item.endswith('.md'):                                                                                                                                                         
                    base_name = os.path.splitext(item)[0]                                                                                                                                          
                    camel_case_name = self.to_camel_case(base_name)                                                                                                                                     
                    tree.append({camel_case_name: relative_path})                                                                                                                                  
            return tree                                                                                                                                                                            
                                                                                                                                                                                                
        return walk_dir(self.docs_folder)   









def __ENTRY__POINT__():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index',  type = str , default= None  , required = False )
    parser.add_argument('--docs',  type = str , default= os.path.join(os.getcwd() , "docs")  , required = False )
    parser.add_argument('--mkdocs', type = str , default= None   , required = False )
    parser.add_argument('--site_name',  type = str , default= os.path.basename(os.getcwd())   , required = False)

    args = parser.parse_args()
    Template_mkdocs = DEFAULT_MKDOCS
    if args.mkdocs is not None  : 
        with open(args.mkdocs) as buff  : 
            Template_mkdocs = buff.read()

    if args.index is not None  : 
        with open(args.index,"r") as buff : 
            print(buff.read() , file = open(os.path.join(args.docs ,"index.md"),"w"))

    _MkdocsUtils = MkdocsUtils(docs_folder = args.docs  , Template_mkdocs = Template_mkdocs  ,site_name = args.site_name)
    _MkdocsUtils.buildTree()