
<div class="onelinetext" align="center" style="padding-top:35px;">
<h2>Simple and dynamic printing animation styles for Python project</h2> 

[![PyPI Version (latest by date)](https://badge.fury.io/py/test-dvs-printf.svg?achebuster=1)](https://badge.fury.io/py/dvs-printf)
![PyPI Version](https://img.shields.io/pypi/v/test-dvs-printf.svg?achebuster=1)
[![Build Status](https://github.com/dhruvan-vyas/dvs_printf/actions/workflows/module_test.yml/badge.svg)](https://github.com/dhruvan-vyas/dvs_printf/actions)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/dhruvan-vyas/dvs_printf)](https://github.com/dhruvan-vyas/dvs_printf/releases/tag/v1.3)<br>
![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/dhruvan-vyas/dvs_printf/blob/main/LICENSE)
[![PEP8](https://img.shields.io/badge/PEP8-compliant-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/) 
</div> 


[![PyPI version](https://badge.fury.io/py/test-dvs-printf.png)](https://badge.fury.io/py/test-dvs-printf)

![PyPI Version](https://img.shields.io/pypi/v/test-dvs-printf.svg?achebuster=1)


<a href="https://github.com/dhruvan-vyas/dvs_printf">
<img src="https://github.com/dhruvan-vyas/dvs_printf/blob/main/card.png?raw=true"><br></a>


Enhanced way to handle console output for Python projects. The module offers `printf` style animation 
functions designed to improve the visual appearance of terminal-based Python projects, 
Key features include different animation styles, customizable speeds, and flexible formatting options.

<br>

# Installation
choose the appropriate one-liner command according to your system. \
ensure a Straight Forward setup process. 

### Linux / macOS
```bash
pip3 install dvs_printf
``` 
```bash
python3 -m pip install dvs_printf
```

### Windows
```bash
pip install dvs_printf 
```
```bash
python -m pip install dvs_printf
```


### **Clone the repository**
```bash
git clone https://github.com/dhruvan-vyas/test_dvs_printf.git
```

<br>

# Documentation

<a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#printf-function" >**printf**</a> The printf function is the core of the module, 
allowing users to apply various animation styles to their values. Supports different data types 
***(string, int, float, list, set, tuple, dict)*** and classes ***(numpy, tensorflow, pytorch, pandas)*** as input. 
Users can choose from a range of animation styles, including typing, async, headlines, Center, Left, Right and more. 
Customizable parameters include style, speed, interval, getmat and the stay option to make the printed values stay or disappear. 

<a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#dvs_printfinit-method" >**dvs_printf.init**</a> A dynamic initializer for printf that allows users to preset parameters for consistent usage.  
Priority order for setting parameters: printf's keywords > Setter Variables > dvs_printf.init's keywords > Defaults. <br>
more about on GitHub README.

<a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#showloding-function" > **showLoading**</a> A function for creating loading bars in the terminal, 
useful for waiting times during tasks like downloading files or running background functions. 
Users can customize loading text, loading bar, and other parameters. 

<a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf?tab=readme-ov-file#listfunction" >**listfunction**</a> A supplementary function used by printf to 
create new lists based on input values. Can handle various data types and optionally convert matrices into rows of strings. 

<br>

***

The <a style="text-decoration:none" href="https://github.com/dhruvan-vyas/dvs_printf#dvs_printf" >Github-README</a> file includes clear examples, code snippets, videos, 
and explanations to assist users in implementing the module effectively. 
All links above lead to the very same file.



