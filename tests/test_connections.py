import pytest
from mdd.core.connection import Input, Output


@pytest.mark.core
def test_connect_input_output():
    in0 = Input(default_value=[12.90, 14])
    output = Output(default_value=[1, 3])

    def test_disconect(ins, outs):
        outs.disconnect(ins)
        assert outs.get_value() != ins.get_value()

    def test_connect(ins, outs):
        outs.connect(ins)
        assert outs.get_value() == ins.get_value()

    test_disconect(in0, output)
    test_connect(in0, output)
    test_disconect(in0, output)
