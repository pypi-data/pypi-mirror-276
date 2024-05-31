# capdata

python 数据接口

官网地址：https://www.caprisktech.com/

发布到pypi步骤:
1.安装必要的工具 pip install twine setuptools wheel
2.构建包 python setup.py sdist bdist_wheel
3.上传包 twine upload dist/*

使用步骤
#下载capdata库
pip install capdata==1.0.3.1 --index-url https://pypi.org/project/
python
#登录
import data.token as auth
auth.get_token("username", "pwd")
#获取数据
import data.refer as refer
print(refer.get_holidays('CFETS'))