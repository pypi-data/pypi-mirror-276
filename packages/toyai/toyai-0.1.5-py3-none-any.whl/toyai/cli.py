import subprocess
import sys
import os
import argparse
import shutil
import runpy
from pathlib import Path
import zipfile
from toyai.tools.os import mkdir
import tempfile


def main():
    version = "1.1.0a"

    def run_script_with_realtime_output(cmd, script_path, extra):
        with subprocess.Popen(
            ["python", f"{script_path}/__{cmd}__.py"] + extra,
            text=True,
            bufsize=1,
        ) as proc:
            pass

    # สร้าง ArgumentParser
    parser = argparse.ArgumentParser(description=f"%(prog)s v{version}")

    # เพิ่ม argument ใหม่
    parser.add_argument(
        "action",
        choices=["install", "learn", "test", "build"],
        help="Action to perform: learn, install, or test",
    )
    parser.add_argument("path", help="Path")
    parser.add_argument("-v", "--version", action="version", version=f"v{version}")
    parser.add_argument("-f", "--filename", required=False)

    # รับ argument ที่เหลือทั้งหมด
    parser.add_argument("extra_args", nargs=argparse.REMAINDER)
    # แสดง help ถ้าไม่มี arguments ถูกใส่
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.action == "build":
        name = Path(args.path).name
        if args.filename is not None:
            name = args.filename

        zip_path = f"build/{name}.zip"
        with zipfile.ZipFile(mkdir(zip_path), "w") as zf:
            for root, _, files in os.walk(args.path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=args.path)
                    zf.write(file_path, arcname)

        with zipfile.ZipFile(zip_path, "a") as zf:
            zf.setpassword("super@password".encode())

        new_zip_path = zip_path.replace(".zip", "")
        os.rename(zip_path, new_zip_path)

        print(f"Created: {new_zip_path}")

    else:
        if zipfile.is_zipfile(args.path):
            with tempfile.TemporaryDirectory() as temp_dir:
                # แตกไฟล์ zip ไปยังไดเรกทอรีชั่วคราว
                with zipfile.ZipFile(args.path, "r") as zip_ref:
                    zip_ref.setpassword("super@password".encode())
                    zip_ref.extractall(temp_dir)

                # เพิ่มไดเรกทอรีชั่วคราวใน sys.path
                sys.path.insert(0, temp_dir)
                runpy.run_module(f"__{args.action}__", run_name="__main__")

            pass
        else:
            run_script_with_realtime_output(args.action, args.path, args.extra_args)
