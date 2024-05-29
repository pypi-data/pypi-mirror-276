# -*- coding:utf-8 -*-

__all__ = [
    'local_now', 'local_today', 'local_time',
    'naive_time',
    'get_latest_neat_time', 'get_nearest_neat_time', 'get_neat_beg_end',
]

import six
from django.utils import timezone
from dt_utils import T, TD
from dt_utils import neat


def local_now():
    return timezone.now().astimezone(timezone.get_current_timezone())


def local_today():
    return local_now().date()


def local_time(raw_time):
    if raw_time is None:
        return None

    time = T(raw_time)
    if timezone.is_aware(time):
        return timezone.localtime(time)
    else:
        return timezone.make_aware(time)


def naive_time(raw_time):
    if raw_time is None:
        return None

    time = T(raw_time)
    if timezone.is_aware(time):
        # make local first, lest the result is based on a wrong timezone
        return timezone.make_naive(timezone.localtime(time))
    else:
        return time


def get_latest_neat_time(time=None, freq='1H', naive=False):
    """获取最新的一个整齐时点, 带时区版
    :param time: 不提供时, 默认从当前时间算起
    :param freq:
    :param naive: 是否返回无时区(naive)的结果
    """
    time = local_now() if time is None else local_time(time)
    result = neat.get_latest_neat_time(time=time, freq=freq)
    if naive:
        result = naive_time(result)
    return result


def get_nearest_neat_time(time=None, freq='1H', naive=False):
    """获取距离最近的一个整齐时点, 带时区版
    :param time: 不提供时, 默认从当前时间算起
    :param freq:
    :param naive: 是否返回无时区(naive)的结果
    """
    time = local_now() if time is None else local_time(time)
    result = neat.get_nearest_neat_time(time=time, freq=freq)
    if naive:
        result = naive_time(result)
    return result


def get_neat_beg_end(beg=None, end=None, freq='1H', offset=0, periods=1, naive=False):
    """获取整齐的起止时间, 带时区版
    :param beg:
    :param end:
    :param freq:
    :param offset: 将结果平移几个周期
    :param periods: 当没有提供beg时, 给出时长为几个周期的时段
    :param naive: 是否返回无时区(naive)的结果
    """
    t_delta = TD(freq)
    neat_end = get_latest_neat_time(end, freq, naive=naive)
    neat_beg = neat_end - t_delta * periods if beg is None else get_latest_neat_time(beg, freq, naive=naive)
    if offset != 0:
        neat_beg += t_delta * offset
        neat_end += t_delta * offset
    return neat_beg, neat_end
