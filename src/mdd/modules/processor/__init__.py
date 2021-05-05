from ...core import Processor, Option
from ...core.connection import Input, Output
import time
import math


class DefaultProcessor(Processor):
    def __init__(self):
        self.__opt_prio = Option(id="prio",
                                 title="Priority:",
                                 description="""
                                        Choose a priority with which the modules should be updated!
                                        """,
                                 selection=["manual", "static", "dynamic", "time"], default_value=["time"])

        self.__opt_max_iterations = Option(id="iters",
                                           title="Maximum Iterations:",
                                           description="""
                                                Maximum number iteration after the process should definitely terminate.
                                                """,
                                           default_value=1000)

        super().__init__(inputs=[],
                         outputs=[Output()],
                         options=[self.__opt_prio,
                                  ])

    def process(self) -> None:
        # update inputs
        # ->simple

        # update modules
        # -> hard
        priority = "manual"

        # manual -> finished
        # with static +:
        # prioities after
        # lowest number of connected inputs
        #   then highest number of connected outputs
        class Priority:
            def __init__(self, element, time_score=0):
                self.element = element
                self.time_score = time_score
                pass

            def update(self) -> bool:
                return self.element.update()

            def eval_tim_score(self, dtime):
                self.time_score = round(math.log10(dtime))

        module_priority = []
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
                if priority != "dynamic" or priority != "time":
                    continue
                # TODO ignore if connected inputs are 0?
                if module_priority[m_id].inputs() == module_priority[m_id + 1].inputs():
                    # register inflicted changes

                    # priority by:
                    # lower connected inputs
                    # then lower time score
                    # then lowest change counter: connected inputs - input changes
                    # then highest changes
                    # then highest output connections
                    pass

        # update outputs
        # -> simple

        pass
