from ..core import Module, Option


class NetworkModule(Module):
    def __init__(self):
        self.__opt_connection = Option(id="connection",
                                       title="Connection-Type:",
                                       description="""
                                                Enter mathematical Expression!
                                                The input value can be accessed by using the according input name.
                                                """,
                                       selection=["HTTP", "HTTPS", "SSH"])

        self.__opt_addr = Option(id="address",
                                 title="Address:",
                                 description="""
                                                Enter the host address:
                                                Examples:
                                                - localhost:8080
                                                - 123.23.123:40
                                                - msys.org/tests/test0
                                                """,
                                 default_value="localhost")

        super().__init__(options=[self.__opt_connection, self.__opt_addr])

    def send_changes(self, changes: dict) -> bool:
        pass

    def get_status(self) -> dict:
        pass

    def from_dict(self, json: dict) -> bool:
        if "inputs" in json.keys():
            print("TODO")
        if not super().from_dict():
            return False
        # update layout

    def process(self) -> None:
        connection = self.__opt_connection.value
        status = self.get_status()
        if not status:
            return False
        if not self.send_changes(self.to_dict()):
            return False
        # external processing

        # test if finished
        status = self.get_status()
        while not status:
            # sleep
            status = self.get_status()

        # update
        self.from_dict(status)
