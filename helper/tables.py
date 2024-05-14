import csv


def latex_safe_string(title):
    translation_table = str.maketrans ( {char: f'\{char}' for char in '\`*_{}[]()<>#+-.!$:;,/'} )
    latex_safe_title = title.translate ( translation_table )
    return latex_safe_title


def export_single_general_stat_to_latex(data_dict, parent_dir, title):
    underscore_title = title.replace ( ' ', '_' )
    latex_filename = parent_dir + f'/{underscore_title}_general_statistics.tex'
    safe_title = latex_safe_string ( title )
    with open ( latex_filename, 'w' ) as latexfile:
        latexfile.write ( "\\begin{table}[ht]\n" )
        latexfile.write ( "\\centering\n" )
        latexfile.write ( "\\caption{" + safe_title + " General Statistics}\n" )
        latexfile.write ( "\\begin{tabular}{|c|c|c|c|c|c|}\n" )
        latexfile.write ( "\\hline\n" )
        latexfile.write (
            "\\textbf{Metric} & \\textbf{Mean} & \\textbf{Median} & \\textbf{Minimum} & \\textbf{Maximum} & \\textbf{Standard Deviation} \\\\\n" )
        latexfile.write ( "\\hline\n" )
        for metric, stats in data_dict.items ():
            if isinstance ( stats, dict ) and 'Individual' not in metric and 'Bandwidth Distribution' not in metric:
                if 'Duration' in metric or 'Slack' in metric or 'Overhead' in metric:
                    units = ' (ns)'
                else:
                    units = ' (B)'

                metric = metric + units
                mean = stats.get ( 'Mean', '' )
                median = stats.get ( 'Median', '' )
                minimum = stats.get ( 'Minimum', '' )
                maximum = stats.get ( 'Maximum', '' )
                std_dev = stats.get ( 'Standard Deviation', '' )
                latexfile.write ( f"{metric} & {mean} & {median} & {minimum} & {maximum} & {std_dev} \\\\\n" )
                latexfile.write ( "\\hline\n" )
        latexfile.write ( "\\end{tabular}\n" )
        latexfile.write ( "\\label{tab:" + underscore_title + "_general_stats}\n" )
        latexfile.write ( "\\end{table}\n" )


def export_single_general_stat_to_CSV(data_dict, parent_dir, title):
    underscore_title = title.replace ( ' ', '_' )
    csv_filename = parent_dir + f'/{underscore_title}_general_statistics.csv'
    with open ( csv_filename, 'w', newline='' ) as csvfile:
        writer = csv.writer ( csvfile )
        writer.writerow ( [f"{title} General Statistics"] )
        writer.writerow ( ['Metric', 'Mean', 'Median', 'Minimum', 'Maximum', 'Standard Deviation'] )
        for metric_name, stats in data_dict.items ():
            if isinstance ( stats,
                            dict ) and 'Individual' not in metric_name and 'Bandwidth Distribution' not in metric_name:
                if 'Duration' in metric_name or 'Slack' in metric_name or 'Overhead' in metric_name:
                    units = ' (ns)'
                else:
                    units = ' (B)'
                writer.writerow ( [metric_name + units] + [stats.get ( stat, '' ) for stat in
                                                           ['Mean', 'Median', 'Minimum', 'Maximum',
                                                            'Standard Deviation']] )


def export_summary_stat_to_latex(data_dict, parent_dir, title, stat_name):
    stat_name_replaced = stat_name.replace ( ' ', '_' )
    latex_filename = parent_dir + f'/{stat_name_replaced}_summary_statistics.tex'
    safe_title = latex_safe_string ( title )

    if 'Duration' in stat_name or 'Slack' in stat_name or 'Overhead' in stat_name:
        header = "\\textbf{Name} & \\textbf{Total Time (\\%)} & \\textbf{Total Time (us)} & \\textbf{Instances} & \\textbf{Mean (ns)} & \\textbf{Median (ns)} & \\textbf{Minimum (ns)} & \\textbf{Maximum (ns)} & \\textbf{Standard Deviation} \\\\\n"
    else:
        header = "\\textbf{Name} & \\textbf{Total Time (\\%)} & \\textbf{Total Time (us)} & \\textbf{Instances} & \\textbf{Mean (B)} & \\textbf{Median (B)} & \\textbf{Minimum (B)} & \\textbf{Maximum (B)} & \\textbf{Standard Deviation} \\\\\n"

    with open ( latex_filename, 'w' ) as latexfile:
        latexfile.write ( "\\begin{table}[ht]\n" )
        latexfile.write ( "\\centering\n" )
        latexfile.write ( "\\caption{" + safe_title + " Summary " + stat_name + " Statistics}\n" )
        latexfile.write ( "\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}\n" )
        latexfile.write ( "\\hline\n" )
        latexfile.write (header)
        latexfile.write ( "\\hline\n" )
        for metric, stats in data_dict.items ():
            name = stats['Name'] if "Kernel" in title else metric
            name = latex_safe_string ( name )
            time_percent = stats['Time Percent']
            time_duration = stats['Time Total']
            instances = stats['Instance']

            if isinstance ( stats[stat_name], dict ):
                mean = stats[stat_name].get ( 'Mean', '' )
                median = stats[stat_name].get ( 'Median', '' )
                minimum = stats[stat_name].get ( 'Minimum', '' )
                maximum = stats[stat_name].get ( 'Maximum', '' )
                std_dev = stats[stat_name].get ( 'Standard Deviation', '' )
                latexfile.write ( f"{name} & {time_percent} & {time_duration} & {instances} & {mean} & {median} & {minimum} & {maximum} & {std_dev} \\\\\n" )
                latexfile.write ( "\\hline\n" )
        latexfile.write ( "\\end{tabular}\n" )
        latexfile.write ( "\\label{tab:" + stat_name_replaced + "_summary_stats}\n" )
        latexfile.write ( "\\end{table}\n" )


def export_summary_stat_to_CSV(data_dict, parent_dir, title, stat_name):
    stat_name_replaced = stat_name.replace ( ' ', '_' )
    csv_filename = parent_dir + f'/{stat_name_replaced}_summary_statistics.csv'
    with open ( csv_filename, 'w', newline='' ) as csvfile:
        writer = csv.writer ( csvfile )
        writer.writerow ( [f"{title} Summary {stat_name} Statistics"] )
        if 'Duration' in stat_name or 'Slack' in stat_name or 'Overhead' in stat_name:
            writer.writerow ( ['Name', 'Total Time (%)', 'Total Time (us)', 'Instances', 'Mean (ns)', 'Median (ns)', 'Minimum (ns)', 'Maximum (ns)', 'Standard Deviation'] )
        else:
            writer.writerow ( ['Name', 'Total Time (%)', 'Total Time (us)', 'Instances', 'Mean (B)', 'Median (B)', 'Minimum (B)', 'Maximum (B)', 'Standard Deviation'] )

        for metric_name, stats in data_dict.items ():
            name = stats['Name'] if "Kernel" in title else metric_name
            time_percent = stats['Time Percent']
            time_duration = stats['Time Total']
            instances = stats['Instance']

            if isinstance ( stats[stat_name], dict ):
                writer.writerow ( [name, time_percent, time_duration, instances] +
                                  [stats[stat_name].get ( stat, '' ) for stat in
                                   ['Mean', 'Median', 'Minimum', 'Maximum', 'Standard Deviation']] )


def export_overall_summary_stat_to_latex(data_dict, parent_dir):
    latex_filename = parent_dir + '/overall_application_summary_statistics.tex'
    total_time = data_dict['Time Total']

    with open ( latex_filename, 'w' ) as latexfile:
        latexfile.write ( "\\begin{table}[ht]\n" )
        latexfile.write ( "\\centering\n" )
        latexfile.write ( "\\caption{Overall Application Duration Summary}\n" )
        latexfile.write ( "\\begin{tabular}{|c|c|c|c|}\n" )
        latexfile.write ( "\\hline\n" )
        latexfile.write ("\\textbf{Name} & \\textbf{Total Time (\\%)} & \\textbf{Total Time (us)} & \\textbf{Instances} \\\\\n")
        latexfile.write ( "\\hline\n" )
        for name, stats in data_dict.items():
            if isinstance(stats, dict):
                time_duration = stats['Time Total']
                instances = stats['Instance']
                time_percent = round( time_duration / total_time * 100, 2)
                latexfile.write ( f"{name} & {time_percent} & {time_duration} & {instances} \\\\\n" )
                latexfile.write ( "\\hline\n" )
        latexfile.write ( "\\end{tabular}\n" )
        latexfile.write ( "\\label{tab:overall_summary_stats}\n" )
        latexfile.write ( "\\end{table}\n" )


def export_summary_summary_stat_to_CSV(data_dict, parent_dir):
    csv_filename = parent_dir + f'/overall_application_summary_statistics.csv'
    total_time = data_dict['Time Total']

    with open ( csv_filename, 'w', newline='' ) as csvfile:
        writer = csv.writer ( csvfile )
        writer.writerow ( [f"Overall Application Duration Summary"] )
        writer.writerow ( ['Name', 'Total Time (%)', 'Total Time (us)', 'Instances'] )
        for name, stats in data_dict.items():
            if isinstance(stats, dict):
                time_duration = stats['Time Total']
                instances = stats['Instance']
                time_percent = round( time_duration / total_time * 100, 2)
                writer.writerow ( [name, time_percent, time_duration, instances] )