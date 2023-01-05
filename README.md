<div align="center">
  <img width="600px" src="https://i.ibb.co/1T2TX8j/logo.png") />
</div>

[![Language - Python](https://img.shields.io/static/v1?label=Language&message=Python%203.8&color=blue&logo=github)](https://github.com/mase-git/spotrends "Go to GitHub repo")
[![build](https://github.com/mase-git/spotrends/workflows/build/badge.svg)](https://github.com/mase-git/spotrends/actions?query=workflow:"build")
[![issues - spotrends](https://img.shields.io/github/issues/mase-git/spotrends)](https://github.com/mase-git/spotrends/issues)
[![License](https://img.shields.io/badge/License-GNU_3.0-blue)](#license)
# Spotrends - Trends Analyser
Spotrends is a tool that helps you analyze the trends and popularity of songs in the Spotify ranking. By using a dataset of track features, Spotrends provides insights into the current state of the music industry and helps you make informed decisions about your music career.

## Features

- Analyze the popularity and engagement of songs in the Spotify ranking.
- Extract track features such as genre, tempo, and instrumentation from the Spotify API.
- Use machine learning algorithms to identify trends and patterns in the data.
- Visualize the data in intuitive charts and graphs.

## Installation

To install Spotrends locally, you will need to have Python 3 and the following dependencies installed on your system:
- [Spotipy](https://spotipy.readthedocs.io/en/latest/)
- [NumPy](https://numpy.org)
- [pandas](https://pandas.pydata.org)
- [scikit-learn](https://scikit-learn.org/stable/)
- [matplotlib](https://matplotlib.org)

Once you have these dependencies installed, you can clone the Spotrends repository and install the remaining dependencies using the following commands:

```
git clone https://github.com/your-username/spotrends.git
cd spotrends
pip install -r requirements.txt
```

## Datasets
To retrieve data, you will need to register for a [Spotify API key](https://developer.spotify.com/documentation/web-api/quick-start/). Once you have obtained an API key, you can use it to retrieves dataset running the main script into the source folder:
```
python3 src/__main__.py
```
Input parameters are specified in artists data source available via [Google Drive](https://drive.google.com/file/d/1ER-uBsnffjsGRjheptpPTPh6VN3tegJ1/view).

## Acknowledgments

We would like to thank the following open-source projects for their contributions to this project:

- [Spotify API](https://developer.spotify.com/documentation/web-api/)

We would also like to thank Spotify for providing access to their API and for their support throughout the development of related projects. 

## License

This project is licensed under the GPT 3.0 license. See [LICENSE](https://github.com/mase-git/spotrends/blob/main/LICENSE) for more information.

The GPT 3.0 license is a permissive license that allows for the use and modification of the licensed software, as long as the original copyright notice and license are included in any copies or derivative works. It is a good choice for open-source projects that want to allow others to use and modify their code without imposing too many restrictions.


