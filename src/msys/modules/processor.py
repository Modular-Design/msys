from msys.core import Processor, Option
from msys.core.connection import Input, Output
from msys.types.vector import VectorType
import time
import math


class Priority:
    def __init__(self, element, time_score=0):
        self.element = element
        self.time_score = time_score
        pass

    def inputs(self):
        return self.element.inputs

    def outputs(self):
        return self.element.outputs

    def update(self) -> bool:
        return self.element.update()

    def eval_tim_score(self, dtime):
        if dtime <= 1:
            dtime = 1
        self.time_score = round(math.log10(dtime))


class DefaultProcessor(Processor):
    def __init__(self):
        self.__opt_prio = Option(id="prio",
                                 title="Priority:",
                                 description="""
                                        Choose a priority with which the modules should be updated!
                                        """,
                                 selection=["static", "dynamic", "time"], default_value=["time"])

        self.__opt_max_iterations = Option(id="iters",
                                           title="Maximum Iterations:",
                                           description="""
                                                Maximum number iteration after the process should definitely terminate.
                                                """,
                                           default_value=1000)

        self.iteration = Output(VectorType([0]))

        super().__init__(inputs=[],
                         outputs=[self.iteration],
                         options=[self.__opt_prio,
                                  ])

    def process(self) -> None:

        # update inputs
        # ->simple
        for i in self.inputs:
            i.update()

        # update modules
        # -> hard
        priority = self.__opt_prio.value[0]

        # manual -> finished
        # with static +:
        module_priority = []
        for m in self.modules:
            module_priority.append(Priority(m))

        # prioities after
        # lowest number of connected inputs
        #   then highest number of connected outputs

        module_priority  = sorted(module_priority, key=lambda module: (module.inputs().get_no_connected(),
                                                                       -module.outputs().get_no_connected()))

        group_changed = True
        iterations = 0
        max_iterations = 5000
        start_from = 0  # part of the optimisation
        while group_changed:
            if iterations > max_iterations:
                break
            ++ iterations
            group_changed = False
            for m_id in range(start_from, len(module_priority)):
                start = time.time()
                changed = module_priority[m_id].update()
                delta_time = time.time() - start
                if priority == "time":
                    module_priority[m_id].eval_tim_score(delta_time)
                if changed:
                    group_changed = True

                # ignore modules which can change only once in the future
                if module_priority[m_id].inputs() == 0:  # TODO inputs is not implemented yet
                    start_from = m_id
                if not (m_id + 1 < len(module_priority)):
                    continue
                if priority == "static" :
                    continue
                # TODO ignore if connected inputs are 0?
                if module_priority[m_id].inputs().get_no_connected() == module_priority[m_id + 1].inputs().get_no_connected():
                    # register inflicted changes
                    for m in module_priority:
                        m.inputs().update_numbers()

                    # priority by:
                    # lower connected inputs
                    # then lower time score
                    # then lowest change counter: connected inputs - input changes
                    # then highest changes
                    # then highest output connections

                    module_priority = sorted(module_priority, key=lambda module: (
                    module.inputs().get_no_connected(),
                    module.time_score,
                    module.inputs().get_no_connected() - module.inputs().get_no_changed(),
                    -module.inputs().get_no_changed(),
                    module.outputs().get_no_connected()))
                    pass

        # update outputs
        # -> simple
        for o in self.outputs:
            o.update()

        pass
