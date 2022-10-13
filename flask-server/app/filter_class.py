import app.event_log as event_log
import random

SEED = 10


class Filter:

    def __init__(self, parameters) -> None:
        self.parameters = parameters
        self.name = "NAME not DEFIEND"

    def filter(self, eventLog) -> event_log.EventLog:
        pass

    def getName(self) -> str:
        name = self.name
        for parameter in self.parameters:
            name += " " + parameter
        return name

    def getDict(self):
        return {"filterName": self.name, "activityName": self.parameters}

    def __hash__(self):
        return hash((self.name, *self.parameters))

    def __eq__(self, filter) -> bool:
        return self.name == filter.name and self.parameters == filter.parameters

    def get_function(self) -> str:
        pass

    def get_comment(self) -> str:
        pass

    def parameters_to_string(self):
        string = ""
        for parameter in self.parameters:
            string += " and " + parameter
        return string

    @staticmethod
    def generateFilter(parameters):
        pass


class FilterOut(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "filterOut"

    def filter(self, eventLog):
        indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            bool_list = [True for _ in range(len(self.parameters))]
            for event in trace.events:
                for i, par in enumerate(self.parameters):
                    if event.activity == par:
                        bool_list[i] = False
            if sum(bool_list) == 0:
                indicesToRemove.append(count)
        eventLog.removeTraces(indicesToRemove)
        return eventLog

    def get_function(self, varnumber):
        return """indicesToRemove = []
for count, trace in enumerate(eventLog.traces):
    bool_list = [True for _ in range(len(filterout{}))]
    for event in trace.events:
        for i, par in enumerate(filterout{}):
            if event.activity == par:
                bool_list[i] = False
        if sum(bool_list) == 0:
            indicesToRemove.append(count)
eventLog.removeTraces(indicesToRemove)""".format(varnumber, varnumber), ["filterout{}".format(varnumber)], [self.parameters]

    def get_comment(self):
        return f"#This filters out traces {self.parameters_to_string()}."

    @staticmethod
    def generateFilter(parameters):
        return FilterOut(parameters)


class ThroughPut(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "throughPut"

    def filter(self, eventLog):
        event_a = self.parameters[0]
        event_b = self.parameters[1]
        throughputtime = self.parameters[2]
        mode = self.parameters[3]

        indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = False
            time_a = 0
            for event in trace.events:
                if event.activity == event_a:
                    if mode == "longer":
                        if time_a == 0:
                            time_a = event.time
                    else:
                        time_a = event.time
                elif event.activity == event_b:
                    if mode == "longer":
                        if (time_a != 0 and event.time - time_a > int(throughputtime)):
                            keep = True
                            break
                    else:
                        if (time_a != 0 and event.time - time_a < int(throughputtime)):
                            keep = True
                            break
            if not keep:
                indicesToRemove.append(count)
        eventLog.removeTraces(indicesToRemove)
        return eventLog

    def get_function(self, varnumber):
        return """indicesToRemove = []
for count, trace in enumerate(eventLog.traces):
    keep = False
    time_a = 0
    for event in trace.events:
        if event.activity == event_a{}:
            if mode{} == "longer":
                if time_a == 0:
                    time_a = event.time
            else:
                time_a = event.time
        elif event.activity == event_b{}:
            if mode{} == "longer":
                if (time_a != 0 and event.time - time_a > int(throughputtime{})):
                    keep = True
                    break
            else:
                if (time_a != 0 and event.time - time_a < int(throughputtime{})):
                    keep = True
                    break
    if not keep:
        indicesToRemove.append(count)
eventLog.removeTraces(indicesToRemove)""".format(varnumber, varnumber, varnumber, varnumber, varnumber, varnumber), ["event_a{}".format(varnumber), "throughputtime{}".format(varnumber), "event_b{}".format(varnumber), "mode{}".format(varnumber)], ["\""+self.parameters[0]+"\"", self.parameters[2], "\""+self.parameters[1]+"\"", "\""+self.parameters[3]+"\""]

    def get_comment(self):
        return f"#This filters out traces based on throughput time with the following parameters: {self.parameters_to_string()}."

    @staticmethod
    def generateFilter(parameters):
        return ThroughPut(parameters)


class FlowSelection(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "flowSelection"

    def filter(self, eventLog):
        event_a = self.parameters[0]
        event_b = self.parameters[1]

        indicesToRemove = []
        for count, trace in enumerate(eventLog.traces):
            keep = False
            previous_event = None
            for event in trace.events:
                if previous_event is not None and previous_event.activity == event_a and event.activity == event_b:
                    keep = True
                    break
                previous_event = event
            if not keep:
                indicesToRemove.append(count)
        eventLog.removeTraces(list(set(indicesToRemove)))
        return eventLog

    def get_function(self, varnumber):
        return """indicesToRemove = []
for count, trace in enumerate(eventLog.traces):
    keep = False
    previous_event = None
    for event in trace.events:
        if previous_event is not None and previous_event.activity == event_a{} and event.activity == event_b{}:
                keep = True
                break
        
        previous_event = event
    if not keep:
        indicesToRemove.append(count)
eventLog.removeTraces(indicesToRemove)""".format(varnumber, varnumber), ["event_a{}".format(varnumber), "event_b{}".format(varnumber)], ["\""+self.parameters[0]+"\"", "\""+self.parameters[1]+"\""]

    def get_comment(self):
        return f"#This filters out traces that do not have the directly follow pattern between {self.parameters[0], self.parameters[1]}."

    @staticmethod
    def generateFilter(parameters):
        return FlowSelection(parameters)


class RemoveBehavior(Filter):

    def __init__(self, parameters):
        super().__init__(parameters)
        self.name = "removeBehavior"

    def filter(self, eventLog):
        remove = self.parameters[0]
        random.seed(SEED)
        total = eventLog.get_total_number_events()
        sample = random.sample(range(total), int(total * float(remove)))
        sample.sort()
        seen_events = 0
        for ti, trace in enumerate(eventLog.traces):
            sample_trace = [i for i in sample if i >=
                            seen_events and i < seen_events + len(trace.events)]
            sample_trace = [number - seen_events for number in sample_trace]
            seen_events += len(trace.events)
            trace.removeEvents(sample_trace)
        eventLog.remove_empty_traces()
        return eventLog

    def get_function(self, varnumber):
        return """random.seed(SEED)
total = eventLog.get_total_number_events()
sample = random.sample(range(total), int(total * float(remove{})))
sample.sort()
seen_events = 0
for ti, trace in enumerate(eventLog.traces):
    sample_trace = [i for i in sample if i>=seen_events and i<seen_events + len(trace.events)]
    sample_trace = [number - seen_events for number in sample_trace]
    seen_events += len(trace.events)
    trace.removeEvents(sample_trace)
eventLog.remove_empty_traces()""".format(varnumber), ["remove{}".format(varnumber)], self.parameters

    def get_comment(self):
        return f"#This filters out {self.parameters[0]} of each trace."

    @staticmethod
    def generateFilter(parameters):
        return RemoveBehavior(parameters)
