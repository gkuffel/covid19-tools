import requests


def upload_file(path, url):
    with open(path, "rb") as data:
        r = requests.put(url, data=data)
        print("status: {}\ncontent: {}".format(r.status_code, r.content))
        return r.status_code


class FileHelper:
    def __init__(self, base_url, program_name, project_code, access_token):
        self.base_url = base_url
        self.program_name = program_name
        self.project_code = project_code
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def find_by_name(self, filename):
        url = f"{self.base_url}/index/index?file_name={filename}"
        r = requests.get(url)
        data = r.json()
        if data["records"]:
            assert (
                len(data["records"]) == 1
            ), f"multiple records for filename, something wrong: {filename}"
            did = data["records"][0]["did"]
            rev = data["records"][0]["rev"]
            md5sum = data["records"][0]["hashes"]["md5"]
            size = data["records"][0]["size"]
            return did, rev, md5sum, size
        return None, None, None, None

    def update_authz(self, did, rev):
        url = f"{self.base_url}/index/index/{did}?rev={rev}"
        r = requests.put(
            url,
            json={
                "authz": [
                    f"/programs/{self.program_name}/projects/{self.project_code}"
                ],
                "uploader": None,
            },
        )
        if r.status_code == 200:
            return True
        return False

    def get_presigned_url(self, filename):
        upload_url = f"{self.base_url}/user/data/upload"
        body_json = {
            "file_name": filename,
        }
        r = requests.post(upload_url, json=body_json, headers=self.headers)
        data = r.json()
        return data["url"], data["guid"]

    def upload_file(self, path):
        basename = path.name
        presigned_url, guid = self.get_presigned_url(basename)
        upload_status = upload_file(path, presigned_url)
        if upload_status == 200:
            return guid, upload_status
        return None, upload_status
