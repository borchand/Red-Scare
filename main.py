from Utils.Tasks import WriteOutput, RunTask
import Utils.task_names as tasks_names
import argparse


def main(task:str, output:bool)-> None:
    """
    Summary:
        Run the task or create the output file from the results

    Args:
        task (str): Task to run/overwrite. Allowed values: none, alternate, some, many, few, all
        output (bool): Generate output file from the results
    """
    if task != 'noTask':
        if task not in ['none', 'alternate', 'some', 'many', 'few', 'all']:
            raise Exception("Task not found")
        
        if task == 'all':
            tasks_to_run = [getattr(tasks_names, attr) for attr in dir(tasks_names) if not attr.startswith('__')]
            for task in tasks_to_run:
                RunTask(task)
        else:
            RunTask(task)

    if output == 't':
        WriteOutput()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the task or create the output file from the results")

    parser.add_argument("-t", "--task", type=str, default='noTask', choices=['noTask', 'none', 'alternate', 'some', 'many', 'few', 'all'], help="Task to run/overwrite.")
    parser.add_argument("-o", "--output",  default='t', choices=['t', 'f'], help="Generate output file from the results")

    args = parser.parse_args()

    main(args.task, args.output)

