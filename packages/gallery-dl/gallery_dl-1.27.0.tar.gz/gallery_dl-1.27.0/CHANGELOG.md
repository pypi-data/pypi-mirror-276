## 1.27.0 - 2024-06-01
### Extractors
#### Additions
- [mastodon] add `favorite`, `list`, and `hashtag` extractors ([#5529](https://github.com/mikf/gallery-dl/issues/5529))
- [mastodon] add support for card images
- [pixeldrain] add support for single-file album downloads ([#5641](https://github.com/mikf/gallery-dl/issues/5641))
- [reddit] support comment embeds ([#5366](https://github.com/mikf/gallery-dl/issues/5366))
- [seiga] re-implement login with username & password
- [tapas] add `creator` extractor ([#5306](https://github.com/mikf/gallery-dl/issues/5306))
- [vsco] add `avatar` extractor ([#5341](https://github.com/mikf/gallery-dl/issues/5341))
- [wikimedia] support `wiki.gg` wikis
#### Fixes
- [4archive] fix extraction
- [8chan] fix file downloads by sending a `TOS` cookie ([#5578](https://github.com/mikf/gallery-dl/issues/5578))
- [artstation] disable TLS 1.2 ciphers by default ([#5564](https://github.com/mikf/gallery-dl/issues/5564), [#5658](https://github.com/mikf/gallery-dl/issues/5658))
- [bluesky] filter reposts only for user timelines ([#5528](https://github.com/mikf/gallery-dl/issues/5528))
- [common] disable `check_hostname` for custom SSLContexts ([#3614](https://github.com/mikf/gallery-dl/issues/3614), [#4891](https://github.com/mikf/gallery-dl/issues/4891), [#5576](https://github.com/mikf/gallery-dl/issues/5576))
- [exhentai] fix Multi-Page Viewer detection ([#4969](https://github.com/mikf/gallery-dl/issues/4969))
- [exhentai] fix blank page detection
- [hiperdex] update domain to `hiperdex.top` ([#5635](https://github.com/mikf/gallery-dl/issues/5635))
- [hotleak] download files returning a 404 status code ([#5395](https://github.com/mikf/gallery-dl/issues/5395))
- [imgur] match URLs with title slugs ([#5593](https://github.com/mikf/gallery-dl/issues/5593))
- [kemonoparty] fix `KeyError - 'path'` for posts without files ([#5368](https://github.com/mikf/gallery-dl/issues/5368), [#5394](https://github.com/mikf/gallery-dl/issues/5394), [#5422](https://github.com/mikf/gallery-dl/issues/5422), [#5488](https://github.com/mikf/gallery-dl/issues/5488))
- [kemonoparty] fix crash on posts with missing datetime info ([#5422](https://github.com/mikf/gallery-dl/issues/5422))
- [mastodon] send canonical `true`/`false` boolean values ([#5516](https://github.com/mikf/gallery-dl/issues/5516))
- [newgrounds] update and fix login procedure ([#5109](https://github.com/mikf/gallery-dl/issues/5109))
- [patreon] fix `bootstrap` data extraction ([#5624](https://github.com/mikf/gallery-dl/issues/5624))
- [poipiku] fix downloading R-18 posts ([#5567](https://github.com/mikf/gallery-dl/issues/5567))
- [poipoku] avoid language-specific extraction ([#5590](https://github.com/mikf/gallery-dl/issues/5590), [#5591](https://github.com/mikf/gallery-dl/issues/5591))
- [realbooru] fix videos and provide fallback URLs ([#2530](https://github.com/mikf/gallery-dl/issues/2530))
- [slideshare] fix extraction
- [subscribestar] fix file URLs ([#5631](https://github.com/mikf/gallery-dl/issues/5631))
- [twitter] update domain to `x.com` ([#5597](https://github.com/mikf/gallery-dl/issues/5597))
- [twitter] transfer `twitter.com` cookies to `x.com` ([#5597](https://github.com/mikf/gallery-dl/issues/5597))
- [twitter] prevent crash when extracting `birdwatch` metadata ([#5403](https://github.com/mikf/gallery-dl/issues/5403))
- [twitter] handle missing `expanded_url` fields ([#5463](https://github.com/mikf/gallery-dl/issues/5463), [#5490](https://github.com/mikf/gallery-dl/issues/5490))
- [wikimedia] suppress exception for entries without `imageinfo` ([#5384](https://github.com/mikf/gallery-dl/issues/5384))
- [wikimedia] fix exception for files with empty `metadata`
#### Improvements
- [exhentai] detect CAPTCHAs during login ([#5492](https://github.com/mikf/gallery-dl/issues/5492))
- [foolfuuka] improve `board` pattern & support pages ([#5408](https://github.com/mikf/gallery-dl/issues/5408))
- [furaffinity] match `fxfuraffinity.net`/`fxraffinity.net`/`xfuraffinity.net` URLs ([#5511](https://github.com/mikf/gallery-dl/issues/5511), [#5568](https://github.com/mikf/gallery-dl/issues/5568))
- [gelbooru] improve pagination logic for meta tags ([#5478](https://github.com/mikf/gallery-dl/issues/5478))
- [kemonoparty:favorite] return artists/posts in native order and support `sort` and `order` query parameters ([#5375](https://github.com/mikf/gallery-dl/issues/5375), [#5620](https://github.com/mikf/gallery-dl/issues/5620))
- [oauth] use `Extractor.request()` for HTTP requests to support proxy servers etc ([#5433](https://github.com/mikf/gallery-dl/issues/5433))
- [pixiv] change `sanity_level` debug message to a warning ([#5180](https://github.com/mikf/gallery-dl/issues/5180))
- [twitter] improve username & password login procedure ([#5445](https://github.com/mikf/gallery-dl/issues/5445))
- [twitter] wait for rate limit reset before encountering a 429 error ([#5532](https://github.com/mikf/gallery-dl/issues/5532))
- [twitter] match `fixvx.com` URLs ([#5511](https://github.com/mikf/gallery-dl/issues/5511))
- [twitter] match Tweet URLs with query parameters ([#5371](https://github.com/mikf/gallery-dl/issues/5371), [#5372](https://github.com/mikf/gallery-dl/issues/5372))
- [twitter] match `/photo/` and `/video/` Tweet URLs ([#5443](https://github.com/mikf/gallery-dl/issues/5443), [#5601](https://github.com/mikf/gallery-dl/issues/5601))
#### Options
- [common] add `sleep-429` option ([#5160](https://github.com/mikf/gallery-dl/issues/5160))
- [common] implement `skip-filter` option ([#5255](https://github.com/mikf/gallery-dl/issues/5255))
- [common] implement `keywords-eval` option ([#5621](https://github.com/mikf/gallery-dl/issues/5621))
- [kemonoparty] add `announcements` option ([#5262](https://github.com/mikf/gallery-dl/issues/5262))
- [pixiv:novel] add `covers` option ([#5373](https://github.com/mikf/gallery-dl/issues/5373))
- [twitter] implement `relogin` option ([#5445](https://github.com/mikf/gallery-dl/issues/5445))
### Downloaders
- [http] add MIME type and signature for `.m4v` files ([#5505](https://github.com/mikf/gallery-dl/issues/5505))
### Post Processors
- [mtime] do not overwrite `_mtime` values with `None` ([#5439](https://github.com/mikf/gallery-dl/issues/5439))
- [ugoira] log errors for general exceptions
### Archives
- [archive] move DownloadArchive code into its own module
- [archive] implement `DownloadArchiveMemory` class ([#5255](https://github.com/mikf/gallery-dl/issues/5255))
- [archive] add `archive-mode` option ([#5255](https://github.com/mikf/gallery-dl/issues/5255))
### Cookies
- [cookies] use temporary file when saving cookies.txt files ([#5461](https://github.com/mikf/gallery-dl/issues/5461))
- [cookies] optimize `_find_most_recently_used_file()` for exact profiles ([#5538](https://github.com/mikf/gallery-dl/issues/5538))
- [cookies] set proper `expires` value for Chrome session cookies
### Documentation
- [docs] update docs/configuration links ([#5059](https://github.com/mikf/gallery-dl/issues/5059), [#5369](https://github.com/mikf/gallery-dl/issues/5369), [#5423](https://github.com/mikf/gallery-dl/issues/5423))
- [docs] update link to "nightly" builds ([#5618](https://github.com/mikf/gallery-dl/issues/5618))
- [docs] replace AnchorJS with custom script
- [docs] update defaults of `sleep-request`, `browser`, `tls12`
- [docs] complete Authentication info in docs/supportedsites
### Formatter
- [formatter] allow dots in `'...'` literals ([#5539](https://github.com/mikf/gallery-dl/issues/5539))
### Output
- [output] enable colored output by default
- [output] extend `output.colors` ([#2566](https://github.com/mikf/gallery-dl/issues/2566))
- [output] support `NO_COLOR` environment variable
- [output] add `--no-colors` command-line option
- [output] add `-w/--warning` command-line option ([#5474](https://github.com/mikf/gallery-dl/issues/5474))
### Tests
- [tests] select unused port number for local HTTP server
- [tests] allow filtering extractor result tests by URL or comment
- [tests] mark tests with missing auth as `only_matching`
### Update
- implement update-related command-line options ([#5233](https://github.com/mikf/gallery-dl/issues/5233))
  - `-U`/`--update` updates an executable file to the latest release
  - `--update-check` checks if the local version is up to date
  - `--update-to` allows switching to a different release channel (`stable` or `dev`)
    as well as upgrading/downgrading to a specific tag.
    - `--update-to dev`
    - `--update-to dev@2024.05.25`
    - `--update-to v1.25.2`
  - (non-executable installations have only access to `-U`/`--update-check` for version checks)
### Miscellaneous
- add workaround for requests 2.32.3 issues ([#5665](https://github.com/mikf/gallery-dl/issues/5665))
- fix exit status of `--clear-cache`/`--list-extractors`/`--list-modules`
- restore `LD_LIBRARY_PATH` for executables built with PyInstaller  ([#5421](https://github.com/mikf/gallery-dl/issues/5421))
- store `match` and `groups` values in Extractor objects
