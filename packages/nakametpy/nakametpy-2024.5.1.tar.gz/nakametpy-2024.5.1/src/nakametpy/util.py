# Copyright (c) 2021-2024, NakaMetPy Develoers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Function load_jmara_grib2 is based on Qiita article
# URL: https://qiita.com/vpcf/items/b680f504cfe8b6a64222
#

import struct
import tarfile
import gzip
import numpy as np
from itertools import repeat
from ._error import NotHaveSetArgError, NotMatchTarContentNameError, NotSupportedExtentionError
import glob
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
# logging.disable(logging.CRITICAL)

def _set_table(section5):
  max_level = struct.unpack_from('>H', section5, 15)[0]
  table = (
    -10, # define representative of level 0　(Missing Value)
    *struct.unpack_from('>'+str(max_level)+'H', section5, 18)
  )
  return np.array(table, dtype=np.int16)

def _decode_runlength(code, hi_level):
  for raw in code:
    if raw <= hi_level:
      level = raw
      pwr = 0
      yield level
    else:
      length = (0xFF - hi_level)**pwr * (raw - (hi_level + 1))
      pwr += 1
      yield from repeat(level, length)

def _get_binary(file, tar_flag=False, tar_contentname=None):
  _ext1 = file.split(sep=".")[-1]
  logging.debug(f"_ext = {_ext1}")
  if tar_flag:
    _found_flag = False
    if tar_contentname == None:
      raise NotHaveSetArgError("tar_flag", "tar_contentname")
    if _ext1.lower() == "tar":
      with tarfile.open(file, mode="r") as tar:
        for tarinfo in tar.getmembers():
          logging.debug(f"tarinfo.name = {tarinfo.name}")
          if tarinfo.name == tar_contentname:
            binary = b''.join(tar.extractfile(tarinfo).readlines())
            _found_flag = True
            break
    if _found_flag == False:
      raise NotMatchTarContentNameError(file, tar_contentname)
  elif (_ext1.lower() == "gz") or (_ext1.lower() == "gzip"):
    with gzip.open(file, mode="rb") as gz:
      binary = gz.read()
  elif _ext1.lower() == "bin":
    with open(file, 'rb') as f:
      binary = f.read()
  else:
    raise NotSupportedExtentionError(_ext1, "bin, tar, gz, gzip")
  return binary

def load_jmara_grib2(file, tar_flag=False, tar_contentname=None):
  r'''気象庁解析雨量やレーダー雨量を返す関数

  欠損値は負の値として表現される。
  ファイルはgrib2, tar, gz(gzip)を受け付ける

  Parameters
  --------
  file: `str`
    file path 
    ファイルのPATH
  tar_flag: `bool`
    file type are GRIB2, tar and gz(gzip).
  tar_contentname: `str`
    content name in tar file.

  Returns
  -------
  rain: `numpy.ma.MaskedArray`
    Units(単位) [mm/h]

  Note
  -----
  ``jma_rain_lat`` , ``jma_rain_lon`` はそれぞれ返り値に対応する
  `np.ndarray` 型の緯度経度である。
  '''
  binary = _get_binary(file=file, tar_flag=tar_flag, tar_contentname=tar_contentname)
  
  # The Sector 0, 1, 3, 4, 6 are fixed.
  len_ = {'sec0':16, 'sec1':21, 'sec3':72, 'sec4':82, 'sec6':6}
  end1 = len_['sec0'] + len_['sec1'] - 1
  # +31 is octet of grid numbers align latitude line.
  nlon = struct.unpack_from('>I', binary, end1+31)[0]
  nlat = struct.unpack_from('>I', binary, end1+35)[0]
  logging.debug(f"nlon = {nlon}")
  logging.debug(f"nlat = {nlat}")
  
  end4 = len_['sec0'] + len_['sec1'] + len_['sec3'] + len_['sec4'] - 1
  # +1 is octet
  len_['sec5'] = struct.unpack_from('>I', binary, end4+1)[0]
  section5 = binary[end4:(end4+len_['sec5']+1)]
  power = section5[17]
  logging.debug(f"power = {power}")
  
  end6 = end4 + len_['sec5'] + len_['sec6']
  # +1 is octet
  len_['sec7'] = struct.unpack_from('>I', binary, end6+1)[0]
  section7 = binary[end6:(end6+len_['sec7']+1)]
  
  highest_level = struct.unpack_from('>H', section5, 13)[0]
  level_table = _set_table(section5)
  decoded = np.fromiter(
    _decode_runlength(section7[6:], highest_level), dtype=np.int16
  )
  decoded=decoded.reshape((nlat, nlon))
  
  # convert level to representative
  return np.ma.masked_less((level_table[decoded]/(10**power))[::-1, :], 0)

def get_jmara_lat():
  r'''解析雨量の緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`
  '''
  return np.linspace(48, 20, 3360, endpoint=False)[::-1] - 1/80/1.5 / 2
    

def get_jmara_lon():
  r'''解析雨量の経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  '''
  return np.linspace(118, 150, 2560, endpoint=False) + 1/80 / 2

def get_jmarlev_lat():
  r'''レーダーエコー頂高度の緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`
  '''
  return np.linspace(48, 20, 1120, endpoint=False)[::-1] - 1/80/1.5 / 2
    

def get_jmarlev_lon():
  r'''レーダーエコー頂高度の経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  '''
  return np.linspace(118, 150, 1024, endpoint=False) + 1/80 / 2

def get_grib2_latlon(file, tar_flag=False, tar_contentname=None):
  r'''気象庁解析雨量やレーダー雨量の緯度経度を返す関数

  欠損値は負の値として表現される。
  ファイルはgrib2, tar, gz(gzip)を受け付ける

  Parameters
  --------
  file: `str`
    file path 
    ファイルのPATH
  tar_flag: `bool`
    file type are GRIB2, tar and gz(gzip).
  tar_contentname: `str`
    content name in tar file.

  Returns
  -------
  latlon: set(`numpy.ma.MaskedArray`, `numpy.ma.MaskedArray`)
    (Latitude, Longitude)
  '''
  
  binary = _get_binary(file=file, tar_flag=tar_flag, tar_contentname=tar_contentname)
  
  # The Sector 0, 1, 3, 4, 6 are fixed.
  len_ = {'sec0':16, 'sec1':21, 'sec3':72, 'sec4':82, 'sec6':6}
  end1 = len_['sec0'] + len_['sec1'] - 1
  # +31 is octet of grid numbers align latitude line.
  nlon = struct.unpack_from('>I', binary, end1+31)[0]
  nlat = struct.unpack_from('>I', binary, end1+35)[0]
  slat = struct.unpack_from('>I', binary, end1+47)[0]
  slon = struct.unpack_from('>I', binary, end1+51)[0]
  elat = struct.unpack_from('>I', binary, end1+56)[0]
  elon = struct.unpack_from('>I', binary, end1+60)[0]
  logging.debug(f"nlon = {nlon}")
  logging.debug(f"nlat = {nlat}")
  logging.debug(f"slat = {slat}")
  logging.debug(f"slon = {slon}")
  logging.debug(f"elat = {elat}")
  logging.debug(f"elon = {elon}")
  return (np.linspace(slat, elat, nlat)[::-1]/1E6, np.linspace(slon, elon, nlon)/1E6)

def get_gsmap_lat():
  r'''GSMaPの緯度を返す関数

  Returns
  -------
  lat: `numpy.ndarray`
  '''
  return np.arange(-60, 60, 0.1)[::-1] + 0.05
    

def get_gsmap_lon():
  r'''GSMaPの経度を返す関数

  Returns
  -------
  lon: `numpy.ndarray`
  '''
  return np.arange(0, 360, 0.1) + 0.05


def dt_ymdhm(date, opt=1):
  r'''
  datetime.datetime から year, month, day, hour, minute の set を返す関数。
  opt = 1 : string, 0 : int

  Return the set of year, month, day, hour, minute from datetime.datetime.

  Parameters
  ----------
  date: `datetime.datetime`
    datetime
  opt: `int`
    return string or not
  
  Returns
  -------
  `set`
    (year, month, day, hour, minute)
  '''
  if opt == 0:
    return (date.year, date.month, date.day, date.hour, date.minute)
  elif opt == 1:
    return (f"{date.year}", f"{date.month:02}", f"{date.day:02}", f"{date.hour:02}", f"{date.minute:02}")


def dt_yyyymmdd(date, fmt="yyyymmdd"):
  r'''
  datetime.datetime を yyyymmdd 形式の文字列で返す関数。

  Return yyyymmdd format string from datetime.

  Parameters
  ----------
  date: `datetime.datetime`
    datetime
  fmt: `str`
    yyyymmdd format. Default is yyyymmdd
  
  Returns
  -------
  `str`
    string in fmt.
  '''
  for iymd, ifmt in (("yyyy", "%Y"), ("mm", "%m"), ("dd", "%d"), ("HH", "%H"), ("MM", "%M"), ("SS", "%S"), ("yy", "%y")):
    while True:
      if iymd in fmt:
        fmt = fmt.replace(iymd, ifmt)
      else:
        break
  return date.strftime(fmt)


jma_rain_lat = np.linspace(48, 20, 3360, endpoint=False)[::-1] - 1/80/1.5 / 2
jma_rain_lon = np.linspace(118, 150, 2560, endpoint=False) + 1/80 / 2

gsmap_lat = np.arange(-60, 60, 0.1)[::-1] + 0.05
gsmap_lon = np.arange(0, 360, 0.1) + 0.05

def unit_ms1_knots(ms):
  r"""
  Convert unit m/s into knots.
  
  Parameters
  ----------
  ms: `int`
    Velocity in meter per second.
  
  Returns
  -------
  `kt`
    Velocity in knots.
  """
  return ms*3600/1852

def unit_knots_ms1(kt):
  r"""
  Convert unit knots into m/s.
  
  Parameters
  ----------
  kt: `int`
    Velocity in knots.
  
  Returns
  -------
  `ms`
    Velocity in meter per second.
  """
  return kt*1852/3600

def anom_levels(levs):
  r"""
  Return minus ans plus levels.

  Parameters
  ----------
  levs: `list`or`np.ndarray`

  Returns
  -------
  anom levels: `np.ndarray`
  
  Examples  
  --------
      >>> levs = [0.5, 1., 2.]
      >>> print(anom_levels(levs))
      [-2.  -1.  -0.5  0.5  1.   2. ]
  
  
  """
  levs = list(set(np.abs(levs)))
  levs.sort()
  return np.array([-i for i in levs[::-1]]+levs)

def check_tar_content(file):
  r'''tar ファイルの中身のファイル名を表示する関数

  Print the content name of the tar file.

  Parameters
  --------
  file: `str`
    file path 
    ファイルのPATH
  '''
  with tarfile.open(file, mode="r") as tar:
    for tarinfo in tar.getmembers():
      print(tarinfo.name)

def concat_array(*arr, sort=True):
  r"""
  Return concatenated array in numpy.ndarray.

  Parameters
  ----------
  arr: some of `list`or`np.ndarray`

  Returns
  -------
  concat_ndarray: `np.ndarray`
  
  Examples  
  --------
      >>> levs = concat_array(np.arange(0.5, 2., 0.5), np.arange(2., 5.1, 1.))
      >>> print(levs)
      [0.5  1.   1.5  2.   2.5  3.   3.5  4.   4.5  5. ]

  """
  _list = []
  for _irr in arr:
    _list.extend(list(np.array(_irr)))
  if sort:
    _list = sorted(list(set(_list)))
  return np.array(_list)

def myglob(path, reverse=False):
    r"""
    Return sorted glob results.
    Parameters
    ----------
    path: `str`
    
    reverse: `bool`

    Returns
    -------
    result_list: `list`
    """
    return sorted(glob.glob(path), reverse=reverse)
