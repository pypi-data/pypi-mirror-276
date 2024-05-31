from cuminai.constants import (
    _LINK_KIND,
    _TEXT_KIND,
)

import cuminai.validator as validator
from pathlib import Path  

def isValidKnowledgeSource(source_details, kind):
    if kind == _LINK_KIND:
        return validator.LinkValidator.match(source_details.source)
    
    if kind == _TEXT_KIND:
        return validator.TextFileValidator.match(source_details.source)
    
    return False

def get_processed_tag(tag):
    return tag.lower().replace("-","_").replace(" ", "_")

def num_found(page_content, tag):
    return page_content.lower().count(tag)

def get_file_name(path):
    return Path(path).name