# quartr_project

Python automation for fetching the latest 10-K filing URLs from the SEC EDGAR API and saving each filing as a PDF.

## What It Does

The current workflow in `main.py`:

1. Loads configuration from `config.yaml`.
2. Reads `SEC_USER_AGENT` from a `.env` file.
3. Resolves each configured ticker to its SEC CIK.
4. Looks up the most recent `10-K` filing in the company's recent submissions.
5. Converts the filing page to PDF with `wkhtmltopdf`.
6. Saves PDFs into a dated folder under `output/`.

## Project Structure

```text
.
|-- main.py
|-- config.yaml
|-- requirements.txt
|-- output/
`-- src/
		|-- providers/
		|   |-- base_provider.py
		|   `-- sec_provider.py
		`-- utils/
				`-- utilities.py
```

## Requirements

- Python 3.10+ recommended
- Windows environment
- `wkhtmltopdf` installed locally
- Network access to `sec.gov` and `data.sec.gov`

The code currently expects the `wkhtmltopdf` executable path to be configured in `config.yaml`.

## Installation

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Install `wkhtmltopdf` and confirm the executable path matches the value in `config.yaml`:

```yaml
local_directory:
	wkhtmltopdf_directory: 'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
```

## Environment Setup

Create a `.env` file in the project root with a valid SEC user agent:

```env
SEC_USER_AGENT=Your Name your.email@example.com
```

The SEC expects a descriptive user agent that identifies the requester.

## Configuration

`config.yaml` controls the company list, SEC endpoints, request behavior, output folder, and the local `wkhtmltopdf` binary.

Current configuration shape:

```yaml
companies:
	- AAPL
	- META
	- GOOGL
	- AMZN
	- NFLX
	- GS

endpoints:
	sec_ticker_url: "https://www.sec.gov/files/company_tickers.json"
	sec_submissions_url: "https://data.sec.gov/submissions/CIK{cik}.json"
	sec_filing_url: "https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{filename}"

requests:
	timeout_seconds: 30
	retry_total: 3
	retry_backoff_factor: 1
	retry_status_forcelist:
		- 429
		- 500
		- 502
		- 503
		- 504

output:
	form_10k_directory: ".\\output\\"

local_directory:
	wkhtmltopdf_directory: 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
```

## Running The Project

Run the script from the project root so `main.py` can find `config.yaml`:

```powershell
python main.py
```

If you are using the checked-in virtual environment in this workspace, the equivalent command is:

```powershell
.\myenv\Scripts\python.exe .\main.py
```

## Output

Generated files are written into a date-stamped folder:

```text
output/
`-- YYYY-MM-DD/
		|-- AAPL_10-K.pdf
		|-- META_10-K.pdf
		`-- ...
```

## Implementation Notes

- `SECProvider` uses a `requests.Session` with retry handling for transient SEC errors.
- `common_utils.rate_limit()` enforces a simple cap of 10 requests per second.
- The downloader currently saves PDFs directly from the filing URL by using `pdfkit.from_url(...)`.
- The script targets the first recent filing whose form type equals `10-K`.

## Known Constraints

- The script is designed around Windows-style paths in `config.yaml`.
- `main.py` reads `config.yaml` using a relative path, so it should be launched from the repository root.
- If a ticker does not appear in the SEC ticker mapping, it is skipped.
- If a company has no recent `10-K` in the `recent` filings block, no PDF is generated for that company.

## Troubleshooting

`ValueError: SEC_USER_AGENT environment variable is not set.`

- Add `SEC_USER_AGENT` to the root `.env` file.

`No wkhtmltopdf executable found`

- Install `wkhtmltopdf`.
- Update `local_directory.wkhtmltopdf_directory` in `config.yaml`.

HTTP 403 or rate-limit-related SEC errors

- Verify that `SEC_USER_AGENT` is valid and descriptive.
- Reduce request volume if you customize the code.
- Retry later if the SEC temporarily throttles the client.