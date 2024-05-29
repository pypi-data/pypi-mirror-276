import csv
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pendulum
import serial
from deprecated import deprecated
from loguru import logger
from pydantic import BaseModel
from tqdm import tqdm

from .config import Daq


class RealEvent(BaseModel):
    """実イベント

    OSECHIに接続したUSBポートから、シリアル通信で受け取った値を格納するためのデータクラス。
    ファイルに書き出したり、`pandas.DataFrame`に変換できるように自作メソッドを追加。

    """

    timestamp: datetime = pendulum.now()
    """測定時刻。宇宙線イベントが通過した日時。タイムゾーン付きの日付オブジェクト"""
    top: int = 0
    """topレイヤーのヒット。0 - 10の値"""
    mid: int = 0
    """midレイヤーのヒット。0 - 10の値"""
    btm: int = 0
    """btmレイヤーのヒット。0 - 10の値"""
    adc: int = 0
    """topレイヤーにヒットがあったときのADC値。0 - 1023の値"""
    tmp: float = 0.0
    """BME280で測定した気温。[degC]"""
    atm: float = 0.0
    """BME280で測定した気圧。[Pa]"""
    hmd: float = 0.0
    """BME280で測定した湿度。[%]"""

    def to_list_string(self) -> list[str]:
        """List

        メンバー変数を文字列にしたリストに変換します。

        ```python
        >>> real_data = RealEvent()
        >>> read_data.to_list_string()
        ['2024-05-21 08:44:20.389786+09:00', '0', '0', '0', '0', '0', '0', '0']
        ```

        """
        data = self.model_dump()
        values = [str(v) for v in data.values()]
        return values

    def to_csv_string(self) -> str:
        """Comma Separated Values

        メンバー変数をCSV形式（カンマ区切り）の文字列に変換します。
        OSECHIから受け取ったデータを、ファイルに保存する際に使うことを想定したメソッドです。

        ```python
        >>> real_data = RealEvent()
        >>> real_data.to_csv_string()
        '2024-05-21 08:44:20.389786+09:00,0,0,0,0,0,0,0'
        ```

        """
        data = self.model_dump().values()
        values = [str(v) for v in data]
        csv_string = (",").join(values)
        return csv_string

    def to_tsv_string(self) -> str:
        """Tab Separated Values

        メンバー変数をTSV形式（タブ区切り）の文字列に変換します。

        ```python
        >>> real_data = RealEvent()
        >>> real_data.to_tsv_string()
        '2024-05-21 08:44:20.389786+09:00\t0\t0\t0\t0\t0\t0\t0'
        ```

        """
        data = self.model_dump().values()
        values = [str(v) for v in data]
        tsv_string = ("\t").join(values)
        return tsv_string

    def to_ltsv_string(self) -> str:
        """Labeled Tab-Separated Values

        メンバー変数をLTSV形式（ラベルありのタブ区切り）の文字列に変換します。

        ```python
        >>> real_data = RealEvent()
        >>> real_data.to_ltsv_string()
        'timestamp:2024-05-21 08:44:20.389786+09:00\ttop:0\tmid:0\tbtm:0\tadc:0\ttmp:0\tatm:0\thmd:0'
        ```
        """
        data = self.model_dump().items()
        values = [f"{k}:{v}" for k, v in data]
        ltsv_string = ("\t").join(values)
        return ltsv_string


@deprecated(version="0.15.0", reason="Use mkdir_saved")
def init_saved(daq: Daq) -> None:
    logger.warning("Deprecated since 0.15.0: Use mkdir_saved")
    return mkdir_saved(daq)


def mkdir_saved(daq: Daq) -> None:
    """Initialize destination directory to save data files

    保存先のディレクトリを初期化します。
    ディレクトリが存在しない場合は、新しく作成します。
    ディレクトリが存在する場合は、そのままにします。

    :Args:
    - daq(Daq): DAQ設定オブジェクト
    ```
    """

    p = Path(daq.saved)
    p.mkdir(exist_ok=True)
    msg = f"Save files to : {p}"
    logger.info(msg)

    return


def get_savef(args: Daq, fid: int | str) -> Path:
    """Get filename to save data

    保存するファイル名を生成します。
    DAQ設定の接頭辞（``prefix``）と拡張子（``suffix``）の値を使って
    ``{prefix}_{連番:06}.{suffix}``の形式で生成します。

    :Args:
    - args(Daq): DAQ設定オブジェクト
        - prefix: ファイルの接頭辞
        - suffix: ファイルの拡張子
    - n(int): ファイル番号

    :Example:
    ```console
    osechi_data_000000.csv
    osechi_data_000001.csv
    osechi_data_000002.csv
    ```

    """
    stem = f"{args.prefix}_{fid:07}"
    fname = Path(stem).with_suffix(args.suffix)
    savef = Path(args.saved, fname)

    msg = "deprecation warning: use get_savef_with_timestamp instaed."
    logger.warning(msg)

    return savef


def get_savef_with_timestamp(args: Daq, fid: int | str) -> Path:
    """Get filename to save data with timestamp

    作成日を含んだファイル名を生成する。
    ファイル名は、DAQ設定の接頭辞（``prefix``）、ファイルを開いた時刻（``pendulum.now``）と
    拡張子（``suffix``）の値を使って生成する。

    時刻のフォーマットは、ファイル名が分かりやすいように独自フォーマットにした。

    :Args:
    - `args (Daq)`: Daqオブジェクト
    - `fid (int|str)`: ファイル識別子

    :Returns:
    - `savef (Path)`: ファイル名（Pathオブジェクト）

    :Examples:
    ```console
    20240520/osechi_data_2024-05-20T12h34m56s_000000.csv
    20240520/osechi_data_2024-05-20T13h53m24s_000001.csv
    20240520/osechi_data_2024-05-20T14h46m23s_000000.csv  // 走り直すとリセット
    20240520/osechi_data_2024-05-20T14h36m32s_000001.csv
    ```

    """
    ts = pendulum.now().format("YYYY-MM-DDTHH[h]mm[m]ss[s]")
    # fidはintもしくはstrなので 07 とした
    # 07d だとstrのときにエラーがでる
    stem = f"{args.prefix}_{ts}_{fid:07}"
    fname = Path(stem).with_suffix(args.suffix)
    savef = Path(args.saved, fname)
    return savef


def open_serial_connection(daq: Daq) -> serial.Serial:
    """Open and return a serial connection.

    シリアル通信（UART）に使うポートを準備します。
    ``with``構文で使う想定です。

    通信に使うUSBポート名（``device``）、
    ボーレート（``baudrate``）、
    通信開始／書き込みのタイムアウト秒（``timeout``）は
    DAQ用の設定ファイルで変更できるようにしてあります。

    :Args:
    - daq(Daq): DAQ設定オブジェクト
        - device: USBポート名
        - baudrate: ボーレート（通信速度）[bps]
        - timeout: タイムアウト秒 [sec]

    :Returns:
    - port(serial.Serial): 通信を開始したシリアルオブジェクト

    :Example:

    ```python
    >>> with open_serial_connection(daq) as port:
    >>>     # データ測定の処理
    >>>
    ```

    """
    port = serial.Serial(
        daq.device,
        baudrate=daq.baudrate,
        timeout=daq.timeout,
        write_timeout=daq.timeout,
    )
    port.rts = False
    port.dtr = False

    # logger.debug(f"Port opened: {port}")

    return port


def write_vth(port: serial.Serial, ch: int, vth: int):
    """Write threshold to OSECHI.

    シリアル通信（UART）を使って閾値を書き込みます。
    値を書き込んだあとに、値が読み出せるかを確認します。

    読み出した値が ``dame`` となっている場合は書き込みに失敗しています。
    その場合は、もういちど設定し直すよう警告を表示します。

    ESP32のバッファサイズの制限から、閾値は2回に分割して転送しています。

    - ``val1`` は vth を右に6ビットシフト（=64で割る）して、head を足した値
    - ``val2`` は vth を左に2ビットシフト（=4をかける）して、下位8ビットを取り出した値

    詳細はこの関数のソースコードを確認してください。
    """
    val = vth
    head = 0b10000
    val1 = head + (val >> 6)
    val2 = (val << 2) & 0xFF

    logger.debug(f"Write: ch = {ch}")
    logger.debug(f"Write: val1 = {val1:b}")
    logger.debug(f"Write: val2 = {val2:b}")

    port.write(ch.to_bytes(1, "big"))
    port.write(val1.to_bytes(1, "big"))
    port.write(val2.to_bytes(1, "big"))

    read0 = port.readline().decode("utf-8", "ignore").strip()
    read1 = port.readline().decode("utf-8", "ignore").strip()
    read2 = port.readline().decode("utf-8", "ignore").strip()

    logger.debug(f"Read: ch = {read0}")
    logger.debug(f"Read: val1 = {read1}")
    logger.debug(f"Read: val2 = {read2}")

    success = False

    if read0 == "dame":
        success = False
        msg = f"Ch{ch}: Set threshold failed. Try again."
        logger.warning(msg)
    elif read0 == str(ch):
        success = True
        msg = f"Ch{ch}: Set threshold to {vth}."
        logger.success(msg)
    else:
        success = True
        msg = f"Ch{ch}: Set threshold to {vth}. Maybe."
        logger.success(msg)
    return success


def set_vth(daq: Daq, ch: int, vth: int) -> bool:
    """Set threshold

    チャンネル番号を指定し、閾値を設定します。
    チャンネル番号は1 - 3 の範囲で指定してください。
    閾値は1 - 1023 の範囲で指定してください。

    書き込みに成功すると ``success=True`` を返します。
    書き込みに失敗した場合は、警告メッセージを表示します。
    このとき、設定済みの閾値はそのままになります。

    :Args:
    - daq(Daq): DAQ設定オブジェクト
    - ch(int): チャンネル番号。1 - 3の範囲で指定してください
    - vth(int): 閾値の値。1 - 1023 の範囲で指定してください
    """

    # check values
    if ch not in range(1, 4):
        msg = f"value of ch is out of range: {ch}"
        logger.error(msg)
        sys.exit()

    if vth not in range(1, 1024):
        msg = f"value of vth is out of range: {vth}"
        logger.error(msg)
        sys.exit()

    mkdir_saved(daq)

    try:
        with open_serial_connection(daq) as port:
            success = write_vth(port, ch, vth)
            fname = Path(daq.saved) / daq.fname_logs

            with fname.open("a", newline="") as f:
                now = pendulum.now().to_iso8601_string()
                row = [str(now), str(ch), str(vth), str(success)]
                writer = csv.writer(f)
                writer.writerow(row)
            msg = f"Saved data to {fname}."
            logger.info(msg)
        return success
    except serial.SerialException as e:
        logger.error(e)
        msg = """Could not open the port. Device name might be wrong.
        Run 'arduino-cli board list' and check the device name.
        Edit 'daq.toml' if you needed.
        """
        logger.warning(msg)
        sys.exit()
    except Exception as e:  # noqa
        logger.error(e)
        msg = """
        Unaware error occurred.
        Please think if you need to handle this error.
        """
        sys.exit()


def set_vth_retry(daq: Daq, ch: int, vth: int, max_retry: int) -> bool:
    """
    Retry setting threshold.

    :Args:
    - daq (Daq): Daqオブジェクト
    - ch (int): チャンネル番号
    - vth (int): スレッショルド値
    - max_retry (int): 設定に失敗ししたときにトライする最大回数

    :Returns:
    - success (bool): スレッショルド値の設定の結果
    """

    for i in range(max_retry):
        success = set_vth(daq, ch, vth)
        if success:
            return True
        msg = f"Retry: {i} / {max_retry} times."
        logger.warning(msg)

    return False


@deprecated(
    version="0.15.0",
    reason="Will be deprecated. Use _read_serial_data_as_event with validation.",
)
def _read_serial_data_as_list(port: serial.Serial) -> list:
    """(Will be deprecated) Read serial data from port.

    OSECHIが接続されているポートからデータを読み出します。
    引数に指定するポートは、あらかじめ開いたものを渡してください。
    ``run_daq``や``time_daq``でデータを取得するために使います。

    :Args:
    - port (serial.Serial): Serialオブジェクト

    :Returns:
    - row (list): 読み出した時刻を追加したデータのリスト

    :Examples:
    ```python
    >>> with open_serial_connection() as port:
    >>>     row = read_serial_data(port)
    >>>     row
    [日付, top, mid, btm, adc, tmp, atm, hmd]
    ```

    """
    msg = "Will be deprecated."
    logger.warning(msg)
    now = pendulum.now().to_iso8601_string()
    data = port.readline().decode("UTF-8").strip()
    if len(data) == 0:
        msg = f"No data to readout. Timed-out: {port.timeout}"
        logger.warning(msg)
    row = f"{now} {data}".split()
    return row


def _read_serial_data_as_event(port: serial.Serial) -> RealEvent:
    """Read serial data from port.

    OSECHIが接続されているポートからデータを読み出します。
    引数に指定するポートは、あらかじめ開いたものを渡してください。
    ``run_daq``や``time_daq``でデータを取得するために使います。

    :Args:
    - port (serial.Serial): Serialオブジェクト

    :Returns:
    - row (list): 読み出した時刻を追加したデータのリスト

    :Examples:
    ```python
    >>> with open_serial_connection() as port:
    >>>     row = read_serialc_data(port)
    >>>     row
    [日付, top, mid, btm, adc, tmp, atm, hmd]
    ```

    """
    data = port.readline().decode("UTF-8").strip().split()
    if len(data) == 0:
        msg = f"No data to readout. Timed-out: {port.timeout}"
        logger.warning(msg)
    event = RealEvent()
    event.timestamp = pendulum.now()
    event.top = int(data[0])
    event.mid = int(data[1])
    event.btm = int(data[2])
    event.adc = int(data[3])
    event.tmp = float(data[4])
    event.atm = float(data[5])
    event.hmd = float(data[6])
    return event


def read_serial_data(port: serial.Serial) -> list:
    # data = _read_serial_data_as_list(port)
    data = _read_serial_data_as_event(port)
    return data.to_list_string()


def _loop_events(port: serial.Serial, rows: list) -> RealEvent:
    """イベント取得ループ

    :Args:
    - `port (serial.Serial)`: 接続済みのSerialオブジェクト
    - `rows (list)`: ループする回数

    :Yield:
    - event (RealEvent): OSECHIの測定データ

    """
    for _ in tqdm(rows, leave=False, desc="loops"):
        event = _read_serial_data_as_event(port)
        yield event


def loop_and_save_events(f, daq: Daq, port: serial.Serial) -> list[RealEvent]:
    rows = range(daq.max_rows)
    events = []
    for event in _loop_events(port, rows):
        events.append(event.model_dump_json())
        row = event.to_list_string()
        if daq.suffix in [".csv"]:
            row = event.to_csv_string()
            f.write(row + "\n")
        elif daq.suffix in [".dat", ".tsv"]:
            row = event.to_tsv_string()
            f.write(row + "\n")
        elif daq.suffix in [".json", ".jsonl"]:
            row = event.model_dump_json()
            f.write(row + "\n")
        f.flush()
    return events


@deprecated(version="0.15.0", reason="Will be deprecated. Use loop_and_save_events instead.")
def save_serial_data(f, daq: Daq, port: serial.Serial) -> list:
    """
    :Args:
    - f: ファイルポインタ
    - daq (Daq): Daqオブジェクト
    - port (serial.Serial): Serialオブジェクト

    :Return:
    - rows (list[list]): 取得したデータのリスト

    :TODO:
    - Daqオブジェクトに依存しない関数にしたい（ジェネレーターにするのがいいのかな？）
    - pd.DataFrameを返した方がいいかもしれない？
    """
    max_rows = daq.max_rows
    rows = []
    for _ in tqdm(range(max_rows), leave=False, desc="rows"):
        row = read_serial_data(port)
        rows.append(row)
        if daq.suffix == ".csv":
            writer = csv.writer(f)
            writer.writerow(row)
        else:
            writer = csv.writer(f, delimiter=" ")
            writer.writerow(row)
        f.flush()
    return rows


def run_daq(daq: Daq) -> None:
    """メインDAQ

    OSECHIが接続されたUSBポートとシリアル通信をして、データ取得する。
    指定したファイル数と行数をでループ処理する。

    :TODO:
    - 関数名をより適切なものに変えたい
    - while_daq みたいなのを作ってもいいかもしれない
    """
    # Open serial connection
    with open_serial_connection(daq) as port:
        mkdir_saved(daq)

        for nfile in tqdm(range(daq.max_files), desc="files"):
            savef = get_savef_with_timestamp(daq, nfile)
            msg = f"Saving data to: {savef}."
            logger.info(msg)
            logger.info("Press Ctrl-c to stop.")

            with savef.open("a") as f:
                # save_serial_data(f, daq, port)
                loop_and_save_events(f, daq, port)

            msg = f"Saved data to: {savef}."
            logger.success(msg)


def run(args: Daq):
    """メインのDAQ

    run_daqのラッパー。例外処理などで囲んだもの。

    :versionadded: `0.6.0`.
    """

    try:
        run_daq(args)
    except serial.SerialException as e:
        logger.error(e)
        msg = """Could not open the port. Device name might be wrong.
        Run 'arduino-cli board list' and check the device name.
        Edit 'daq.toml' if you needed.
        """
        logger.warning(msg)
        sys.exit()
    except KeyboardInterrupt as e:
        logger.warning(e)
        msg = """Quit."""
        logger.info(msg)
        sys.exit()
    except Exception as e:  # noqa
        logger.error(e)
        msg = """Exit.
        Unaware error occurred.
        Please think if you need to handle this error.
        """
        logger.error(msg)
        sys.exit()


def time_daq(args: Daq, duration: int) -> pd.DataFrame:
    """
    測定時間を指定してDAQを走らせます。

    :Args:
    - args (Daq): Daqオブジェクト
    - duration (int): 測定時間を秒で指定

    :Returns:
    - data (pd.DataFrame): 測定結果のデータフレーム
    """

    rows = []
    with open_serial_connection(args) as port:
        mkdir_saved(args)

        logger.debug("Port opened.")
        daq_start = pendulum.now()
        daq_stop = daq_start.add(seconds=duration)

        logger.debug(f"- DAQ Started: {daq_start}")
        logger.debug(f"- DAQ Stop   : {daq_stop}")

        while pendulum.now() < daq_stop:
            row = read_serial_data(port)
            event = RealEvent()
            event.timestamp = pendulum.now()
            event.top = int(row[1])
            event.mid = int(row[2])
            event.btm = int(row[3])
            event.adc = int(row[4])
            event.tmp = float(row[5])
            event.atm = float(row[6])
            event.hmd = float(row[7])
            rows.append(event.model_dump())
    daq_end = pendulum.now()
    diff = daq_end - daq_start
    elapsed_time = diff.in_seconds()
    logger.debug(f"- DAQ Closed : {daq_end} / Elapsed: {elapsed_time} sec.")
    data = pd.DataFrame(rows)
    return data


@deprecated(
    version="0.14.0",
    reason="Will be deprecated. Use threshold.scan_threshold_by_channel instead.",
)
def scan_ch_vth(daq: Daq, duration: int, ch: int, vth: int) -> list:
    """
    Run threshold scan.

    :Args:
    - daq (Daq): Daqオブジェクト
    - duration (int): 測定時間（秒）
    - ch (int): 測定するチャンネル番号
    - vth (int): スレッショルド値

    :Returns:
    - data (list): [測定時刻、チャンネル番号、スレッショルド値、イベント数]のリストを返します。
    """

    logger.warning("Will be deprecated. Please use threshold.scan_by_channel instead.")

    # Try to set the threshold
    if not set_vth_retry(daq, ch, vth, 3):
        msg = f"Failed to set threshold: ch{ch} - {vth}"
        logger.error(msg)
        return []

    # Collect data
    try:
        rows = time_daq(daq, duration)
        counts = len(rows)
        tmp = rows["tmp"].mean()
        atm = rows["atm"].mean()
        hmd = rows["hmd"].mean()
        fname = get_savef_with_timestamp(daq, ch)
        rows.to_csv(fname, index=False)
        msg = f"Saved data to: {fname}"
        logger.info(msg)
    except Exception as e:
        msg = f"Failed to collect data due to: {str(e)}"
        logger.error(msg)
        counts = 0
        tmp = 0
        atm = 0
        hmd = 0

    # Save Summary
    now = pendulum.now().to_iso8601_string()
    data = [now, duration, ch, vth, counts, tmp, atm, hmd]
    fname = Path(daq.saved) / daq.fname_scan
    with fname.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)
    msg = f"Added data to: {fname}"
    logger.info(msg)

    return data


@deprecated(
    version="0.14.0",
    reason="Will be deprecated. Use threshold.scan_thresholds instead.",
)
def scan_ch_thresholds(daq: Daq, duration: int, ch: int, thresholds: list[int]) -> list[list]:
    """
    Run threshold scan.

    :Args:
    - daq (Daq): Daqオブジェクト
    - duration (int): 測定時間（秒）
    - ch (int): チャンネル番号
    - thresholds (list[int]): スレッショルド値のリスト

    :Returns:
    - rows (list[list]): [測定時刻、チャンネル番号、スレッショルド値、イベント数]のリスト
    """

    logger.warning("Will be deprecated. Please use threshold.scan_thresholds instead.")
    # Estimated time for scan
    msg = f"Number of points: {len(thresholds)}"
    logger.info(msg)
    estimated_time = len(thresholds) * duration
    msg = f"Estimated time: {estimated_time} sec."
    logger.info(msg)

    # すべてのチャンネルの閾値を高くする
    set_vth_retry(daq, 1, 500, 5)
    set_vth_retry(daq, 2, 500, 5)
    set_vth_retry(daq, 3, 500, 5)

    rows = []
    n = len(thresholds)
    for i, vth in enumerate(thresholds):
        msg = "-" * 40 + f"[{i+1:2d}/{n:2d}: {vth}]"
        logger.info(msg)
        row = scan_ch_vth(daq, duration, ch, vth)
        if row:
            rows.append(row)

    return rows
