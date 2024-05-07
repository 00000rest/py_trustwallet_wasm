import pytest
import trustwasm

def test_known_seed():
    mnemonic = trustwasm.mnemonic_generate(0xc92b023d)
    mnemonic_known = "stick bench smart report motor arrive enter river scale manage viable squeeze" 
    assert mnemonic == mnemonic_known