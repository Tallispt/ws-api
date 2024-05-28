import numpy as np
import pandas as pd
import statsmodels.api as sm


def rgb_to_cmyk(data):
    r, g, b = np.split(data / 255.0, 3, axis=1)
    k = 1 - np.max(np.hstack([r, g, b]), axis=1)
    r = r.ravel()
    g = g.ravel()
    b = b.ravel()
    c = np.round((1 - r - k) * 100 / (1 - k), 2)
    m = np.round((1 - g - k) * 100 / (1 - k), 2)
    y = np.round((1 - b - k) * 100 / (1 - k), 2)
    return np.vstack((c, m, y, np.round(k * 100, 2))).T


def rgb_to_hsv(data):
    r, g, b = np.split(data / 255.0, 3, axis=1)
    min_value = np.min(np.hstack([r, g, b]), axis=1)
    max_value = np.max(np.hstack([r, g, b]), axis=1)
    delta = max_value - min_value
    r = r.ravel()
    g = g.ravel()
    b = b.ravel()

    hsv_list = []
    for i in range(len(data)):
        if delta[i] == 0:
            h = 0
        elif max_value[i] == r[i]:
            h = ((g[i] - b[i]) / delta[i]) % 6
        elif max_value[i] == g[i]:
            h = (b[i] - r[i]) / delta[i] + 2
        else:
            h = (r[i] - g[i]) / delta[i] + 4

        h = np.round(h * 60)

        if max_value[i] == 0:
            s = 0
        else:
            s = delta[i] / max_value[i]

        s = np.round(s, 2)
        v = np.round(max_value[i], 2)

        hsv_list.append((h, np.round(s * 100, 2), np.round(v * 100, 2)))
    return np.array(hsv_list)


def rgb_to_de(data):
    return [np.round(np.sqrt(ch[0] ^ 2 + ch[1] ^ 2 + ch[2] ^ 2), 2) for ch in data]


def convert_colors(values, channel):
    match channel:
        case "RGB":
            return values
        case "CMYK":
            return rgb_to_cmyk(values)
        case "HSV":
            return rgb_to_hsv(values)
        case "E":
            return rgb_to_de(values)
        case _:
            return


def create_spots_df(values, channel):
    df = (
        pd.DataFrame(values, columns=list(channel))
        .reset_index()
        .rename(columns={"index": "spots"})
    )
    df.spots = np.arange(1, len(df) + 1)
    return df


def create_replicates_df(data, info, channel_type, number_channels):
    df = pd.DataFrame({info["xLabel"]: info["xValues"][::-1]})
    df.attrs = info
    df.attrs["chanType"] = channel_type
    df.attrs["chanNum"] = number_channels

    if number_channels > 1:
        for i in range(len(data[0])):
            channel = [subarray[i] for subarray in data]
            for j in range(info["replicateNum"]):
                df["{color}{j}".format(color=channel_type[i], j=j + 1)] = channel[j::3]
        return df

    for i in range(info["replicateNum"]):
        df["{color}{i}".format(color=channel_type, i=i + 1)] = data[i::3]

    return df.sort_values(by=[info["xLabel"]]).reindex()


def create_avs_df(df: pd.DataFrame, discrete=False):
    new_df = pd.DataFrame({df.attrs["xLabel"]: df.attrs["xValues"]})
    new_df.attrs = df.attrs
    repl = df.attrs["replicateNum"]
    chan_type = df.attrs["chanType"]
    chan_num = df.attrs["chanNum"]
    for i in range(chan_num):
        new_df["{v}_av".format(v=chan_type[i : i + len(chan_type) // chan_num])] = (
            df.iloc[:, (1 + repl * i) : (4 + repl * i)].mean(axis=1).round(2)
        )
        new_df["{v}_std".format(v=chan_type[i : i + len(chan_type) // chan_num])] = (
            df.iloc[:, (1 + repl * i) : (4 + repl * i)].std(axis=1).round(2)
        )

    if discrete:
        new_df.iloc[:, 1::2] = new_df.iloc[:, 1::2].round(0)

    return new_df


def create_regressions_df(df, channels):
    X = list(df.iloc[:, 0])
    X = sm.add_constant(X)

    channel_dict = dict()
    plot_regression_dict = dict()

    for index, channel in enumerate(channels):
        y = list(df.iloc[:, index * 2 + 1])

        model = sm.OLS(y, X).fit()
        predict = model.predict()

        summary = {
            "Ang_coef": model.params[1],
            "Ang_std": model.bse[1],
            "Lin coef": model.params[0],
            "Lin_std": model.bse[0],
            "R2": model.rsquared,
            "t-value_ang": model.tvalues[1],
            "p-value_ang": model.pvalues[1],
            "t-value_lin": model.tvalues[0],
            "p-value_lin": model.pvalues[0],
        }

        predict_values = {"x": list(df.iloc[:, 0]), "y": np.round(predict, 2).tolist()}

        channel_dict[channel] = summary
        plot_regression_dict[channel] = predict_values

    return (
        pd.DataFrame(channel_dict)
        .T.reset_index()
        .rename(columns={"index": "channel"})
        .round(decimals=5),
        pd.DataFrame(plot_regression_dict),
    )
