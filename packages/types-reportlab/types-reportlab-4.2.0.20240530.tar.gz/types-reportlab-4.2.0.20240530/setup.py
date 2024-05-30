from setuptools import setup

name = "types-reportlab"
description = "Typing stubs for reportlab"
long_description = '''
## Typing stubs for reportlab

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the `reportlab` package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`reportlab`.

This version of `types-reportlab` aims to provide accurate annotations
for `reportlab==4.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/reportlab. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `c82d29fc7614a9ecd33bd416386062ba2915850d` and was tested
with mypy 1.10.0, pyright 1.1.364, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="4.2.0.20240530",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/reportlab.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['reportlab-stubs'],
      package_data={'reportlab-stubs': ['__init__.pyi', 'graphics/__init__.pyi', 'graphics/barcode/__init__.pyi', 'graphics/barcode/code128.pyi', 'graphics/barcode/code39.pyi', 'graphics/barcode/code93.pyi', 'graphics/barcode/common.pyi', 'graphics/barcode/dmtx.pyi', 'graphics/barcode/eanbc.pyi', 'graphics/barcode/ecc200datamatrix.pyi', 'graphics/barcode/fourstate.pyi', 'graphics/barcode/lto.pyi', 'graphics/barcode/qr.pyi', 'graphics/barcode/qrencoder.pyi', 'graphics/barcode/usps.pyi', 'graphics/barcode/usps4s.pyi', 'graphics/barcode/widgets.pyi', 'graphics/charts/__init__.pyi', 'graphics/charts/areas.pyi', 'graphics/charts/axes.pyi', 'graphics/charts/barcharts.pyi', 'graphics/charts/dotbox.pyi', 'graphics/charts/doughnut.pyi', 'graphics/charts/legends.pyi', 'graphics/charts/linecharts.pyi', 'graphics/charts/lineplots.pyi', 'graphics/charts/markers.pyi', 'graphics/charts/piecharts.pyi', 'graphics/charts/slidebox.pyi', 'graphics/charts/spider.pyi', 'graphics/charts/textlabels.pyi', 'graphics/charts/utils.pyi', 'graphics/charts/utils3d.pyi', 'graphics/renderPDF.pyi', 'graphics/renderPM.pyi', 'graphics/renderPS.pyi', 'graphics/renderSVG.pyi', 'graphics/renderbase.pyi', 'graphics/samples/__init__.pyi', 'graphics/samples/bubble.pyi', 'graphics/samples/clustered_bar.pyi', 'graphics/samples/clustered_column.pyi', 'graphics/samples/excelcolors.pyi', 'graphics/samples/exploded_pie.pyi', 'graphics/samples/filled_radar.pyi', 'graphics/samples/line_chart.pyi', 'graphics/samples/linechart_with_markers.pyi', 'graphics/samples/radar.pyi', 'graphics/samples/runall.pyi', 'graphics/samples/scatter.pyi', 'graphics/samples/scatter_lines.pyi', 'graphics/samples/scatter_lines_markers.pyi', 'graphics/samples/simple_pie.pyi', 'graphics/samples/stacked_bar.pyi', 'graphics/samples/stacked_column.pyi', 'graphics/shapes.pyi', 'graphics/svgpath.pyi', 'graphics/transform.pyi', 'graphics/utils.pyi', 'graphics/widgetbase.pyi', 'graphics/widgets/__init__.pyi', 'graphics/widgets/adjustableArrow.pyi', 'graphics/widgets/eventcal.pyi', 'graphics/widgets/flags.pyi', 'graphics/widgets/grids.pyi', 'graphics/widgets/markers.pyi', 'graphics/widgets/signsandsymbols.pyi', 'graphics/widgets/table.pyi', 'lib/PyFontify.pyi', 'lib/__init__.pyi', 'lib/abag.pyi', 'lib/arciv.pyi', 'lib/attrmap.pyi', 'lib/boxstuff.pyi', 'lib/codecharts.pyi', 'lib/colors.pyi', 'lib/corp.pyi', 'lib/enums.pyi', 'lib/extformat.pyi', 'lib/fontfinder.pyi', 'lib/fonts.pyi', 'lib/formatters.pyi', 'lib/geomutils.pyi', 'lib/logger.pyi', 'lib/normalDate.pyi', 'lib/pagesizes.pyi', 'lib/pdfencrypt.pyi', 'lib/pygments2xpre.pyi', 'lib/randomtext.pyi', 'lib/rl_accel.pyi', 'lib/rl_safe_eval.pyi', 'lib/rltempfile.pyi', 'lib/rparsexml.pyi', 'lib/sequencer.pyi', 'lib/styles.pyi', 'lib/testutils.pyi', 'lib/textsplit.pyi', 'lib/units.pyi', 'lib/utils.pyi', 'lib/validators.pyi', 'lib/yaml.pyi', 'pdfbase/__init__.pyi', 'pdfbase/acroform.pyi', 'pdfbase/cidfonts.pyi', 'pdfbase/pdfdoc.pyi', 'pdfbase/pdfform.pyi', 'pdfbase/pdfmetrics.pyi', 'pdfbase/pdfpattern.pyi', 'pdfbase/pdfutils.pyi', 'pdfbase/rl_codecs.pyi', 'pdfbase/ttfonts.pyi', 'pdfgen/__init__.pyi', 'pdfgen/canvas.pyi', 'pdfgen/pathobject.pyi', 'pdfgen/pdfgeom.pyi', 'pdfgen/pdfimages.pyi', 'pdfgen/textobject.pyi', 'platypus/__init__.pyi', 'platypus/doctemplate.pyi', 'platypus/figures.pyi', 'platypus/flowables.pyi', 'platypus/frames.pyi', 'platypus/multicol.pyi', 'platypus/para.pyi', 'platypus/paragraph.pyi', 'platypus/paraparser.pyi', 'platypus/tableofcontents.pyi', 'platypus/tables.pyi', 'platypus/xpreformatted.pyi', 'rl_config.pyi', 'rl_settings.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
