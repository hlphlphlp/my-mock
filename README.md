推荐版本：
python==3.7
pytest>=3.5.0
flask>=1.0

安装步骤：
1、python setup.py build
2、python setup.py install

################################
部署gunicorn：
1、安装gunicorn
pip install gunicorn
2、开启后台运行
gunicorn -w 8 -b :5000 run:app --daemon
################################