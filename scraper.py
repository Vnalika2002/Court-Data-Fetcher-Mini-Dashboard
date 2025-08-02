from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup

# Map from user-friendly input to the actual <option> value attribute on Delhi High Court form
CASE_TYPE_MAPPING = {
    "Civil": "O.S.",              # Original Suit
    "Bail Application": "BAIL APPLN.",
    "Criminal": "CRL.",
    "Company Petition": "COMPANY PETITION",
    "IMA": "IMA",
    # Add more mappings as needed — verify with site
}

def fetch_case_details(case_type, case_number, filing_year):
    url = "https://delhihighcourt.nic.in/case.asp"  # Actual case search page

    # Map user input case_type to dropdown value
    case_type_value = CASE_TYPE_MAPPING.get(case_type)
    if case_type_value is None:
        return None, {
            "error": f"Unrecognized case type. Please use one of: {list(CASE_TYPE_MAPPING.keys())}"
        }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True when stable
        page = browser.new_page()
        page.goto(url)

        try:
            # Wait for form fields
            page.wait_for_selector('select[name="ctl00$ContentPlaceHolder1$ddlCaseType"]', timeout=20000)
            page.wait_for_selector('input[name="ctl00$ContentPlaceHolder1$txtCaseNo"]', timeout=20000)
            page.wait_for_selector('select[name="ctl00$ContentPlaceHolder1$ddlYear"]', timeout=20000)
            page.wait_for_selector('input[name="ctl00$ContentPlaceHolder1$txtCaptcha"]', timeout=20000)
            page.wait_for_selector('input[id="ctl00_ContentPlaceHolder1_btnSearch"]', timeout=20000)

            # Fill form properly
            page.select_option('select[name="ctl00$ContentPlaceHolder1$ddlCaseType"]', case_type_value)
            page.fill('input[name="ctl00$ContentPlaceHolder1$txtCaseNo"]', case_number)
            page.select_option('select[name="ctl00$ContentPlaceHolder1$ddlYear"]', filing_year)

            # CAPTCHA handling — manual input prompt
            page.screenshot(path="captcha.png")
            print("CAPTCHA screenshot saved as captcha.png")
            captcha_text = input("Please enter CAPTCHA exactly as seen in captcha.png: ")
            page.fill('input[name="ctl00$ContentPlaceHolder1$txtCaptcha"]', captcha_text)

            # Submit the form
            page.click('input[id="ctl00_ContentPlaceHolder1_btnSearch"]')

            # Wait for results table (adjust selector if needed)
            page.wait_for_selector('#ctl00_ContentPlaceHolder1_gvCaseDetails', timeout=15000)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Parse case data — adapt if site structure changes
            try:
                # The parties and other info are usually inside a GridView with id gvCaseDetails
                table = soup.find('table', id='ctl00_ContentPlaceHolder1_gvCaseDetails')
                if not table:
                    return html, {'error': 'Case not found or no details available.'}

                rows = table.find_all('tr')
                # Assume first row is header, parse data from second row as example:

                # Parsing some columns by table headers; adjust indexes if changed
                if len(rows) < 2:
                    return html, {'error': 'No case data rows found.'}

                data_cells = rows[1].find_all('td')
                cases_info = {}
                if len(data_cells) >= 5:
                    cases_info['parties'] = data_cells[1].get_text(strip=True)
                    cases_info['filing_date'] = data_cells[2].get_text(strip=True)
                    cases_info['next_hearing'] = data_cells[3].get_text(strip=True)
                    # For PDF link, check if 5th cell has an <a> tag
                    pdf_tag = data_cells[4].find('a')
                    cases_info['pdf_url'] = pdf_tag['href'] if pdf_tag else None
                else:
                    return html, {'error': 'Unexpected table format.'}

                cases_info['error'] = None
                browser.close()
                return html, cases_info

            except Exception as parse_err:
                browser.close()
                return html, {'error': f'Parsing error: {str(parse_err)}'}

        except PlaywrightTimeoutError:
            browser.close()
            return None, {'error': 'Timeout waiting for form elements or results — site changed or slow network.'}
        except Exception as e:
            browser.close()
            return None, {'error': f'Unexpected error: {str(e)}'}
