# Command Line Interface (CLI) Torrent Downloader

<img src="https://img.shields.io/badge/status-work%20in%20progress-red" />

This is a command-line interface (CLI) Torrent Downloader developed entirely in Python without using external libraries. It provides a simple and lightweight way to download and manage torrents.

## BitTorrent Protocol

This project is an implementation of the BitTorrent protocol for file sharing. The BitTorrent protocol is a popular peer-to-peer (P2P) file-sharing protocol that allows users to distribute large files efficiently without putting too much strain on a single server. For more information on the BitTorrent protocol, please refer to the [official BitTorrent specification](https://www.bittorrent.org/beps/bep_0003.html).

## Features
* Download and manage torrents from a local .torrent file
* Display information about the torrent file
* Save the downloaded files to a specified folder

## Requirements
This program requires Python 3.x installed on your computer.

## Installation
To use this CLI Torrent Downloader, simply download the project and run it using the following command:

``
python start.py --t <path_to_torrent_file>
``

## Usage
Once the program is running, it will prompt you to enter the path to the torrent file you want to download. After that, it will display information about the torrent file and ask you to choose a download location.

You can choose to download the entire file or select specific files from the torrent. The program will download the files to the specified folder.

## Development
This CLI Torrent Downloader was developed entirely in Python using the Clean Architecture pattern. It is a lightweight and simple project designed for educational purposes.

## Future Improvements
This project can be further improved by adding more features such as support for magnet links, support for multiple torrent files, and more advanced download options.

## Contributions
Contributions are always welcome! If you want to contribute to this project, please create a fork and submit a pull request.
