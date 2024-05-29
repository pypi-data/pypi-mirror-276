#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/26
# @Author  : yanxiaodong
# @File    : config.py
"""
from typing import Dict
import os
from abc import ABCMeta

from gaea_tracker import ExperimentTracker
from windmillclient.client.windmill_client import WindmillClient
from windmillmodelv1.client.model_api_model import ModelMetadata, InputSize

from gaea_operator.utils import DEFAULT_TRANSFORM_CONFIG_FILE_NAME, Accelerator, read_file
from .generate_transform_config import generate_transform_config
from .modify_package_files import ModifyEnsembleFile, ModifyPackageFiles, KEY_SUB_MODELS
from .generate_transform_config import KEY_EVAL_SIZE, \
    KEY_EVAL_WIDTH, \
    KEY_EVAL_HEIGHT, \
    KEY_MAX_BATCH_SIZE, \
    KEY_MAX_BOX_NUM


class Config(metaclass=ABCMeta):
    """
    Config write for train, transform and package.
    """
    accelerator2model_format = {Accelerator.T4: "TensorRT",
                                Accelerator.A100: "TensorRT",
                                Accelerator.V100: "TensorRT",
                                Accelerator.R200: "PaddleLite"}

    def __init__(self, windmill_client: WindmillClient, tracker_client: ExperimentTracker, metadata: Dict = {}):
        self.windmill_client = windmill_client
        self.tracker_client = tracker_client
        self._metadata = metadata

    @property
    def metadata(self):
        """
        Get metadata.
        """
        return self._metadata

    def write_train_config(self,
                           dataset_uri: str,
                           model_uri: str,
                           advanced_parameters: dict,
                           pretrain_model_uri: str):
        """
        Config write for train.
        """
        pass

    def write_eval_config(self, dataset_uri: str, model_uri: str, ):
        """
        Config write for eval.
        """
        pass

    def write_transform_config(self, model_uri: str, advanced_parameters: dict):
        """
        Config write for transform.
        """
        cfg_path = os.path.join(model_uri, DEFAULT_TRANSFORM_CONFIG_FILE_NAME)
        self._update_transform_metadata(advanced_parameters)

        generate_transform_config(advanced_parameters, cfg_path, self.metadata)

    def write_sub_model_config(self, transform_model_uri: str, modify_model_names: dict):
        """
        Config write for package.
        """
        pass

    def write_triton_package_config(self,
                                    transform_model_uri: str,
                                    ensemble_model_uri: str,
                                    modify_model_names: dict,
                                    ensemble_local_name: str,
                                    accelerator: str):
        """
        Config write for package.
        """
        response = read_file(input_dir=transform_model_uri)
        transform_model_name = response["localName"]
        transform_model_cn_name = response["displayName"]
        cfg = ModifyPackageFiles(ensemble_model_uri=ensemble_model_uri,
                                 metadata=self.metadata,
                                 modify_model_names=modify_model_names,
                                 ensemble_local_name=ensemble_local_name,
                                 accelerator=accelerator,
                                 transform_model_name=transform_model_name,
                                 transform_model_cn_name=transform_model_cn_name)
        cfg.modify_ppyoloe()

    def write_ensemble_config(self, ensemble_model_uri: str, model_config: Dict):
        """
        Config write for ensemble.
        """
        cfg = ModifyEnsembleFile(ensemble_model_uri=ensemble_model_uri,
                                 model_config=model_config)

        advanced_parameters = {KEY_SUB_MODELS: {}}
        for k, v in model_config.items():
            advanced_parameters[KEY_SUB_MODELS][v['localName']] = str(v['artifact']['version'])
        self._update_ensemble_metadata(advanced_parameters=advanced_parameters)

        cfg.modify_ensemble()

    def _update_train_metadata(self, advanced_parameters: Dict):
        meta_data = ModelMetadata(experimentName=self.tracker_client.experiment_name,
                                  experimentRunID=self.tracker_client.run_id)
        self._metadata.update(meta_data.dict())

    def _update_ensemble_metadata(self, advanced_parameters: Dict):
        meta_data = ModelMetadata(subModels=advanced_parameters[KEY_SUB_MODELS])
        self._metadata.update(meta_data.dict())

    def _update_transform_metadata(self, advanced_parameters: Dict):
        if KEY_EVAL_SIZE in advanced_parameters:
            width, height = advanced_parameters.pop(KEY_EVAL_SIZE).split('*')
            advanced_parameters[KEY_EVAL_WIDTH] = width
            advanced_parameters[KEY_EVAL_HEIGHT] = height

        input_size = InputSize(width=int(advanced_parameters[KEY_EVAL_WIDTH]),
                               height=int(advanced_parameters[KEY_EVAL_HEIGHT]))

        meta_data = ModelMetadata(**self._metadata)
        meta_data.inputSize = input_size
        maxBoxNum = int(advanced_parameters[KEY_MAX_BOX_NUM]) \
            if KEY_MAX_BOX_NUM in advanced_parameters else 1
        meta_data.maxBoxNum = maxBoxNum
        advanced_parameters = {
            'inferenceMaxBatchSize': int(advanced_parameters[KEY_MAX_BATCH_SIZE]),
            'maxBoxNum': maxBoxNum,
            'evalWidth': int(advanced_parameters[KEY_EVAL_WIDTH]),
            'evalHeight': int(advanced_parameters[KEY_EVAL_HEIGHT])}

        if meta_data.algorithmParameters is None:
            meta_data.algorithmParameters = advanced_parameters
        else:
            meta_data.algorithmParameters.update(advanced_parameters)

        self._metadata = meta_data.dict()
