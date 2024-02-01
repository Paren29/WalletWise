# WalletWise

## Project Description

Tired of spreadsheet fatigue and pulling transactions from account statements every month to keep logs of your expense? This Python script will be your companion.

### Phase 1 - Data Extraction

This script pulls information from Australian banks such as NAB, CBA (more incoming) and organises it into a single, neat, tidy sheet. Segmenting expenses of each year to a sheet and distributing monthly expenses to a seperate workbook.

### Phase 2 - Analytics

Dive deeper into your spending habits. Clean, organized data awaits, ready for analysis. Time-series predictions are on the horizon, helping you provide insights.

The project is work in progress, but you can experience the magic of Phase 1.

**P.S.** *Coding enthusiasts, feel free to join the journey and contribute!*

## Target Audience

This project welcomes everyone curious about their finances and eager to unlock the power of data!

* **Hobbyists:** Say goodbye to spreadsheet drudgery! Our script effortlessly transforms bank PDFs into organized sheets, making it easy to track your spending and reach your financial goals.
* **Researchers:** Dive deeper into your financial data! Extracted transactions are neatly presented in a research-friendly format, ready for your analysis and insights.
* **Developers:** Join a thriving community and code alongside us! Contribute to expanding this project's functionality, refine its automation, and learn while shaping a valuable tool for everyone.

## Key Features

* **Automatic PDF parsing:** Effortlessly extract data from Australian banks (Commonwealth Bank of Australia and National Australian Bank) PDF file.
* **Clean and organized data:** No more manual data entry; enjoy neatly formatted spreadsheets for easy analysis.
* **Customizable reports:** Generate personalized reports to track spending trends and reach your budgeting goals.
* **Advanced analytics (future):** Predict future expenses and optimize your financial future with time-series modeling (coming soon!).

## Installation

**1. Set Up Your Environment:**

* **Install Python:** Ensure you have Python 3.x installed on your system. If not, download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
* **Create a Virtual Environment (Recommended):** To isolate project dependencies and avoid conflicts, it's highly recommended to create a virtual environment. Use tools like `venv` or `virtualenv` for this purpose.

**2. Install Required Libraries:**

* Using`pip`**:** Navigate to the project's directory in your terminal and run the following command:
  `pip install -r requirements.txt`

**3. Install Poppler:**

* **Download:** Download the appropriate Poppler package for your operating system from [https://poppler.freedesktop.org/](https://poppler.freedesktop.org/).
* **Install:** Follow the installation instructions provided on the Poppler website, ensuring you add Poppler to your system's PATH environment variable.
  * **Windows:** The installer usually handles this automatically.
  * **macOS:** Use package managers like Homebrew or MacPorts for simplified installation.
  * **Linux:** Use your distribution's package manager (e.g., `apt-get` on Ubuntu).

**4. Verify Installation:**

* Open a Python console and try importing the `poppler` library:
  `import poppler`
* If no errors occur, you're ready to use the script!

**Troubleshooting:**

* If you encounter issues during installation, refer to the detailed Poppler documentation for your operating system or seek assistance in online communities or forums.

## Usage

**1. Gather Your Statements:**

* Download your bank statements as PDF files.
* Place them in a folder named `to_process` within the same directory as the script. **(Create the folder if it doesn't exist.)**

**2. Indicate Bank Type:**

* Prefix each PDF filename with either:
  * `cba` for Commonwealth Bank of Australia statements
  * `nab` for National Australian Bank statements

**Example:**`cba_statement_january2024.pdf`

**3. Run the Script:**

* Open a terminal or command prompt in the script's directory.
* Execute the following command: `python main.py`

**4. View Your Data:**

* A new Excel spreadsheet (`.xlsx`) will be generated, containing all extracted transactions from the processed PDFs.

**Additional Notes:**

* Ensure you have Python and the required libraries installed (listed in the Dependencies section).
* For multiple statements, download them to the `to_process` folder and repeat steps 1-3.
* If you encounter any issues, reach out for assistance.

## Contributions

I actively encourage contributions to this project! Whether you're a seasoned developer or just starting out, your ideas and skills can make a difference. Feel free to contribute bug fixes, feature improvements, documentation updates, or anything that can enhance this script's functionality and usefulness.

To contribute:

1. Fork this repository and create a new branch.
2. Make your changes and add a clear and concise description of your contribution to the pull request.
3. Submit a pull request and await review.

I'm always happy to answer any questions and discuss potential contributions. Thanks for helping me make this project even better!

## License

This project is licensed under the MIT License.

Copyright (c) 2024 Paren Kansara

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
