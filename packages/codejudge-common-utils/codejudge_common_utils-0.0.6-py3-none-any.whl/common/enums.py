from enum import Enum
from builtins import classmethod
from enum import Enum

from common.enum_util import EnumUtil


class Status(Enum):
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'


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
    TESTS = "Tests"

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


class ExecutionMode(Enum):
    SERVER = 'SERVER'
    WORKER = 'WORKER'


class RunTestCaseStatus(Enum):
    TRUE = 'True'
    FALSE = 'False'
    TIMED_OUT = 'Timed_out'
    PROJECT_CRASHED = 'PROJECT_CRASHED'
    MULTIPLE_TEST_FILES_PRESENT = 'MULTIPLE_TEST_FILES_PRESENT'
    NO_TEST_FILE_PRESENT = 'NO_TEST_FILE_PRESENT'
    NO_TEST_PRESENT = 'NO_TEST_PRESENT'
    INCORRECT_TEST_REPORT_FORMAT = 'INCORRECT_TEST_REPORT_FORMAT'
    QUERY_ERROR = 'QUERY_ERROR'

    @classmethod
    def get_mapped_run_status(cls, value):
        test_case_to_run_status_mapping = dict()
        test_case_to_run_status_mapping[RunTestCaseStatus.TRUE.value] = RunStatus.ACCEPTED.get_enum_value()
        test_case_to_run_status_mapping[RunTestCaseStatus.FALSE.value] = RunStatus.WRONG_ANSWER.get_enum_value()
        test_case_to_run_status_mapping[
            RunTestCaseStatus.TIMED_OUT.value] = RunStatus.TIME_LIMIT_EXCEEDED.get_enum_value()
        test_case_to_run_status_mapping[
            RunTestCaseStatus.PROJECT_CRASHED.value] = RunStatus.PROJECT_CRASHED.get_enum_value()
        test_case_to_run_status_mapping[RunTestCaseStatus.MULTIPLE_TEST_FILES_PRESENT.value] = None
        test_case_to_run_status_mapping[RunTestCaseStatus.NO_TEST_FILE_PRESENT.value] = None
        test_case_to_run_status_mapping[RunTestCaseStatus.NO_TEST_PRESENT.value] = None
        test_case_to_run_status_mapping[RunTestCaseStatus.QUERY_ERROR.value] = RunStatus.QUERY_ERROR.get_enum_value()

        return test_case_to_run_status_mapping[value]


class LiveRunStatus(Enum):
    IN_QUEUE = (1, 'In Queue', None)
    PROCESSING = (2, 'Processing', None)
    ACCEPTED = (3, 'Accepted', RunTestCaseStatus.TRUE.value)
    WRONG_ANSWER = (4, 'Wrong Answer', RunTestCaseStatus.FALSE.value)
    TIMED_OUT = (5, 'Time Limit Exceeded', RunTestCaseStatus.TIMED_OUT.value)
    SYSTEM_ERROR = (6, 'System Error', None)
    SETUP_ERROR = (7, 'Setup Issue', None)
    CANCELLED = (8, 'Cancelled', None)
    QUERY_ERROR = (9, 'Query Error', RunTestCaseStatus.QUERY_ERROR.value)

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_output_values(cls):
        return [LiveRunStatus.ACCEPTED.get_enum_value(), LiveRunStatus.WRONG_ANSWER.get_enum_value(),
                LiveRunStatus.TIMED_OUT.get_enum_value(), LiveRunStatus.QUERY_ERROR.get_enum_value()]

    @classmethod
    def get_run_test_case_status(cls, live_run_status_value):
        return EnumUtil.get_enum_from_value_tuple(LiveRunStatus, live_run_status_value, 0).value[2]


class LiveRunType(Enum):
    SERVER = ('Server', 'Backend Micro Project')
    WEB = ('Web', 'Frontend Micro Project')
    WEB_V2 = ('Web_V2', 'Frontend New')
    SQL = ('SQL', 'SQL Micro Project')

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, LiveRunType)


class TestType(Enum):
    PRACTICE = 'PRACTICE'
    TEST = 'TEST'
    CONTEST = 'CONTEST'

    @classmethod
    def get_test_related_types(cls):
        return [TestType.TEST.value, TestType.CONTEST.value]


class SubmissionType(Enum):
    PROJECT = 'PROJECT'
    DS_ALGO = 'DS_ALGO'


class PlagiarismStatus(Enum):
    RAW = 'RAW'
    PLAGIARISED = 'PLAGIARISED'
    NON_PLAGIARISED = 'NON_PLAGIARISED'
    NA = "NA"

    @classmethod
    def get_statuses_for_non_plagiarised_submissions(cls):
        return [PlagiarismStatus.NON_PLAGIARISED.value, PlagiarismStatus.NA.value]


class QuestionExecutionType(Enum):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'
    FILE_UPLOAD = 'FILE_UPLOAD'


class DeployStatus(Enum):
    PENDING = 'PENDING'
    STOPPING = 'STOPPING'
    DEPLOYING = 'DEPLOYING'
    DEPLOYED = 'DEPLOYED'
    FAILED = 'FAILED'
    TERMINATED = 'TERMINATED'

    @classmethod
    def is_non_deployable_status(cls, enum_value):
        return enum_value == DeployStatus.PENDING.value or enum_value == DeployStatus.DEPLOYING.value


class InstanceStatus(Enum):
    NA = 'NA'
    PASSWORD_READY = 'PASSWORD_READY'
    STOPPED_FOR_SG_UPDATE_BEFORE_START = 'STOPPED_FOR_SG_UPDATE_BEFORE_START'
    REBOOT_AND_WAITING_FOR_SSM_BEFORE_START = 'REBOOT_AND_WAITING_FOR_SSM_BEFORE_START'
    SSM_READY_BEFORE_START = 'SSM_READY_BEFORE_START'
    CMD_EXEC_AND_READY = 'CMD_EXEC_AND_READY'
    STOPPED_FOR_SG_UPDATE = 'STOPPED_FOR_SG_UPDATE'
    REBOOT_AND_WAITING_FOR_SSM = 'REBOOT_AND_WAITING_FOR_SSM'
    SSM_READY = 'SSM_READY'
    FAILED = 'FAILED'

    @classmethod
    def get_deployed_statuses(cls):
        return [InstanceStatus.PASSWORD_READY.value, InstanceStatus.CMD_EXEC_AND_READY.value]

    @classmethod
    def get_waiting_for_ssm_statuses(cls):
        return [InstanceStatus.REBOOT_AND_WAITING_FOR_SSM.value,
                InstanceStatus.REBOOT_AND_WAITING_FOR_SSM_BEFORE_START.value]

    @classmethod
    def get_completed_statuses(cls):
        return [InstanceStatus.SSM_READY.value]


class Ec2InstanceStatus(Enum):
    PENDING = ('pending', 0)
    RUNNING = ('running', 16)
    SHUTTING_DOWN = ('shutting-down', 32)
    TERMINATED = ('terminated', 48)
    STOPPING = ('stopping', 64)
    STOPPED = ('stopped', 80)

    def get_enum_value(self):
        return self.value[0]

    def get_enum_code(self):
        return self.value[1]

    @classmethod
    def get_code_from_value(cls, ins_status):
        return EnumUtil.get_second_arg_from_first_arg(ins_status, Ec2InstanceStatus)


class PortStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    INUSE = 'INUSE'


class DeployType(Enum):
    DOCKER = 'DOCKER'
    GIT = 'GIT'
    AWS_LT = 'AWS_LT'

    @classmethod
    def get_deploy_type_meta(cls, deploy_type, data):
        if deploy_type == DeployType.GIT.value:
            return [data.get('git_url', None), 'Git Url']
        elif deploy_type == DeployType.DOCKER.value:
            return [data.get('docker_image_name', None), 'Docker Image Name']
        elif deploy_type == DeployType.AWS_LT.value:
            return [data.get('aws_lt_id', None), 'AWS Launch Template Id']
        else:
            return None

    @classmethod
    def requires_alb(cls, deploy_type):
        if deploy_type in [DeployType.DOCKER.value]:
            return True
        return False

    @classmethod
    def get_instance_related(cls):
        return [DeployType.AWS_LT.value]

    @classmethod
    def get_non_instance_related(cls):
        return [DeployType.DOCKER.value]


class ClusterType(Enum):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'

    @classmethod
    def is_online(cls, value):
        return value == ClusterType.ONLINE.value


class NetworkMode(Enum):
    BRIDGE = 'bridge'
    NONE = 'none'


class CodeDeployEvalStatus(Enum):
    NA = 'NA'
    NOT_STARTED = 'NOT_STARTED'
    COMPLETED = 'COMPLETED'


class CodeDeployPurpose(Enum):
    BUILDER = 'BUILDER' # for running the ques itself (git) from ques builder table, not the main ques table
    LIVE = 'LIVE' # for running only the backend (docker) for frontend, mobile, backend, etc questions
    WORKSPACE = 'WORKSPACE'
    CODE_PLAY = 'CODE_PLAY'
    OFFLINE_WORKSPACE = 'OFFLINE_WORKSPACE'

    @classmethod
    def is_builder_question(cls, purpose):
        return True if purpose == CodeDeployPurpose.BUILDER.value else False

    @classmethod
    def is_online_workspace(cls, purpose):
        return True if purpose in [CodeDeployPurpose.WORKSPACE.value] else False

    @classmethod
    def is_offline_workspace(cls, purpose):
        return True if purpose in [CodeDeployPurpose.OFFLINE_WORKSPACE.value] else False

    @classmethod
    def is_workspace(cls, purpose):
        return True if purpose in [CodeDeployPurpose.WORKSPACE.value, CodeDeployPurpose.OFFLINE_WORKSPACE.value] \
            else False

    @classmethod
    def get_execution_mapping(cls):
        return {
            CodeDeployPurpose.BUILDER.value: QuestionExecutionType.ONLINE.value,
            CodeDeployPurpose.LIVE.value: QuestionExecutionType.ONLINE.value,
            CodeDeployPurpose.WORKSPACE.value: QuestionExecutionType.ONLINE.value,
            CodeDeployPurpose.CODE_PLAY.value: QuestionExecutionType.ONLINE.value,
            CodeDeployPurpose.OFFLINE_WORKSPACE.value: QuestionExecutionType.OFFLINE.value
        }

    @classmethod
    def is_valid_execution(cls, purpose, exec_type):
        execution_mapping = cls.get_execution_mapping()
        return execution_mapping[purpose] == exec_type

    @classmethod
    def is_run_id_required(cls, purpose):
        return purpose == CodeDeployPurpose.CODE_PLAY.value

    @classmethod
    def get_ram_mapping(cls):
        return {
            CodeDeployPurpose.BUILDER.value: 1024,
            CodeDeployPurpose.LIVE.value: 1024,
            CodeDeployPurpose.WORKSPACE.value: 1024,
            CodeDeployPurpose.CODE_PLAY.value: 1024,
            CodeDeployPurpose.OFFLINE_WORKSPACE.value: 1024
        }

    @classmethod
    def get_network_mapping(cls):
        return {
            CodeDeployPurpose.BUILDER.value: NetworkMode.BRIDGE.value,
            CodeDeployPurpose.LIVE.value: NetworkMode.BRIDGE.value,
            CodeDeployPurpose.WORKSPACE.value: NetworkMode.BRIDGE.value,
            CodeDeployPurpose.CODE_PLAY.value: NetworkMode.BRIDGE.value,
            CodeDeployPurpose.OFFLINE_WORKSPACE.value: NetworkMode.BRIDGE.value
        }

    @classmethod
    def get_volume_mapping(cls, efs_id, root_folder):
        return {
            CodeDeployPurpose.BUILDER.value: [],
            CodeDeployPurpose.LIVE.value: [],
            CodeDeployPurpose.WORKSPACE.value: [],
            CodeDeployPurpose.CODE_PLAY.value: [],
            CodeDeployPurpose.OFFLINE_WORKSPACE.value: [{
                'name': 'efs-online-workspace',
                'efsVolumeConfiguration': {
                    'fileSystemId': efs_id,
                    'rootDirectory': root_folder,
                    'transitEncryption': 'ENABLED'
                }
            }]
        }

    @classmethod
    def get_mount_point_mapping(cls):
        return {
            CodeDeployPurpose.BUILDER.value: [],
            CodeDeployPurpose.LIVE.value: [],
            CodeDeployPurpose.WORKSPACE.value: [],
            CodeDeployPurpose.CODE_PLAY.value: [],
            CodeDeployPurpose.OFFLINE_WORKSPACE.value: [{
                'sourceVolume': 'efs-online-workspace',
                'containerPath': '/mnt/efs'
            }]
        }

    @classmethod
    def get_cluster_type_mapping(cls):
        return {
            CodeDeployPurpose.BUILDER.value: ClusterType.ONLINE.value,
            CodeDeployPurpose.LIVE.value: ClusterType.ONLINE.value,
            CodeDeployPurpose.WORKSPACE.value: ClusterType.ONLINE.value,
            CodeDeployPurpose.CODE_PLAY.value: ClusterType.ONLINE.value,
            CodeDeployPurpose.OFFLINE_WORKSPACE.value: ClusterType.OFFLINE.value
        }

    @classmethod
    def get_ram(cls, purpose):
        ram_mapping = cls.get_ram_mapping()
        return ram_mapping[purpose]

    @classmethod
    def get_network(cls, purpose):
        network_mapping = cls.get_network_mapping()
        return network_mapping[purpose]

    @classmethod
    def get_volumes(cls, purpose, efs_id, root_folder):
        volume_mapping = cls.get_volume_mapping(efs_id, root_folder)
        return volume_mapping[purpose]

    @classmethod
    def get_mount_point(cls, purpose):
        mount_point_mapping = cls.get_mount_point_mapping()
        return mount_point_mapping[purpose]

    @classmethod
    def get_cluster_type(cls, purpose):
        cluster_type_mapping = cls.get_cluster_type_mapping()
        return cluster_type_mapping[purpose]


class AwsResourceType(Enum):
    S3 = (1, 'S3')

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]


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

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, RunStatus)

    @classmethod
    def get_status_for_plagiarism(cls):
        return [RunStatus.ACCEPTED.get_enum_value()]

    @classmethod
    def get_re_run_statuses(cls):
        return [RunStatus.IN_QUEUE.get_enum_value(), RunStatus.PROCESSING.get_enum_value(),
                RunStatus.INTERNAL_ERROR.get_enum_value()]

    @classmethod
    def is_valid_status_for_cd_eval(cls, status):
        return status in [RunStatus.ACCEPTED.get_enum_value(), RunStatus.WRONG_ANSWER.get_enum_value(),
                          RunStatus.TIME_LIMIT_EXCEEDED.get_enum_value()]

    @classmethod
    def get_processing_statuses(cls):
        return [RunStatus.IN_QUEUE.get_enum_value(), RunStatus.PROCESSING.get_enum_value()]

    @classmethod
    def get_statuses_required_for_quality_eval(cls):
        return [RunStatus.ACCEPTED.get_enum_value(), RunStatus.WRONG_ANSWER.get_enum_value(), RunStatus.TIME_LIMIT_EXCEEDED.get_enum_value()]


class RunDiscrepancyStatus(Enum):
    NONE = (1, 'None')
    PARTIAL = (2, 'Partial')
    COMPLETE = (3, 'Complete')

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]


class CodeSubmissionTestCaseStatus(Enum):
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

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, CodeSubmissionTestCaseStatus)


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

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, CodeSubmissionStatus)

    @classmethod
    def get_in_processing_statuses(cls):
        return [CodeSubmissionStatus.PROCESSING.get_enum_value()]

    @classmethod
    def get_re_run_statuses(cls):
        return [CodeSubmissionStatus.IN_QUEUE.get_enum_value(), CodeSubmissionStatus.PROCESSING.get_enum_value(),
                CodeSubmissionStatus.INTERNAL_ERROR.get_enum_value(),
                CodeSubmissionStatus.CJ_INTERNAL_ERROR.get_enum_value()]

    @classmethod
    def get_status_for_plagiarism(cls):
        return [CodeSubmissionStatus.ACCEPTED.get_enum_value()]

    @classmethod
    def get_value_to_name_map(cls):
        response = dict()
        for status in CodeSubmissionStatus:
            response[status.get_enum_value()] = EnumUtil.get_second_arg_from_first_arg(status.get_enum_value(), CodeSubmissionStatus)
        return response


class RefreshMetadataWorkflowVersion(Enum):
    V1 = 'V1'
    V2 = 'V2'
    V3 = 'V3'


class UpdateCodeQualityWorkflowVersion(Enum):
    V1 = 'V1'
    V2 = 'V2'
    V3 = 'V3'


class TagFeatureType(Enum):
    ATTRIBUTE = 'ATTRIBUTE'
    FILTER = 'FILTER'


class TagType(Enum):
    TECHNOLOGY_ATTR = 'TECHNOLOGY_ATTR'
    QUESTION_TYPE = 'QUESTION_TYPE'


class RunEvalType(Enum):
    INTEGRATION = 'INTEGRATION'
    UNIT = 'UNIT'
    MUTATION = 'MUTATION'
    QUALITY = 'QUALITY'
    NO_EVAL = 'NO_EVAL'
    EXTERNAL_INTEGRATION = 'EXTERNAL_INTEGRATION'

    @classmethod
    def ignore_build_deploy(cls, run_eval_types):
        if RunEvalType.EXTERNAL_INTEGRATION in run_eval_types:
            return True
        return False

    @classmethod
    def has_external_endpoint(cls, run_eval_types):
        if RunEvalType.EXTERNAL_INTEGRATION in run_eval_types:
            return True
        return False

    @classmethod
    def has_no_repo(cls, run_eval_types):
        if RunEvalType.EXTERNAL_INTEGRATION in run_eval_types:
            return True
        return False

    @classmethod
    def has_no_docker(cls, run_eval_types):
        if RunEvalType.EXTERNAL_INTEGRATION in run_eval_types:
            return True
        return False


class QuestionEvalType(Enum):
    INTEGRATION = ('INTEGRATION', [RunEvalType.INTEGRATION], True, False)
    UNIT = ('UNIT', [RunEvalType.UNIT], True, False)
    INTEGRATION_AND_UNIT = ('INTEGRATION_AND_UNIT', [RunEvalType.INTEGRATION, RunEvalType.UNIT], True, False)
    UNIT_AND_MUTATION = ('UNIT_AND_MUTATION', [RunEvalType.UNIT, RunEvalType.MUTATION], True, False)
    INTEGRATION_AND_UNIT_AND_MUTATION = ('INTEGRATION_AND_UNIT_AND_MUTATION', [RunEvalType.INTEGRATION,
                                                                               RunEvalType.UNIT,
                                                                               RunEvalType.MUTATION], True, False)
    QUALITY = ('QUALITY', [RunEvalType.QUALITY], True, False)
    NO_EVAL = ('NO_EVAL', [RunEvalType.NO_EVAL], False, True)
    EXTERNAL_INTEGRATION = ('EXTERNAL_INTEGRATION', [RunEvalType.EXTERNAL_INTEGRATION], False, False)

    @classmethod
    def get_eval_type_env_args(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, QuestionEvalType)

    @classmethod
    def requires_lang_validation(cls, eval_type):
        eval_type_enum = EnumUtil.get_enum_from_value_tuple(QuestionEvalType, eval_type, 0)
        return eval_type_enum.value[2]

    @classmethod
    def has_manual_eval(cls, eval_type):
        eval_type_enum = EnumUtil.get_enum_from_value_tuple(QuestionEvalType, eval_type, 0)
        return eval_type_enum.value[3]


class QuestionRepoType(Enum):
    DEFAULT = 'DEFAULT'
    CUSTOM = 'CUSTOM'


class OptionEvalType(Enum):
    INTEGRATION = 'INTEGRATION'
    UNIT = 'UNIT'
    INTEGRATION_UNIT = 'INTEGRATION_UNIT'
    INTEGRATION_POSTMAN = 'INTEGRATION_POSTMAN'
    INTEGRATION_UNIT_MUTATION = 'INTEGRATION_UNIT_MUTATION'
    MUTATION = 'MUTATION'
    QUALITY = 'QUALITY'
    NO_EVAL = 'NO_EVAL'
    METRICS = 'METRICS'
    LOG_ANALYSIS = 'LOG_ANALYSIS'

    @classmethod
    def is_mutation_required(cls, eval_type):
        if eval_type in [OptionEvalType.UNIT.value, OptionEvalType.MUTATION.value,
                         OptionEvalType.INTEGRATION_UNIT_MUTATION.value]:
            return True
        return False

    @classmethod
    def is_unit_required(cls, eval_type):
        if eval_type in [OptionEvalType.UNIT.value]:
            return True
        return False

    @classmethod
    def is_integration_test_required(cls, eval_type):
        if eval_type in [OptionEvalType.INTEGRATION_UNIT.value]:
            return True
        return False

    @classmethod
    def is_postman_integration_test(cls, eval_type):
        if eval_type in [OptionEvalType.INTEGRATION_POSTMAN.value]:
            return True
        return False


class QuestionType(Enum):
    BACKEND_MICRO_PROJECT = ('BACKEND_MICRO_PROJECT', 'Backend Micro Project', False, True, 1024, True, False, False)
    WEB_MICRO_PROJECT = ('WEB_MICRO_PROJECT', 'Frontend Micro Project', False, True, 1024, True, False, True)
    WEB_MICRO_PROJECT_V2 = ('WEB_MICRO_PROJECT_V2', 'Frontend Project (New)', False, False, 1024, True, False, False)
    ANDROID_MICRO_PROJECT = ('ANDROID_MICRO_PROJECT', 'Android Micro Project', False, False, 1024, True, False, False)
    IOS_MICRO_PROJECT = ('IOS_MICRO_PROJECT', 'IOS Micro Project', False, False, 1024, True, False, False)
    HYBRID_MICRO_PROJECT = ('HYBRID_MICRO_PROJECT', 'Hybrid Micro Project', False, False, 1024, True, False, False)
    DS_ALGO = ('DS_ALGO', 'DS Algo Question', False, False, 1024, True, False, False)
    SQL_MICRO_PROJECT = ('SQL_MICRO_PROJECT', 'SQL Micro Project', True, False, 1024, True, False, False)
    MACHINE_LEARNING_MICRO_PROJECT = ('MACHINE_LEARNING_MICRO_PROJECT', 'Machine Learning Micro Project', False, False, 2048, True, False, False)
    QA_MICRO_PROJECT = ('QA_MICRO_PROJECT', 'Machine Learning Micro Project', False, False, 1024, True, False, False)
    DEVOPS_MICRO_PROJECT = ('DEVOPS_MICRO_PROJECT', 'DevOps Micro Project', False, False, 1024, True, False, False)
    SUBJECTIVE = ('SUBJECTIVE', 'Subjective Question', True, False, 1024, False, True, False)

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_types_having_eval_via_async_thread(cls):
        return [QuestionType.WEB_MICRO_PROJECT_V2.get_enum_value()]

    @classmethod
    def is_chrome_url_required_for_verification(cls, ques_type):
        enum = EnumUtil.get_enum_from_value_tuple(QuestionType, ques_type, 0)
        return enum.value[7]

    @classmethod
    def get_ram_for_workspace(cls, ques_type):
        enum = EnumUtil.get_enum_from_value_tuple(QuestionType, ques_type, 0)
        return enum.value[4]

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, QuestionType)

    @classmethod
    def validate_code_ques_types(cls, ques_type):
        for member in QuestionType:
            if member.value[0] == ques_type and member.value[2] is True:
                return True
        return False

    @classmethod
    def is_live_run_via_utility(cls, ques_type):
        for member in QuestionType:
            if member.value[0] == ques_type and member.value[3] is True:
                return True
        return False

    @classmethod
    def requires_lang_validation(cls, ques_type):
        eval_type_enum = EnumUtil.get_enum_from_value_tuple(QuestionType, ques_type, 0)
        return eval_type_enum.value[5]

    @classmethod
    def get_default_code_deploy_ques_type(cls):
        return QuestionType.BACKEND_MICRO_PROJECT.get_enum_value()

    @classmethod
    def has_manual_eval(cls, ques_type):
        for member in QuestionType:
            if member.value[0] == ques_type and member.value[6] is True:
                return True
        return False

    @classmethod
    def get_ques_type_to_display_name_map_for_worker_li(cls):
        return {
            QuestionType.DS_ALGO.value[0]: 'DS_ALGO',
            QuestionType.BACKEND_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.WEB_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.WEB_MICRO_PROJECT_V2.value[0]: 'MICRO_PROJECT',
            QuestionType.ANDROID_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.IOS_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.HYBRID_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.SQL_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.QA_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.MACHINE_LEARNING_MICRO_PROJECT.value[0]: 'MICRO_PROJECT',
            QuestionType.DEVOPS_MICRO_PROJECT.value[0]: 'MICRO_PROJECT'
        }


class RestEvaluatorSubTestStatus(Enum):
    SUCCEEDED = ('SUCCEEDED',)
    FAILED = ('FAILED',)
    TIMED_OUT = ('TIMED_OUT',)

    def get_enum_value(self):
        return self.value[0]


class WebEvaluatorSubTestStatus(Enum):
    FAILED = ('failed',)
    PASSED = ('passed',)

    def get_enum_value(self):
        return self.value[0]


class SQLEvaluatorSubTestStatus(Enum):
    SUCCEEDED = ('SUCCEEDED', RunStatus.ACCEPTED.value, LiveRunStatus.ACCEPTED, RunTestCaseStatus.TRUE.value)
    FAILED = ('FAILED', RunStatus.WRONG_ANSWER.get_enum_value(), LiveRunStatus.WRONG_ANSWER,
              RunTestCaseStatus.FALSE.value)
    TIMED_OUT = ('TIMED_OUT', RunStatus.TIME_LIMIT_EXCEEDED.get_enum_value(), LiveRunStatus.TIMED_OUT,
                 RunTestCaseStatus.TIMED_OUT.value)
    QUERY_ERROR = ('QUERY_ERROR', RunStatus.QUERY_ERROR.get_enum_value(), LiveRunStatus.QUERY_ERROR,
                   RunTestCaseStatus.QUERY_ERROR.value)

    def get_enum_value(self):
        return self.value[0]

    @classmethod
    def get_live_run_statuses_for_csv_upload(cls):
        return [LiveRunStatus.ACCEPTED.get_enum_display_value(), LiveRunStatus.WRONG_ANSWER.get_enum_display_value()]

    @classmethod
    def get_run_statuses_for_csv_upload(cls):
        return [RunStatus.ACCEPTED.get_enum_value(), RunStatus.WRONG_ANSWER.get_enum_value()]

    @classmethod
    def get_mapped_run_status(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, SQLEvaluatorSubTestStatus)

    @classmethod
    def get_mapped_live_run_status(cls, value):
        enum = EnumUtil.get_enum_from_value_tuple(SQLEvaluatorSubTestStatus, value, 0)
        return enum.value[2]

    @classmethod
    def get_mapped_run_test_case_status(cls, value):
        enum = EnumUtil.get_enum_from_value_tuple(SQLEvaluatorSubTestStatus, value, 0)
        return enum.value[3]


class QualityEvaluatorSubTestCaseStatus(Enum):
    FAILED = ('FAILED',)
    PASSED = ('SUCCEEDED',)

    def get_enum_value(self):
        return self.value[0]


class ProgrammingWorkflowVersion(Enum):
    V1 = ('V1',)
    V2 = ('V2',)

    def get_enum_value(self):
        return self.value[0]


class ProjectWorkflowVersion(Enum):
    V1 = ('V1', True, 1)
    V2 = ('V2', False, 1)
    V3 = ('V3', False, 1) # New Front End
    V4 = ('V4', False, 2) # Extended version of V2

    def get_enum_value(self):
        return self.value[0]

    @classmethod
    def is_user_token_required(cls, version):
        enum = EnumUtil.get_enum_from_value_tuple(ProjectWorkflowVersion, version, 0)
        return enum.value[1]

    @classmethod
    def get_min_commit_length(cls, version):
        enum = EnumUtil.get_enum_from_value_tuple(ProjectWorkflowVersion, version, 0)
        return enum.value[2]


class UserUrlVersion(Enum):
    V1 = 'V1'
    V2 = 'V2'

    def get_enum_value(self):
        return self.value[0]


class CodeSubmissionLiveRunStatus(Enum):
    PROCESSING = (1, )
    COMPLETED = (2, )

    def get_enum_value(self):
        return self.value[0]


class SqlArtifactStatus(Enum):
    PENDING = 'PENDING'
    UPLOADED = 'UPLOADED'


class RunWorkflow(Enum):
    RUN = 'RUN'
    QUALITY = 'QUALITY'


class CommandType(Enum):
    AWS_S3_DETAILS = 'AWS_S3_DETAILS'


class UserUrlMode(Enum):
    LOCAL = (1, 'Local')
    CLOUD = (2, 'Cloud')

    def get_enum_value(self):
        return self.value[0]

    def get_enum_display_value(self):
        return self.value[1]

    @classmethod
    def get_display_value_from_value(cls, value):
        return EnumUtil.get_second_arg_from_first_arg(value, UserUrlMode)

    @classmethod
    def is_valid(cls, mode_value):
        for member in UserUrlMode:
            if member.value[0] == mode_value:
                return True
        return False


class WorkerType(Enum):
    PROGRAMMING_SUBMISSION = 'PROGRAMMING_SUBMISSION'
    PROGRAMMING_LIVERUN = 'PROGRAMMING_LIVERUN'
    API_RUN_SUBMISSION = 'API_RUN_SUBMISSION'

    @classmethod
    def get_statuses_for_worker_status(cls, worker_type=None):
        if worker_type in [WorkerType.PROGRAMMING_SUBMISSION, WorkerType.PROGRAMMING_LIVERUN, WorkerType.API_RUN_SUBMISSION]:
            return [CodeSubmissionStatus.IN_QUEUE.get_enum_value(), CodeSubmissionStatus.PROCESSING.get_enum_value()]


class WorkerUpdateInstancesStatus(Enum):
    INITIATED = 'Initiated'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    ERROR = 'Error'


class LaunchInstancesWorkerStage(Enum):
    WORKFLOW_INITIATED = 'WORKFLOW INITIATED'
    EXECUTED_UPDATE_SERVICES = 'EXECUTED UPDATE SERVICES'
    EXECUTED_ADD_INSTANCES = 'EXECUTED ADD INSTANCES'
    EXECUTED_REMOVE_INSTANCES = 'EXECUTED REMOVE INSTANCES'
    UPDATED_DB = 'UPDATED DB'



class LanguageTransformers(Enum):
    TYPESCRIPT_TO_JAVASCRIPT = 'TS_TO_JS'

    @classmethod
    def get_enum_name_from_enum_value(cls, value):
        return EnumUtil.get_enum_from_value(LanguageTransformers, value)


class ProjectSetUpStatus(Enum):
    SETTING_UP_WRK = 'Setting up the workspace'
    SETTING_UP_ENV = 'Setting up the environment'
    ENV_UP = 'Environment up'
    STARTING_SRVR = 'Starting server'
    CONN_TO_SRVR = 'Connected to server'
    STARTING_CONN_VERIFY = 'Starting connection verification'
    CONN_VERIFY = 'Connection verified (Endpoint is Up)'
    CONN_VERIFY_FAILED = 'Connection verified failed (Endpoint is Down)'
    SRVR_CONN_FAILED = 'Server connection failed'
    ENV_SETUP_FAILED = 'Error in setting up environment'
    SETTING_UP_NGROK = "Setting up ngrok"
    NGROK_UP = "Ngrok up"
    VERIFYING_COMMIT = "Verifying commit"
    VERIFIED_COMMIT = "verified commit"


class LocalIdeOsType(Enum):
    WINDOWS = ('WINDOWS', 0)
    MAC_OS = ('MAC_OS', 1)
    LINUX_UBUNTU = ('LINUX_UBUNTU', 2)
    LINUX_OTHER = ('LINUX_OTHER', 3)

    @classmethod
    def is_valid(cls, mode_value):
        for member in LocalIdeOsType:
            if member.value[1] == mode_value:
                return True
        return False
