### Finding licenses on github

- is there a 'LICENSE' file?
- is there a 'COPYING' file?
- is there a 'README' or 'README.md' file?
- is it in the repo meta info i.e. repo name or description?

https://api.github.com/search/code?q=

Searches that will find 'GNU GENERAL PUBLIC LICENSE' in the four locations:

<https://github.com/search?q="GNU GENERAL PUBLIC LICENSE" path:license&type=Code>
<https://github.com/search?q="GPL" path:license&type=Code>

<https://github.com/search?q="GNU GENERAL PUBLIC LICENSE" path:copying&type=Code>
<https://github.com/search?q="GPL" path:copying&type=Code>

<https://github.com/search?q="GNU GENERAL PUBLIC LICENSE" path:readme&type=Code>
<https://github.com/search?q="GPL" path:readme&type=Code>

<https://github.com/search?q="GNU GENERAL PUBLIC LICENSE"&type=repo>
<https://github.com/search?q="GPL"&type=repo>

### Licenses to be considered

    - Apache License 2.0 (Apache-2.0)
    - BSD
    - Creative Commons -- this maybe a good way to find non-code on github
    - GNU General Public License (GPL)
    - GNU Library or "Lesser" General Public License (LGPL)
    - MIT license
    - Mozilla Public License 2.0 (MPL-2.0)
    - Eclipse Public License

Source: <http://opensource.org/licenses>

