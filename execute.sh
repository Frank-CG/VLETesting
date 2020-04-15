#pip install -r requirements
python3 -m pytest -v -qs -m "scheduler" "./" --html="report.html" --self-contained-html
