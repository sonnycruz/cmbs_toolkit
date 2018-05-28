import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def cmbs_bar(dict_data, ylim_high, ylabel, ylim_low=0, title='',
              y_thousands=True, text_message='', text_c1=0, text_c2=0,
              style='seaborn-bright', bar_color='darkblue', xtick_rotation=0,
              xtick_font='large', facecolor='lightgray', grid_line_style='-',
              grid_line_width=0.5, grid_color='gray'):
    """
    Create Bar Graph from dictionary.

    Creates Bar Graph from dictionary using Matplotlib.pyplot library
    and allows many matplotlib aesthetic specifications.

    Parameters
    ----------
    dict_data : dict
        Of the form {'label' : int} where 'label' are the x-labels
        and int are the y-values.
    ylim_high : int
        Set max y-value displayed.
    ylabel : str
    ylim_low : int, default 0, of course.
    title : str, default ''
    y_thousands : boolean, default True
        Format y-axis values to have thousands separator.
    text_message : str, default ''
        Text annotation to accompany graphic.
    text_c1 : int, default 0
        X-coordinate of text_message.
    text_c2 : int, default 0
        Y-coordinate of text_message.
    style : str, default 'seaborn-bright'
    bar_color : str, default darkblue
    xtick_rotation : int, default 0
    xtick_font : str, default 0
    facecolor : str, default 'lightgray'
    grid_line_style : str, default '-'
    grid_line_width : float, default 0.5
    grid_color : str, default 'gray'

    Returns
    -------
    matplotlib bar plot
    """
    
    data = sorted(dict_data.items(), key=lambda x: x[1], reverse=True)
    data_keys = [key[0] for key in data]
    data_index = range(len(data_keys))
    data_values = [value[1] for value in data]
    plt.style.use(style)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.bar(data_index, data_values, align='center', color=bar_color)
    plt.xticks(data_index, data_keys, rotation=xtick_rotation,
               fontsize=xtick_font)
    ax1.set_ylim(ylim_low, ylim_high)
    plt.ylabel(ylabel)
    plt.text(text_c1, text_c2, text_message)
    plt.title(title)
    ax1.set_facecolor(color=facecolor)
    ax1.grid()
    ax1.grid(linestyle=grid_line_style, linewidth=grid_line_width,
             color=grid_color)
    ax1.set_axisbelow(True)
    if y_thousands:
        ax1.get_yaxis().set_major_formatter(
            plt.FuncFormatter(
                lambda x, loc: "{:,}".format(int(x)))
            )
    plt.show()


def cmbs_pie(xpie, ypie, x_name, y_name, title='', title_size=15, title_y=0.9,
             x_color='darkblue', y_color='lightgray', text_size='large',
             text_color='white', ha_align='center', va_align='top',
             font_weight='bold', autotext_size='large', autotext_color='white'):
    """
    Create Pie Chart from two values.

    Parameters
    ----------
    xpie : int
    ypie : int
    x_name : str
    y_name : str
    title : str, default ''
    title_size : int, default 15
    title_y : int, default 0.9
    x_color : str, default 'darkblue'
    y_color : str, default 'lightgray'
    text_size : str, default 'large'
    text_color : str, default 'white'
    ha_align : str, default 'center'
        Sets horizontal alignment.
    va_align : str, default 'top'
        Sets vertical alignment.
    font_weight : str, default 'bold'
    autotext_size : str, default 'large'
    autotext_color : str, default 'white'

    Returns
    -------
    matplotlib pie chart.
    """
    
    plt.rc('font', weight=font_weight)
    xpie = xpie
    ypie = ypie
    groups = [x_name, y_name]
    fracs = [xpie, ypie]
    patches, texts, autotexts = plt.pie(fracs, labels=groups, autopct='%1.1f%%',
                                        colors=[x_color, y_color])
    [text.set_size(text_size) for text in texts]
    [text.set_color(text_color) for text in texts]
    [text.set_horizontalalignment(ha_align) for text in texts]
    [text.set_verticalalignment(va_align) for text in texts]
    [text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()]) for text in texts]
    [autotext.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'),
                            path_effects.Normal()]) for autotext in autotexts]
    [autotext.set_size(autotext_size) for autotext in autotexts]
    [autotext.set_color(autotext_color) for autotext in autotexts]
    plt.suptitle(title, fontsize=title_size, y=title_y)
    plt.show()
    plt.rc('font', weight='normal')
