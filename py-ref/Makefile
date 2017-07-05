test.out: test.py Gimli.py
	python3 test.py > test.out
	cmp test.out test.exp

clean:
	@echo cleaning...
	@rm test.out 2> /dev/null || true
	@rm __pycache__ 2> /dev/null || true
