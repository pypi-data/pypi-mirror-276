
## Static-analysis-script 
Welcome to the Static Analysis Script! This Python tool is crafted to extract emails, paths, files, URLs, and IPs from the specified file for analysis.
## Purpose
This tool aids in the collection of data essential for static analysis, accelerating the detection of Indicators of Compromise (IOCs) and other potentially malicious activities executed by files.
## Installation

### option 1:
pip install from the pypi project
```bash
  python -m pip install static-analysis-script
```
please make sure to download the latest version, currently 0.2.3

### option 2:
git clone the project.
pip install local from the git directory
```bash
  git clone https://github.com/perzibel/static-analysis-script.git
  cd static-analysis-script
  python -m pip install .
```
    
## Usage

![image](https://github.com/perzibel/static-analysis-script/assets/58742092/2734c00a-3f4d-4f36-bed4-48e72e8656a9)


## Analysis of Executables and DLL Files
The tool employs strings.exe to pull strings from executable (EXE) and dynamic link library (DLL) files, analyzing these strings to pinpoint paths, files, IP addresses, and URLs.

NEW! extract WinApi commands in the file 

## Analysis of CSV Files
For Comma-Separated Values (CSV) files, the tool extracts relevant information by directly reading the contents of the files.

## Analysis of Word Documents
Utilizing the zipfile library, the tool processes Word documents, extracting embedded emails and URLs from various sections.

## Analysis of PDF Files
extract ALL visiable and hidden URIs
