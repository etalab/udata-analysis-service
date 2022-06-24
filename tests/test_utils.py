import os
from unittest import mock

import pytest

from udata_analysis_service.utils.kafka import get_topic

@mock.patch.dict(os.environ, {'UDATA_INSTANCE_NAME': 'udata'})
def test_get_topic():
    topic = get_topic('test')
    assert topic == 'udata.test'
