from enum import Enum

from common.enum_util import EnumUtil


class Status(Enum):
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'


class RunStatus(Enum):
    IN_QUEUE = (1, 'In Queue')
    PROCESSING = (2, 'Processing')
    ACCEPTED = (3, 'Accepted')
    WRONG_ANSWER = (4, 'Wrong Answer')
    TIME_LIMIT_EXCEEDED = (5, 'Time Limit Exceeded')
    FAILED_TO_START_PROJECT = (6, 'Failed to Start Project')
    INTERNAL_ERROR = (7, 'Internal Error')
    BUILD_TIMEOUT_EXCEEDED = (8, 'Build Timeout Exceeded')
    BUILD_ERROR = (9, 'Build Error')
    MEMORY_EXCEEDED = (10, 'Memory Exceeded')
    PROJECT_CRASHED = (11, 'Project Crashed')
    FAILED_TO_RUN_TESTS = (12, 'Failed to run tests')
    QUERY_ERROR = (13, 'Invalid Query')
    INVALID_EXPERIMENT = (14, 'INVALID_EXPERIMENT')
    MANUAL_EVAL = (15, 'Manual Evaluation')
    LOW_QUALITY = (16, 'Low Quality')

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, RunStatus)


class CodeSubmissionStatus(Enum):
    IN_QUEUE = (1, 'In Queue')
    PROCESSING = (2, 'Processing')
    ACCEPTED = (3, 'Accepted')
    WRONG_ANSWER = (4, 'Wrong Answer')
    TIME_LIMIT_EXCEEDED = (5, 'Time Limit Exceeded')
    COMPILATION_ERROR = (6, 'Compilation Error')
    RUNTIME_ERROR_SIGSEGV = (7, 'Runtime Error (SIGSEGV)')
    RUNTIME_ERROR_SIGXFSZ = (8, 'Runtime Error (SIGXFSZ)')
    RUNTIME_ERROR_SIGFPE = (9, 'Runtime Error (SIGFPE)')
    RUNTIME_ERROR_SIGABRT = (10, 'Runtime Error (SIGABRT)')
    RUNTIME_ERROR_NZEC = (11, 'Runtime Error (NZEC)')
    RUNTIME_ERROR_OTHER = (12, 'Runtime Error (Other)')
    INTERNAL_ERROR = (13, 'Internal Error')
    CJ_INTERNAL_ERROR = (14, 'Internal Error')
    COMPILATION_TIME_LIMIT_EXCEEDED = (15, 'Compilation Time Limit Exceeded')

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, CodeSubmissionStatus)


class OperatorType(Enum):
    EQUAL_TO = '='
    GREATER_THAN = '>'
    LESS_THAN = '<'
    GREATER_THAN_AND_EQUAL_TO = '>='
    LESS_THAN_AND_EQUAL_TO = '<='

    @classmethod
    def get_default_operator_for_candidate_filter(cls):
        return OperatorType.GREATER_THAN_AND_EQUAL_TO.value

    @classmethod
    def get_all_operators_symbol(cls):
        all_operators = []
        for enum in OperatorType:
            all_operators.append(enum.value)
        return all_operators


class Environment(Enum):
    DEV = 'dev'
    PROD = 'prod'
    LOCAL = 'local'
    TEST = 'test'


class SubjectiveCustomFieldTypes(Enum):
    HTML_EDITOR = 'HTML_EDITOR'
    TEXT = 'TEXT'
    DROPDOWN = 'DROPDOWN'
    LINK = 'LINK'
    RADIO = 'RADIO'
    CHECKBOX = 'CHECKBOX'
    FILE = 'FILE'
    NUMBER = 'NUMBER'
    SLIDER = 'SLIDER'
    VOICE = 'VOICE'
    VIDEO = 'VIDEO'
    WHITEBOARD = 'WHITEBOARD'
    DIAGRAM = 'DIAGRAM'

    @classmethod
    def get_subjective_custom_field_types(cls, names):
        return [field.value for field in SubjectiveCustomFieldTypes]


class QuestionSubTypes(Enum):
    TEXT = {"label": 'Enter your answer', "type": SubjectiveCustomFieldTypes.HTML_EDITOR.name,  "id": 'answer'}
    VOICE = {"label": 'Record your answer', "type": SubjectiveCustomFieldTypes.VOICE.name,  "id": 'VOICE'}
    VIDEO = {"label": 'Record your answer', "type": SubjectiveCustomFieldTypes.VIDEO.name,  "id": 'VIDEO'}
    WHITEBOARD = {"label": 'Draw your answer', "type": SubjectiveCustomFieldTypes.WHITEBOARD.name,  "id": 'WHITEBOARD'}
    DIAGRAM = {"label": 'Draw your answer', "type": SubjectiveCustomFieldTypes.DIAGRAM.name,  "id": 'DIAGRAM'}
    ZIP = {"label": 'Upload your answer', "type": SubjectiveCustomFieldTypes.FILE.name,  "id": 'ZIP'}
    A_COMMENTS = {"label": 'Additional Comments', "type": SubjectiveCustomFieldTypes.HTML_EDITOR.name,  "id": 'a_comments'}

    @classmethod
    def get_types_for_additional_comments(cls,):
        return [QuestionSubTypes.WHITEBOARD.name, QuestionSubTypes.DIAGRAM.name, QuestionSubTypes.ZIP.name]

    @classmethod
    def get_ques_sub_types_info(cls, field_type):
        fields = []
        for field in QuestionSubTypes:
            if field.name == field_type:
                fields.append(field.value)
                if field_type in cls.get_types_for_additional_comments():
                    fields.append(QuestionSubTypes.A_COMMENTS.value)
                break
        return fields


class ArchiveTablesList(Enum):
    AI_PROCTORING = "AIProctoring"
    LIVE_RUN_INFO = "LiveRunInfo"
    CODE_SUBMISSION_LIVE_RUN = "CodeSubmissionLiveRun"
    CANDIDATES = "Candidates"

    @classmethod
    def get_main_table_name(cls, table_name_key):
        return cls[table_name_key].value


class IntervalType(Enum):
    QUARTERLY = "QUARTERLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    @classmethod
    def get_all_interval_types(cls):
        return [field.value for field in IntervalType]
