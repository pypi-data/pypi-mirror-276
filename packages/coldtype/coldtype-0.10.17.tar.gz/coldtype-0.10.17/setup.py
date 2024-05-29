import setuptools, sys

long_description = """
# Coldtype

### Programmatic display typography

More info available at: [coldtype.goodhertz.com](https://coldtype.goodhertz.com)
"""

basic_deps = [
    "blackrenderer>=0.6.0",
    "fonttools[ufo,unicode]",
    "fontPens",
    "easing-functions",
    "mido",
    "defcon",
    "freetype-py",
    "uharfbuzz>=0.14.0",
    "python-bidi",
    "requests",
    "b3denv>=0.0.12",
]

#if sys.platform.startswith("darwin"):
#    basic_deps.extend(["pyobjc-framework-Cocoa", "pyobjc-framework-CoreText"])

setuptools.setup(
    name="coldtype",
    version="0.10.17",
    author="Rob Stenson / Goodhertz",
    author_email="rob@goodhertz.com",
    description="Functions for manual vectorized typesetting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goodhertz/coldtype",
    #package_dir={"": "coldtype"},
    packages=[
        "coldtype",
        "coldtype.fx",
        "coldtype.img",
        "coldtype.midi",
        "coldtype.pens",
        "coldtype.text",
        "coldtype.grid",
        "coldtype.color",
        "coldtype.runon",
        "coldtype.timing",
        "coldtype.physics",
        "coldtype.capture",
        "coldtype.blender",
        "coldtype.geometry",
        "coldtype.timing.nle",
        "coldtype.notebook",
        "coldtype.renderer",
        "coldtype.text.colr",
        "coldtype.renderable",
        "coldtype.fontgoggles",
        "coldtype.interpolation",
        "coldtype.runon.mixins",
        "coldtype.renderer.winman",
        "coldtype.fontgoggles.font",
        "coldtype.fontgoggles.misc",
        "coldtype.fontgoggles.compile",
    ],
    include_package_data=True,
    package_data={
        "": [
            "assets/glyphNamesToUnicode.txt",
            "demo/transparency_blocks.png",
            "demo/RecMono-CasualItalic.ttf",
            "demo/ColdtypeObviously-VF.ttf",
            "demo/JetBrainsMono.ttf",
            "demo/MutatorSans.ttf",
            "demo/demo.py",
            "demo/glyphs.py",
            "demo/glyphloop.py",
            "demo/midi.py",
            "demo/blank.py",
            "demo/boiler.py",
            "demo/vf.py",
            "demo/gifski.py",
            "renderer/.coldtype.py"
        ],
    },
    entry_points={
        'console_scripts': [
            'coldtype = coldtype.renderer:main'
        ],
    },
    extras_require={
        "drawbot": [
            "numpy",
        ],
        "viewer": [
            "glfw",
            "PyOpenGL",
            "skia-pathops", # can this be taken from skia-python?
            "ufo2ft",
            #"ufoLib2",
            "numpy",
            "potracer",
        ],
        "viewer:python_version < '3.12'": [
            "skia-python==87.5",
        ],
        "viewer:python_version >= '3.12'": [
            "skia-python>87.5",
        ],
        "experimental": [
            "pynput",
            "rtmidi",
            "noise",
        ],
        "c": [
            #"srt",
            "noise",
        ],
        "unicode": [
            "unicodedata2"
        ],
        "blender": [
            "skia-pathops",
            "ufo2ft",
            "ufoLib2", # temporary for a bug in ufo2ft
        ],
        "notebook": [
            "skia-pathops",
            "skia-python",
            "potracer",
        ],
        "audio": [
            "pyaudio",
            "soundfile",
        ]
    },
    install_requires=basic_deps,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
