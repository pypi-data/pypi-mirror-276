

from common.enums import RunStatus, CodeSubmissionTestCaseStatus, CodeSubmissionStatus
from common.util import Util


class OnlineJudgeError(Exception):
    def __init__(self, message, failure_output=None):
        super().__init__(message)
        self.failure_output = Util.transform_failure_output(failure_output)
        self.message = str(message)
        self.run_status = RunStatus.INTERNAL_ERROR.get_enum_value()


class CodejudgeBuildException(Exception):
    def __init__(self, message, failure_output=None, send_email=True):
        super().__init__(message)
        self.failure_output = Util.transform_failure_output(failure_output)
        self.message = str(message)
        self.send_email = send_email
        self.run_status = RunStatus.BUILD_ERROR.get_enum_value()


class CodejudgeDeployException(Exception):
    def __init__(self, message, failure_output=None, send_email=True):
        super().__init__(message)
        self.failure_output = Util.transform_failure_output(failure_output)
        self.message = str(message)
        self.send_email = send_email
        self.run_status = RunStatus.FAILED_TO_START_PROJECT.get_enum_value()


class CodejudgeEvalPendingException(Exception):
    def __init__(self, message, send_email=True):
        super().__init__(message)
        self.message = str(message)
        self.send_email = send_email


class CodejudgeSystemException(Exception):
    def __init__(self, message, status, send_email=True):
        super().__init__(message)
        self.message = str(message)
        self.status = status
        self.send_email = send_email
        self.run_status = RunStatus.INTERNAL_ERROR.get_enum_value()


class CodejudgeTestException(Exception):
    def __init__(self, message, test_case_status, failure_output=None, send_email=True):
        super().__init__(message)
        self.failure_output = Util.transform_failure_output(failure_output)
        self.message = str(message)
        self.send_email = send_email
        self.run_status = RunStatus.FAILED_TO_RUN_TESTS.get_enum_value()
        self.test_case_status = test_case_status


class TestFolderNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = str(message)


class TestFileNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = str(message)


class TestFileEmptyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = str(message)


class MultipleSameNameFilePresentException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = str(message)


class IncorrectTestReportFormatException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = str(message)


class CodejudgeCodeSubmissionException(Exception):
    def __init__(self, message, failure_output=None, send_email=True):
        super().__init__(message)
        self.failure_output = Util.transform_failure_output(failure_output)
        self.message = str(message)
        self.send_email = send_email
        self.code_submission_status = CodeSubmissionTestCaseStatus.INTERNAL_ERROR.get_enum_value()


class CodejudgeException(Exception):
    def __init__(self, message, status, send_email=True):
        super().__init__(message)
        self.message = Util.transform_message(message)
        self.status = status
        self.send_email = send_email
        self.run_status = RunStatus.INTERNAL_ERROR.get_enum_value()
        self.code_execution_status = CodeSubmissionStatus.CJ_INTERNAL_ERROR.get_enum_value()


class RecruitException(Exception):

    def __init__(self, message, status, send_email=True, ignore=False):
        super().__init__(message)
        self.message = message
        self.status = status
        self.send_email = send_email
        self.ignore = ignore


class NaukriRecruitException(Exception):

    def __init__(self, message, status, error, send_email=True):
        super().__init__(message)
        self.message = message
        self.status = status
        self.error = error
        self.send_email = send_email
