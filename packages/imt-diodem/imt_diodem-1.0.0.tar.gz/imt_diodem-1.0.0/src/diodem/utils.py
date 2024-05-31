import math
import os
from pathlib import Path
from typing import Optional
import warnings

import numpy as np
from qmt import nanInterp
from qmt import quatInterp
from qmt import vecInterp
from scipy.interpolate import CubicSpline
import tree
import tree_utils
from tree_utils import PyTree


def crop_sequence(data: dict, dt: float, t1: float = 0.0, t2: Optional[float] = None):
    # crop time left and right
    if t2 is None:
        t2i = tree_utils.tree_shape(data)
    else:
        t2i = int(t2 / dt)
    t1i = int(t1 / dt)
    return tree.map_structure(lambda arr: np.array(arr)[t1i:t2i], data)


def crop_tail(
    signal: PyTree,
    hz: Optional[int | float | PyTree] = None,
    strict: bool = True,
    verbose: bool = True,
):
    "Crop all signals to length of shortest signal."
    verbose_msg_index = False
    if hz is None:
        hz = 1.0
        verbose_msg_index = True

    if isinstance(hz, (int, float)):
        hz = tree.map_structure(lambda _: hz, signal)

    # int -> float
    hz = tree.map_structure(float, hz)

    def length_in_seconds(arr, hz):
        assert arr.ndim < 3
        return len(arr) / hz

    signal_lengths = tree.map_structure(length_in_seconds, signal, hz)
    shortest_length = min(tree.flatten(signal_lengths))
    hz_of_shortest_length = tree.flatten(hz)[np.argmin(tree.flatten(signal_lengths))]

    if strict:
        # reduce shortest_length until it becomes a clearn crop for all other
        # frequencies
        i = -1
        cleancrop = False
        while not cleancrop:
            i += 1
            shortest_length -= i * (1 / hz_of_shortest_length)
            cleancrop = True

            for each_hz in tree.flatten(hz):
                if (shortest_length * each_hz) % 1 != 0.0:
                    cleancrop = False
                    break

            if i > int(hz_of_shortest_length):
                warnings.warn(
                    f"Must crop more than i={i} and still no clean crop possible."
                )

            if i > 100:
                break

    if verbose:
        if verbose_msg_index:
            print(
                f"`crop_tail`: Crop off at index i="
                f"{shortest_length / hz_of_shortest_length}"
            )
        else:
            print(
                f"`crop_tail`: Crop off at t={shortest_length / hz_of_shortest_length}s"
            )

    def crop(arr, hz):
        if strict:
            crop_tail = np.round(shortest_length * hz, decimals=10)
            err_msg = (
                f"No clean crop possible: shortest_length={shortest_length}; hz={hz}"
            )
            assert (crop_tail % 1) == 0.0, err_msg
            crop_tail = int(crop_tail)
        else:
            crop_tail = math.ceil(shortest_length * hz)
        return arr[:crop_tail]

    return tree.map_structure(crop, signal, hz)


def hz_helper(
    segments: list[str],
    imus: list[str] = ["imu_rigid", "imu_flex"],
    markers: list[int] = [1, 2, 3, 4],
    hz_imu: float = 40.0,
    hz_omc: float = 120.0,
):
    hz_in = {}
    imu_dict = dict(acc=hz_imu, mag=hz_imu, gyr=hz_imu)
    for seg in segments:
        hz_in[seg] = {}
        for imu in imus:
            hz_in[seg][imu] = imu_dict
        for marker in markers:
            hz_in[seg][f"marker{marker}"] = hz_omc
        hz_in[seg]["quat"] = hz_omc

    return hz_in


def resample(
    signal: PyTree,
    hz_in: int | float | PyTree,
    hz_out: int | float | PyTree,
    quatdetect: bool = True,
    vecinterp_method: str = "linear",
) -> PyTree:
    # int -> float
    hz_in, hz_out = tree.map_structure(float, (hz_in, hz_out))

    if isinstance(hz_in, float):
        hz_in = tree.map_structure(lambda _: hz_in, signal)
    if isinstance(hz_out, float):
        hz_out = tree.map_structure(lambda _: hz_out, signal)

    def resample_array(signal: np.ndarray, hz_in, hz_out):
        is1D = False
        if signal.ndim == 1:
            is1D = True
            signal = signal[:, None]
        assert signal.ndim == 2

        N = signal.shape[0]
        ts_out = np.arange(N, step=hz_in / hz_out)
        signal = nanInterp(signal)
        if quatdetect and signal.shape[1] == 4:
            signal = quatInterp(signal, ts_out)
        else:
            if vecinterp_method == "linear":
                signal = vecInterp(signal, ts_out)
            elif vecinterp_method == "cubic":
                signal = _cubic_interpolation(signal, ts_out)
            else:
                raise NotImplementedError(
                    "`vecinterp_method` must be one of ['linear', 'cubic']"
                )
        if is1D:
            signal = signal[:, 0]
        return signal

    return tree.map_structure(resample_array, signal, hz_in, hz_out)


def _cubic_interpolation(signal: np.ndarray, ts_out: np.ndarray):
    ts_in = np.arange(len(signal))
    interp_1D = lambda arr: (CubicSpline(ts_in, arr)(ts_out))
    return np.array([interp_1D(signal[:, i]) for i in range(signal.shape[1])]).T


def autodetermine_imu_freq(path_imu_folder: str) -> int:
    hz = []
    for file in os.listdir(path_imu_folder):
        file = Path(path_imu_folder).joinpath(file)
        if file.suffix != ".txt":
            continue

        with open(file) as f:
            f.readline()
            # second line in txt file is: // Update Rate: 40.0Hz
            second_line = f.readline()
            before = len("// Update Rate:")
            hz.append(int(float(second_line[before:-3])))

    assert len(set(hz)) == 1, f"IMUs have multiple sampling rates {hz}"
    return hz[0]


def autodetermine_optitrack_freq(path_optitrack: str):
    def find_framerate_in_line(line: str, key: str):
        before = line.find(key) + len(key) + 1
        return int(float(line[before:].split(",")[0]))

    # first line is:
    # ...,Capture Frame Rate,120.000000,Export Frame Rate,120.000000,...
    with open(path_optitrack) as f:
        line = f.readline()
        hz_cap = find_framerate_in_line(line, "Capture Frame Rate")
        hz_exp = find_framerate_in_line(line, "Export Frame Rate")
        if hz_cap != hz_exp:
            warnings.warn(
                f"Capture ({hz_cap}) and exported ({hz_exp}) frame rate are not equal"
            )

    return hz_exp


def autodetermine_imu_file_prefix(path_imu_folder: str) -> str:
    prefixes = []
    for file in os.listdir(path_imu_folder):
        if file[-4:] != ".txt":
            continue
        prefixes.append(file[:-6])

    assert len(set(prefixes)) == 1, f"IMUs have multiple different prefixes {prefixes}"
    return prefixes[0]


_POSSIBLE_DELIMITERS = [";", "\t"]


def autodetermine_imu_file_delimiter(path_imu_folder: str) -> str:
    delimiters = []
    for file in os.listdir(path_imu_folder):
        file = Path(path_imu_folder).joinpath(file)
        if file.suffix != ".txt":
            continue

        with open(file) as f:
            # throw away header
            for _ in range(10):
                f.readline()
            # read in some data row
            data_row = f.readline()
            for delim in _POSSIBLE_DELIMITERS:
                # 9D IMU + packet count = 10, or
                # 9D IMU + packet count + finite time + quat estimate = 15
                if len(data_row.split(delim)) in [10, 15]:
                    delimiters.append(delim)
                    break
            else:
                raise Exception(f"No possible delimiter found for row={data_row}")

    assert (
        len(set(delimiters)) == 1
    ), f"IMUs have multiple different delimiters {delimiters}"
    return delimiters[0]


def autodetermine_space_units(path_optitrack: str) -> float:
    # Example first row of header
    # Format Version,1.23,Take Name,S_04,Take Notes,,Capture Frame Rate,30.000000,
    # Export Frame Rate,120.000000,Capture Start Time,2023-06-02 12.09.45.344 PM,
    # Capture Start Frame,246045,Total Frames in Take,19421,Total Exported Frames,
    # 77681,Rotation Type,Quaternion,Length Units,Meters,Coordinate Space,Global

    def find_length_units_in_line(line: str, key: str):
        before = line.find(key) + len(key) + 1
        return line[before:].split(",")[0]

    # first line is:
    # ...,Capture Frame Rate,120.000000,Export Frame Rate,120.000000,...
    with open(path_optitrack) as f:
        line = f.readline()
        units = find_length_units_in_line(line, "Length Units")

    return {"Meters": 1.0, "Millimeters": 1000.0}[units]


# could use instead of `qmt.nanInterp`
def _interp_nan_values(arr: np.ndarray, interp_fn):
    """Interpolate intermediate nan-values, and crop nan beginning and end.

    Args:
        arr (np.ndarray): NxF array.
        interp_fn: (2xF, float) -> F,
    """
    assert arr.ndim == 2

    nan_values = []
    current_idx = -1
    current_run = 0
    for i in range(len(arr)):
        if np.any(np.isnan(arr[i])):
            if current_run == 0:
                current_idx = i
            current_run += 1
        else:
            if current_run > 0:
                nan_values.append((current_idx, current_run))
                current_run = 0

    for start, length in nan_values:
        for i in range(length):
            alpha = (i + 1) / (length + 1)
            left = start - 1 if start != 0 else 0
            arr[start + i] = interp_fn(arr[[left, start + length]], alpha)

    # now `arr` has no more NaNs except if very first or very last value was NaN
    for start in range(len(arr)):
        if np.any(np.isnan(arr[start])):
            continue
        break

    for stop in range(len(arr) - 1, -1, -1):
        if np.any(np.isnan(arr[stop])):
            continue
        break

    return arr[start:stop]
