# hashsan

[![made-with-Python](https://img.shields.io/badge/made%20with-Python-blue.svg)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![issues](https://img.shields.io/github/issues/X-Projetion/hashsan?color=blue)](https://github.com/X-Projetion/hashsan/issues)

<p align="center">
    <img src="gambar.png" alt="hashsan" width="60%">
</p>
<h4 align="center">Hashsan is a tool for opening passwords that are encrypted using MD5.</h4>

# hashsan
Hashsan is a lookup tool that searches for original text from text that has been encrypted or locked. This allows you to enter MD5 and search for matching ("found") plain text in the wordlist you have created.

## Resources
- [Installation](#installation)
- [Usage](#usage)
- [Help](#help)
- [Disclaimer](#Disclaimer)

## Installation

```bash
git clone https://github.com/X-Projetion/hashsan/ && cd hashsan
pip install -r requirements.txt
```

## Usage
- python main.py -p xxxxx

## Help
```bash
usage: main.py [-h] [-o OUTPUT] [-w WORDLIST] [-p HASH] [-l HASHLIST]

Simple password cracker using a wordlist

optional arguments:
  -h, --help            Show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file for cracked passwords
  -w WORDLIST, --wordlist WORDLIST
                        Path to the wordlist file
  -p HASH, --hash HASH  Target hash to crack
  -l HASHLIST, --hashlist HASHLIST
                        Path to the hash list file
```
                        

## Disclaimer
The script provided is for educational purposes only, I am not responsible for your actions.

<br>
<a href="https://www.instagram.com/lutfifakee/" target="_blank" rel="noopener noreferrer">Follow</a>
    <br>
Made by X-Projetion
