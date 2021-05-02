import pytest
from mdd.core.connection import Input, Output

@pytest.mark.core
def test_connect_input_output():
    in0 = Input(default_value=[12.90, 14])
    output = Output(default_value=[1, 3])

    def test_disconect(input, output):
        output.disconnect(input)
        assert output.value() != input.value()

    def test_connect(input, output):
        output.connect(input)
        assert output.value() == input.value()

    test_disconect(in0, output)
    test_connect(in0, output)
    test_disconect(in0, output)
