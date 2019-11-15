from rhodes import StateMachine
from rhodes.states import Choice, Fail, Parallel, Task, Wait


def artifact_builder(parse_requirements_arn: str, build_python_36_arn: str, build_python_37_arn: str):

    parse_requirements = Task("ParseRequirements", Resource=parse_requirements_arn)

    build_python = Parallel(
        "BuildPython",
        Branches=[
            StateMachine(StartAt=Task("BuildPython36", Resource=build_python_36_arn, End=True)),
            StateMachine(StartAt=Task("BuildPython37", Resource=build_python_37_arn, End=True)),
        ],
        ResultPath="$.build_results",
    )

    unknown_language = Fail("UnknownLanguage", Cause="Unknown Language")

    select_language = Choice(
        "SelectLanguage", Choices=[StringEquals("$.language", "python", build_python)], Default=unknown_language
    )

    sm = StateMachine(Comment="Artifact Builder", StartAt=parse_requirements)

    # select_language.after(parse_requirements)
    parse_requirements.then(select_language)

    send_notices = Task("SendNotices", Resource="", End=True)

    # send_notices.after(build_python)
    build_python.then(send_notices)

    return sm


def artifact_collector(locate_artifact_arn: str, publish_layer_arn: str, write_manifest_arn: str):

    locate_artifact = Task("LocateArtifact", Resource=locate_artifact_arn)

    wait_and_retry = Wait("WaitForReplication", Seconds=15)
    # wait_and_retry.next(locate_artifact)
    wait_and_retry.before(locate_artifact)

    publish_layer = Task("PublishLayer", Resource=publish_layer_arn)

    artifact_found = Choice(
        "ArtifactFound", Choices=[BooleanEquals("$.artifact_found", True, publish_layer)], Default=wait_and_retry
    )

    sm = StateMachine(Comment="Artifact Collector", StartAt=locate_artifact)

    locate_artifact.then(artifact_found)
    # artifact_found.after(locate_artifact)

    write_version_manifest = Task("WriteVersionManifest", Resource=write_manifest_arn, End=True)

    # write_version_manifest.after(publish_layer)
    publish_layer.then(write_version_manifest)

    return sm
