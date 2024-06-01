import unittest
import os
from roboto_ingestion_utils.ingestion_utils import setup_output_folder_structure


def test_setup_output_folder_structure(tmp_path):
    input_dir = os.path.join(tmp_path, "input")
    file_path = os.path.join(input_dir, "file.txt")

    output_dir_path_topics, output_dir_temp = setup_output_folder_structure(file_path, input_dir)
