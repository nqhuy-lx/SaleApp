echo "tai thu vien"
pip install -r requirement.txt

echo "tao du lieu"
python eapp/models.py

echo "run server"
python -m run flask eapp/index.py