from dicomweb_client import DICOMwebClient, session_utils
from pydicom import Dataset


class AditClient:
    def __init__(self, server_url: str, auth_token: str, verify: str | bool = True) -> None:
        self.server_url = server_url
        self.auth_token = auth_token
        self.verify = verify

    def search_for_studies(
        self, ae_title: str, query: dict[str, str] | None = None
    ) -> list[Dataset]:
        """Query an ADIT server for studies."""
        results = self._create_dicom_web_client(ae_title).search_for_studies(search_filters=query)
        return [Dataset.from_json(result) for result in results]

    def search_for_series(
        self, ae_title: str, study_instance_uid: str, query: dict[str, str] | None = None
    ) -> list[Dataset]:
        """Query an ADIT server for series."""
        results = self._create_dicom_web_client(ae_title).search_for_series(
            study_instance_uid, search_filters=query
        )
        return [Dataset.from_json(result) for result in results]

    def retrieve_study(self, ae_title: str, study_instance_uid: str) -> list[Dataset]:
        """Retrieve a study from an ADIT server."""
        if not study_instance_uid:
            raise ValueError("Study instance UID must be provided to retrieve study.")

        return self._create_dicom_web_client(ae_title).retrieve_study(study_instance_uid)

    def retrieve_series(
        self,
        ae_title: str,
        study_instance_uid: str,
        series_instance_uid: str,
    ) -> list[Dataset]:
        """Retrieve a series from an ADIT server."""
        if not study_instance_uid:
            raise ValueError("Study instance UID must be provided to retrieve series.")

        if not series_instance_uid:
            raise ValueError("Series instance UID must be provided to retrieve series.")

        return self._create_dicom_web_client(ae_title).retrieve_series(
            study_instance_uid, series_instance_uid=series_instance_uid
        )

    def store_instances(self, ae_title: str, instances: list[Dataset]) -> None:
        """Store some instances on an ADIT server."""
        self._create_dicom_web_client(ae_title).store_instances(instances)

    def _create_dicom_web_client(self, ae_title: str) -> DICOMwebClient:
        session = session_utils.create_session()

        if isinstance(self.verify, bool):
            session.verify = self.verify
        else:
            session = session_utils.add_certs_to_session(session=session, ca_bundle=self.verify)

        return DICOMwebClient(
            session=session,
            url=f"{self.server_url}/api/dicom-web/{ae_title}",
            qido_url_prefix="qidors",
            wado_url_prefix="wadors",
            stow_url_prefix="stowrs",
            headers={"Authorization": f"Token {self.auth_token}"},
        )
