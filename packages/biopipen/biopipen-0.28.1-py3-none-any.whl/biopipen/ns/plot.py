"""Plotting data"""

from ..core.proc import Proc
from ..core.config import config


class VennDiagram(Proc):
    """Plot Venn diagram

    Needs `ggVennDiagram`

    Input:
        infile: The input file for data
            If `envs.intype` is raw, it should be a data frame with row names
            as categories and only column as elements separated by comma (`,`)
            If it is `computed`, it should be a data frame with row names
            the elements and columns the categories. The data should be binary
            indicator (`0, 1`) indicating whether the elements are present
            in the categories.

    Output:
        outfile: The output figure file

    Envs:
        inopts: The options for `read.table()` to read `in.infile`
        intype: `raw` or `computed`. See `in.infile`
        devpars: The parameters for `png()`
        args: Additional arguments for `ggVennDiagram()`
        ggs: Additional ggplot expression to adjust the plot
    """

    input = "infile:file"
    output = "outfile:file:{{in.infile | stem}}.venn.png"
    lang = config.lang.rscript
    envs = {
        "inopts": {"row.names": -1, "header": False},
        "intype": "raw",
        "devpars": {"res": 100, "width": 1000, "height": 1000},
        "args": {},
        "ggs": None,
    }
    script = "file://../scripts/plot/VennDiagram.R"


class Heatmap(Proc):
    """Plot heatmaps using `ComplexHeatmap`

    Examples:
        >>> pipen run plot Heatmap \
        >>> --in.infile data.txt \
        >>> --in.annofiles anno.txt \
        >>> --envs.args.row_names_gp 'r:fontsize5' \
        >>> --envs.args.column_names_gp 'r:fontsize5' \
        >>> --envs.args.clustering_distance_rows pearson \
        >>> --envs.args.clustering_distance_columns pearson \
        >>> --envs.args.show_row_names false \
        >>> --envs.args.row_split 3 \
        >>> --args.devpars.width 5000 \
        >>> --args.devpars.height 5000 \
        >>> --args.draw.merge_legends \
        >>> --envs.args.heatmap_legend_param.title AUC \
        >>> --envs.args.row_dend_reorder \
        >>> --envs.args.column_dend_reorder \
        >>> --envs.args.top_annotation \
        >>>   'r:HeatmapAnnotation( \
        >>>       Mutation = as.matrix(annos[,(length(groups)+1):ncol(annos)]) \
        >>>   )' \
        >>> --envs.args.right_annotation \
        >>>   'r:rowAnnotation( \
        >>>       AUC = anno_boxplot(as.matrix(data), outline = F) \
        >>>   )' \
        >>> --args.globals \
        >>>   'fontsize8 = gpar(fontsize = 12); \
        >>>    fontsize5 = gpar(fontsize = 8); \
        >>>    groups = c  ("Group1", "Group2", "Group3")' \
        >>> --args.seed 8525

    Input:
        infile: The data matrix file
        annofiles: The files for annotation data

    Output:
        outfile: The heatmap plot
        outdir: Other data of the heatmap
            Including RDS file of the heatmap, row clusters and col clusters.

    Envs:
        inopts: Options for `read.table()` to read `in.infile`
        anopts: Options for `read.table()` to read `in.annofiles`
        draw: Options for `ComplexHeatmap::draw()`
        args: Arguments for `ComplexHeatmap::Heatmap()`
        devpars: The parameters for device.
        seed: The seed
        globals: Some globals for the expression in `args` to be evaluated

    Requires:
        bioconductor-complexheatmap:
            - check: {{proc.lang}} <(echo "library(ComplexHeatmap)")
    """
    input = "infile:file, annofiles:files"
    output = [
        'outfile:file:{{in.infile | stem0 | append: ".heatmap"}}/'
        '{{in.infile | stem0 | append: ".heatmap"}}.png',
        'outdir:dir:{{in.infile | stem0 | append: ".heatmap"}}',
    ]
    lang = config.lang.rscript
    envs = {
        "inopts": {"header": True, "row.names": -1},
        "anopts": {"header": True, "row.names": -1},
        "draw": {},
        "devpars": {},
        "args": {"heatmap_legend_param": {}},
        "seed": None,
        "globals": "",
    }
    script = "file://../scripts/plot/Heatmap.R"


class ROC(Proc):
    """Plot ROC curve using [`plotROC`](https://cran.r-project.org/web/packages/plotROC/vignettes/examples.html).

    Input:
        infile: The input file for data, tab-separated.
            The first column should be ids of the records (this is optional if `envs.noids` is True).
            The second column should be the labels of the records (1 for positive, 0 for negative).
            If they are not binary, you can specify the positive label by `envs.pos_label`.
            From the third column, it should be the scores of the different models.

    Output:
        outfile: The output figure file

    Envs:
        noids: Whether the input file has ids (first column) or not.
        pos_label: The positive label.
        ci: Whether to use `geom_rocci()` instead of `geom_roc()`.
        devpars: The parameters for `png()`
        args: Additional arguments for `geom_roc()` or `geom_rocci()` if `envs.ci` is True.
        style_roc: Arguments for `style_roc()`
    """  # noqa: E501
    input = "infile:file"
    output = "outfile:file:{{in.infile | stem}}.roc.png"
    lang = config.lang.rscript
    envs = {
        "noids": False,
        "pos_label": 1,
        "ci": False,
        "devpars": {"res": 100, "width": 750, "height": 600},
        "args": {"labels": False},
        "style_roc": {},
        "show_auc": True,
    }
    script = "file://../scripts/plot/ROC.R"
