from __future__ import print_function
import rdoinfo
import sys

MASTER_TAG='queens-uc'

def find_tags_for_source_branch(package, source_branch):
    info = rdoinfo.parse_info_file('/tmp/rdoinfo/rdo.yml', include_fns=[])
    tags = []

    for pkg in info['packages']:
        if pkg['name'] == package:
            # If the package is under review, always return the master tag
            if 'under-review' in pkg['tags']:
                return [MASTER_TAG]

            # A second possible case is that the source branch is either
            # master or stable/something. In that case, if the corresponding
            # tag value is None, add it
            if source_branch == 'master':
                if pkg['tags'][MASTER_TAG] == None:
                    tags.append(MASTER_TAG)                
            elif source_branch.startswith('stable/'):
                tag = source_branch.replace('stable/', '')
                if tag in pkg['tags']:
                    if pkg['tags'][tag] == None:
                        tags.append(tag)
            
            # Finally, let's check for all tags to find the source_branch
            for tag in pkg['tags']:
                if pkg['tags'][tag] is not None:
                    if 'source-branch' in pkg['tags'][tag]:
                       if pkg['tags'][tag]['source-branch'] == source_branch:
                            tags.append(tag)

    return tags

if __name__ == '__main__':
    tags = find_tags_for_source_branch(sys.argv[1], sys.argv[2])
    for tag in tags:
        print(tag)
