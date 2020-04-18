#pip install -r requirements

python3 -m pytest -v -qs -m "scheduler" "./" --html="report.html" --self-contained-html


python3 -m pytest -v -qs -m "scheduler_cur" "./" --html="report.html" --self-contained-html
