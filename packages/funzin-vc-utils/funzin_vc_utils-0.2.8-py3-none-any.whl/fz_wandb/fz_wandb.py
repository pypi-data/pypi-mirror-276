import wandb
from datetime import datetime


class FZWandb:
    def __init__(self, project_name, experiment_name) -> None:
        print("wandb init")
        wandb.init(project=project_name)

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        wandb.run.name = experiment_name + "_" + date_time

    def set_watch_model(self, model):
        wandb.watch(model)

    def log_config(self, **args):
        wandb.config.update(args)

    def log_dic(self, **dict):
        wandb.log(dict)

    def log(self, title, param):  # check : wandb 는 dict 만 입력가능?
        wandb.log({f"{title} : {param}"})

    def upload_artifact(self, path):
        wandb.save(path)
