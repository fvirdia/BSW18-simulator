# BSW18 simulator

**An improved version of this simulator has become [part](https://github.com/fplll/fpylll/blob/master/src/fpylll/tools/bkz_simulator.py) of [fpylll](https://github.com/fplll/fpylll), and should be preferred to the code in this repository.**

This repository contains an implementation of the BKZ simulator proposed in
> _Measuring, simulating andexploiting the head concavity phenomenon in BKZ_  
> Shi Bai, Damien Stehlé, and Weiqiang Wen. ASIACRYPT 2018

It follows the API used by FPyLLL's implementation of the [CN11] simulator, to allow easier integration.

## Instructions

For examples on how to run the simulator, see `test.py` or `rhf.py`.
In order to compare the output with that of the [original implementation](https://github.com/BKZsimulator/probabilistic_simulator), run `make setup` and then run `og.py`.

## References

[CN11] Yuanmi Chen and Phong Q Nguyen. Bkz 2.0: Better lattice security estimates. In ASIACRYPT, 2011.
