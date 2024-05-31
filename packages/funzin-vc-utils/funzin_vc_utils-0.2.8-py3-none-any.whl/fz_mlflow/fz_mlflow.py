# source >  https://www.programcreek.com/python/?code=Unbabel%2FOpenKiwi%2FOpenKiwi-master%2Fkiwi%2Floggers.py

import logging
import threading
import uuid
import mlflow
from mlflow.tracking import MlflowClient
import traceback
import os

logger = logging.getLogger(__name__)


class FZMLflowLogger:
    """MLflow simple logger
    TODO :: check previous running instance
    """

    @staticmethod
    def set_environment(track_uri, s3_url, secret_key, access_id):
        # export MLFLOW_S3_ENDPOINT_URL=http://192.168.1.145:30575
        # export MLFLOW_TRACKING_URI=http://192.168.1.145:31442
        # export AWS_SECRET_ACCESS_KEY=minio123
        # export AWS_ACCESS_KEY_ID=minio
        if track_uri is not None and len(track_uri) > 0:
            os.environ["MLFLOW_TRACKING_URI"] = track_uri
            os.environ["MLFLOW_S3_ENDPOINT_URL"] = s3_url
            os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key
            os.environ["AWS_ACCESS_KEY_ID"] = access_id
        else:
            print("bashrc 에 mlflow environment variables 정의됨")
            # # * -------------for mlflow-----------------------
            # export MLFLOW_S3_ENDPOINT_URL=http://172.16.200.207
            # export MLFLOW_TRACKING_URI=http://172.16.200.204
            # export AWS_SECRET_ACCESS_KEY=minio123
            # export AWS_ACCESS_KEY_ID=minio
            # # * -------------for mlflow-----------------------

    def __init__(self) -> None:
        self.clinet = None
        self.experiment_id = None
        self.EXPERIMENT_NAME = None

        if not os.environ["MLFLOW_TRACKING_URI"]:
            raise Exception("Set Environment for mlflow first, please! [call set_environment]")

    def init_mlflow(self, EXPERIMENT_NAME, ARTIFACT_PATH_URI=None):
        self.client = MlflowClient()
        self.experiment_id = self.client.get_experiment_by_name(name=EXPERIMENT_NAME)
        if self.experiment_id is None:
            self.client.create_experiment(name=EXPERIMENT_NAME, artifact_location=ARTIFACT_PATH_URI)
        mlflow.set_experiment(experiment_name=EXPERIMENT_NAME)
        self._print_info()

    def init_mlflow_with_tag(self, EXPERIMENT_NAME, tag1, tag2):
        # Create an experiment with a name that is unique and case sensitive.
        self.EXPERIMENT_NAME = EXPERIMENT_NAME
        self.client = MlflowClient()
        self.experiment_id = self.client.create_experiment(EXPERIMENT_NAME)
        self.client.set_experiment_tag(self.experiment_id, tag1, tag2)
        self._print_info()

    @staticmethod
    def _retrieve_mlflow_experiment_id(name, create=False):
        experiment_id = None
        if name:
            existing_experiment = MlflowClient().get_experiment_by_name(name)
            if existing_experiment:
                experiment_id = existing_experiment.experiment_id
            else:
                if create:
                    experiment_id = mlflow.create_experiment(name)
                else:
                    raise Exception('Experiment "{}" not found in {}'.format(name, mlflow.get_tracking_uri()))
        return experiment_id

    def _print_info(self):
        return "not working yet!"
        # Fetch experiment metadata information
        # experiment = self.client.get_experiment(self.experiment_id) # max retry error
        experiment = self._retrieve_mlflow_experiment_id(self.EXPERIMENT_NAME, True)
        print("Name: {}".format(experiment.name))
        print("Experiment_id: {}".format(experiment.experiment_id))
        print("Artifact Location: {}".format(experiment.artifact_location))
        print("Tags: {}".format(experiment.tags))
        print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    @property
    def experiment_name(self):
        return self._experiment_name

    @staticmethod
    def start(nest=False):
        mlflow.start_run(nested=nest)

    @staticmethod
    def stop():
        mlflow.end_run()

    @staticmethod
    def log_artifact(path):
        mlflow.log_artifact(local_path=path)

    @staticmethod
    def log_artifacts(path, tag):
        mlflow.log_artifacts(path, tag)

    @staticmethod
    def log_param(**rpt):
        mlflow.log_params(rpt)

    @staticmethod
    def log_metric(name, value):
        mlflow.log_metric(name, value)

    @staticmethod
    def log_metrics(**dict):
        mlflow.log_metrics(dict)
        # for key in dict:
        #     mlflow.log_metric(key, dict[key])

    @staticmethod
    def log_tag(key, value):
        mlflow.set_tag(key, value)

    @staticmethod
    def log_tags(**dict):
        for key in dict:
            mlflow.set_tag(key, dict[key])

    @staticmethod
    def get_tracking_uri():
        return mlflow.get_tracking_uri()


# * ============================================== #
# * ============================================== #
# * ============================================== #
# * ============================================== #


# ! - not ready yet
class ___MLflowLogger:
    def __init__(self):
        self.always_log_artifacts = False
        self._experiment_name = None
        self._run_name = None

    def configure(
        self,
        run_uuid,
        experiment_name,
        tracking_uri,
        run_name=None,
        always_log_artifacts=False,
        create_run=True,
        create_experiment=True,
        nest_run=True,
    ):
        if mlflow.active_run() and not nest_run:
            logger.info("Ending previous MLFlow run: {}.".format(self.run_uuid))
            mlflow.end_run()

        self.always_log_artifacts = always_log_artifacts
        self._experiment_name = experiment_name
        self._run_name = run_name

        # MLflow specific
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

        if run_uuid:
            existing_run = MlflowClient().get_run(run_uuid)
            if not existing_run and not create_run:
                raise FileNotFoundError(
                    "Run ID {} not found under {}".format(run_uuid, mlflow.get_tracking_uri())
                )

        experiment_id = self._retrieve_mlflow_experiment_id(experiment_name, create=create_experiment)
        return mlflow.start_run(
            run_uuid,
            experiment_id=experiment_id,
            run_name=run_name,
            nested=nest_run,
        )

    def start_nested_run(self, run_name=None):
        return mlflow.start_run(run_name=run_name, nested=True)

    @property
    def run_uuid(self):
        return mlflow.tracking.fluent.active_run().info.run_uuid

    @property
    def experiment_id(self):
        return mlflow.tracking.fluent.active_run().info.experiment_id

    @property
    def experiment_name(self):
        # return MlflowClient().get_experiment(self.experiment_id).name
        return self._experiment_name

    def should_log_artifacts(self):
        return self.always_log_artifacts or self._is_remote()

    @staticmethod
    def get_tracking_uri():
        return mlflow.get_tracking_uri()

    @staticmethod
    def log_metric(key, value):
        mlflow.log_metric(key, value)

    @staticmethod
    def log_param(key, value):
        mlflow.log_param(key, value)

    @staticmethod
    def log_artifact(local_path, artifact_path=None):
        t = threading.Thread(
            target=mlflow.log_artifact,
            args=(local_path,),
            kwargs={"artifact_path": artifact_path},
            daemon=True,
        )
        t.start()

    @staticmethod
    def log_artifacts(local_dir, artifact_path=None):
        def send(dpath, e, path):
            mlflow.log_artifacts(dpath, artifact_path=path)
            e.set()

        event = threading.Event()
        t = threading.Thread(target=send, args=(local_dir, event, artifact_path), daemon=True)
        t.start()
        return event

    @staticmethod
    def get_artifact_uri():
        return mlflow.get_artifact_uri()

    @staticmethod
    def end_run():
        mlflow.end_run()

    def _is_remote(self):
        return not mlflow.tracking.utils._is_local_uri(mlflow.get_tracking_uri())

    @staticmethod
    def _retrieve_mlflow_experiment_id(name, create=False):
        experiment_id = None
        if name:
            existing_experiment = MlflowClient().get_experiment_by_name(name)
            if existing_experiment:
                experiment_id = existing_experiment.experiment_id
            else:
                if create:
                    experiment_id = mlflow.create_experiment(name)
                else:
                    raise Exception('Experiment "{}" not found in {}'.format(name, mlflow.get_tracking_uri()))
        return experiment_id


# def main():
#     try:
#         import mlflow
#         from mlflow.tracking import MlflowClient

#         # tracking_logger = MLflowLogger()
#         tracking_logger = FZMLflowLogger()
#         tracking_logger.init_mlflow("ksg_0621-1")

#         tracking_logger.start()

#         params = {
#             "epochs": 7,
#             "optimizer": "adam",
#             "loss": "BCE",
#             "batch_size": 192,
#             "copy_X": "True",
#             "normalize": "False",
#             "fit_intercept": "True",
#             "n_jobs": "None",
#         }
#         tracking_logger.log_param(**params)

#         metrics = {
#             "training_score": 1.0,
#             "training_rmse": 4.440892098500626e-16,
#             "training_r2_score": 1.0,
#             "training_mae": 2.220446049250313e-16,
#             "training_mse": 1.9721522630525295e-31,
#         }
#         tracking_logger.log_metrics(**metrics)

#         tags = {
#             "estimator_class": "sklearn.linear_model._base.LinearRegression",
#             "estimator_name": "LinearRegression",
#         }
#         tracking_logger.log_tags(**tags)

#         model = "/home/sgkim/projects/ocr_kor/saved_models/TPS-VGG-None-Attn-Seed607/best_accuracy.pth"
#         tracking_logger.log_artifact(model)

#         model_folder = "/home/sgkim/projects/ocr_kor/saved_models/TPS-VGG-None-Attn-Seed607"
#         tracking_logger.log_artifacts(model_folder, "my models")

#         tracking_logger.stop()

#         print("done")

#     except ImportError as e:
#         print(f"can not create MLflowLogger : {e}")
#         print(f"------------")
#         traceback.print_stack()
#         print(f"------------")
#         traceback.print_exception()


# if __name__ == "__main__":
#     main()
