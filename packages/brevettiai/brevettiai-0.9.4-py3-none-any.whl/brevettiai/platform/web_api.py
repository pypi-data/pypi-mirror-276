import base64
import json
import logging
import os
import time
from pathlib import Path
from typing import Type, Optional
from typing import Union, List
from urllib.parse import urlparse, unquote

from oauthlib.oauth2 import LegacyApplicationClient, OAuth2Token
from pydantic import parse_raw_as
from requests_oauthlib import OAuth2Session

from brevettiai.datamodel import Dataset
from brevettiai.datamodel import Tag
from brevettiai.datamodel import web_api_types as api
from brevettiai.io.utils import prompt_for_password
from brevettiai.platform import PlatformBackend
from brevettiai.platform import annotations
from brevettiai.platform import backend as default_backend
from brevettiai.platform.dataset_items import delete_item, get_items, put_item
from brevettiai.platform.models import Job, JobSettings
from brevettiai.platform.platform_credentials import PlatformDatasetCredentials
from brevettiai.utils import env_variables

log = logging.getLogger(__name__)

OAUTH_CLIENT_ID = 'generic_client'
OAUTH_TOKEN_URL = '/connect/token'
OAUTH_SCOPE = 'api offline_access'
OAUTH_TOKENS_PATH = os.path.join(os.path.expanduser("~"), ".brevetti")


class PlatformAPI:
    """
    API interface to brevetti platform

    use `BREVETTI_AI_USER` and `BREVETTI_AI_PW` environment variables to use
    system-wide default username and password
    """
    _session: OAuth2Session = None
    persist_tokens = False
    _token_path = None

    def __init__(self, username=None, password=None, organization="default", host=None,
                 remember_me: bool = True):
        self.host = host or default_backend

        self._s3_credentials = PlatformDatasetCredentials(self)

        self.persist_tokens = remember_me
        self.login(username, password, organization=organization)

    @property
    def host(self):
        return self._host.host if isinstance(self._host, PlatformBackend) else self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def backend(self):
        if isinstance(self._host, PlatformBackend):
            return self._host
        else:
            raise AttributeError("Backend unknown")

    def token_updater(self, token):
        if self.persist_tokens:
            # Persist token
            log.info(f"Persisting token to {self._token_path}")
            self._token_path.parent.mkdir(parents=True, exist_ok=True)
            self._token_path.write_text(json.dumps(token))

    @property
    def session(self):
        if self._session is None:
            self._session = OAuth2Session(
                client=LegacyApplicationClient(client_id=OAUTH_CLIENT_ID, scope=OAUTH_SCOPE),
                auto_refresh_kwargs={
                    'client_id': OAUTH_CLIENT_ID,
                },
                auto_refresh_url=self.host + OAUTH_TOKEN_URL,
                token_updater=self.token_updater,
            )
        return self._session

    def login(self, username=None, password=None, organization="default"):
        username = username or os.getenv(env_variables.BREVETTI_AI_USER)
        password = password or os.getenv(env_variables.BREVETTI_AI_PW)

        token_dir = Path(OAUTH_TOKENS_PATH).joinpath()
        token_id = "/".join((("webapi." + self.host.split('://', 1)[-1]), f"{username or '*'}", organization))
        if username and password:
            self._token_path = token_dir / token_id
            token = self.session.fetch_token(
                token_url=self.host + OAUTH_TOKEN_URL, client_id=OAUTH_CLIENT_ID,
                username=username, password=password, organization_id=organization
            )
            self.token_updater(token)
            return
        else:
            token_paths = list(token_dir.glob(token_id))
            token_paths_map = {p.name: [p] for p in token_paths}
            token_paths = token_paths_map.get(token_id, token_paths_map.get("default", token_paths))
            try:
                for token_path in token_paths:
                    token = OAuth2Token(json.loads(token_path.read_text()))
                    self._token_path = token_path
                    self.session.token = token
                    # If expired get new token

                    if token["expires_at"] < time.time():
                        token = self.session.refresh_token(token_url=self.host + OAUTH_TOKEN_URL)
                        self.session.token = token
                        self.token_updater(token)
                    return
            except Exception:
                pass

            # Fallback to request login details
            if username is None:
                username = input(f"{self.host} - username: ")
            if password is None:
                password = prompt_for_password()

            self.login(username, password, organization=organization)

    def get_user_organizations(self):
        r = self.session.get(self.host + "/api/account/organizations")
        if r.ok:
            return r.json()
        raise Exception("Error getting organizations: HTTP{r.status_code}")

    def get_dataset(self, id: str = None, write_access=False, extended_details=False, **kwargs) -> Union[
        Dataset, List[Dataset]]:
        """
        Get dataset, or list of all datasets

        Args:
            id: dataset id
            write_access: resolve accessrights to the dataset
            extended_details: Include extended details
            **kwargs: Extended search criteria: use ('name', 'reference' 'locked', ...)

        Returns:
            dataset if id is given, otherwise list of datasets
        """
        url = self.host + "/api/data"
        url = url if id is None else url + "/" + id
        if extended_details:
            url += "?extendedDetails=true"
        r = self.session.get(url)
        credentials = self._s3_credentials if write_access else None
        if id is None:
            return [Dataset(**x, backend=self.backend, credentials=credentials)
                    for x in r.json() if all(x.get(k) == v for k, v in kwargs.items())]
        else:
            return Dataset(**r.json(), backend=self.backend, credentials=credentials)

    def get_tag(self, id=None) -> Union[Tag, List[Tag]]:
        """
        Get tag or list of all tags

        Args:
            id: Tag id

        Returns:
            tag if id is given, otherwise a list of tags
        """
        url = self.host + "/api/resources/tags"
        url = url if id is None else url + "/" + id
        r = self.session.get(url)
        return parse_raw_as(Union[Tag, List[Tag]], r.content)

    def get_model(self, id=None, **kwargs) -> Union[api.Model, List[api.Model]]:
        """
        Get model or list of all models

        Args:
            id: model id
            **kwargs: Extended search criteria: use ('name', 'reference' 'locked', ...)

        Returns:
            model if id is given, otherwise a list of models
        """
        url = self.host + "/api/models"
        url = url if id is None else url + "/" + id
        r = self.session.get(url)
        if id is None:
            models = parse_raw_as(List[api.Model], r.content)
            return [x for x in models if all(getattr(x, k, None) == v for k, v in kwargs.items())]
        else:
            return parse_raw_as(api.Model, r.content)

    def get_report(self, id=None, **kwargs) -> Union[api.Report, List[api.Report]]:
        """
        Get test report, or list of all reports

        Args:
            id: report id
            **kwargs: Extended search criteria: use ('name', 'reference' 'locked', ...)

        Returns:
            report if id is given, otherwise a list of reports
        """
        url = self.host + "/api/reports"
        url = url if id is None else url + "/" + id
        r = self.session.get(url)
        if id is None:
            reports = parse_raw_as(List[api.Report], r.content)
            return [x for x in reports if all(getattr(x, k, None) == v for k, v in kwargs.items())]
        else:
            return parse_raw_as(api.Report, r.content)

    def get_artifacts(self, obj: Union[api.Model, api.Report], prefix: str = '', recursive: bool = False,
                      add_prefix=False) -> List[api.FileEntry]:
        """
        Get artifacts for model or test report

        Args:
            obj: model/test report object
            prefix: object prefix (folder)

        Returns:
            List of files
        """
        if isinstance(obj, api.Model):
            r = self.session.get(f"{self.host}/api/models/{obj.id}/artifacts?prefix={prefix}")
        elif isinstance(obj, api.Report):
            r = self.session.get(f"{self.host}/api/reports/{obj.id}/artifacts?prefix={prefix}")
        else:
            raise NotImplementedError("Artifacts not available for type")
        artifacts = parse_raw_as(List[api.FileEntry], r.content)

        if not recursive:
            if add_prefix:
                for a in artifacts:
                    a.name = prefix + a.name
            return artifacts

        all_artifacts = []
        for a in artifacts:
            if a.mime_type == "folder":
                all_artifacts.extend(
                    self.get_artifacts(obj, prefix=f"{prefix}{a.name}/", recursive=True, add_prefix=add_prefix))
            else:
                if add_prefix:
                    a.name = prefix + a.name
                all_artifacts.append(a)

        return all_artifacts

    def get_application_classification(self, application: api.Application = None,
                                       project: api.Project = None) -> Union[api.Application, List[api.Application]]:
        url = self.host + f"/api/resources/projects/{project.id}/applications/{application.id}/classification"
        if application.type == 1:  # Classification application type
            r = self.session.get(url)
            return parse_raw_as(api.Application, r.content)
        elif application.type == 0:  # Generic application type
            return application
        else:  # Unknow application type
            raise ValueError("Unknown application type")

    def get_application(self, id=None) -> Union[api.Application, List[api.Application]]:
        """
        Get application by id

        Args:
            id:

        Returns:
            application if id is given, otherwise a list of applications
        """
        projects = self.get_project()
        applications = [a for p in projects for a in p.applications if id == a.id]
        if len(applications) == 1:
            return applications[0]
        else:
            return applications

    def get_device(self, id=None):
        url = self.host + "/api/devices"
        url = url if id is None else url + "/" + id
        r = self.session.get(url)
        return parse_raw_as(List[api.Device], r.content)

    def get_project(self, id=None) -> Union[api.Project, List[api.Project]]:
        url = self.host + "/api/resources/projects"
        url = url if id is None else url + "/" + id
        r = self.session.get(url)
        return parse_raw_as(Union[api.Project, List[api.Project]], r.content)

    def get_modeltype(self, id=None, master=False) -> Union[api.ModelType, List[api.ModelType]]:
        """
        Get model type

        Args:
            id:
            master: use master mode

        Returns:

        """
        url = f"{self.host}/api/{'master/' if master else 'resources/'}modeltypes/{id if id else ''}"
        r = self.session.get(url)
        return parse_raw_as(Union[api.ModelType, List[api.ModelType]], r.content)

    def get_reporttype(self, id=None, master=False) -> Union[api.ReportType, List[api.ReportType]]:
        """
        Get report type

        Args:
            id:
            master: use master mode

        Returns:

        """
        url = f"{self.host}/api/{'master/' if master else 'resources/'}reporttypes/{id if id else ''}"
        r = self.session.get(url)
        return parse_raw_as(Union[api.ReportType, List[api.ReportType]], r.content)

    def get_available_model_types(self):
        """
        List all available model types
        """
        r = self.session.get(f"{self.host}/api/models/availabletypes")
        return parse_raw_as(List[api.ModelType], r.content)

    def get_dataset_annotations(self, dataset, **kwargs):
        if hasattr(dataset, "id"):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        return annotations.get_dataset_annotations(self.host, dataset_id, get_fn=self.session.get, **kwargs)

    def update_annotation(self, dataset, image_path, annotation, **kwargs):
        if hasattr(dataset, "id"):
            dataset_id = dataset.id
        else:
            dataset_id = dataset

        return annotations.update_annotation(self.host, dataset_id,
                                             image_path=image_path, annotation=annotation,
                                             post_fn=self.session.post, **kwargs)

    def create_annotation(self, dataset, image_path, annotation_name=None):
        return annotations.create_annotation(self.host, dataset=dataset, image_path=image_path,
                                             annotation_name=annotation_name, post_fn=self.session.post)

    def delete_annotation(self, dataset, image_path, annotation_name):
        return annotations.delete_annotation(self.host, dataset=dataset, image_path=image_path,
                                             annotation_name=annotation_name, delete_fn=self.session.delete)

    def rename_annotation(self, dataset, image_path, annotation_name, new_annotation_name):
        entry = self.get_dataset_annotations(dataset, image_path=image_path)
        annotation = entry.annotation_files[annotation_name]
        self.create_annotation(dataset, image_path, annotation_name=new_annotation_name)
        self.update_annotation(dataset, image_path, annotation_name=new_annotation_name, annotation=annotation)
        self.delete_annotation(dataset, image_path, annotation_name=annotation_name)

    def get_items(self, dataset=None, item_id=None, filter: dict = None, **kwargs):
        return get_items(host=self.host, get_fn=self.session.get,
                         dataset=dataset, item_id=item_id, filter=filter, **kwargs)

    def put_item(self, item, **kwargs):
        return put_item(host=self.host, put_fn=self.session.put, item=item, **kwargs)

    def delete_item(self, dataset_id, item_id, **kwargs):
        return delete_item(host=self.host, delete_fn=self.session.delete,
                           dataset_id=dataset_id, item_id=item_id, **kwargs)

    def create(self, obj: Union[Dataset, Tag, api.Model, api.Report], **kwargs):
        if isinstance(obj, Dataset):
            payload = obj.dict(include={"name", "reference", "notes", "locked"}, by_alias=True)
            payload["tagIds"] = [tag.id for tag in obj.tags]
            r = self.session.post(f"{self.host}/api/data/", json=payload)
            return self.get_dataset(r.json()["datasetId"], **kwargs)
        elif isinstance(obj, Tag):
            payload = obj.dict(include={"name", "parent_id"}, by_alias=True, exclude_none=True)
            self.session.post(f"{self.host}/api/resources/tags/", json=payload)

            # TODO: return tag id on api
            parent = self.get_tag(obj.parent_id)
            tag = next(filter(lambda x: x.name == obj.name, (parent.children if isinstance(parent, Tag) else parent)))
            return tag
        elif isinstance(obj, api.Model):
            payload = obj.dict(include={"name", "model_type_id", "application_id",
                                        "settings", "dataset_ids", "tag_ids"}, by_alias=True)
            payload["datasetIds"] = payload.pop("datasets")
            r = self.session.post(f"{self.host}/api/models", json=payload)
            return api.Model.parse_raw(r.content)
        elif isinstance(obj, api.Report):
            payload = obj.dict(include={"name", "parent_id", "parent_type", "report_type_id",
                                        "model_ids", "settings", "dataset_ids", "tag_ids"}, by_alias=True)
            payload["datasetIds"] = payload.pop("datasets")
            payload["modelIds"] = payload.pop("models")
            payload["submitToCloud"] = ("submitToCloud" in kwargs and kwargs["submitToCloud"])

            r = self.session.post(f"{self.host}/api/reports", json=payload)
            report = self.get_report(r.json()["id"])
            return report
        else:
            raise NotImplementedError(f"create not implemented for type {type(obj)}")

    def update(self, obj, master=False):
        if isinstance(obj, Dataset):
            payload = obj.dict(include={"name", "reference", "notes", "locked"})
            payload["tagIds"] = [tag.id for tag in obj.tags]
            self.session.post(f"{self.host}/api/data/{obj.id}", json=payload)
        elif isinstance(obj, Tag):
            payload = obj.dict(include={"name", "parent_id"}, by_alias=True, exclude_none=True)
            self.session.post(f"{self.host}/api/resources/tags/{obj.id}", json=payload)
        elif isinstance(obj, api.ModelType):
            if not master:
                raise PermissionError("Not authorized")
            self.session.post(f"{self.host}/api/master/modeltypes/update", json=obj.dict(by_alias=True))
        elif isinstance(obj, api.ReportType):
            if not master:
                raise PermissionError("Not authorized")
            self.session.post(f"{self.host}/api/master/reporttypes/update", json=obj.dict(by_alias=True))
        else:
            raise NotImplementedError(f"create not implemented for type {type(obj)}")

    def update_application_datasets(self, app: api.Application):
        project_id = next(p for p in self.get_project() for a in p.applications if a.id == app.id).id
        self.session.post(f"{self.host}/api/resources/projects/{project_id}/applications/{app.id}/datasets",
                          json=app.dict(by_alias=True, include={"name", "training_dataset_ids", "test_dataset_ids"}))

    def delete(self, obj: Union[Dataset, Tag, api.Model, api.Report, api.SftpUser, api.ReportType, api.ModelType]):
        if isinstance(obj, Dataset):
            self.session.delete(f"{self.host}/api/data/{obj.id}")
        elif isinstance(obj, Tag):
            self.session.delete(f"{self.host}/api/resources/tags/{obj.id}")
        elif isinstance(obj, api.Model):
            self.session.delete(f"{self.host}/api/models/{obj.id}")
        elif isinstance(obj, api.Report):
            self.session.delete(f"{self.host}/api/reports/{obj.id}")
        elif isinstance(obj, api.SftpUser):
            self.session.delete(f"{self.host}/api/data/{obj.folder}/sftp/{obj.user_name}")
        elif isinstance(obj, api.ModelType):
            self.session.delete(f"{self.host}/api/resources/modeltypes/{obj.id}")
        elif isinstance(obj, api.ReportType):
            self.session.delete(f"{self.host}/api/resources/reporttypes/{obj.id}")
        else:
            raise NotImplementedError(f"delete not implemented for type {type(obj)}")

    def update_dataset_permission(self, id, user_id, group_id=None, permission_type="Editor"):
        """
        Update dataset permissions for user

        Args:
            id:
            user_id:
            group_id:
            permission_type:

        Returns:

        """
        payload = {"groupId": group_id, "userId": user_id, "resourceId": id, "objectType": 0,
                   "permissionType": permission_type}
        r = self.session.post(self.host + "/api/admin/datasets/" + id + "/permissions", json=payload)
        return r

    def get_dataset_sts_assume_role_response(self, guid):
        cred = self.session.get(f"{self.host}/api/data/{guid}/securitycredentials")
        return cred.text

    def get_schema(self, obj: Union[api.ModelType, api.ReportType]):
        """
        Get schema for a certain model type

        Args:
            obj: modeltype or report type

        Returns:

        """
        r = self.session.get(obj.settings_schema_path, headers={})
        return r.json()

    def get_userinfo(self):
        """
        Get info on user
        """
        url = self.host + "/api/manage/index"
        r = self.session.get(url)
        return api.User.parse_raw(r.content)

    def get_sftp_users(self, dataset, **kwargs) -> List[api.SftpUser]:
        r = self.session.get(f"{self.host}/api/data/{dataset.id}/sftp", **kwargs)
        users = parse_raw_as(List[api.SftpUser], r.content)
        for user in users:
            user.folder = user.folder or dataset.id
        return users

    def create_sftp_user(self, dataset, **kwargs) -> api.SftpUser:
        r = self.session.post(f"{self.host}/api/data/{dataset.id}/sftp", **kwargs)
        return api.SftpUser.parse_raw(r.content)

    def create_model(self, name, datasets, settings: JobSettings = None,
                     model_type=None, tags=None, application: api.Application = None):
        """
        Create a model on the platform

        Args:
            name:
            datasets:
            settings:
            model_type:
            tags:
            application:

        Returns:
            Model after its creation on the platform
        """
        tags = tags or []
        settings = settings or {}
        try:
            settings = settings.json()
        except AttributeError:
            settings = json.dumps(settings)

        model_type = model_type or self.backend.custom_model_type
        settings = settings or {}

        application_id = None if application is None else application.id
        model = api.Model(name=name, dataset_ids=[x.id for x in datasets], model_type_id=model_type.id,
                          model_type_status=model_type.status, settings=settings, application_id=application_id,
                          tag_ids=[x.id for x in tags], id="<unknown>", api_key="<unknown>", created="<unknown>")
        return self.create(model)

    def create_testreport(self, name, model, datasets, report_type=None, settings=None, tags=None, submitToCloud=False):
        """
        Create a test report on the platform

        Args:
            name:
            model:
            datasets:
            report_type:
            settings:
            tags:
            submitToCloud: start test report in the cloud

        Returns:
            Test report after its creation on the platform
        """
        tags = tags or []
        tag_ids = [tag if isinstance(tag, str) else tag.id for tag in tags]
        report_type = report_type or self.backend.custom_report_type
        report_type_id = report_type if isinstance(report_type, str) else report_type.id

        settings = settings or {}
        try:
            settings = settings.json()
        except AttributeError:
            settings = json.dumps(settings)

        report = api.Report(name=name, model_ids=[model.id], dataset_ids=[x.id for x in datasets],
                            id="<unknown>", api_key="<unknown>", created="<unknown>",
                            parent_id=model.id, parent_name=model.name, parent_type="model",
                            settings=settings, tag_ids=tag_ids, report_type_id=report_type_id)
        return self.create(report, submitToCloud=submitToCloud)

    def initialize_training(self, model: Union[str, api.Model], job_type: Type[Job] = None,
                            submitToCloud=False) -> Union[Job, None]:
        """
        Start training flow of a model

        Args:
            model: model or model id
            job_type:
            submitToCloud: start model in the cloud

        Returns:
            Job if submitToCloud is false, otherwise None
        """
        payload = {"submitToCloud": "true" if submitToCloud else "false"}

        if isinstance(model, str):
            model = self.get_model(model)

        if model.completed:
            print("Model already completed")
            return None

        r = self.session.post(f"{self.host}/api/models/{model.id}/start", params=payload)
        if submitToCloud:
            return None
        job_config = json.loads(self.download_url(r.json(), cache=False))
        type_selector = job_type or Job

        job = Job.init(type_selector=type_selector, job_config=job_config, backend=self.backend)
        return job

    def initialize_report(self, report: Union[str, api.Report], job_type: Type[Job] = None) -> Union[Job, None]:
        """
        Start training flow of a model

        Args:
            report: model or model id
            job_type:

        Returns:
            Job
        """

        if isinstance(report, str):
            report = self.get_report(report)

        if report.completed:
            print("Model already completed")
            return None

        type_selector = [job_type] if issubclass(job_type, Job) else job_type

        job = Job.init(job_id=report.id, api_key=report.api_key,
                       type_selector=type_selector, backend=self.backend)
        return job

    def stop_model_training(self, model):
        """
        Stop training of model

        Args:
            model:

        Returns:

        """
        r = self.session.post(f"{self.host}/api/models/{model.id}/stop")
        return api.Model.parse_raw(r.content)

    def download_url(self, url, dst=None, **kwargs):
        if kwargs.get("headers") is not None:
            log.warning("Headers not supported")

        # by default withhold bearer token for download requests
        withhold_token = True

        if url.startswith("/api/"):
            # Unless it is a request to the API
            url = self.host + url
            withhold_token = False

        r = self.session.get(url, withhold_token=withhold_token)
        if not r.ok:
            raise Exception("Error downloading file")

        content = r.content

        if dst is None:
            return content

        if os.path.isdir(dst):
            fname = os.path.basename(unquote(urlparse(url).path))
            dst = os.path.join(dst, fname)
        else:
            if os.path.dirname(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)

        with open(dst, 'wb') as f:
            f.write(content)

        return dst

    def experiment(self, name, job_type=None, settings=None,
                   datasets: Optional[List] = None, application=None, **kwargs):
        """
        :param name: Name of the experiment
        :param job_type: class of the Job
        :param settings: Settings object or dict for the job
        :param datasets: list of datasets or string names
        :param application: string id or Application object
        :param kwargs: Other args; see tooling.experiments
        :return:
        """
        from brevettiai.tooling.experiments import experiment
        experiment = experiment(name=name, job_type=job_type, settings=settings or {}, datasets=datasets,
                                application=application, **kwargs, web=self)
        print(f"{self.host}/models/{experiment.model.id}")
        return experiment

    def run_test(self, name, job_type, settings, on,
                 datasets: Optional[List] = None, application=None, **kwargs):
        """
        :param name: Name of the experiment
        :param job_type: class of the Job
        :param settings: Settings object or dict for the job
        :param on: Model to run testreport on
        :param datasets: list of datasets or string names
        :param application: string id or Application object
        :param kwargs: Other args; see tooling.experiments
        :return:
        """
        from brevettiai.tooling.experiments import run_test_report
        return run_test_report(name=name, job_type=job_type, settings=settings, parent=on, datasets=datasets,
                               application=application, **kwargs, web=self)

    @property
    def s3_credentials(self):
        """Return S3 sts credentials chain"""
        return self._s3_credentials


def decode_jwt_token(access_token):
    return json.loads(str(base64.b64decode(access_token.split(".")[1] + "=="), "utf-8"))
