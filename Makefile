setup: clean
	git clone https://github.com/fvirdia/probabilistic_simulator
	cd probabilistic_simulator; git checkout fb23bbe; touch __init__.py; mv probabilistic_bkz_simulator.sage probabilistic_bkz_simulator.py

clean:
	rm -rf probabilistic_simulator