from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["requests", "bs4","tkinter"],
    "include_files": [
        "image_links.txt",
        "video_data.csv",
    ],
}

base = None

executables = [Executable("hqporner.py", base=base)]

setup(
    name="VideoDataScraper",
    version="1.0",
    description="Video Data Scraper",
    options={"build_exe": build_exe_options},
    executables=executables,
)
