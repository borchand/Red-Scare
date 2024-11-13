from Utils.ReadInput import ReadFile
from prettytable import PrettyTable
import Utils.data_files as files
import Utils.task_names as tasks_names
from many import solve_many 
from nizp_resy_alternate import has_alternating_path
from tqdm import tqdm
import networkx as nx
import time
import pandas as pd
import os


from Some import someFlowPathRed, readInputSome

class Tasks:
    """
    Summary:
        This class contains the tasks for the Red Scare assignment.
        The tasks are:
            - few : Return the minimum number of red vertices on any path from s 
    """
    def __init__(self, path: str) -> None:
        self.path = path
        self.data = ReadFile(path)

    def none(self):
        pass

    def alternate(self) -> bool:
        graph = self.data.toGraph().nxGraph
        # Create dictionary of red nodes, ensuring node names match graph nodes
        color_of_nodes = {}
        for node in self.data.nodes:
            # Clean up node name to match graph representation
            color_of_nodes[node] = node.is_red
        return has_alternating_path(graph, color_of_nodes, self.data.s, self.data.t)

    def some(self) -> tuple[bool, bool]:
        readFile, gnx, source, sink, reds = readInputSome(self.path)
        return someFlowPathRed(readFile, gnx, source, sink, reds)

    def many(self) -> tuple[int, bool]:
        return solve_many(self.data)

    def few(self, draw : bool = False) -> int:
        """
        Return the minimum number of red vertices on any path from s
        to t. To be precise, let P be the set of s, t-paths and let r(p) denote
        the number of red vertices on a path p. Return min{r(p): p ∈ P }.
        If no path from s to t exists, return ‘-1’. In Gex, the answer is 0
        (because of the path 0, 1, 2, 3.)

        Inputs
            <b>draw (bool)</b>: If True, draw the graph
        """
        weightedGraph = self.data.toWeightedGraph(1, 0)

        G = weightedGraph.nxGraph

        if draw:
            weightedGraph.draw()

        try:
            return nx.dijkstra_path_length(G, self.data.s, self.data.t, weight='weight')
        except (nx.NodeNotFound,  nx.NetworkXNoPath):
            return -1

class RunTask:
    """
    Summary:
        This class is used to run a task on all the network data files.
        The results are saved in a csv file in the results folder.
        This will overwrite the csv file if it already exists.

        There is a timeout of 10 minutes for each task. If the task takes more than 10 minutes, it will be interrupted and the result will be "Timeout".

    Inputs:
        <b>task (str)</b>: The task to run (None, Alternate, Some, Many, Few)
        You can use the tasks_names.py file to get the task names
        <b>min_before_interrupt (int)</b>: The time in minutes before the task is interrupted (default is 10 minutes)

    Variables:
        <b>task (str)</b>: The task to run
        <b>networkDataFiles (list)</b>: List of network data
        <b>min_before_interrupt (int)</b>: The time in minutes before the task is interrupted (default is 10 minutes)

    Methods:
        <b>run</b>: Run the task (this is in the constructor)

    """
    def __init__(self, task: str, min_before_interrupt = 10) -> None:
        self.networkDataFiles = [getattr(files, attr) for attr in dir(files) if not attr.startswith('__')]
        self.min_before_interrupt = min_before_interrupt

        self.task = task
        self.run()

    def run(self) -> None:

        if not self.task:
            raise Exception("Task not specified")

        results = []
        print(f"Running task: {self.task}")
        
        for filename in tqdm(self.networkDataFiles):
            start_time = time.time()
            tasks = Tasks(filename)
            num_nodes = tasks.data.num_nodes

            result = None
            np_hard = None
            if self.task == tasks_names.Task_None:
                result = tasks.none()
            elif self.task == tasks_names.Task_Alternate:
                result = tasks.alternate()
            elif self.task == tasks_names.Task_Some:
                result, np_hard = tasks.some()
            elif self.task == tasks_names.Task_Many:
                result, np_hard = tasks.many()
            elif self.task == tasks_names.Task_Few:
                result = tasks.few()
            else:
                raise Exception("Task not found")



            results.append((filename, num_nodes, result, time.time() - start_time, np_hard))

        # create df
        df = pd.DataFrame(results, columns=["filename", "num_nodes", "result", "execution_time", "np_hard"])

        # create folder if not exists
        if not os.path.exists("results"):
            os.makedirs("results")
        df.to_csv(f"results/{self.task}_results.csv", index=False)

class WriteOutput:
    """
        Summary:
            This class is used to write the output of the tasks to a text file based on the csv files in the results folder.
            If there is no csv file for a task, we will write "Not run" as result.
            The output is saved in the results_output.txt file.

            If you wish to overwrite the csv files, you can delete the csv files in the results folder or run the RunTask class.
        
        Variables:
            <b>tasks_to_run (list)</b>: List of tasks to run
            <b>networkDataFiles (list)</b>: List of network data files
            <b>data (dict)</b>: Dictionary to store the data
        
        Methods:
            <b>create_output</b>: Create the output
            <b>write_output</b>: Write the output to a text file
        """
    def __init__(self) -> None:
        self.tasks_to_run = [getattr(tasks_names, attr) for attr in dir(tasks_names) if not attr.startswith('__')]
        self.networkDataFiles = [getattr(files, attr) for attr in dir(files) if not attr.startswith('__')]

        self.data = {}
        for task in self.tasks_to_run:
            print(f"Writing output for task: {task}")
            # check if file exists
            if os.path.exists(f"results/{task}_results.csv"):
                df = pd.read_csv(f"results/{task}_results.csv")

                # add data to dict
                self.data[task] = {}
                self.data[f"{task}-Num nodes"] = {}

                for _, row in df.iterrows():
                    self.data[task][row["filename"]] = row["result"]
                    self.data[f"{task}-Num nodes"][row["filename"]] = row["num_nodes"]

                self.data[f"{task}-Execution Time"] = df["execution_time"].sum()

            else:
                self.data[task] = {}

                for filename in self.networkDataFiles:
                    self.data[task][filename] = "Not run"
                
                self.data[f"{task}-Execution Time"] = 0
                self.data[f"{task}-Num nodes"] = 0

        self.create_output()   
        self.write_output()     

    def create_output(self) -> None:

        self.output_lines = []

        total_time = 0
        for task in self.tasks_to_run:
            total_time += self.data[f"{task}-Execution Time"]
        
        self.summaryTable = PrettyTable()
        self.summaryTable.align = "r"
        self.summaryTable.field_names = ["Total tests", "Total Execution Time", "Average Execution Time"]

        if total_time > 60:
            total_minutes = total_time // 60
            total_sec = total_time % 60
            total_time_txt = f"{total_minutes:.0f} minutes {total_sec:.2f} seconds"
        else:
            total_time_txt = f"{total_time:.2f} seconds"

        avg_time = total_time / len(self.networkDataFiles)

        if avg_time > 60:
            avg_minutes = avg_time // 60
            avg_sec = avg_time % 60
            avg_time_txt = f"{avg_minutes:.0f} minutes {avg_sec:.2f} seconds"
        else:
            avg_time_txt = f"{avg_time:.2f} seconds"

        self.summaryTable.add_row([len(self.networkDataFiles), f"{total_time_txt}", f"{avg_time_txt}"])

        self.table = PrettyTable()
        self.table.align = "r"
        self.table.field_names = ["Instance name", "# nodes", "Result_A", "Result_F", "Result_M", "Result_N", "Result_S"]
        self.table.align["Instance name"] = "l"

        for filename in self.data[self.tasks_to_run[0]].keys():
            # get number of nodes from the first task that is run
            num_nodes = [self.data[f"{task}-Num nodes"][filename] for task in self.tasks_to_run if self.data[task][filename] != "Not run"]
            if num_nodes:
                num_nodes = num_nodes[0]
            else:
                num_nodes = 0

            self.table.add_row([filename, num_nodes, self.data[self.tasks_to_run[0]][filename], self.data[self.tasks_to_run[1]][filename], self.data[self.tasks_to_run[2]][filename], self.data[self.tasks_to_run[3]][filename], self.data[self.tasks_to_run[4]][filename]])

    def write_output(self) -> None:
        with open('results_output.txt', 'w') as f:
            f.write("Summary:\n")
            f.write(str(self.summaryTable))
            f.write("\nResults:\n")
            f.write(str(self.table))