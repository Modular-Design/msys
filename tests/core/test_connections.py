import pytest
from msys.core import Connectable, StandardType


@pytest.mark.core
@pytest.mark.connection
def test_connect_input_output():
    in0 = Connectable(StandardType([12.90, 14]))
    output = Connectable(StandardType([1, 3]))

    def test_disconect(ins, outs):
        Connectable.disconnect(ins, outs)
        ins.set_value([23, 1223])
        assert outs.get_value() != ins.get_value()

    def test_connect(ins, outs):
        Connectable.connect(ins, outs)
        assert outs.get_value() == ins.get_value()

    test_disconect(in0, output)
    test_connect(in0, output)
    test_disconect(in0, output)
