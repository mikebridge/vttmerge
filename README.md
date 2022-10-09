# VTT Merge

Merge multiple VTT subtitle files into one file.  Each language will appear in a different 
colour in video players that support different colours, such as [vlc](https://www.videolan.org/).


![Preview](https://github.com/mikebridge/vttmerge/blob/master/img/preview.png?raw=true)

## Setup

  1) Set up [python](https://www.python.org/downloads/):

  2) (Optional) set up a virtual environment

```
python -m venv vttmerge
. .\vttmerge\Scripts\Activate.ps1
```

  3) Install the libraries

```
pip install -r requirements.txt
```

## Usage

Choose the VTT files that you want to merge together:

```
python -m main -f FILE1.da.vtt FILE2.en.vtt
```

This will create a file called `FILE1.all.vtt`, replacing the first file's language with 'all'

