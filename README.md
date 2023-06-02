# XNAT Downloader
The XNAT Downloader is a Python script designed specifically for downloading scans from OASIS on XNAT Central. It facilitates the retrieval of imaging data for neuroimaging research purposes.

## Prerequisites
Before using this script, ensure that you have the following dependencies installed:

* Python 3.9
* Poetry

## Installation
To install and set up the XNAT Downloader, follow these steps:

1. Clone or download the repository to your local machine.
2. Open a terminal or command prompt and navigate to the XNAT Downloader project directory.
3. Run the following command to install the project dependencies using Poetry:

```bash
poetry install
```

## Usage
To use the XNAT Downloader:

Update the oasis_scripts/downloader.py file with any necessary modifications or customizations.

Open a terminal or command prompt and navigate to the XNAT Downloader project directory.

Run the following command to execute the script:

```bash
poetry run xnat-download --project_id <project_id> --directory_name <directory_name> --xnat_central_username <xnat_central_username> --scan_type <scan_type> --reset_credentials
```

Replace the placeholders (`<project_id>`, `<directory_name>`, `<xnat_central_username>`, and `<scan_type>`) with the appropriate values.

* `project_id`: The project ID on XNAT Central.
* `directory_name`: The directory path to save the scan files to.
* `xnat_central_username`: Your XNAT Central username.
* `scan_type` (optional): The scan type to download. The default value is ALL.
* `reset_credentials` (optional): Include this flag if you want to reset stored credentials in the keyring.

## License
The XNAT Downloader is licensed under the MIT License. See the LICENSE file for more details.

### Note
Please use the XNAT Downloader responsibly and in compliance with the terms and conditions of the OASIS project and XNAT Central. Ensure that you have the necessary permissions and rights to access and download the scans. Respect any data usage agreements and guidelines provided by OASIS and XNAT Central.

Please note that the XNAT Downloader has been tested specifically with OASIS3 data on XNAT Central. It may not be suitable for other XNAT projects.

If you have any questions or need further assistance, please feel free to reach out.