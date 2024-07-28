cat requirements.txt | sed -e '/^\s*#.*$/d' -e '/^\s*$/d' | xargs -n 1 pip install
python -m scrape_and_process.scrapers
python -m scrape_and_process.price_predict