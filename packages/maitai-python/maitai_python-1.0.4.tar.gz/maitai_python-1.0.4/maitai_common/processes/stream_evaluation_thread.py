import maitai
from maitai_common.processes.io_thread import IOThread


class StreamEvaluationThread(IOThread):
    def __init__(self):
        super(StreamEvaluationThread, self).__init__(interval=0.01)
        self.input = []
        self.output = []

    def process(self):
        if len(self.input) == 0:
            return
        input_list = self.input
        self.input = []
        session_id, reference_id, action_type, content_type, proto_messages, application_ref_name, partial = input_list.pop()
        result = maitai.Evaluator.evaluate(session_id, reference_id, action_type, proto_messages, content_type=content_type, application_ref_name=application_ref_name, partial=partial)
        if len(result.evaluation_results) > 0:
            if result.evaluation_results[0].status == "FAULT":
                self.output = result

    def print(self, *args, **kwargs):
        pass
