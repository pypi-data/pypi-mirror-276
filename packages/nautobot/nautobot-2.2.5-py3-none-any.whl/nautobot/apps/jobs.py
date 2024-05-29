"""Nautobot Jobs API."""

from nautobot.core.celery import register_jobs
from nautobot.core.celery.encoders import NautobotKombuJSONEncoder
from nautobot.core.jobs import GitRepositoryDryRun, GitRepositorySync
from nautobot.extras.jobs import (
    BaseJob,
    BooleanVar,
    ChoiceVar,
    DatabaseFileField,
    DryRunVar,
    enqueue_job_hooks,
    FileVar,
    get_job,
    get_jobs,
    IntegerVar,
    IPAddressVar,
    IPAddressWithMaskVar,
    IPNetworkVar,
    is_job,
    is_variable,
    Job,
    JobButtonReceiver,
    JobHookReceiver,
    JSONVar,
    MultiChoiceVar,
    MultiObjectVar,
    ObjectVar,
    RunJobTaskFailed,
    ScriptVariable,
    StringVar,
    TextVar,
)

__all__ = (
    "BaseJob",
    "BooleanVar",
    "ChoiceVar",
    "DatabaseFileField",
    "DryRunVar",
    "enqueue_job_hooks",
    "FileVar",
    "get_job",
    "get_jobs",
    "GitRepositoryDryRun",
    "GitRepositorySync",
    "IntegerVar",
    "IPAddressVar",
    "IPAddressWithMaskVar",
    "IPNetworkVar",
    "is_job",
    "is_variable",
    "Job",
    "JobButtonReceiver",
    "JobHookReceiver",
    "JSONVar",
    "MultiChoiceVar",
    "MultiObjectVar",
    "NautobotKombuJSONEncoder",
    "ObjectVar",
    "register_jobs",
    "RunJobTaskFailed",
    "ScriptVariable",
    "StringVar",
    "TextVar",
)
