from Utils.ReadInput import ReadFile
from prettytable import PrettyTable
import Utils.data_files as files
import Utils.task_names as tasks_names
from tqdm import tqdm
import networkx as nx
import time
import pandas as pd
import os

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

    def alternate(self):
        pass

    def some(self):
        pass

    def many(self):
        pass

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

    Inputs:
        <b>task (str)</b>: The task to run (None, Alternate, Some, Many, Few)
        You can use the tasks_names.py file to get the task names

    Variables:
        <b>task (str)</b>: The task to run
        <b>networkDataFiles (list)</b>: List of network data

    Methods:
        <b>run</b>: Run the task (this is in the constructor)

    """
    def __init__(self, task: str) -> None:
        self.networkDataFiles = [getattr(files, attr) for attr in dir(files) if not attr.startswith('__')]

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
            if self.task == tasks_names.none:
                result = tasks.none()
            elif self.task == tasks_names.alternate:
                result = tasks.alternate()
            elif self.task == tasks_names.some:
                result = tasks.some()
            elif self.task == tasks_names.many:
                result = tasks.many()
            elif self.task == tasks_names.few:
                result = tasks.few()
            else:
                raise Exception("Task not found")

            results.append((filename, num_nodes, result, time.time() - start_time))

        # create df
        df = pd.DataFrame(results, columns=["filename", "num_nodes", "result", "execution_time"])

        # create folder if not exists
        if not os.path.exists("results"):
            os.makedirs("results")
        df.to_csv(f"results/{self.task}_results.csv", index=False)

class WriteOutput:
    """
        Summary:
            This class is used to write the output of the tasks to a text file based on the csv files in the results folder.
            If there is no csv file for a task, we will run the task.
            The output is saved in the results_output.txt file.

            This means that you only need to use this class to run all the tasks and write the output to a text file.
            But it is atviable to use the RunTask class to run a single task as some tasks may take a long time to run.

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
            if not os.path.exists(f"results/{task}_results.csv"):
                RunTask(task)
            df = pd.read_csv(f"results/{task}_results.csv")

            # add data to dict
            self.data[task] = {}

            for _, row in df.iterrows():
                self.data[task][row["filename"]] = row["result"]

            self.data[f"{task}-Execution Time"] = df["execution_time"].sum()

            self.data[f"{task}-Num nodes"] = df["num_nodes"][0]

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
        self.summaryTable.add_row([len(self.networkDataFiles), f"{total_time:.2f} seconds", f"{total_time/len(self.networkDataFiles):.4f} seconds"])

        self.table = PrettyTable()
        self.table.align = "r"
        self.table.field_names = ["Instance name", "# nodes", "Result_A", "Result_F", "Result_M", "Result_N", "Result_S"]
        self.table.align["Instance name"] = "l"

        for filename in self.data[self.tasks_to_run[0]].keys():
            self.table.add_row([filename, self.data[f"{self.tasks_to_run[0]}-Num nodes"], self.data[self.tasks_to_run[0]][filename], self.data[self.tasks_to_run[1]][filename], self.data[self.tasks_to_run[2]][filename], self.data[self.tasks_to_run[3]][filename], self.data[self.tasks_to_run[4]][filename]])

    def write_output(self) -> None:
        with open('results_output.txt', 'w') as f:
            f.write("Summary:\n")
            f.write(str(self.summaryTable))
            f.write("\nResults:\n")
            f.write(str(self.table))