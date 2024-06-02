import setuptools

setuptools.setup(
    name="jsoniq-jupyter-lsp",
    version="1.0.0",
    description="Jupyter extension to support RumbleDB development in notebooks. The extension runs the language server for JSONiq to provide code auto-completion, syntax highlighting, and diagnostics.",
    url="https://www.jsoniq.org/",
    author="David-Marian Buzatu",
    author_email="davidm.buzatu@gmail.com",
    license="Apache License 2.0",
    keywords="rumble jsoniq rumbledb json IPython jupyter",
    entry_points={
        "console_scripts": ["jsoniq_lsp_start = src.jsoniq_lsp:main"],
        "jupyter_lsp_spec_v1": [
            "jupyter_jsoniq_language_server = src.jsoniq_spec:load"
        ],
    },
    classifiers=[
        # Intended Audience.
        "Intended Audience :: Developers",
        # Operating Systems.
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
