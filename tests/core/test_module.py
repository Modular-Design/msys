import pytest
from msys.core import Module, Connectable, StandardType, Option


@pytest.mark.core
def test_uniqueness():
    module1 = Module()
    module2 = Module()
    assert module1.id != module2.id


@pytest.mark.parametrize(
    "options",
    [
        [],
        [Option()],
    ]
)
@pytest.mark.parametrize(
    "inputs",
    [
        [],
        [Connectable(StandardType(123))],
    ]
)
@pytest.mark.parametrize(
    "outputs",
    [
        [],
        [Connectable(StandardType(456))],
    ]
)
def test_basics(options, inputs, outputs):
    module = Module(options=options,
                    inputs=inputs, outputs=outputs)
    assert module
    assert module.get_inputs() == inputs
    assert module.get_outputs() == outputs
    assert module.get_options() == options
    assert module.get_childs() == inputs + outputs


@pytest.mark.core
@pytest.mark.parametrize(
    "json, correct",
    [
        (
                {'id': "1",
                 'inputs': [],
                 'metadata': {},
                 'options': [],
                 'outputs': []
                 }, True
        ),
        ({}, False)
    ]
)
def test_serialisation(json, correct):
    module = Module()
    assert module.from_dict(json) == correct
    if correct:
        json2 = module.to_dict()
        assert json == json2


long_opt = Option(id="opt_long", title="Evaluate:", description="""
                                        Enter mathematical Expression!
                                        The input value can be accessed by using the according input name.
                                        """,
                  )
short_opt = Option(id="opt_short", title="Evaluate:", )


@pytest.mark.core
@pytest.mark.parametrize(
    "options",
    [
        [short_opt],
        [long_opt],
        [short_opt, long_opt],
    ]
)
def test_options(options):
    module = Module(options=options)
    assert module
    mdict = module.to_dict()
    assert mdict["options"]
    res = mdict["options"]
    json = []
    for o in options:
        json.append(o.to_dict())
    assert res == json


@pytest.mark.core
def test_update():
    module = Module(inputs=[Connectable(StandardType(123))], outputs=[Connectable(StandardType(123))])
    assert module.update()


child0_0 = Module()
child0_0.from_dict({"id": 0})
child0 = Module(sub_modules=[child0_0])
child0.from_dict({"id": 0})

child1_0 = Module()
child1_0.from_dict({"id": 0})
child1 = Module(sub_modules=[child1_0])
child1.from_dict({"id": 1})

parent = Module(sub_modules=[child0, child1])
parent.from_dict({"id": 0})


@pytest.mark.core
@pytest.mark.parametrize(
    "identifier, correct",
    [
        ([0, 0, 0], child0_0),
        ([0, 1, 0], child1_0),
        ([0, 0], child0),
        ([0, 1], child1),
        ([0], parent),
        ([1], None),
        ([0, 2], None),
        ([0, 1, 1], None),
    ]
)
def test_find(identifier, correct):
    assert parent.find(identifier) == correct

@pytest.mark.core
@pytest.mark.parametrize(
    "identifier, correct",
    [
        ([0, 0, 0], [child0_0]),
        ([0, 1, 0], [child1_0]),
        ([0, 0], [child0]),
        ([0, 1], [child1]),
        ([0], [parent]),
        ([1], []),
        ([0, 2], []),
        ([0, 1, 1], []),
    ]
)
def test_find_all(identifier, correct):
    assert parent.find_all(identifier) == correct