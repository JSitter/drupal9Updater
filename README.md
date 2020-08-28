# Drupal9 Semi-Auto Updater

Update your Drupal 8 or Drupal 9 Projects with relative ease.

This script is designed to run on Hostgator Shared servers that don't want to run scripts using Python3. In order to run the updater on Hostgator sites use hostgator-runner.sh script to force the server to run the updater using a more modern version of Python, otherwise just run ./updater.py when not using on Hostgator.

## Usage

`-d` or `--download` Download update from url.(Work in progress)

`-l` or `--local` Update from local zipped Drupal package.

`-h` Show help screen.

## MIT License

Copyright 2020 Justin Sitter

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.