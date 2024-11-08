# Red-Scare

## Python version >=3.9

## Runing tests and creating output
The `main.py` file is used to run the tests and create the output files. The output file are saved as `results_output.txt`. The result of a task is saved in the `results`folder as csv.

### Options
The `main.py` file has two options that can be used to run the program. The options are as follows:

- `-t` or `--task` is used to specify which task to run. The default value is 'noTask' which means that no task is run. The value can be set to 'all' to run all the tasks.

- `-o` or `--output` is used to specify if the output file should be created. The default value is 't' which means that the output file will be created. The value can be set to 'f' to disable the output file.

<!-- table showing choices for vars -->
| Variable | Choices | Default | Description |
| --- | --- | --- | --- |
| -t | noTask, none, alternate, some, many, few, all | noTask | Specify which task to run |
| -o | t, f | t | Specify if the output file should be created |

Note that the task none is the name of a task and not a value to disable the task. The value to disable the task is 'noTask'.

Below is examples on how to run the program with the options.

### Run specific task
To run a specific task, you can change the `task` variable in the `main.py` file. The tasks are as follows:

```bash
python main.py -t none
```
By default the task is set to 'noTask' which means that no task is run. Be aware that the result file will be overwritten if you run the program with the same task.

### Run all tasks
To run all tasks, you can change the `task` variable in the `main.py` file to 'all'. This will run all the tasks and save the results in the `results` folder.

```bash
python main.py -t all
```

### Create output file
By default the output variable is set to 't'. This means that the `results_output.txt` file will be created. If you want to disable this, you can change the `output` variable in the `main.py` file to 'f'.

```bash
python main.py -o f
```
Running this command will not create the `results_output.txt` file and will no run any task.
If you want to run a task and not create the output file, you can run the following command:

```bash
python main.py -t <task_name> -o f
```



## Links
- [Report docs](https://drive.google.com/drive/folders/1W_EWitnYJpkVWnakoz5EF27qoRUI0tSa?usp=drive_link)

- [red scare thore](https://github.com/thorehusfeldt/algdes-labs/tree/master/red-scare)

- [Link to repo](https://github.com/borchand/Red-Scare)

- [Link to Overleaf ](https://www.overleaf.com/project/67223c5d16737d416959d718)

## Read data
Examples on how to read data can be found in [example.ipynb](example.ipynb)

## Set up env
Create env
```bash
python3 -m venv venv
```
Activate env
```bash
source venv/bin/activate
```
Deactivate env
```bash
deactivate
```

## Install requirements
This is used to install all the required packages from the requirements file
```bash
pip install -r requirements.txt
```

## Update requirements file
This is used to update the requirements file with the current packages.
```bash
pip freeze > requirements.txt
```

