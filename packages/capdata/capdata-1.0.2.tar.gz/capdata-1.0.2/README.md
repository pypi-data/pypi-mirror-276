# capdata

python 数据接口

官网地址：https://www.caprisktech.com/


发布到pypi步骤:
1.安装必要的工具 pip install twine setuptools wheel
2.构建包 python setup.py sdist bdist_wheel
3.上传包 twine upload dist/*

pip install capdata==1.0.1 --index-url https://pypi.org/project/