import platform
from unittest import TestCase
import os

import pytest
import yaml
from autobrew.aws.test_utils import cloudFormationValidator
import json

local_only = pytest.mark.skipif(
    platform.system() != "Windows", reason="requires aws account"
)

def getBaseLambdaFolder() -> str:
    my_path = os.path.abspath(os.path.dirname(__file__))
    return my_path[: my_path.rfind("test")]

def formPath():
    lambda_folder = getBaseLambdaFolder()
    path = os.path.join(lambda_folder, "serverless.yml")
    return path


def formRulesPath():
    lambda_folder = getBaseLambdaFolder()
    return os.path.join(lambda_folder, "test_utils", "cf-rules.json")


class TestCloudFormation(TestCase):
    @local_only
    def test_validate(self):
        """ Validates the Cloudformation part of the serverless yaml for syntax errors, etc"""
        cloudFormationValidator.aws_region = "eu-west-1"
        path = formPath()
        cf_template = cloudFormationValidator.get_template(path)
        y = yaml.load(cf_template, Loader=yaml.Loader)
        cf = str(y["resources"])
        out = cloudFormationValidator.validate_cf_template(cf, "no")
        self.assertTrue(out)

    def test_apply_rules(self):
        cloudFormationValidator.aws_region = "eu-west-1"
        path = formPath()
        cf_template = cloudFormationValidator.get_template(path)
        y = yaml.load(cf_template, Loader=yaml.Loader)
        cf = str(y["resources"]).replace("'", '"')
        j_cf = json.loads(cf)
        cf_rules_path = formRulesPath()
        (
            allow_root_keys,
            allow_parameters,
            allow_resources,
            require_ref_attributes,
            allow_additional_attributes,
            not_allow_attributes,
        ) = cloudFormationValidator.get_configuration(cf_rules_path)

        self.assertTrue(
            cloudFormationValidator.validate_root_keys(j_cf.keys(), allow_root_keys)
        )

        if j_cf.get("Parameters"):
            self.assertTrue(
                cloudFormationValidator.validate_parameters(
                    j_cf["Parameters"].keys(), allow_parameters
                )
            )

        self.assertTrue(
            cloudFormationValidator.validate_resources(
                j_cf["Resources"], allow_resources
            )
        )

        self.assertTrue(
            cloudFormationValidator.validate_attributes(
                j_cf["Resources"],
                require_ref_attributes,
                allow_additional_attributes,
                not_allow_attributes,
            )
        )
