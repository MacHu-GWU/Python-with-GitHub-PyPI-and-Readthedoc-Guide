如何将你的Python项目用Github保管, 并在Pypi上发布, 和部署你的在线文档网站
================================================================================

.. image:: http://www.techweekeurope.co.uk/wp-content/uploads/2011/02/Open-Source-Software-.jpg

前言:

	本文提供的演示项目的网址: https://github.com/MacHu-GWU/How-to-release-document-your-open-source-Python-project, 可以用于跟着本文的介绍, 完整地练习一遍。

	- 示例Github项目主页: https://github.com/MacHu-GWU/windtalker
	- 示例PyPI页面: https://pypi.python.org/pypi/windtalker
	- 示例在线文档网站: http://windtalker.readthedocs.org/

正文
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当你开始使用第三方Python扩展包时, 经常看到各种各样的第三方Python扩展包有完整的:

- 项目主页
- Github代码库: https://github.com/
- PyPI页面, 支持pip下载: https://pypi.python.org/
- 漂亮的在线文档网站: https://readthedocs.org/

很羡慕是不是? 别着急, 本文就是要详细地介绍在项目开发完成之后, 用Github保管你的代码, 如何添加到Pypi, 部署你的在线文档网站。更进阶地, 还要教会你如何在版本更新时, 用最少的工作更新这些事情。

一个组织良好的Python扩展包项目的文件结构看起来应该是这样的:

.. code-block:: console

	<project_name> # 项目名称
		|--- build # setup.py 生成的build文件, sphinx生成的html网站
		|--- source # document 源代码
		|--- tests # 单元测试 (可选)
		|--- <package_name> # 你开发的扩展包的名字, 你的Python代码都在这里了
		|--- LICENSE.txt # 版权信息
		|--- requirements.txt # 为pypi提供了所依赖的其他包的信息
		|--- setup.cfg # setup的额外配置信息
		|--- setup.py # 安装文件
		|--- readme.rst (or readme.md) # github, pypi项目主页说明文档
		|--- make.bat # sphinx用于生成网站的批处理文件

另外地, 出于个人开发方便起见, 有一些自定义的文件, 目前就不进行详细介绍了。

.. code-block:: console

	<project_name>
		|--- create_doctree.py # 用于生成 module and index
		|--- build_doc.bat # 用于一键重新安装package, 执行create_doctree.py, 执行make.bat
		|--- view_doc.bat # 用于一键打开build好的网站主页


使用Github保管你的代码库
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://blog.kanbanize.com/wp-content/uploads/2014/11/GitHub.jpg

如何使用Github管理你的代码版本, 并不在本文的讨论范围之内, 请自行咨询 `谷神 <www.google.com>`_, `度娘 <www.baidu.com>`_。

Github提供了一个 `release <https://help.github.com/articles/creating-releases/>`_ 功能, 其功能是将你当前Commit的代码库打包成一个 ``.zip`` 和 ``.tar.gz`` 文件, 并加上标签。然后其他人就可以通过 ``https://github.com/<username>/<project_name>/archive/<tag>.zip`` 进行下载了。所以在PyPI页面或者其他页面, 只要你附上这个链接, 别人就可以直接下载你的源代码。在 ``setup.py`` 中专门有一项 ``download_url`` 就是起这个作用的。这个下载链接在之后的PyPI页面中会用到。

具体管理tag的方法, 你可以使用:

1. Github网页界面: ``Github repository`` -> ``release`` (推荐)。
2. 在github shell中使用 ``$ git tag ...`` 命令。在git中管理tag请参考: https://git-scm.com/book/en/v2/Git-Basics-Tagging


创建你的setup.py文件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://avatars3.githubusercontent.com/u/13561481?v=3&s=96

很久以前Python社区为了让大家能够更佳容易地发布自己的开源扩展包, 所以在标准库中包含了 `distutils <https://docs.python.org/2.7/library/distutils.html#module-distutils>`_ 库帮助用户distribute自己的扩展包。

在PyPI社区壮大, 成为Python扩展包的主发布社区后, 出现了 `pip <https://pypi.python.org/pypi/pip>`_ 这一跨平台的工具使得用户进行管理自己的Python第三方包变得异常轻松。在用户安装 ``pip`` 时, 另一个强大的工具 `setuptools <https://pypi.python.org/pypi/setuptools>`_ 也会被自动安装。这一工具不仅是 ``pip`` 所依赖的, 而且可以替代 ``distutils``, 用更简单的方式完成更复杂的工作。

- 如何写setup.py文件: https://docs.python.org/2/distutils/setupscript.html

关于setup.py文件的详细介绍, 我会在我的另一篇文章中详细陈述。


部署你的项目在PyPI上的主页
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://pbs.twimg.com/profile_images/104712585/pypi_twitter_400x400.jpg

我们以 `requests <https://pypi.python.org/pypi/requests>`_ 这一Python社区最流行的http扩展包(作者是Python社区顶级大牛, 他的项目值得每一个Python开发者作为教科书来学习, 无论是代码还是文档)为例进行解说。

首先我们来看看PyPI页面有哪几个主要元素?

1. Long Description, 一段长的文本介绍, 介绍你的扩展包的所有相关信息。

	这部分用 `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ 标记语言所写成。通常使用 ``readme.rst`` 文件中的内容, 同时也通常被作为github主页的页面。值得注意的是, **这部分内容中使用的是纯rst文件所支持的语法。并不支持sphinx中所支持的特殊语法。**

2. File, 用户可下载的文件。

	这部分默认会包含一个源代码包, 通常文件名是 ``<package_name>-<version>.tar.gz``。这部分是当用户使用 ``pip install package_name`` 时所下载的源码包, 然后 ``pip`` 会自动完成 `build, install <https://docs.python.org/2/install/#splitting-the-job-up>`_, clean up的全过程。	这个源码包的生成是自动的, 具体原理在下一节中介绍。

	同时用户还可以自己上传一些其他格式的安装文件, 比如: ``.egg``, ``.whl``, ``.zip``, ``.exe``(用于windows下的安装)。我们可以通过命令:

	.. code-block::

		$ python setup.py sdist upload -r pypi

	上传, 也可以登录你的PyPI, 找到你的包, 然后使用网页界面手动上传。其他安装包的制作和上传, 请参考: `The Python Package Index (PyPI) <https://docs.python.org/2/distutils/packageindex.html>`_

3. MetaData, 其他相关信息。

	这里存放的是你在 ``setup.py`` 文件中填写的例如: Author, Home Page, Lisence。这部分可以在 ``setup.py`` 中定义, 也可以在PyPI网站界面进行手动填写。

	了解其他的 meta-data field `请戳这里 <https://docs.python.org/2/distutils/setupscript.html#additional-meta-data>`_

当用户完成了 ``setup.py`` 文件的制作之后, 就可以将这些信息**注册到PyPI了**。具体做法是在命令行中输入如下命令:

.. code-block:: console
	
	$ python setup.py register -r pypi

第一次注册时, 会需要你的PyPI账号密码, 然后系统会在你的操作系统用户根目录下生成一个.pypirc文件, 里面包含了你的身份信息。在同一台机器同一个账户, 以后就不会需要输入账号密码了。


让你的包能通过 ``pip install`` 被安装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://caligari.treboada.net/public/img/posts/python-pip-and-the-staff-group-a.png

如果你有仔细阅读上一节的内容, 其实在 **File** 部分中所提到的一个默认的源代码包。(可以没有其他 ``.whl``, ``.exe`` 但一定会有的源码包)。使用下面的命令所上传的安装包是带有版本信息记录的, 只要你上传过一次, 就会在PyPI服务器上留下记录, 以同样的软件版本号无法再次上传。当开发流程熟悉稳定之后, 用户可以使用 ``upload`` 命令上传所有种类的安装包。但我推荐新手自己build安装包, 然后针对一个版本号在网页界面进行手动上传, 删除管理。

为防止忘记, 附上上传默认源码安装包的命令:

.. code-block:: console
	
	$ python setup.py sdist upload -r pypi


部署你的文档网站
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://blog.huangz.me/_images/readthedocs-logo.png

在 `sphinx <http://sphinx-doc.org/>`_ 的帮助下, 我们完全可以将生成的静态网页部署在自己的网站上。例如 `Amazon Web Service S3 <http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html>`_ 就是一种很方便很便宜的选择。既然如此, 那 https://readthedocs.org/ 的好处是什么呢?

1. 完全免费。
2. 自动关联Github账户, 当有更新时, 自动更新网站。
3. 同时维护多个版本的文档。让使用老版本用户也能看到老版本的文档。
4. 可以关联google analytic, 追踪访问量。

如果使用自己的网站, 每当你有更新时, 你都要更新你的网页文件。而如果使用readthedoc, 当你的source目录内的文件在Github上有更新, readthedoc会自动检测到更新, 并重新build所有页面。所以你所要做的就是在commit之前, 在本地使用 ``make_html.bat`` build一次网页, 确认无误之后更新到github即可。

**注意:** 如果你的包对其他第三方包的依赖较大, 那么就需要设置requirements.txt, 以及virtual environment。requirements.txt告诉readthedoc在build的时候要安装哪些依赖的包, virtual env能配置出合适的虚拟环境。这是因为sphinx在build网页的时候, 要保证包里所有的模块都是可以被import的。这算是使用readthedoc的一个不好的地方吧。


Readthedoc简明介绍
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 问: 我申请了readthedoc账号, 第一件事要做什么?

	从github导入你的项目。具体方法是: 

	1. 登陆你的github, 进入你的github repository
	2. settings -> webhooks & service -> add readthedoc
	3. 回到readthedoc, Import a project -> Import from github -> 找到你的项目 -> Create

- 问: 我已经导入了我的项目了, 那怎么让readthedoc开始生成我的文档网站?

	首先你要进行一些设置, 告诉readthedoc一些信息: 

	1. 进入你的readthedoc project
	2. 进入Admin菜单
	3. 进入Setting菜单
	4. 指定Programming language = Python。(我们都是大蟒蛇~)
	5. 进入Advance菜单
	6. 如果你的包依赖其他第三方库, 请勾选: Install your project inside a virtualenv using setup.py install. 并指定requirement file, 通常为 ``requirements.txt``。这样在尝试Build网站时, readthedoc就会使用 ``pip`` 把 ``requirements.txt`` 中的包都安装了。
	7. 如果你只想要保留最新的文档(通常需要保证你的库向下兼容), 请勾选: Single version
	8. 在 Python configuration file: 一栏中填写从项目目录到 Sphinx 的 ``conf.py`` 的路径。这样readthedoc才能找到你的文档放在哪里了。
	9. 在 Python interpreter 中选择Python2/3。保持这个和你开发时测试所使用的一致。
	10. 如果想要用Google Analytic, 填写 Analytics Code

	然后回到readthedoc project页面, 进入Build菜单, 如果还没有开始自动Build, 则点击Build。如果发生Failed, 点击Failed查看错误信息。如果Passed, 恭喜你, 可以点击View Docs浏览你的文档了!

**至此, 你应该可以顺利的完成, 源代码保管在github, 在pypi发布你的扩展包, 支持pip install安装和发布你的在线文档网站了。撒花, 撒花!**

.. image:: http://www.appguru.com.tw/appguru/apps/files/2012/10/A_006_300dpi1.gif

CopyRight: Sanhe Hu 2015, 转载请注明出处

