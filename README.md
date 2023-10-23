# Rutilea 選考課題2
## About
Developing an application that uses LLM to select music appropriate to the atmosphere of a given photograph.

## Usage
Run following command in your terminal. Program should be ran in top directory (`Rutilea`).
> python main.py

## Files & Directories
- `main.py` : Toplevel of application.
- `environment.yml` : Requirements for conda environment.
- `src`
    + `spotify.py`
    + `visual_LLM.py`
    + `image_tools.py`
- `img` : Directory to store artwork image while the app is runnning.
- `experiments`

## API Requirements
- OpenAI API key : for using GPT-3.5 as LLM in `src/visual_LLM.py`.
- Spotify Client ID & Secret : for Spotify searching in `src/spotify.py`.

## Links
- [Tasks for Non-AI-native Application](https://docs.google.com/document/d/1BQRDnBziHUUKzwzlD68ZyD3Bq0XrTHt2dYSwgHeLGP8/edit)