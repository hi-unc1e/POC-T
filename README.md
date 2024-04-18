# POC-T: *Pentest Over Concurrent Toolkit*

[![Python 3.9](https://img.shields.io/badge/python-3.9-yellow.svg)](https://www.python.org/) [![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Xyntax/POC-T/master/doc/LICENSE.txt) [![PoC/Scripts](https://img.shields.io/badge/PoC/Scripts-100-blue.svg)](https://github.com/hi-unc1e/POC-T/wiki/%E5%86%85%E7%BD%AE%E8%84%9A%E6%9C%AC%E5%BA%93) 

Roadmap:
- [ ] 兼容pocSuite
- [ ] 兼容Nuclei YAML
- [x] 已兼容Python3.x ! 直接跑。
- [x] PoC更好管理。现支持搜索script/的二级目录了！如`script/weakpass/xxx.py`
  - 依然用`-s xxx.py`调用
  - 文件夹名字不能以`.`/`_`/`-`开头


脚本调用框架，用于渗透测试中 **采集|爬虫|爆破|批量PoC** 等需要并发的任务。  


![banner.png](doc/banner.png) 


脚本收录 
------------------------------------------------------------------
欢迎提交PoC及实用脚本(提PR或邮件联系i@cdxy.me)，您贡献的PoC相关信息将会在以下位置公开。
* [脚本库](https://github.com/Xyntax/POC-T/wiki/%E5%86%85%E7%BD%AE%E8%84%9A%E6%9C%AC%E5%BA%93)
* [致谢](https://github.com/Xyntax/POC-T/wiki/%E8%87%B4%E8%B0%A2)


特点
---
* 支持多线程/Gevent两种并发模式  
* 极简式脚本编写，无需参考文档  
* 内置脚本扩展及常用PoC函数  
* 支持第三方搜索引擎API(已完成ZoomEye/Shodan/Google/Fofa免费版)  


依赖
---
* Python 2.7 / 3.9
* pip
```markdown
python2 ./shodan-python-1.27.0/setup.py install

sudo yum -y install python-devel
```

用户手册
----

* [快速开始](https://github.com/Xyntax/POC-T/wiki/02-%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
* [编写脚本](https://github.com/Xyntax/POC-T/wiki/03-%E7%BC%96%E5%86%99%E8%84%9A%E6%9C%AC)
* [脚本扩展工具](https://github.com/Xyntax/POC-T/wiki/04-%E8%84%9A%E6%9C%AC%E6%89%A9%E5%B1%95%E5%B7%A5%E5%85%B7)
* [第三方搜索引擎](https://github.com/Xyntax/POC-T/wiki/05-%E7%AC%AC%E4%B8%89%E6%96%B9%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E)
* [需求与设计](https://github.com/Xyntax/POC-T/wiki/01-%E9%9C%80%E6%B1%82%E4%B8%8E%E8%AE%BE%E8%AE%A1)

其他
---
* [问题反馈](https://github.com/Xyntax/POC-T/issues/new)
* [版权声明](https://github.com/Xyntax/POC-T/wiki/%E7%89%88%E6%9D%83%E5%A3%B0%E6%98%8E)

联系作者
----
* 原作者（已暂停更新）mail:i@cdxy.me  
* 现作者 mail: root@zuoxueba.org
  
