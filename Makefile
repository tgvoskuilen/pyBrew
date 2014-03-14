clean:
	find . -name '*~' -delete
	find . -name '*.pyc' -delete
	rm -rf build
	rm -rf dist
	rm -f pyBrew.exe
