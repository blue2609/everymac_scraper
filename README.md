# Create virtual environment on your machine

The easiest way is to setup a virtual environment on your machine to run the spider is to use either `conda` or `mamba` package manager and then run either:
- `mamba env create -f environment.yaml` if you're using mamba package manager **(the recommended way)**
- `conda env create -f environment.yaml` if you're using conda package manager

The command above will create `everymac_scraper` mamba/conda virtual environment on your machine. You can then activate the virtual environment with `conda activate everymac_scraper`

# Running the spider

In order to run the spider, navigate to the root directory of the project and then run `scrapy crawl macbook -o <some_output_filename>.csv`

You can see that there are 2 outputs already available inside `output_csv` folder:
- `macbook_pro.csv` contains hardware spec details for all Apple MacBook Pro lineup (MacBook Pro 16", MacBook Pro 15", etc.)
- `macbook.csv` contains hardware spec details for all Apple Macbooks (Macbook 12", Macbook, etc.)

