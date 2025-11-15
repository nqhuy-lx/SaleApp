echo "tai thu vien"
pip install -r requirement.txt

echo "tao du lieu"
python eapp/model.py

echo "run server"
python -m run flash eapp/index.py