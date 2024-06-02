import os
import shutil
import uuid
import logging
import argparse
from .tools.os import mkdir


class UnknownArgs:
    def __init__(self, args):
        self.args_dict = {}
        for arg in args:
            if arg.startswith("--"):
                key, value = arg[2:].split("=")
                self.args_dict[key] = value

    def __getattr__(self, item):
        return self.args_dict.get(item)

    def __getitem__(self, item):
        return self.args_dict.get(item)

    def __str__(self):
        return str(self.args_dict)


class ETL:
    def __init__(
        self,
        name=None,
        datasets_dir=None,
        inventory_dir=None,
        output_dir=None,
    ) -> None:
        parser = argparse.ArgumentParser(description="Base ETL")
        parser.add_argument("-n", "--name", required=False)
        parser.add_argument("-o", "--output_dir", required=False, default="dist")
        parser.add_argument("-i", "--inventory_dir", required=False)
        parser.add_argument("-d", "--datasets_dir", required=False)
        args, unknown_args = parser.parse_known_args()

        self.name = args.name
        self.output_dir = args.output_dir
        self.root_output_dir = self.output_dir
        self.inventory_dir = args.inventory_dir
        self.datasets_dir = args.datasets_dir

        if name is not None:
            self.name = name

        if datasets_dir is not None:
            self.datasets_dir = datasets_dir

        if inventory_dir is not None:
            self.inventory_dir = inventory_dir

        if output_dir is not None:
            self.output_dir = output_dir

        self.args = UnknownArgs(unknown_args)

    def __enter__(self):
        self.nameunique = f"{self.name}"
        self.output_dir = f"{self.output_dir}/_{self.nameunique}"

        # สร้าง logger
        self.logger = logging.getLogger(f"{self.name}_logger")
        self.logger.setLevel(logging.INFO)

        # ตรวจสอบว่า logger ไม่มี handler ซ้ำซ้อน
        if not self.logger.handlers:
            # สร้าง handler สำหรับเขียนลงไฟล์
            file_handler = logging.FileHandler(
                mkdir(f"{self.output_dir}/{self.name}.log")
            )
            file_handler.setLevel(logging.INFO)

            # สร้าง handler สำหรับแสดงใน console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # สร้าง formatter และกำหนดให้กับทั้งสอง handler
            formatter = logging.Formatter(
                "%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # เพิ่ม handler ทั้งสองให้กับ logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.output_dir):
            # เปลี่ยนชื่อโฟลเดอร์
            to_dir = self.output_dir.replace(f"_{self.nameunique}", self.nameunique)
            if os.path.exists(to_dir):
                shutil.move(
                    to_dir,
                    f"{self.root_output_dir}/.tmp/{self.name}/{uuid.uuid4()}",
                    copy_function=shutil.copy2,
                )
            shutil.move(
                self.output_dir,
                to_dir,
                copy_function=shutil.copy2,
            )
