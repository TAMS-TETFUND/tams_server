.PHONY: black
black:
		black -l 80 *.py
		black -l 80 academicsession/*.py
		black -l 80 attendance/*.py
		black -l 80 course/*.py
		black -l 80 courseregistration/*.py
		black -l 80 department/*.py
		black -l 80 faculty/*.py
		black -l 80 nodedevice/*.py
		black -l 80 staff/*.py
		black -l 80 student/*.py
		black -l 80 tams_server/*.py
		black -l 80 upload/*.py