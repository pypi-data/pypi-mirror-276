import subprocess
import sys
import os
import argparse
import shutil
import runpy
from pathlib import Path
import zipfile


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

    if args.action == "install":
        pass
    elif args.action == "build":
        # file_path = "/Users/supanutpgs/work/programming/ai/python/pytorch/ai-framework/modules/classify/feeling"
        name = Path(args.path).name
        if args.filename is not None:
            name = args.filename
        zip_path = shutil.make_archive(
            f"build/{name}",
            "zip",
            args.path,
        )
        new_zip_path = os.path.splitext(zip_path)[0]
        os.rename(zip_path, new_zip_path)
        print(f"Created {new_zip_path}")

    else:
        if zipfile.is_zipfile(args.path):
            sys.path.insert(
                0,
                args.path,
            )
            runpy.run_module(f"__{args.action}__", run_name="__main__")
            pass
        else:
            run_script_with_realtime_output(args.action, args.path, args.extra_args)
