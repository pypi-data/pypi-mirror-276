import os

import oss2

from oss2.credentials import EnvironmentVariableCredentialsProvider


def path_split(path):
    directories = []
    while True:
        path, directory = os.path.split(path)
        if directory != "":
            directories.append(directory)
        else:
            if path != "":
                directories.append(path)
            break

    directories.reverse()
    return directories


class Bucket:
    def __init__(self, end_point, bucket_name):
        auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
        self.bucket = oss2.Bucket(auth, end_point, bucket_name,connect_timeout=1000,session=oss2.Session(pool_size=10))
        if not self._bucket_exist():
            self.bucket.create_bucket()

    def _bucket_exist(self):
        try:
            self.bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            return False
        except:
            raise
        return True

    def mkdir(self, path):
        try:
            directories = path_split(path)
            for i in range(1, len(directories)+1):
                new_dir = os.path.join(*directories[:i])
                new_dir = new_dir if new_dir.endswith('/') else new_dir + '/'
                if self.bucket.object_exists(new_dir):
                    continue
                else:
                    self.bucket.put_object(new_dir, '')

            return True
        except Exception as e:
            return False

    def upload(self, oss_path, local_file):
        # directories = path_split(oss_path)
        # self.mkdir(directories[:-1])

        rsp = self.bucket.put_object_from_file(oss_path, local_file)

        return rsp

    def download(self, oss_file, local_path):
        rsp = self.bucket.get_object_to_file(oss_file, local_path)

        return rsp

    def append_content(self, oss_file, content, position=0):
        if position != 0 and not self.bucket.object_exists(oss_file):
            raise f"{oss_file} is not existed!"
        # if position == 0:
        #     directories = path_split(oss_file)
        #     self.mkdir(directories[:-1])

        rsp = self.bucket.append_object(oss_file, position, content)

        return rsp

    def write(self, oss_file_path, content):
        # directories = path_split(oss_file_path)
        # self.mkdir(directories[:-1])

        rsp = self.bucket.put_object(oss_file_path, content)

        return rsp


if __name__ == "__main__":
    endpoint = 'https://oss-cn-beijing.aliyuncs.com'
    bucket_name = 'wuying-yuankong'

    bucket = Bucket(endpoint, bucket_name)

    # bucket.mkdir('admin/test')

    # rsp = bucket.upload('admin/test/debug.xml', './debug.xml')
    # print(rsp)

    rsp = bucket.download('6136e19a7f624ea3b33c8d6b70e22dce/2fc5ee66526d453fbee6214dde70c979/milestone.log', './milestone.log')
    print(rsp)
