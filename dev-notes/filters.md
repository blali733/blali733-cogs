## Original json state:
4 independent *filters.json* files, containing dictionaries in form:
* list of server id's
* default

Each dictionary element is list of applied filters as strings.

## Desired json state:
1 *filters.json* file, containing dictionary in form:
* list of server id's
* default

Each dictionary element contains tuple of list of applied
filters as strings.
## File array list:
0. lolibooru
0. danbooru
0. gelbooru
0. konachan