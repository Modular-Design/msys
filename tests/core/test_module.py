import pytest
from msys.core import Module, Connectable, Type, Option


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
        [Connectable(Type(123))],
    ]
)
@pytest.mark.parametrize(
    "outputs",
    [
        [],
        [Connectable(Type(456))],
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
                {
                    'id': "1",
                    'identifier': ['1'],
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
    module = Module(inputs=[Connectable(Type(123))],
                    sub_modules=[
                        Module(inputs=[Connectable(Type(123))],
                               sub_modules=[],
                               outputs=[Connectable(Type(123))])],
                    outputs=[Connectable(Type(123))])
    assert module.update()
    # assert not module.update()


child0_12 = Module(id=12,
                   inputs=[Connectable(Type(0), 0), Connectable(Type(0), 1)],
                   outputs=[Connectable(Type(0), 2), Connectable(Type(0), 3)], )
child0 = Module(sub_modules=[child0_12], id=0)

child1_5 = Module(id=5,
                  inputs=[Connectable(Type(0), 0), Connectable(Type(0), 1)],
                  outputs=[Connectable(Type(0), 2), Connectable(Type(0), 3)], )
child1 = Module(sub_modules=[child1_5], id=1)

parent = Module(sub_modules=[child0, child1],
                id=0,
                inputs=[Connectable(Type(0), 3), Connectable(Type(0), 4)],
                outputs=[Connectable(Type(0), 5), Connectable(Type(0), 5)])


@pytest.mark.core
@pytest.mark.parametrize(
    "obj, identifier",
    [
        (child0_12, [0, 0, 12]),
        (child1_5, [0, 1, 5]),
        (child0, [0, 0]),
        (child1, [0, 1]),
        (parent, [0]),
    ]
)
def test_identifier(obj, identifier):
    assert obj.identifier() == identifier


@pytest.mark.core
@pytest.mark.parametrize(
    "identifier, correct",
    [
        ([0, 0, 12], child0_12),
        ([0, 1, 5], child1_5),
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
        ([0, 0, 12], [child0_12]),
        ([0, 1, 5], [child1_5]),
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


def test_update_child():
    assert parent.update()


def test_is_tree_positive():
    """

        0 -> 1 -+-> 3 -> 4
                |        A
                v        |
                2 -------+

    """

    child0 = Module(inputs=[Connectable(Type(0))], outputs=[Connectable(Type(0))])
    child1 = Module(inputs=[Connectable(Type(1))], outputs=[Connectable(Type(1))])
    child2 = Module(inputs=[Connectable(Type(2))], outputs=[Connectable(Type(2))])
    child3 = Module(inputs=[Connectable(Type(3))], outputs=[Connectable(Type(3))])
    child4 = Module(inputs=[Connectable(Type(4)), Connectable(Type(4))],
                    outputs=[Connectable(Type(4))])

    Connectable.connect(child0.get_outputs()[0], child1.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child2.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child3.get_inputs()[0])
    Connectable.connect(child2.get_outputs()[0], child4.get_inputs()[0])
    Connectable.connect(child3.get_outputs()[0], child4.get_inputs()[1])

    tree = Module(sub_modules=[child0, child1, child2, child3, child4])
    assert tree.is_tree()


def test_is_tree_negative():
    """

        +----------------+
        |                |
        v                |
        0 -> 1 -+-> 3 -> 4
                |        A
                v        |
                2 -------+

    """

    child0 = Module(inputs=[Connectable(Type(0))], outputs=[Connectable(Type(0))])
    child1 = Module(inputs=[Connectable(Type(1))], outputs=[Connectable(Type(1))])
    child2 = Module(inputs=[Connectable(Type(2))], outputs=[Connectable(Type(2))])
    child3 = Module(inputs=[Connectable(Type(3))], outputs=[Connectable(Type(3))])
    child4 = Module(inputs=[Connectable(Type(4)), Connectable(Type(4))],
                    outputs=[Connectable(Type(4))])

    Connectable.connect(child0.get_outputs()[0], child1.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child2.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child3.get_inputs()[0])
    Connectable.connect(child2.get_outputs()[0], child4.get_inputs()[0])
    Connectable.connect(child3.get_outputs()[0], child4.get_inputs()[1])
    Connectable.connect(child4.get_outputs()[0], child0.get_inputs()[0])

    graph = Module(sub_modules=[child0, child1, child2, child3, child4])
    assert not graph.is_tree()


@pytest.mark.core
@pytest.mark.parametrize(
    "id0, id1, correct",
    [
        ([0, 0], [0, 3], True),
        ([0, 0], [0, 4, 0], True),
        ([0, 4, 0], [0, 1], True),
        ([0, 0], [0, 4], False),
        ([0, 5, 0], [0, 5, 6, 0], True),
    ]
)
def test_connection(id0, id1, correct):
    """

            |             [0,4]                                                                         |
            |   #########################                                                               |
     [0,0]  |   [0,4,0] |       | [0,4,2]                              [0,5]                            |
            |   [0,4,1] |       | [0,4,3]     #######################################################   |   [0,2]
            |                                         |               [0,5,6]               |           |
            |                                 [0,5,0] |     ###########################     | [0,5,3]   |
            |                                 [0,5,1] |     [0,5,6,0] |     | [0,5,6,2]     | [0,5,4]   |
            |                                 [0,5,2] |     [0,5,6,1] |     | [0,5,6,3]     | [0,5,5]   |
     [0,1]  |                                                                                           |   [0,3]
            |                                                                                           |


    """

    mod0_4 = Module(id=4,
                    inputs=[Connectable(Type(0), 0), Connectable(Type(0), 1)],
                    outputs=[Connectable(Type(0), 2), Connectable(Type(0), 3)],
                    sub_modules=[])

    mod0_5_6 = Module(id=6,
                      inputs=[Connectable(Type(0), 0), Connectable(Type(0), 1)],
                      outputs=[Connectable(Type(0), 2), Connectable(Type(0), 3)],
                      sub_modules=[])

    mod0_5 = Module(id=5,
                    inputs=[Connectable(Type(0), 0),
                            Connectable(Type(0), 1),
                            Connectable(Type(0), 2)],
                    outputs=[Connectable(Type(0), 3),
                             Connectable(Type(0), 4),
                             Connectable(Type(0), 5)],
                    sub_modules=[mod0_5_6])

    mod0 = Module(id=0,
                  inputs=[Connectable(Type(0), 0), Connectable(Type(0), 1)],
                  outputs=[Connectable(Type(0), 2), Connectable(Type(0), 3)],
                  sub_modules=[mod0_4, mod0_5])

    obj0 = mod0.find(id0)
    assert obj0
    obj1 = mod0.find(id1)
    assert obj1
    assert mod0.connect(obj0, obj1) == correct


def test_process_tree():
    """

            0 -> 1 -+-> 3 -> 4
                    |        A
                    v        |
                    2 -------+

        """

    def move_min(self):
        print("min")
        min_val = 4
        for input in self.get_inputs():
            val = input.get_value()
            print(val)
            if min_val > val:
                min_val = val
        print("min", min_val)
        self.get_outputs()[0].set_value(min_val)
        return True

    child0 = Module(inputs=[Connectable(Type(0))], outputs=[Connectable(Type(0))])
    child1 = Module(inputs=[Connectable(Type(1))], outputs=[Connectable(Type(1))])
    child2 = Module(inputs=[Connectable(Type(2))], outputs=[Connectable(Type(2))])
    child3 = Module(inputs=[Connectable(Type(3))], outputs=[Connectable(Type(3))])
    child4 = Module(inputs=[Connectable(Type(4)), Connectable(Type(4))],
                    outputs=[Connectable(Type(4))])

    childs = [child0, child1, child2, child3, child4]

    import types
    for child in childs:
        child.process = types.MethodType(move_min, child)

    Connectable.connect(child0.get_outputs()[0], child1.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child2.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child3.get_inputs()[0])
    Connectable.connect(child2.get_outputs()[0], child4.get_inputs()[0])
    Connectable.connect(child3.get_outputs()[0], child4.get_inputs()[1])

    tree = Module(sub_modules=childs)
    assert tree.update()
    assert not tree.update()
    assert child4.get_outputs()[0].get_value() == 0


def test_is_tree_negative():
    """

        +----------------+
        |                |
        v                |
        0 -> 1 -+-> 3 -> 4
                |        A
                v        |
                2 -------+

    """

    def move_min(self):
        print("min")
        min_val = 4
        for input in self.get_inputs():
            val = input.get_value()
            print(val)
            if min_val > val:
                min_val = val
        print("min", min_val)
        self.get_outputs()[0].set_value(min_val)
        return True

    child0 = Module(inputs=[Connectable(Type(0)), Connectable(Type(0))], outputs=[Connectable(Type(0))])
    child1 = Module(inputs=[Connectable(Type(1)), Connectable(Type(1))], outputs=[Connectable(Type(1))])
    child2 = Module(inputs=[Connectable(Type(2))], outputs=[Connectable(Type(2))])
    child3 = Module(inputs=[Connectable(Type(3))], outputs=[Connectable(Type(3))])
    child4 = Module(inputs=[Connectable(Type(4)), Connectable(Type(4))],
                    outputs=[Connectable(Type(4))])

    childs = [child0, child1, child2, child3, child4]

    import types
    for child in childs:
        child.process = types.MethodType(move_min, child)

    Connectable.connect(child0.get_outputs()[0], child1.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child2.get_inputs()[0])
    Connectable.connect(child1.get_outputs()[0], child3.get_inputs()[0])
    Connectable.connect(child2.get_outputs()[0], child4.get_inputs()[0])
    Connectable.connect(child3.get_outputs()[0], child4.get_inputs()[1])
    Connectable.connect(child4.get_outputs()[0], child0.get_inputs()[0])

    graph = Module(sub_modules=childs)

    assert graph.update()
    assert not graph.update()
    assert child4.get_outputs()[0].get_value() == 0