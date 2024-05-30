import enum
import functools

import sh

from pytest_tf.exception import InvalidTFRunner


class TFRunner(str, enum.Enum):
    TERRAFORM = "terraform"
    OPEN_TOFU = "tofu"

    @functools.cached_property
    def command(self):
        match self:
            case TFRunner.TERRAFORM:
                return sh.terraform
            case TFRunner.OPEN_TOFU:
                return sh.tofu
            case _:
                raise InvalidTFRunner(self)
