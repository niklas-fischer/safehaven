# Building a Safe Haven Investment Portfolio

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a **Windows/Linux/Mac** machine running the latest version, because security.
- You have installed the latest versions of **Python** and **Anaconda**. You can download Anaconda [here](https://www.anaconda.com/products/distribution).
- You like maths, Bernouilli, investments and boats.
- You need to get a [Quandl API Key](https://docs.data.nasdaq.com/v1.0/docs/getting-started) and put it into a new file: `touch /notebooks/credentials.txt`

## Installation

Step by step guide on how to install and set up the project locally.

1. Clone the repository: `git clone https://github.com/niklas-fischer/safehaven.git`
2. Navigate to the project directory: `cd safehaven`
3. If Anaconda is not installed, install it from [here](https://www.anaconda.com/products/distribution)
4. Create a new Conda environment: `conda create --name safehaven`
5. Activate the environment: `conda activate safehaven`
6. Install the necessary packages (including Jupyter): `conda install --file requirements.yml`

## Usage

How to use the project once it is set up.

1. Start the Jupyter notebook server: `jupyter notebook`
2. In your web browser, navigate to the URL provided in the command line output (it usually starts with `localhost:`)
3. Open the `main.ipynb` file and have fun

## File Structure

```bash
├── LICENCE
├── modules
│   ├── __init__.py
│   ├── *.py
├── notebooks
│   ├── credentials.txt
│   └── main.ipynb
├── output
│   └── sp500.csv
├── plots
├── README.md
├── requirements.yml
└── tests
```

- `LICENCE`: The license under which the project is released.
- `modules/`: This directory contains Python modules.
   - `__init__.py`: Makes the directory a Python package.
   - `*.py`: Contains the code related to chapters of book
- `notebooks/`: This directory contains the Jupyter notebooks.
   - `credentials.txt`: Contains credentials for _Quandl_. Is not synced with this project.
   - `main.ipynb`: The main Jupyter notebook.
- `output/`: This directory contains the output files of your analysis.
- `plots/`: This directory is intended to contain the plot images created by the project.
- `README.md`: This file.
- `requirements.yml`: A file containing the list of libraries required for installing.
- `tests`: This directory is intended for the test scripts to validate your code.

## License

This project is licensed under the terms of the GNU Affero General Public License v3.0 (AGPL-3.0).

The GNU Affero General Public License is similar to the ordinary GNU GPL, but has an additional term to allow users who interact with the licensed software over a network to receive the source for that program. 

Please see [AGPL-3.0](LICENCE) for detailed license description.

If you use this project in your work, we would appreciate it if you would provide attribution to the original authors.
