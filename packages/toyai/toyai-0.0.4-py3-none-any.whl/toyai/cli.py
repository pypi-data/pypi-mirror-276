import subprocess
import sys
import os
import argparse
import shutil
import py_compile
import importlib.util
import sysconfig
import threading


def main():
    version = "1.1.0a"

    def run_script_with_realtime_output(cmd, script_path, log, extra):
        def read_and_write(stream, func, file=None):
            for line in iter(stream.readline, ""):
                func(line)
                if file:
                    file.write(line)
                    file.flush()
            # stream.close()

        if log is not None:
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = (
                "1"  # Set PYTHONUNBUFFERED to ensure real-time output
            )

            with open(log, "w") as f:
                with subprocess.Popen(
                    ["python", f"{script_path}/__{cmd}__.py"] + extra,
                    # stdout=subprocess.PIPE,
                    # stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    env=env,
                ) as proc:
                    # stdout_thread = threading.Thread(
                    #     target=read_and_write,
                    #     args=(proc.stdout, lambda x: print(x, end=""), f),
                    # )
                    # stderr_thread = threading.Thread(
                    #     target=read_and_write,
                    #     args=(proc.stderr, lambda x: print(x, end=""), f),
                    # )

                    # stdout_thread.start()
                    # stderr_thread.start()

                    # stdout_thread.join()
                    # stderr_thread.join()

                    proc.wait()
                    # for line in proc.stdout:
                    #     print(line, end="")  # แสดงผลลัพธ์ใน console
                    #     f.write(line)  # เขียนผลลัพธ์ลงไฟล์
                    #     f.flush()

                    # for line in proc.stderr:
                    #     print(line, end="")  # แสดงผลลัพธ์ใน console
                    #     f.write(line)  # เขียนผลลัพธ์ลงไฟล์
                    #     f.flush()

        else:
            # เริ่มต้นการสร้าง subprocess โดยใช้ Popen
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
        choices=["install", "learn", "test", "complie"],
        help="Action to perform: learn, install, or test",
    )
    parser.add_argument("path", help="Path")
    parser.add_argument("-v", "--version", action="version", version=f"v{version}")
    parser.add_argument("-l", "--log", required=False, help="Path to the log file")
    # รับ argument ที่เหลือทั้งหมด
    parser.add_argument("extra_args", nargs=argparse.REMAINDER)
    # แสดง help ถ้าไม่มี arguments ถูกใส่
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.action == "install":
        pass
    elif args.action == "complie":
        pass
    else:
        run_script_with_realtime_output(
            args.action, args.path, args.log, args.extra_args
        )
