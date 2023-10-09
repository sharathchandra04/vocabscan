# vocabscan
vocabpy

setuptools
----------
	setuptools build
	----------------
	python setup.py bdist-wheel

	pip install
	-----------
	pip install dist/grps-0.1-py3-none-any.whl

	command to start server after installing as a pip packge
	--------------------------------------------------------
	grpstart

pyinstaller
-----------
	(check spec.txt for cli.spec configuration)
	pyinstaller cli.py
	(or)
	pyinstaller cli.spec

	command to run cli executable : ./dist/cli/cli

