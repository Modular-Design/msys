import pytest
from msys.core import Connectable, Type, Connection


@pytest.mark.core
@pytest.mark.connection
def test_connect_input_output():
    in0 = Connectable(Type([12.90, 14]))
    output = Connectable(Type([1, 3]))

    def test_disconect(ins, outs):
        Connection.disconnect(outs, ins)
        ins.set_value(1)
        assert outs.get_value() != ins.get_value()

    def test_connect(ins, outs):
        Connection.connect(outs, ins)
        assert outs.get_value() == ins.get_value()

    def test_connect_ingoing(ins, outs):
        outs.connect_ingoing(ins)
        assert outs.get_value() == ins.get_value()

    def test_disconnect_ingoing(ins, outs):
        outs.disconnect_ingoing()
        ins.set_value(2)
        assert outs.get_value() != ins.get_value()

    def test_connect_outgoing(ins, outs):
        ins.connect_outgoing(outs)
        assert outs.get_value() == ins.get_value()

    def test_disconnect_outgoing(ins, outs):
        ins.disconnect_outgoing()
        ins.set_value(3)
        assert outs.get_value() != ins.get_value()

    test_disconect(in0, output)
    test_connect(in0, output)
    test_disconect(in0, output)
    test_connect_ingoing(in0, output)
    test_disconnect_ingoing(in0, output)
    test_connect_outgoing(in0, output)
    test_disconnect_outgoing(in0, output)


@pytest.mark.core
@pytest.mark.connection
def test_connect_multiple_input_output():
    in2 = Connectable(Type())
    in1 = Connectable(Type())
    in0 = Connectable(Type())
    inputs = [in0, in1, in2]
    output = Connectable(Type([1, 3]))

    def test_disconect(ins, outs):
        outs.disconnect_outgoing()
        for i in range(len(ins)):
            ins[i].set_value(i)
            assert outs.get_value() != ins[i].get_value()

    def test_connect(ins, outs):
        outs.connect_multiple_outgoing(ins)
        for i in ins:
            assert outs.get_value() == i.get_value()

    test_disconect(inputs, output)
    test_connect(inputs, output)
    test_disconect(inputs, output)
    assert output.connect_multiple_outgoing([])

