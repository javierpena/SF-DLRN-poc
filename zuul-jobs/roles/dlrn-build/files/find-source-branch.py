from __future__ import print_function
import rdoinfo
import sys

MASTER_TAG='queens-uc'

def find_source_branch(package, tag):
    info = rdoinfo.parse_info_file('/tmp/rdoinfo/rdo.yml', include_fns=[])

    for pkg in info['packages']:
        if pkg['name'] == package:
            # If the package is under review, always return the rpm-master branch
            if 'under-review' in pkg['tags']:
                return 'master'

            for key in pkg['tags']:
                if key == tag:   
                    if pkg['tags'][key] is not None:
                        # We have a specific source branch defined. Use it
                        if 'source-branch' in pkg['tags'][key]:
                            return pkg['tags'][key]['source-branch']
                    # Any other case, lets derive it from the tag name
                    if tag == MASTER_TAG:
                        return 'master'
                    else:
                        return "stable/%s" % tag
    return None

if __name__ == '__main__':
    branch = find_source_branch(sys.argv[1], sys.argv[2])
    print(branch)
