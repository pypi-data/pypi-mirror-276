import os
import shutil
import uuid
import logging
from modx.tools.os import mkdir


class ETL:
    def __init__(self, name, datasets_dir, inventory_dir, output_dir) -> None:
        self.name = name
        self.datasets_dir = datasets_dir
        self.inventory_dir = inventory_dir
        self.output_dir = output_dir
        self.root_output_dir = output_dir

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
