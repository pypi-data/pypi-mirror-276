
# htmlExtractor

`htmlExtractor` is a simple Python package to fetch HTML data from a website using the requests and BeautifulSoup libraries. This package simplifies the process of fetching and parsing HTML content from a given URL.


## Usage
Here's a quick example of how to use the `htmlExtractor` package:


# Fetch and parse HTML data from a website
`from htmlExtractor import extractHtml`

`soup = extractHtml('http://example.com', 'html.parser')`

`print(soup)`
## Details
### htmlExtractor(website, parser)
- Fetches and parses HTML data from the specified website.
### Parameters:
- `website (str)`: The URL of the website to fetch HTML from.
- `parser (str)`: The parser to use with BeautifulSoup (e.g., 'html.parser', 'lxml').
### Returns:
`soup_data` (BeautifulSoup object): Parsed HTML data.

## Dependencies
This package requires the following libraries:
- `requests`
- `beautifulsoup4`
These dependencies will be installed automatically when you install the `htmlExtractor` package.

## License:
This project is licensed under the [MIT License](https://opensource.org/license/mit). 

## Contact:
If you have any questions, suggestions, or issues, feel free to open an issue on GitHub or contact me directly at anisurrahman06046@gmail.com or [LinkedIn](https://www.linkedin.com/in/yourprofile)
.
## Acknowledgements

 - This package uses the [requests](https://pypi.org/project/requests/) library to make HTTP requests.
 - It also uses [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) for parsing HTML and XML documents.


