第四节, 为你的项目写一个版本历史信息文件
================

在开始之前, 先来说说版本号吧。

关于版本号的命名, 请参考这篇文章: `Semantic Versioning <http://semver.org/>`_。 总的来说形如 Major.Minor.Patch 的版本号格式遵循下面三点:

- 大版本号指你做了某些API不兼容的改动
- 小版本号指你增加了新的功能, 并且向后兼容
- 补丁号指你做了向后兼容的补丁修改

在每次更新你的项目版本号时, 写明做了哪些改动和更新是一个好习惯。 一个好的 Release History 文件需要具有下面列出的几个元素:

1. 版本号和发布日期
2. 新功能和改进
3. 次要改进
4. Bug修复
5. 杂项

A release and version history log file usually have these elements:

1. version number and release date
2. Features and Improvements
3. Minor Improvements
4. Bugfixes
5. Miscellaneous


下面是一个版本历史文件的模板的源码::

	Release and Version History
	===========================


	0.1.0 (2016-02-01)
	~~~~~~~~~~~~~~~~~~
	**Features and Improvements**

	- balabala


	0.0.2 (2016-01-15)
	~~~~~~~~~~~~~~~~~~
	- Birth!


	0.0.1 (2016-01-01)
	~~~~~~~~~~~~~~~~~~
	- Frustration
	- Conception