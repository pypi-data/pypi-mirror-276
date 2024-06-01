from setuptools import setup, find_packages

import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()
# pypi-AgEIcHlwaS5vcmcCJDc5ODU1YWNiLWQ2M2EtNDU2Ni1hZGMzLWQ3Y2FkNjI0Mzk3NgACKlszLCIzN2Y5NWZmYy00OGUyLTQ2NWYtYWFkNy02ODJhMGIwZTVhMjAiXQAABiDRffU2uinyXDCGaJvaDx0_QqofqIU5sKdtRbjvZvHlnw
setup(
    name="toyai",
    version="0.2",
    author="Supanut Panyagosa",
    author_email="supanut.pgs@gmail.com",
    description="A description of your package",
    # package_dir={"": ""},
    # packages=find_packages(where="modx"),
    packages=find_packages(),
    install_requires=[
        # ใส่ชื่อแพ็คเกจที่ต้องการใช้งานใน requirements.txt
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
