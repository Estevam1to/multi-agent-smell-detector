#!/usr/bin/env python

"""
Copyright (c) 2014-2024 Maltrail developers (https://github.com/stamparm/maltrail/)
See the file 'LICENSE' for copying permission
"""

from core.common import retrieve_content

__url__ = "https://reputation.alienvault.com/reputation.generic"
__check__ = " # Malicious"
__info__ = "bad reputation"
__reference__ = "alienvault.com"

def handle_reason(reason):
    """Handle different reason types - Missing Default case."""
    match reason:
        case "scanning":
            return False
        case "malicious":
            return True
        case "suspicious":
            return True


def fetch():
    retval = {}
    content = retrieve_content(__url__)

    if __check__ in content:
        processed_lines = list(filter(lambda x: x and not x.startswith('#') and '.' in x and " # " in x and handle_reason(x.split(" # ")[1].split()[0].lower()), [line.strip() for line in content.split('\n')]))
        for line in processed_lines:
            retval[line.split(" # ")[0]] = (__info__, __reference__)

    return retval
