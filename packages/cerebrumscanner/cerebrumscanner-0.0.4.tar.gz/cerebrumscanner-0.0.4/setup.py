from setuptools import find_namespace_packages, setup

package_license: str = ""
long_description: str = ""
install_requires = []

with open("LICENSE", encoding="utf-8") as license_file, open(
    "README.md", encoding="utf-8"
) as readme_file, open("requirements.txt", encoding="utf-8") as requirements_file:
    package_license = license_file.read()
    long_description = readme_file.read()
    install_requires = requirements_file.read().split("\n")[0:]

setup(
    name="cerebrumscanner",
    version="0.0.4",
    url="https://gitlab.com/nekodu/cerebrumscanner/cerebrum-scanner",
    license=package_license,
    author="Nekodu Technology",
    author_email="info@nekodu.com",
    description=(
        "Cerebrum Scanner Project"
    ),
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    zip_safe=False,
)
