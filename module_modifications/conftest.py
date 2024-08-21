

from imp import reload
import sys
import pytest


@pytest.fixture(name="modify_module")
def fixture_modify_module():
    print("fixture_modify_module: setup")
    import module_to_modify
    module_to_modify.Operation =
    import new_module as module_to_modify
    print(sys.modules)
    yield

    print("fixture_modify_module: teardown")
    del sys.modules["module_to_modify"]
    import module_to_modify
    print(sys.modules)
