import warnings

import pytest

import matplotlib
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    needs_usetex = pytest.mark.skipif(
        not matplotlib.checkdep_usetex(True),
        reason='Missing TeX of Ghostscript or dvipng')


@needs_usetex
@image_comparison(baseline_images=['test_usetex'],
                  extensions=['pdf', 'png'],
                  tol=0.3)
def test_usetex():
    matplotlib.rcParams['text.usetex'] = True
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.text(0.1, 0.2,
            # the \LaTeX macro exercises character sizing and placement,
            # \left[ ... \right\} draw some variable-height characters,
            # \sqrt and \frac draw horizontal rules, \mathrm changes the font
            r'\LaTeX\ $\left[\int\limits_e^{2e}'
            r'\sqrt\frac{\log^3 x}{x}\,\mathrm{d}x \right\}$',
            fontsize=24)
    ax.set_xticks([])
    ax.set_yticks([])


@needs_usetex
def test_usetex_engformatter():
    matplotlib.rcParams['text.usetex'] = True
    fig, ax = plt.subplots()
    ax.plot([0, 500, 1000], [0, 500, 1000])
    ax.set_xticks([0, 500, 1000])
    formatter = EngFormatter()
    ax.xaxis.set_major_formatter(formatter)
    fig.canvas.draw()
    x_tick_label_text = [label.get_text() for label in ax.get_xticklabels()]
    # Checking if the dollar `$` signs have been inserted around numbers
    # in tick label text.
    assert x_tick_label_text == ['$0$', '$500$', '$1$ k']
