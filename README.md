<!-- PROJECT TITLE -->
<h1 align="center">TI4 Mapmaker API</h1>

<!-- PROJECT BLURB -->
<p align="center">
  <em>API for the Twilight Imperium 4 Mapmaker map generator website</em>
</p>

<!-- PROJECT SHIELDS -->
<div align="center">
  <a href="https://github.com/solbero/ti4-mapmaker-api/actions/workflows/build.yaml/" target="_blank">
    <img src="https://img.shields.io/github/actions/workflow/status/solbero/ti4-mapmaker-api/build.yaml?branch=main&label=build" alt="Build action">
  </a>
  <a href="https://github.com/solbero/ti4-mapmaker-api/actions/workflows/publish.yaml/" target="_blank">
    <img src="https://img.shields.io/github/actions/workflow/status/solbero/ti4-mapmaker-api/publish.yaml?branch=main&label=publish" alt="Publish action">
  </a>
  <a href="https://app.codecov.io/gh/solbero/ti4-mapmaker-api" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/solbero/ti4-mapmaker-api" alt="Code coverage">
  </a>

  <a href="https://github.com/solbero/ti4-mapmaker-api/releases" target="_blank">
    <img src="https://img.shields.io/github/v/release/solbero/ti4-mapmaker-api" alt="Release version">
  </a>
  <a href="https://github.com/solbero/ti4-mapmaker-api/blob/master/LICENSE.txt" target="_blank">
    <img src="https://img.shields.io/github/license/solbero/ti4-mapmaker-api" alt="License">
  </a>
</div>

<!-- ABOUT THE PROJECT -->
## About the Project

This is the API for the TI4 Mapmaker map generator website. The API can be queried for information about maps, factions and tiles in the board game Twilight Imperium 4.

The project is a [FastAPI](https://fastapi.tiangolo.com/) application which is deployed at [Deta](https://www.deta.sh/) using their Micro and Base services.

<!-- PREREQUISITES -->
## Prerequisites

You must have the following programs installed:
  * Python 3.9
  * [Poetry](https://python-poetry.org/docs/#installation)
  * [Deta CLI](https://docs.deta.sh/docs/cli/install)

<!-- INSTALLATION -->
## Installation

Clone the repository,
  ```sh
  git clone https://github.com/solbero/ti4-mapmaker-api.git
  ```

move into the project directory,
  ```sh
  cd ti4-mapmaker-api
  ```

and install the project.
  ```sh
  poetry install
  ```

Then, create a Deta Micro for the project
  ```sh
  deta new --python
```

and a `.env` file in the project's root directory. Paste in
  ```
  DETA_PROJECT_KEY=<deta-project-key>
  ```
and replace `<deta-project-key>` with your Deta project credentials.


<!-- RUNNING -->
## Running

To run the project locally
  ```sh
  poetry run python main.py
  ```

<!-- TESTING -->
## Testing

To run the project's testing suite
  ```sh
  poetry run pytest
  ```

<!-- DEPLOYMENT -->
## Deployment

To deploy the project to Deta Micro
```sh
deta deploy
```

<!-- CONTRIBUTIONS -->
## Contributions

  * Gamedata from [TI4 Generator](https://github.com/KeeganW/ti4) by [KeeganW](https://github.com/KeeganW)

<!-- CONTACT -->
## Contact

* Email: [njord.solberg@gmail.com](mailto:njord.solberg@gmail.com)

<!-- PROJECT LINKS -->
## Project Links

* Github: [https://github.com/solbero/ti4-mapmaker-api](https://github.com/solbero/ti4-mapmaker-api)

<!-- LICENSE -->
## License

Distributed under the GPLv3 License.
See [`LICENSE.txt`](https://github.com/solbero/hexpex/blob/master/LICENSE.txt) for more information.
