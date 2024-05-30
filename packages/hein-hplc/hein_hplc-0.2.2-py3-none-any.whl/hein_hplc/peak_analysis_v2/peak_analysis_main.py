import plotly.graph_objects as go
from pandas import DataFrame, read_csv
from hein_hplc.peak_analysis_v2.peak_deconvolution import *


class PeakAnalysis:
    def __init__(self, data: DataFrame):
        self.y_title = ''
        self.data = data
        self.x_raw = self.data[self.data.columns[0]].values  # the first column is retention time
        self._point_per_min = len(self.x_raw[np.where(self.x_raw < 1)])
        self.y_raw = self.data[self.data.columns[1]].values  # default y is the second column
        self.pre_process_x()
        self.results = {}
        self.retention_time_list = []
        self.plot = {}  # data dict for exporting csv

    def generate_report(self,
                        range_of_interest=None,
                        smooth_window: int = 41,
                        peak_height: float = 0.003,
                        extended_range=50,
                        tailing_fronting: str = "tailing",
                        smooth_derivative: bool = False,
                        use_derivative: bool = False,
                        peak_shift: float = 0.01,
                        dead_volume: float = 60,
                        ):
        column_names = self.data.columns.tolist()
        column_names.pop(0)
        for index, column in enumerate(column_names):
            self.peak_deconvolution(column_name=column,
                                    range_of_interest=range_of_interest,
                                    smooth_window=smooth_window,
                                    peak_height=peak_height,
                                    tailing_fronting=tailing_fronting,
                                    smooth_derivative=smooth_derivative,
                                    use_derivative=use_derivative,
                                    dead_volume=dead_volume,
                                    plot=False,
                                    )
        new_format = format_save_csv(self.results, self.retention_time_list, peak_shift)
        return DataFrame(new_format)

    def peak_deconvolution(self,
                           column_name=None,
                           range_of_interest=None,
                           smooth_window: int = 41,
                           peak_height: float = 0.003,
                           tailing_fronting: str = "tailing",
                           area_in_second: bool = True,
                           peak_width: float = 0.05,
                           use_derivative: bool = False,
                           smooth_derivative: bool = False,
                           show_derivative: bool = False,
                           dead_volume: float = 60,
                           plot: bool = True,
                           ):
        if column_name:
            self.pre_process_data(column_name=column_name)
        x, y = self.select_range(range_of_interest=range_of_interest)
        dead_volume_index = max(dead_volume / 60 - range_of_interest[0], 0) if range_of_interest else dead_volume / 60
        y_max = max(y[int(dead_volume_index * self._point_per_min):])
        normalized_y = y * 100 / y_max

        graph = go.Figure()
        if plot:
            graph.add_trace(go.Scatter(x=x, y=y, name="Original HPLC"))
            self.plot['HPLC'] = dict(x=x, y=y)
        # smoothed_y = savgol_filter(y, window_length=smooth_window, polyorder=2)
        # print(sum(smoothed_y-y))
        peak_group_ranges = find_peak_group(y, smooth_window=smooth_window)
        # graph.add_trace(go.Scatter(x=x, y=smoothed_y, mode='lines', name="Smoothed HPLC"))

        # find normalized second derivative
        dy2 = second_derivative(y, smooth_window=smooth_window, smooth_derivative=smooth_derivative)
        dy2 = dy2 * 100 / max(dy2[int(dead_volume_index * self._point_per_min):])

        # Find the peaks in the second derivative
        if use_derivative:
            all_peaks, _ = find_peaks(dy2, prominence=(peak_height, None), width=10)
        else:
            all_peaks, _ = find_peaks(normalized_y, height=peak_height, prominence=(1, None), width=10, distance=10)

        all_peaks = all_peaks[x[all_peaks] > dead_volume / 60]

        if show_derivative:
            graph.add_trace(go.Scatter(x=x, y=dy2 * y_max / 100, name="Second derivative", line=dict(color='green')))
        print(f"Found peaks at {x[all_peaks]}")

        # initializing
        shapes, peaks_x, peaks_y, tailing_factor, peaks_label = [], [], [], [], []
        result_dict = {}

        # graph.add_trace(go.Scatter(x=x, y=b, name="Adaptive baseline correction"))
        for (start, end) in peak_group_ranges:
            # preliminary fit for each group, separate if there are multiple peak cluster in this region
            baseline = np.linspace(y[start], y[end - 1], end - start)
            x_peak = x[start: end]
            y_peak_original = y[start: end]
            y_peak = y_peak_original - baseline

            peaks = all_peaks[np.where((start < all_peaks) & (all_peaks < end))]
            # reset index
            peaks = peaks - start
            # print(peaks)
            if len(peaks) > 0:
                peaks_params, bounds = find_para(x_peak, y_peak, peaks, peak_width=peak_width,
                                                 tailing_fronting=tailing_fronting)
                (popt, pcov) = curve_fit(fit_peaks, x_peak, y_peak, peaks_params, bounds=bounds)
                label_color = 'rgba(0, 0, 0, 0.1)' if len(peaks) == 1 else 'rgba(255, 0, 0, 0.1)'
                for i in range(len(peaks)):
                    peak_param = popt[i * 4:(i + 1) * 4]
                    peak = asym_peak(x_peak, peak_param)
                    area = np.trapz(peak, x_peak) * 60 if area_in_second else np.trapz(peak, x_peak)
                    retention_time = round(peak_param[1], 3)
                    peak_mid_index = np.argmax(peak)
                    threshold = 0.05 * max(peak)
                    peak_above_1_20 = np.where(peak > threshold)[0]
                    # print(peak_above_1_20[0], peak_above_1_20[-1], peak_mid_index)
                    try:
                        tf = len(peak_above_1_20) / 2 / (peak_mid_index - peak_above_1_20[0])
                    except IndexError:
                        tf = -1
                    tailing_factor.append(tf)
                    peaks_x.append(x_peak[np.argmax(peak)])
                    peaks_y.append(y_peak_original[np.argmax(peak)])
                    peaks_label.append(round(area, 4))
                    print(
                        f"RT: {retention_time}\tArea: {area:.4f}\tTailing: {peak_param[3]:.4f}\tGaussian: {peak_param[2]:.4f}")
                    result_dict[retention_time] = area
                    if retention_time not in self.retention_time_list:
                        self.retention_time_list.append(retention_time)
                    if plot:
                        self.plot[f"Time: {retention_time}, Area: {area:.4f}"] = dict(x=x_peak, y=peak + baseline)
                        if not len(peaks) == 1:
                            graph.add_trace(
                                go.Scatter(x=x_peak, y=peak + baseline, mode='lines',
                                           name=f'Peak at {retention_time} min',
                                           legendgroup="deconvolution",
                                           legendgrouptitle_text="Peak deconvolution results",
                                           line=dict(dash='dash')))
                if plot:
                    if len(peaks) > 1:
                        self.plot["Fitted plot"] = dict(x=x_peak, y=fit_peaks(x_peak, *popt) + baseline)
                        graph.add_trace(
                            go.Scatter(x=x_peak, y=fit_peaks(x_peak, *popt) + baseline, mode='lines',
                                       legendgroup="Fitted plot", name="Fitted plot", line=dict(color='red'), ))
                    shapes.append(dict(
                        type='rect',
                        x0=x[max(0, start)],
                        x1=x[min(len(x) - 1, end)],
                        y0=min(y) - 0.1 * (max(y) - min(y)),
                        y1=max(y) + 0.1 * (max(y) - min(y)),
                        fillcolor=label_color,
                        line=dict(width=0),
                        xref='x',
                        yref='y'
                    ))
                    graph.add_trace(go.Scatter(x=x_peak, y=baseline, mode='lines', legendgroup="Auto baseline",
                                               showlegend=False, line=dict(dash='dash', color='black'), ))
        print("================================================================")
        self.results[column_name] = result_dict
        if plot:
            graph.add_trace(go.Scatter(x=peaks_x, y=peaks_y, name="Peaks", mode="markers",
                                       hovertemplate='<b>Retention time<b>: %{x:.2f}' +
                                                     '<br><b>Peak area<b>: %{customdata[0]}<br>' +
                                                     '<b>Tailing factor<b>: %{customdata[1]:,.2f}<br>',
                                       customdata=np.stack((peaks_label, tailing_factor), axis=-1),
                                       marker=dict(
                                           symbol="line-ns", color="black", size=15, line=dict(color="black", width=2, )
                                       )))
            graph.update_layout(shapes=shapes,
                                xaxis=dict(title_text="retention time / min"),
                                yaxis=dict(title_text=f"intensity {self.y_title}"), )
            x_values = self.plot.get("HPLC")['x']
            csv_data = {'retention time': x_values}
            for layer_name, layer_data in self.plot.items():
                y_values = [layer_data['y'][np.where(layer_data['x'] == x)[0]][0] if x in layer_data['x'] else np.nan
                            for x in x_values]
                csv_data[layer_name] = y_values
            df = DataFrame(csv_data)
            df.to_csv('plot_data.csv', index=False, float_format='%.4f', na_rep='')
        return graph

    def pre_process_data(self, column_name):
        """trim data if sampling rate is higher than 2400 point per min"""
        self.y_raw = self.data[column_name].values
        if self._point_per_min > 2400:
            self.y_raw = self.y_raw[1:-1:4]
        if max(self.y_raw) > 20000:
            self.y_title = "x1000"
            self.y_raw = self.y_raw / 1000

    def select_range(self, range_of_interest=None, ):
        """select range of interest"""
        if range_of_interest:
            index = np.where(np.logical_and(range_of_interest[0] < self.x_raw, self.x_raw < range_of_interest[1]))
            y = self.y_raw[index]
            x = self.x_raw[index]
            return x, y
        return self.x_raw, self.y_raw

    def pre_process_x(self):
        """trim time data if sampling rate is higher than 2400 point per min"""
        if self._point_per_min > 2400:
            self.x_raw = self.x_raw[1:-1:4]


if __name__ == "__main__":
    # Testing plot without Dash app
    filename = r"..\..\sample_data\sample_data.csv"
    df = read_csv(filename)

    columns = df.columns.tolist()
    retention_time_name = columns.pop(0)
    col_name = columns[8]
    tool = PeakAnalysis(df)
    fig = tool.peak_deconvolution(smooth_window=80,
                                  peak_height=1,
                                  column_name=col_name,
                                  smooth_derivative=True
                                  # range_of_interest=[4.5, 15],
                                  )
    fig.show()
