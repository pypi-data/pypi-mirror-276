import gzip
import os
import shutil
import tarfile
import zipfile

import pandas as pd
import pyproj

from digitalarztools.utils.logger import da_logger


class FileIO:
    @classmethod
    def mkdirs_list(cls, file_paths: list):
        for fp in file_paths:
            cls.mkdirs(fp)

    @staticmethod
    def get_file_basedir_basename(file_path: str):
        if os.path.exists(file_path):
            return os.path.dirname(file_path), os.path.basename(file_path)

    @staticmethod
    def mkdirs(file_path: str):
        dir_name = os.path.dirname(file_path) if '.' in file_path[-5:] else file_path
        # dir_name = os.path.dirname(file_path) if is_file else file_path
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return dir_name

    @staticmethod
    def extract_zip_file(input_file, output_folder=None):
        """
        This function extract the zip files

        Keyword Arguments:
        output_file -- name, name of the file that must be unzipped
        output_folder -- Dir, directory where the unzipped data must be
                               stored
        """
        # extract the data
        if not output_folder:
            output_folder = input_file[:-4]
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        z = zipfile.ZipFile(input_file, 'r')
        z.extractall(output_folder)
        z.close()
        return output_folder

    @staticmethod
    def extract_data_gz(fp, output_folder=None):
        """
        This function extract the zip files

        Keyword Arguments:
        zip_filename -- name, name of the file that must be unzipped
        outfilename -- Dir, directory where the unzipped data must be
                               stored
        """
        if output_folder is None:
            output_folder = fp[:-3]
        with gzip.GzipFile(fp, 'rb') as zf:
            file_content = zf.read()
            save_file_content = open(output_folder, 'wb')
            save_file_content.write(file_content)
        save_file_content.close()
        zf.close()
        # os.remove(zip_filename)
        return output_folder

    @staticmethod
    def extract_data_tar_gz(fp, output_folder=None):
        """
        This function extract the tar.gz files

        Keyword Arguments:
        zip_filename -- name, name of the file that must be unzipped
        output_folder -- Dir, directory where the unzipped data must be
                               stored
        """
        if output_folder is None:
            output_folder = fp[:-7]
        os.makedirs(output_folder)
        os.chdir(output_folder)
        tar = tarfile.open(fp, "r:gz")
        tar.extractall()
        tar.close()
        return output_folder

    @staticmethod
    def extract_data_tar(tar_fp, output_folder=None):
        """
        This function extract the tar files

        Keyword Arguments:
        tar_fp -- path and name of the file that must be uncompressed
        output_folder -- Dir, directory where the unzipped data must be
                               stored
        """
        if output_folder is None:
            output_folder = tar_fp[:-4]
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            os.chdir(output_folder)
            tar = tarfile.open(tar_fp, "r")
            tar.extractall()
            tar.close()

        else:
            da_logger.error("Tar extraction, output folder already exists")
        return output_folder

    @staticmethod
    def get_file_name_ext(fp):
        base_name = os.path.basename(fp)
        sfp = base_name.split(".")
        return ",".join(sfp[:-1]), sfp[-1]

    @staticmethod
    def get_file_basedir_basename(file_path: str):
        if os.path.exists(file_path):
            return os.path.dirname(file_path), os.path.basename(file_path)

    @classmethod
    def read_prj_file(cls, prj_path) -> pyproj.CRS:
        name, ext = cls.get_file_name_ext(prj_path)
        if ext == "prj":
            with open(prj_path) as f:
                wkt = f.read()
                crs = pyproj.CRS.from_wkt(wkt)
                return crs
        return None

    @classmethod
    def list_dir_recursively(cls, dir_path: str, level: int = 0, ext=None) -> pd.DataFrame:
        """
        :param dir_path:
        :param level:
        :param ext:
        :return: dataframe with columns category, basename, fp, ext, and level
        """
        df = pd.DataFrame()
        for f in os.listdir(dir_path):
            fp = os.path.join(dir_path, f)
            if os.path.isdir(fp):
                sub_df = cls.list_dir_recursively(fp, level + 1)
                df = pd.concat([df, sub_df])
                # df.reset_index(drop=True, inplace=True)
            else:
                dirname = os.path.dirname(fp).split("/")[-1]
                basename = os.path.basename(fp)
                rec = {"basedir": dirname, "basename": basename, "ext": ext, "level": level, "fp": fp}
                if ext is not None:
                    if cls.get_file_name_ext(fp)[-1].lower() == ext.lower():
                        # df = df.append(rec, ignore_index=True)
                        df = pd.concat([df, pd.DataFrame(rec, index=[0])])
                else:
                    # df = df.append(rec, ignore_index=True)
                    df = pd.concat([df, pd.DataFrame(rec, index=[0])])
        return df.reset_index(drop=True)

    @classmethod
    def list_files_in_folder(cls, dir_path, ext=None):
        only_files = []
        for f in os.listdir(dir_path):
            fp = os.path.join(dir_path, f)
            if os.path.isfile(fp):
                if ext is not None:
                    if cls.get_file_name_ext(fp)[-1].lower() == ext.lower():
                        only_files.append(fp)
                else:
                    only_files.append(fp)
        return only_files

    @classmethod
    def write_file(cls, file_path, content):
        with open(file_path, "wb") as file:
            file.write(content)

    @classmethod
    def delete_folder(cls, folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

    @classmethod
    def copy_file(cls, src_file: str, des_folder: str) -> str:
        """
        :param src_file:
        :param des_folder:
        :return: des file
        """
        return shutil.copy2(src_file, des_folder)

    @staticmethod
    def check_folders_status(folders: list) -> pd.DataFrame:
        exists = []
        is_folder = []
        for f in folders:
            exists.append(os.path.exists(f))
            is_folder.append(os.path.isdir(f))
        return pd.DataFrame({"folders": folders, "exists": exists, "is_folder": is_folder})

    @classmethod
    def extract_data(cls, fp):
        base_name = os.path.basename(fp)
        # output_folder = os.path.dirname(fp)
        output_folder = None
        sfp = base_name.split(".")
        if sfp[-1] == "tar":
            if sfp[-2] == "gz":
                output_folder = cls.extract_data_tar_gz(fp)
            else:
                output_folder = cls.extract_data_tar(fp)
        elif sfp[-1] == "gz":
            output_folder = cls.extract_data_gz(fp)
        elif sfp[-1] == "zip":
            output_folder = cls.extract_zip_file(fp)
        if output_folder is None:
            da_logger.info(f"No tool available for extracting extension {sfp[-1]}")
        else:
            da_logger.info(f"{os.path.basename(fp)} is unzipped extracted successfully")
        return output_folder

    @classmethod
    def mvFile(cls, source_path, destination_folder):
        shutil.move(source_path, destination_folder)

    @staticmethod
    def rmdir( dir_path):
        shutil.rmtree(dir_path)
        print(f"{dir_path} deleted")
