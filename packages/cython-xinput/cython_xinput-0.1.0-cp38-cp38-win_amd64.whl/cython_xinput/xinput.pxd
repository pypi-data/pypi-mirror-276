# SPDX-FileCopyrightText: 2024-present Artur Drogunow <artur.drogunow@zf.com>
#
# SPDX-License-Identifier: MIT

# cython: language_level=3

cdef int one()

cdef extern from "Windows.h":
    ctypedef unsigned char         BYTE
    ctypedef unsigned long         DWORD
    ctypedef short                 SHORT
    ctypedef unsigned short        WORD

cdef extern from "Xinput.h":
    cdef DWORD                     ERROR_SUCCESS
    cdef DWORD                     ERROR_DEVICE_NOT_CONNECTED

    cdef const int                 XUSER_MAX_COUNT 

    cdef const int                 XINPUT_FLAG_GAMEPAD

    cdef const int                 BATTERY_DEVTYPE_GAMEPAD
    cdef const int                 BATTERY_DEVTYPE_HEADSET

    cdef const int                 XINPUT_DEVTYPE_GAMEPAD

    cdef const int                 XINPUT_CAPS_VOICE_SUPPORTED
    cdef const int                 XINPUT_CAPS_FFB_SUPPORTED
    cdef const int                 XINPUT_CAPS_WIRELESS
    cdef const int                 XINPUT_CAPS_PMD_SUPPORTED
    cdef const int                 XINPUT_CAPS_NO_NAVIGATION

    cdef const int                 XINPUT_GAMEPAD_DPAD_UP
    cdef const int                 XINPUT_GAMEPAD_DPAD_DOWN
    cdef const int                 XINPUT_GAMEPAD_DPAD_LEFT
    cdef const int                 XINPUT_GAMEPAD_DPAD_RIGHT
    cdef const int                 XINPUT_GAMEPAD_START
    cdef const int                 XINPUT_GAMEPAD_BACK
    cdef const int                 XINPUT_GAMEPAD_LEFT_THUMB
    cdef const int                 XINPUT_GAMEPAD_RIGHT_THUMB
    cdef const int                 XINPUT_GAMEPAD_LEFT_SHOULDER
    cdef const int                 XINPUT_GAMEPAD_RIGHT_SHOULDER
    cdef const int                 XINPUT_GAMEPAD_A
    cdef const int                 XINPUT_GAMEPAD_B
    cdef const int                 XINPUT_GAMEPAD_X
    cdef const int                 XINPUT_GAMEPAD_Y

    cdef const int                 XINPUT_GAMEPAD_LEFT_THUMB_DEADZONE
    cdef const int                 XINPUT_GAMEPAD_RIGHT_THUMB_DEADZONE
    cdef const int                 XINPUT_GAMEPAD_TRIGGER_THRESHOLD

    ctypedef struct XINPUT_GAMEPAD:
        WORD                       wButtons
        BYTE                       bLeftTrigger
        BYTE                       bRightTrigger
        SHORT                      sThumbLX
        SHORT                      sThumbLY
        SHORT                      sThumbRX
        SHORT                      sThumbRY
    
    ctypedef struct XINPUT_STATE:
        DWORD                      dwPacketNumber
        XINPUT_GAMEPAD             Gamepad
    
    ctypedef struct XINPUT_VIBRATION:
        WORD                       wLeftMotorSpeed
        WORD                       wRightMotorSpeed

    ctypedef struct XINPUT_BATTERY_INFORMATION:
        BYTE                       BatteryType
        BYTE                       BatteryLevel

    ctypedef struct XINPUT_CAPABILITIES:
        BYTE                       Type
        BYTE                       SubType
        WORD                       Flags
        XINPUT_GAMEPAD             Gamepad
        XINPUT_VIBRATION           Vibration

    DWORD XInputGetState(
        DWORD                      dwUserIndex,
        XINPUT_STATE               *pState
    ) nogil

    DWORD XInputGetCapabilities(
        DWORD                      dwUserIndex,
        DWORD                      dwFlags,
        XINPUT_CAPABILITIES        *pCapabilities
    ) nogil

    DWORD XInputSetState(
        DWORD                      dwUserIndex,
        XINPUT_VIBRATION           *pVibration
    ) nogil

    DWORD XInputGetBatteryInformation(
        DWORD                      dwUserIndex,
        BYTE                       devType,
        XINPUT_BATTERY_INFORMATION *pBatteryInformation
    ) nogil

