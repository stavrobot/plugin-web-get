# plugin-web-get

A Stavrobot plugin that fetches web pages and returns their content as a file. HTML can be stripped to plain text (the default) or returned raw.

## Installation

Tell Stavrobot: "Install the plugin at https://github.com/stavrobot/plugin-web-get"

## Tools

### `fetch_page`

Fetches a web page and returns its content as a file.

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | The URL of the page to fetch. |
| `strip_html` | boolean | Strip HTML tags and return plain text. Defaults to `true`. Set to `false` to get the raw HTML. |
