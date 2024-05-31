import pandas as pd

from typing import Any
from visions import Integer, Categorical, Date

from xurpas_data_quality.data.typeset import XFloat
from xurpas_data_quality.data.describer import TableDescription
from xurpas_data_quality.render.renderer import HTMLBase, HTMLContainer, HTMLTable, HTMLVariable, HTMLPlot, HTMLToggle, HTMLCollapse, HTMLDropdown
from xurpas_data_quality.visuals import plot_to_base64, create_tiny_histogram, create_histogram, create_distribution_plot, create_heatmap, create_interaction_plot
from xurpas_data_quality.render.render_types import render_numerical, render_categorical, render_date, render_generic


def render_variable(data: dict, column: str):
    if data['type'] == Integer or data['type'] == XFloat:
        return render_numerical(data, column)
    
    elif data['type'] == Categorical:
        return render_categorical(data, column)
    
    elif data['type'] == Date:
        return render_date(data, column)
    
    else:
        return render_generic(data, column)
    
def render_variables_section(data: TableDescription):
    vars = []
    for key, value in data.variables.items():
        variable = render_variable(value, key)
        vars.append(variable)
    #return [render_variable(value,key) for key, value in data.variables.items()]
    return vars

def render_correlation_section(data: pd.DataFrame):
    return HTMLContainer(
        type="box",
        name="Correlation",
        container_items=[
            HTMLContainer(
                type="tabs",
                container_items=[
                    HTMLPlot(plot=plot_to_base64(create_heatmap(data)),
                             type="large",
                             id="corr",
                             name="Heatmap"),
                    HTMLTable(
                        id='sample',
                        name="Table",
                        data=data.to_html(classes="table table-sm", border=0))
                ]
            )
        ]
    )

def render_interactions_section(data:pd.DataFrame)->HTMLBase:
    df = data.select_dtypes(exclude=['object'])
    outer_tabs = []
    for column in df.columns:
        inner_tabs = []
        for inner_col in df.columns:
            inner_tabs.append(
                HTMLContainer(
                    type="default",
                    name= inner_col,
                    id = f"{column}-{inner_col}-interaction-inner",
                    container_items = [HTMLPlot(
                        plot= plot_to_base64(create_interaction_plot(df[inner_col],df[column])),
                        type = "large",
                        name = f"{column}-{inner_col} Interaction Plot",
                        id = f"{column}-{inner_col}_interaction_plot"
                    )]
                )
            )
        outer_tabs.append(
            HTMLContainer(
                type="tabs",
                name = column,
                id = f"{column}-interaction-outer",
                container_items = inner_tabs
            )
        )
    return outer_tabs

def render_report(data: TableDescription, report_name: str=None) -> Any:
    content = []
    dataset_statistics = {
        'Number of Variables': data.dataset_statistics['num_variables'],
        'Missing Cells': data.dataset_statistics['missing_cells'],
        'Missing Cells (%)': "{:0.2f}%".format(data.dataset_statistics['missing_cells_perc']),
        'Duplicate Rows': data.dataset_statistics['duplicate_rows'],
        'Duplicate Rows (%)': "{:0.2f}%".format(data.dataset_statistics['duplicate_rows_perc'])
    }

    overview_section = HTMLContainer(
        type="box",
        name="Overview",
        container_items = [
            HTMLContainer(
                type="column",
                container_items = HTMLTable(
                    data= dataset_statistics,
                    name="Dataset Statistics"
                )),
            HTMLContainer(
                type="column",
                container_items =  HTMLTable(
                    data= data.variable_types,
                    name="Variable Types"
                )
            )
        ]
    )
    dropdown = [
        HTMLDropdown(
        dropdown_items= list(data.df),
        dropdown_content= HTMLContainer(
            type="default",
            container_items= render_variables_section(data)),
        id="variables-dropdown"
        )
    ]
    variables_section = HTMLContainer(
        type = "box",
        name = "Variables",
        container_items = dropdown
    )

    correlation_section = render_correlation_section(data.correlation)
    
    interactions_section = HTMLContainer(
        type="box",
        name="Interactions",
        container_items=[
            HTMLContainer(
                type="tabs",
                container_items= render_interactions_section(data.df)
            )
        ]
    )
    samples_section = HTMLContainer(
        type="box",
        name="Sample",
        container_items=[
            HTMLTable(
                id = "sample",
                data=data.df.head(10).to_html(classes="table table-sm", border=0)
            )
        ]
    )

    content.extend([overview_section, 
                    variables_section, 
                    correlation_section, 
                    interactions_section,
                    samples_section])


    body = HTMLContainer(
        type="sections",
        container_items = content
    )
    return HTMLBase(body=body, name='Data Report' if report_name is None else report_name)