#!/usr/bin/env python
# !/usr/bin/env python
import re
import subprocess
import math
import threading
import zipfile
import PyPDF2
from PyPDF2 import PdfReader
from tqdm import tqdm
import os
import sys
import time
import pyfiglet
from colorama import Fore, Back, Style

entropy_threshold = 7.0


def winApiStrings(strings):
    winAPIList = ['Open', 'Write', 'Wget', 'Wset', 'Create', 'Exec', 'Wait', 'Virtual', 'Set', 'Get', 'Http', 'Load',
                  'Exit', 'Kill', 'Free', 'Sleep', 'Time', 'Callee']
    returnList = []
    for w in winAPIList:
        pattern = fr"\b{w}\w*\b"
        temp = re.findall(pattern, strings)
        returnList.extend(temp)
    valBack = []
    for i in returnList:
        if i not in valBack:
            valBack.append(i)

    return valBack


def patterns_find(strings):
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', strings)
    ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', strings)
    paths = re.findall(r'[a-zA-Z]:\\(?:[^\s\\]+\\)*[^\s\\]*', strings)
    files_and_dlls = re.findall(r'\b[\w\.]+(?:\.dll|\.exe)\b', strings)
    urls = re.findall(r'(https?://\S+|www\.\S+)', strings)
    urls = [url for url in urls if not url.startswith("http://schemas.")]
    winAPI = winApiStrings(strings)
    findings = (emails, ips, paths, files_and_dlls, urls, winAPI)
    return findings


def unique_patterns_find(finds):
    unique_values = set()
    unique_finds = []
    for find_list in finds:
        unique_find_list = []
        for value in find_list:
            if value not in unique_values:
                unique_values.add(value)
                unique_find_list.append(value)
        unique_finds.append(unique_find_list)
    return tuple(unique_finds)


def analyze_PDF(clean_path):
    PDF = PyPDF2.PdfReader(PDFFile)
    pages = len(PDF.pages)
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    for page in range(pages):
        pageSliced = PDF.pages[page]
        pageObject = pageSliced.get_object()
        if key in pageObject.keys():
            ann = pageObject[key]
            for a in ann:
                u = a.get_object()
                if uri in u[ank].keys():
                    urls.append(u[ank][uri])

    return urls


def analyze_doc(clean_path):
    """
    the function for analyzing doc files
    Args:
        clean_path: the path to the file location

    Returns: a tuple of the findings

    """
    findings = []
    with zipfile.ZipFile(clean_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            with zip_file.open(file_name) as file:
                # Read the content of the file
                if file_name.endswith('.png'):
                    continue
                strings = file.read().decode("utf-8")
            findingsTemp = patterns_find(strings)
            if not findings:
                findings = findingsTemp
            else:
                findings = tuple([x + y for x, y in zip(findings, findingsTemp)])
    return findings


def analyze_PE(clean_path):
    # Extract strings from the file
    strings = extract_strings(clean_path)
    entropy = calculate_entropy_with_loading(clean_path)
    print("the entropy is --> ", entropy)
    if entropy > entropy_threshold:
        print(f"The file '{clean_path}' has high entropy, indicating it may be packed.")
    else:
        print(f"The file '{clean_path}' has low entropy, indicating it may not be packed.")
    findings = patterns_find(strings)
    return findings


def analyze_file(file_path):
    Sfind = ()
    Fpath = file_path.replace('"', "")
    if Fpath.endswith('.exe') or Fpath.endswith('.dll'):
        Sfind = analyze_PE(Fpath)
    elif Fpath.endswith('.csv'):
        # Read the CSV file and search for specific strings
        found_strings = []
        with open(Fpath, "r", encoding="utf-8") as csv_file:
            strings = csv_file.read()
        Sfind = patterns_find(strings)
        return Sfind
    elif Fpath.endswith('.doc') or Fpath.endswith('.docx'):
        Sfind = analyze_doc(Fpath)
    elif Fpath.endswith('.pdf'):
        Sfind = ('still not available for pdf', 'still not available for pdf', 'still not available for pdf',
                 'still not available for pdf', analyze_PDF(Fpath), 'still not available for pdf')
    return Sfind


def unique_analyze(file_path):
    Sfind = ()
    Fpath = file_path.replace('"', "")
    if Fpath.endswith('.exe') or Fpath.endswith('.dll'):
        Sfind = analyze_PE(Fpath)
    elif Fpath.endswith('.csv'):
        # Read the CSV file and search for specific strings
        found_strings = []
        with open(Fpath, "r", encoding="utf-8") as csv_file:
            strings = csv_file.read()
        Sfind = patterns_find(strings)
        return Sfind
    elif Fpath.endswith('.doc') or Fpath.endswith('.docx'):
        Sfind = analyze_doc(Fpath)
    elif Fpath.endswith('.pdf'):
        Sfind = analyze_PDF(Fpath)
    return Sfind


def update_loading_bar(progress):
    bar_length = 50
    filled_length = int(round(bar_length * progress))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()


def extract_cert_info(file_path):
    process = subprocess.Popen(f'certutil -f -v -dump "{file_path}"', shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    animation = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

    # Display loading animation while waiting for the command to finish
    def animate():
        idx = 0
        color_idx = 0
        while process.poll() is None:
            sys.stdout.write(
                "\r" + colors[color_idx % len(colors)] + "Processing " + animation[idx % len(animation)] + " \033[0m ")
            sys.stdout.flush()
            idx = (idx + 1) % len(animation)
            if idx % len(animation) == 0:
                color_idx += 1
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * len("Extracting strings ") + "\r")
        sys.stdout.flush()

    threading.Thread(target=animate, daemon=True).start()
    # Wait for the command to finish
    output, error = process.communicate()
    return output.decode('utf-8')


def extract_strings(file_path):
    """
    extracting strings out of PE file
    Args:
        file_path: the path to the wanted file

    Returns: the strings decoded to utf-8

    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(dir_path)
    # Use strings.exe to extract strings from PE file
    process = subprocess.Popen(f'"{parent_dir}\\bin\\strings.exe" /accepteula "{file_path}"', shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    # CLI animation
    animation = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']

    # Display loading animation while waiting for the command to finish
    def animate():
        idx = 0
        color_idx = 0
        while process.poll() is None:
            sys.stdout.write(
                "\r" + colors[color_idx % len(colors)] + "Processing " + animation[idx % len(animation)] + " \033[0m ")
            sys.stdout.flush()
            idx = (idx + 1) % len(animation)
            if idx % len(animation) == 0:
                color_idx += 1
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * len("Extracting strings ") + "\r")
        sys.stdout.flush()

    threading.Thread(target=animate, daemon=True).start()
    # Wait for the command to finish
    output, error = process.communicate()
    return output.decode('utf-8')


def calculate_entropy(file_path, block_size=65536, progress_callback=None):
    with open(file_path, 'rb') as f:
        byte_frequency = [0] * 256
        total_bytes = 0
        # Calculate frequency of each byte
        byte = f.read(block_size)
        while byte:
            for b in byte:
                byte_value = b
                byte_frequency[byte_value] += 1
                total_bytes += 1
            byte = f.read(block_size)
            if progress_callback:
                progress_callback(total_bytes)
    entropy = 0.0
    for frequency in byte_frequency:
        if frequency != 0:
            probability = frequency / total_bytes
            entropy -= probability * math.log2(probability)
    return entropy


def calculate_entropy_with_loading(file_path, block_size=65536):
    total_bytes = os.path.getsize(file_path)
    with tqdm(total=total_bytes, desc="Calculating Entropy", unit="bytes") as pbar:
        def update_progress(progress):
            pbar.update(progress)

        entropy = calculate_entropy(file_path, block_size, progress_callback=update_progress)
    return entropy


def print_heaeder():
    text = "STATIC ANALYSIS SCRIPT"
    # Create a figlet font object
    figlet = pyfiglet.Figlet(font='ansi_shadow')
    # Render the text as ASCII art
    ascii_art = figlet.renderText(text)
    # Print the ASCII art
    print(Fore.CYAN + ascii_art)
    print(Fore.RESET)


def print_help():
    """
    a function to print the help message
    """
    print_heaeder()
    print("Welcome to the Static Analysis Script! \n \n"
          "This script serves as a tool for extracting valuable insights from specified files. \n"
          "It identifies emails, paths, files, URLs, and IP addresses for in-depth analysis. \n \n"
          "Instructions for Usage: \n"
          "Usage: main.py <file_path> <option> \n"
          "Available Options:\n"
          "-u, -U    Show only unique values from the extracted strings. \n"
          "-e, -E    Print out the entropy calculation only. \n"
          "-c, -C    Print certificate information, including supplementary details. \n"
          "--version Script current version. \n \n"
          "for more information or requests, please visit the project repository. ")


def print_version():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(dir_path)
    src_dir = os.path.dirname(parent_dir)
    process = subprocess.Popen(f'type "{src_dir}\\setup.py" | findstr "version"', shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8')


def main():
    import sys

    num_args = len(sys.argv)
    if num_args == 2 or num_args == 3:
        UserInput = sys.argv[1]
        try:
            clean_path = UserInput.replace('"', "")
            if UserInput == ('-h' or '-H'):
                print_help()
            elif UserInput in '--version':
                ver = print_version()
                print(ver)
            elif os.path.isfile(clean_path):
                print_heaeder()
                try:
                    if sys.argv[2] in ('-C', '-c'):
                        certInfo = extract_cert_info(clean_path)
                        print(certInfo)
                    elif sys.argv[2] in ('-E', '-e'):
                        entropy = calculate_entropy_with_loading(clean_path)
                        print("the entropy is --> ", entropy)
                        if entropy > entropy_threshold:
                            print(f"The file '{clean_path}' has high entropy, indicating it may be packed.")
                        else:
                            print(f"The file '{clean_path}' has low entropy, indicating it may not be packed.")
                    elif sys.argv[2] in ('-U', '-u'):
                        Ufind = unique_patterns_find(findings)
                        print("\n Emails:", Ufind[0])
                        print("\n IPs:", Ufind[1])
                        print("\n Paths:", Ufind[2])
                        print("\n Files and DLLs:", Ufind[3])
                        print("\n Urls:", Ufind[4])
                    else:
                        print("an error in input \n"
                              "please read main.py -h for further explanation")
                except Exception as e:
                    findings = analyze_file(clean_path)
                    #  findings = (emails, ips, paths, unique_files_dlls, urls, winAPI)
                    print("\n Emails:", findings[0])
                    print("\n IPs:", findings[1])
                    print("\n Paths:", findings[2])
                    print("\n Files and DLLs:", findings[3])
                    print("\n Urls:", findings[4])
                    print("\n Windows API:", findings[5])
            else:
                print("file doesn't exists, please read main.py -h for further explanation")
        except Exception as e:
            print("\n ----- error: ", e, " ---------")
    else:
        print_help()


if __name__ == "__main__":
    main()
