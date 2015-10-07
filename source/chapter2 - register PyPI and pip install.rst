将你的包上传至PyPI, 让用户能使用 pip install 进行安装
====================================================================================================

PyPI的全称是 Python Package Index, 是Python官方社区用于host所有的第三方扩展包, Python软件发布的网站平台。 而Python中用于包管理的工具 ``pip`` 就是他们的官方作品。 而本文的主要目的, 就是详细介绍: 如何使得你的包能够被其他用户使用 ``pip install package-name`` 命令下载安装。

简单来说, 让你的包能被其他用户下载, 一共就两个步骤:

1. 将你的包的相关信息, 根据你的PyPI账户的注册信息, 在PyPI主页上注册。 例如包的名字, 版本号, 分类或是首页的文本信息。

.. code-block:: console

	$ python setup.py register -r pypi

2. 将你的包的源代码内容打包上传。 然后当用户执行: ``pip install package-name`` 时, 就会自动下载这个源码包, 并根据包中的内容自动安装。

.. code-block:: console

	$ python setup.py sdist upload -r pypi

那么我们来详细说明这两步的工作原理, 以及需要注意的地方。


Register
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当用户执行 ``register`` 命令时, Python会首先执行 ``setup.py`` 文件, 然后将 ``name``, ``version`` 等信息上传至PyPI主页。

setup函数中的这些关键字跟 ``register`` 命令相关

- ``name`` 会被作为包名称
- ``version`` 会被作为版本号
- ``author`` 会被作为作者
- ``description`` 会被作为主页文本第一行的短介绍
- ``long_description`` 会被作为主页的 ``.rst`` 格式的长介绍文本。 注意, PyPI首页对 ``.rst`` 格式的容错率较低, 请仔细检查这部分的文本
- ``download_url`` 会被作为用户自定义的源码包的下载链接, 可外链任何载点
- ``classifiers`` 会被作为类别标签的列表。 全部的标签文本请点 `这里 <https://pypi.python.org/pypi?%3Aaction=list_classifiers>`_
- ``platforms`` 会被所谓软件支持的平台的列表
- ``license`` 会被作为软件的版权协议
- ``url`` 会被作为项目主页url

其他关键字是用于安装的, 与PyPI注册无关。


Upload
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当执行 ``upload`` 命令时, 会首先执行 ``python setup.py sdist``, 也就是 source distribute 源码包发布命令, 制作源码包。 这一过程中就会检查 ``MANIFEST.in`` 文件中的内容。

``MANIFEST.in`` 文件是用于指定在上传时, 除了包的源码目录下 (``package-name`` 目录) 的所有文件, 还要包含哪些文件。 例如: ``readme.rst``, ``requirements.txt``, ``LICENSE.txt`` 文件。 因为如果没有 ``readme.rst``, 比如在 ``setup.py`` 文件中定义了 ``long_description`` 关键字的内容指向 ``readme.rst`` 文件, 那么在安装时就会出现不可预料的错误。

同时 ``MANIFEST.in`` 也可以用于手动包含一些数据文件。 值得注意的是, ReadTheDoc网站会需要 ``MANIFEST.in`` 来告诉在 Build 你的文档时, 所需要的文件。

这里有两个常用的MANIFEST文件命令, 我把它列在这里, 作为参考:

.. code-block:: console

	include readme.rst LICENSE.txt requirements.txt # 包括 readme.rst, LICENSE.txt, requirements.txt 三个文件
	recursive-include ctmatching *.txt # 在 ctmatching 的所有文件和子文件夹中的文件中, 包括所有的 .txt 文件

有关 ``MANIFEST.in`` 的详细介绍, 请点 `这里 <https://docs.python.org/2/distutils/sourcedist.html#manifest>`_。


pip install 在什么时候会自动安装所依赖的包
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

跟源码安装不同的是 (源码安装时指 ``python setup.py build``, ``python setup.py install``), pip会比较当前Python环境中的包和 ``requirements.txt`` 文件中所指定的包。 如果两者不匹配, 则pip会尝试进行更新和升级。 这一行为和 ``setup.py`` 文件中的 ``install_requires`` 类似, 所以通常我们会从 ``requirments.txt`` 文件中读取 ``install_requires`` 的内容。


扩展阅读:

- `Creating a Source Distribution <https://docs.python.org/2/distutils/sourcedist.html>`_
- `Creating Built Distributions <https://docs.python.org/2/distutils/builtdist.html>`_
