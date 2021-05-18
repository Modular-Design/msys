import pytest
from msys.core.connection import Input, Output, StandardType


@pytest.mark.core
@pytest.mark.connection
def test_connect_input_output():
    in0 = Input(StandardType([12.90, 14]))
    output = Output(StandardType([1, 3]))

    def test_disconect(ins, outs):
        outs.disconnect(ins)
        assert outs.get_value() != ins.get_value()

    def test_connect(ins, outs):
        outs.connect(ins)
        assert outs.get_value() == ins.get_value()

    test_disconect(in0, output)
    test_connect(in0, output)
    test_disconect(in0, output)
