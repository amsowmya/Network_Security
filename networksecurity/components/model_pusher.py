import os 
import sys 
import shutil

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging

from networksecurity.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from networksecurity.entity.config_entity import ModelPusherConfig

from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.main_utils.utils import save_object, load_object, write_yaml_file


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig, model_eval_artifact: ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_model_pusher(self):
        try:
            trained_model_path = self.model_eval_artifact.trained_model_path
            
            # Creating model pusher dir to save model
            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)
            
            # saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)
        
            # prepare artifct
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)