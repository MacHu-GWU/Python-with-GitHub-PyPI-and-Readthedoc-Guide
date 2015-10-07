
.. _setup_file_guide:

setup.py文件详解
================================================================================

``setup.py`` 文件是我们在每一个要发布的package项目都必须的。 其中有林林总总的参数需要我们去设置。 固然我们可以手动输入这些参数, 但因为 ``setup.py`` 本身是Python脚本, 所以完全可以通过编程简化重复性的工作。 本项目的 `setup.py模板 <https://github.com/MacHu-GWU/Python-with-GitHub-PyPI-and-Readthedoc-Guide/blob/master/setup.py>`_ 就可以作为一个很好的例子。 

一个好的 ``setup.py`` 文件应该满足满足: ``setup()`` 函数内的参数都绑定到各自的常量上。 每次为新的包写 ``setup.py`` 文件时, 这该模板拷贝过去, 仅仅修改 ``setup()`` 以外的常量部分即可。 常量名称所有字母大写。 这样做能使得编辑起来更容易, 也更清楚。

下面我们来介绍一下 ``setup.py`` 文件中的常用项:

- ``name``: 包名称, 也就是能够通过 ``import name`` 被导入的名字
- ``packages``: 你要安装的包的路径, 例如: ``["canbeAny", "canbeAny.packages"]``
- ``version``: 版本号, 通常在 ``name.__init__.py`` 中以 ``__version__ = "0.0.1"`` 的形式被定义
- ``description``: PyPI首页的一句话短描述
- ``long_description``: PyPI首页的正文
- ``url``: 你的项目主页, 通常是项目的Github主页
- ``download_url``: 你项目源码的下载链接
- ``license``: 版权协议名

下面我来介绍两个新手经常会遇到的问题: 

在使用 ``python setup.py build``, ``python setup.py install`` 时:

1. 包含子包和子包的子包
2. 包含数据文件


Include sub package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认情况下, ``setup.py`` 只会安装在 ``name`` 参数中被定义的包名, 子包是不会被安装的。 如果你的包里面有很多子包, 子包又有很多子包, 手动添加就变得很不明智了。 所幸的是 ``setuptools.find_packages`` 函数就是做这个事的。 我们来看下面的示例代码:

.. code-block:: python
	
	NAME = "canbeAny"
	PACKAGES = [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]
	setup(
		...
		packages=PACKAGES,
		...
	)

	# PACKAGES = ['canbeAny', 'canbeAny.packages', 'canbeAny.packages.subpackage1', 'canbeAny.packages.subpackage2']

``find_packages("dir")`` 的功能是在 "dir" 目录下找所有带有 ``__init__.py`` 的文件夹, 即为package。 如果不指定dir, 那么就在 ``setup.py`` 所在的根目录下查找。 为什么我们要指定 ``NAME`` 为搜索目录呢? 原因很简单, 因为我们在同一级文件夹下可能有我们自己的一些其他测试文件, 也包含 ``__init__.py`` 文件。 这就有可能被误认为是我们要安装的包。 所以我们只在 ``NAME`` 目录下进行搜索, 然后将 ``NAME`` 作为前缀添加即可。


Include package data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

默认build安装包时, 只会编译 ``.py`` 文件。 而有的时候我们的包需要一些无法在 ``.py`` 文件中包含的数据, 例如图片等。 又或者这些常量的数量巨大, 如果以变量的形式放在 ``.py`` 文件中, 解释器解析脚本的速度是远远慢于使用 ``file.open`` 读取例如 ``.csv``, ``.txt`` 文件的速度。 这时候我们就需要一些数据文件随着我们安装我们的程序的同时一起被安装。 

setup函数中与之相关的是两个参数 ``package_dir`` 和 ``package_data``。 如果你是使用的 ``setuptools.setup`` 而不是 ``distutils.setup`` 那么还有另一个参数 ``include_package_data`` 也很有用。 

在 ``canbeAny`` 项目中, 我们有一个txt文件:

.. code-block:: python

	canbeAny
		|--- dataset
			|--- CnetNews.txt
		|--- packages
		|--- __init__.py
		...

如果我们不指定 ``package_dir`` 参数, 那么默认的当前目录就是 ``setup.py`` 文件所在的目录。 请看下面的代码:

.. code-block:: python

	setup(
		...
	    package_data  = {
	        "canbeAny": ["*.txt"], # or "canbeAny": ["dataset/*.data"]
	    },
	    ...
	)

``package_data`` 参数的值是一个字典, 其含义是:

.. code-block:: python

	在当前目录下, 找到 ``canbeAny`` package, 然后里面的所有 ``*.txt`` 文件, 
	包括子文件夹中的文件, 都要被一并添加到安装包中。

package data的其他方法和详细文档请看: https://pythonhosted.org/setuptools/setuptools.html#including-data-files


setup函数参数详解
====================================================================================================


install_requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

指定了在安装这个包时, 需要哪些其他包。 如果条件不满足, 则会自动安装依赖的库。 这个命令在使用: ``python setup.py build``, ``python setup.py install`` 以及 ``pip install xxx`` 时会起作用

.. code-block:: python

	setup(install_requires=["requests"]) # example1
	setup(install_requires=["numpy >= 1.8.1", "pandas >= 0.14.1"]) # example2


setup_requires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

指定了运行 ``setup.py`` 这个文件本身, 需要哪些其他包。 如果不满足, 则会使用 ``EasyInstall`` 尝试下载安装这些依赖库。 换言之, 如果 ``setup.py`` 文件前几行有 ``import xxx`` 类似的代码, 那么这些被import的第三方包就应该被放在 ``setup_requires`` 关键字中。 

注意: 一但 ``setup.py`` 文件被成功运行, 进入安装状态, ``setup_requires`` 关键字中的包是 **不会被自动安装的**。

.. code-block:: python

	setup(setup_requires=["requests"]) # example

Ref: https://pythonhosted.org/setuptools/setuptools.html#new-and-changed-setup-keywords


附录 官方文档链接:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 如何写setup.py文件: https://docs.python.org/2/distutils/setupscript.html
- 了解其他的 meta-data field： https://docs.python.org/2/distutils/setupscript.html#additional-meta-data