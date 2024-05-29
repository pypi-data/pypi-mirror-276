from setuptools import setup

name = "avocado_job_gmail"
init_klass = "MailInit"
klass = "Mail"
entry_point = f"{name} = {name}:{klass}"
init_entry_point = f"{name} = {name}:{init_klass}"

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name=name,
        version="1.0.1",
        description="Avocado Pre/Post Job Mail Gmail Notification",
        long_description=long_description,
        long_description_content_type="text/markdown",
        py_modules=[name],
        entry_points={
            "avocado.plugins.init": [init_entry_point],
            "avocado.plugins.job.prepost": [entry_point],
        },
    )

