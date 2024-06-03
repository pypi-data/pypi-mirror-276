# SPDX-FileCopyrightText: 2024-present Artur Drogunow <artur.drogunow@zf.com>
#
# SPDX-License-Identifier: MIT

# cython: language_level=3, embedsignature=True, embedsignature.format=python

from libc.math cimport sqrt
from libc.string cimport memset
from cython_xinput.xinput cimport *

from enum import IntFlag

cdef double INT16_MAX = 32767.0
cdef double UINT16_MAX = 65535.0
cdef double UINT8_MAX = 255.0

cdef struct ThumbPos:
    double x
    double y


class XinputButtons(IntFlag):
    DPAD_UP = XINPUT_GAMEPAD_DPAD_UP
    DPAD_DOWN = XINPUT_GAMEPAD_DPAD_DOWN
    DPAD_LEFT = XINPUT_GAMEPAD_DPAD_LEFT
    DPAD_RIGHT = XINPUT_GAMEPAD_DPAD_RIGHT
    START = XINPUT_GAMEPAD_START
    BACK = XINPUT_GAMEPAD_BACK
    LEFT_THUMB = XINPUT_GAMEPAD_LEFT_THUMB
    RIGHT_THUMB = XINPUT_GAMEPAD_RIGHT_THUMB
    LEFT_SHOULDER = XINPUT_GAMEPAD_LEFT_SHOULDER
    RIGHT_SHOULDER = XINPUT_GAMEPAD_RIGHT_SHOULDER
    A = XINPUT_GAMEPAD_A
    B = XINPUT_GAMEPAD_B
    X = XINPUT_GAMEPAD_X
    Y = XINPUT_GAMEPAD_Y


cdef class XinputGamepad:
    cdef DWORD               dwUserIndex
    cdef XINPUT_STATE        state
    cdef XINPUT_CAPABILITIES caps
    cdef double              leftThumbDZ
    cdef double              rightThumbDZ
    cdef double              triggerThr

    def __cinit__(self):
        memset(&self.state, 0, sizeof(self.state))
        memset(&self.caps, 0, sizeof(self.caps))
        self._configure_deadzone(
            XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE / INT16_MAX,
            XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE / INT16_MAX,
            XINPUT_GAMEPAD_TRIGGER_THRESHOLD / UINT8_MAX
        )

    def __init__(self, DWORD user_index) -> None:
        self.dwUserIndex = user_index
        cdef DWORD res = XInputGetCapabilities(user_index,
                                               XINPUT_FLAG_GAMEPAD,
                                               &self.caps)
        if res != ERROR_SUCCESS:
            raise RuntimeError("Gamepad not connected.")

        self.update()

    def update(self) -> bool:
        cdef XINPUT_STATE prevState = self.state
        cdef DWORD res

        with nogil:
            dwPacketNumberPrev = self.state.dwPacketNumber
            res = XInputGetState(self.dwUserIndex, &self.state)
            if res != ERROR_SUCCESS:
                raise RuntimeError("Gamepad not connected.")

        return dwPacketNumberPrev != self.state.dwPacketNumber

    cdef void _configure_deadzone(
            self,
            double left_thumb,
            double right_thumb,
            double trigger):
        if not 0 <= left_thumb <= 1.0:
            raise ValueError("Deadzone values must be inside [0, 1].")
        if not 0 <= right_thumb <= 1.0:
            raise ValueError("Deadzone values must be inside [0, 1].")
        if not 0 <= trigger <= 1.0:
            raise ValueError("Deadzone values must be inside [0, 1].")
        
        self.leftThumbDZ = left_thumb * INT16_MAX
        self.rightThumbDZ = right_thumb * INT16_MAX
        self.triggerThr = trigger * UINT8_MAX

    def configure_deadzone(
            self,
            double left_thumb,
            double right_thumb,
            double trigger,
        ) -> None:
        self._configure_deadzone(left_thumb, right_thumb, trigger)

    def set_vibration(self, double left, double right) -> None:
        if not 0 <= left <= 1.0:
            raise ValueError("Vibration values must be inside [0, 1].")
        if not 0 <= right <= 1.0:
            raise ValueError("Vibration values must be inside [0, 1].")

        cdef XINPUT_VIBRATION vibration = XINPUT_VIBRATION(
            <WORD>(left * UINT16_MAX),
            <WORD>(right * UINT16_MAX),
        )
        cdef DWORD res

        with nogil:
            res = XInputSetState(self.dwUserIndex, &vibration)
            if res != ERROR_SUCCESS:
                raise RuntimeError("Gamepad not connected.")

    @staticmethod
    cdef ThumbPos thumbstick_xy(SHORT Xraw, SHORT Yraw, double dz) nogil:
        cdef ThumbPos pos = ThumbPos(Xraw, Yraw)

        # determine how far the controller is pushed
        cdef double magnitude = sqrt(pos.x*pos.x + pos.y*pos.y)
        if magnitude > INT16_MAX:
            magnitude = INT16_MAX
        cdef double scaling = (magnitude - dz) / (INT16_MAX - dz)

        #check if the controller is inside of circular dead zone
        if magnitude <= dz:
            pos.x = 0.0
            pos.y = 0.0
        else:
            pos.x = pos.x * scaling / INT16_MAX
            pos.y = pos.y * scaling / INT16_MAX
        
        return pos

    def left_thumbstick(self) -> tuple[float, float]:
        cdef ThumbPos pos = XinputGamepad.thumbstick_xy(
            self.state.Gamepad.sThumbLX,
            self.state.Gamepad.sThumbLY,
            self.leftThumbDZ
        )
        return pos.x, pos.y
    
    def right_thumbstick(self) -> tuple[float, float]:
        cdef ThumbPos pos = XinputGamepad.thumbstick_xy(
            self.state.Gamepad.sThumbRX,
            self.state.Gamepad.sThumbRY,
            self.rightThumbDZ
        )
        return pos.x, pos.y

    @staticmethod
    cdef double trigger(BYTE triggerRaw, double thr) nogil:
        cdef double trigger = triggerRaw
        if trigger < thr:
            trigger = 0.0
        else:
            trigger = (trigger - thr) / (UINT8_MAX - thr)
        return trigger

    def left_trigger(self) -> float:
        return XinputGamepad.trigger(
            self.state.Gamepad.bLeftTrigger, self.triggerThr
        )

    def right_trigger(self) -> float:
        return XinputGamepad.trigger(
            self.state.Gamepad.bRightTrigger, self.triggerThr
        )

    def buttons(self) -> XinputButtons:
        return XinputButtons(self.state.Gamepad.wButtons)

    def dpad_up(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_UP)

    def dpad_down(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_DOWN)

    def dpad_left(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_LEFT)

    def dpad_right(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_RIGHT)

    def start(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_START)

    def back(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_BACK)

    def left_thumb(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_LEFT_THUMB)

    def right_thumb(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_RIGHT_THUMB)

    def left_shoulder(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_LEFT_SHOULDER)

    def right_shoulder(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_RIGHT_SHOULDER)

    def a(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_A)

    def b(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_B)

    def x(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_X)

    def y(self) -> bool:
        return bool(self.state.Gamepad.wButtons & XINPUT_GAMEPAD_Y)
