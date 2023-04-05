#!/usr/bin/env python3
# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration tests for the orc8r-controller rock.

These tests assume that the orc8r-controller container is running and available at the url:port
defined below.
"""

import unittest
from pathlib import Path
from time import sleep

import docker  # type: ignore[import]
import requests
import yaml

ORC8R_CONTROLLER_DOCKER_URL = "http://localhost"
ORC8R_CONTROLLER_DOCKER_PORT = 8080


class TestOrc8rControllerRock(unittest.TestCase):
    """Integration tests for the orc8r-controller rock."""

    def setUp(self) -> None:
        """Run the container to test."""
        self.client = docker.from_env()
        self._run_orc8r_controller_container()

    def _run_orc8r_controller_container(self):
        with open(Path("./../rockcraft.yaml"), "r") as f:
            data = yaml.safe_load(f)

        image_name = data["name"]
        version = data["version"]

        self.client.containers.run(
            f"ghcr.io/canonical/{image_name}:{version}",
            detach=True,
            ports={"10112": "8080"},
        )

    def test_given_orc8r_controller_container_is_running_when_http_get_then_hello_message_is_returned(  # noqa: E501
        self,
    ):
        """Test to validate that the container is running."""
        for _ in range(10):
            try:
                response = requests.get(
                    f"{ORC8R_CONTROLLER_DOCKER_URL}:{ORC8R_CONTROLLER_DOCKER_PORT}"
                )
                if response.status_code == 200:
                    assert "hello" in response.text
                    break
            except requests.exceptions.RequestException:
                pass
            sleep(1)
        else:
            assert False, "Failed to get a 200 response within 10 seconds."
