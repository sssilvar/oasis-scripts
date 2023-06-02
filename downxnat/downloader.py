import argparse
import getpass
import json
import os
import ssl

import keyring
import xnat


def is_serializable(data):
    try:
        json.dumps(data)
        return True
    except (TypeError, ValueError):
        return False


def remove_non_serializable(data):
    if isinstance(data, dict):
        # If it's a dictionary, iterate over key-value pairs
        for key in list(data.keys()):  # Use list() to avoid modifying the dictionary during iteration
            if not is_serializable(data[key]):
                del data[key]
            else:
                remove_non_serializable(data[key])
    elif isinstance(data, (list, tuple)):
        # If it's a list or tuple, iterate over elements
        for i in range(len(data)):
            if not is_serializable(data[i]):
                data[i] = None
            else:
                remove_non_serializable(data[i])


def download_dir(subject, target_dir, verbose=True, progress_callback=None):
    """
        Download the entire subject and unpack it in a given directory. Note
        that this method will create a directory structure following
        $target_dir/{subject.label}/{experiment.label}
        and unzip the experiment zips as given by XNAT into that. If
        the $target_dir/{subject.label} does not exist, it will be created.

        :param str target_dir: directory to create subject directory in
        :param bool verbose: show progress
        :param progress_callback: function to call with progress string
                                  should be a function with one argument
    """
    subject_dir = os.path.join(target_dir, subject.label)
    if not os.path.isdir(subject_dir):
        os.mkdir(subject_dir)

    number_of_experiments = len(subject.experiments)

    for n, experiment in enumerate(subject.experiments.values(), start=1):
        if progress_callback is not None:
            progress_callback("Downloading experiment {} of {}".format(n, number_of_experiments))
        try:
            experiment.download_dir(subject_dir, verbose=verbose)
        except AttributeError:
            continue

    # Save clinical data as JSON file
    clinical_data = subject.fulldata
    with open(os.path.join(subject_dir, 'clinical_data.json'), 'w') as f:
        json.dump(clinical_data, f, indent=4)

    if verbose:
        subject.logger.info('Downloaded subject to {}'.format(subject_dir))


def download_oasis_scans(project_id, directory_name, xnat_central_username, scan_type="ALL", reset_credentials=False):
    # Disable SSL certificate verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    if reset_credentials:
        # Delete the stored password from the keyring
        keyring.delete_password("OASIS", xnat_central_username)
        keyring.delete_password("OASIS", "username")

    # Check if the password is already stored in the keyring
    password = keyring.get_password("OASIS", xnat_central_username)

    # If the password is not stored or reset is requested, prompt the user for the password
    if not password or reset_credentials:
        password = getpass.getpass("Enter your password for accessing OASIS data on XNAT Central:")

        # Store the password in the keyring
        keyring.set_password("OASIS", xnat_central_username, password)
    keyring.set_password("OASIS", "username", xnat_central_username)

    # Connect to XNAT Central
    session = xnat.connect('https://central.xnat.org', user=xnat_central_username,
                           password=keyring.get_password("OASIS", xnat_central_username), verify=False)

    # Create the directory if it doesn't exist yet
    os.makedirs(directory_name, exist_ok=True)

    # Get a list of all subjects in the project
    subjects = session.projects[project_id].subjects

    for subject in subjects.values():
        download_dir(subject, directory_name, verbose=True, progress_callback=None)


def main():
    parser = argparse.ArgumentParser(description='Download scans from OASIS on XNAT Central.')
    parser.add_argument('--project_id', help='Project ID on XNAT Central.')
    parser.add_argument('--directory_name', help='Directory path to save scan files to.')
    parser.add_argument('--xnat_central_username', help='Your XNAT Central username.')
    parser.add_argument('--scan_type', help='Scan type to download. Default is ALL.', default='ALL')
    parser.add_argument('--reset_credentials', action='store_true', help='Reset stored credentials in the keyring.')

    args = parser.parse_args()

    # Expand the user's home directory
    args.directory_name = os.path.abspath(os.path.expanduser(args.directory_name))

    download_oasis_scans(args.project_id, args.directory_name, args.xnat_central_username, args.scan_type,
                         args.reset_credentials)
