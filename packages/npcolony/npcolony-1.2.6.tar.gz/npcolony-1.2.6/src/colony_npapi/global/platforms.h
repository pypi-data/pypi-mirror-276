/*
 Hive Colony Framework
 Copyright (c) 2008-2020 Hive Solutions Lda.

 This file is part of Hive Colony Framework.

 Hive Colony Framework is free software: you can redistribute it and/or modify
 it under the terms of the Apache License as published by the Apache
 Foundation, either version 2.0 of the License, or (at your option) any
 later version.

 Hive Colony Framework is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 Apache License for more details.

 You should have received a copy of the Apache License along with
 Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

 __author__    = João Magalhães <joamag@hive.pt>
 __copyright__ = Copyright (c) 2008-2020 Hive Solutions Lda.
 __license__   = Apache License, Version 2.0
*/

#pragma once

/* platform operative system */

#if defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(__TOS_WIN__) || defined(__WINDOWS__)
#define COLONY_PLATFORM_WIN32 true
#define COLONY_PLATFORM_STRING "win32"
#endif

#if defined(linux) || defined(__linux)
#define COLONY_PLATFORM_LINUX true
#define COLONY_PLATFORM_STRING "linux"
#endif

#if defined(__APPLE__) && defined(__MACH__)
#if TARGET_OS_IPHONE
#define COLONY_PLATFORM_IPHONE true
#else
#define COLONY_PLATFORM_MACOSX true
#endif
#define COLONY_PLATFORM_STRING "darwin"
#endif

#if defined(__minix)
#define COLONY_PLATFORM_MINIX true
#define COLONY_PLATFORM_STRING "minix"
#endif

#if defined(__FreeBSD__)
#define COLONY_PLATFORM_FREEBSD true
#define COLONY_PLATFORM_STRING "freebsd"
#endif

#if defined(__CYGWIN__)
#define COLONY_PLATFORM_CYGWIN true
#define COLONY_PLATFORM_STRING "cygwin"
#endif

#if defined(__ANDROID__ ) || defined(ANDROID)
#define COLONY_PLATFORM_ANDROID true
#endif

/* platform api system */

#ifdef unix
#define COLONY_PLATFORM_UNIX true
#endif

#ifdef __MINGW32__
#define COLONY_PLATFORM_MINGW true
#endif

/* platform api level */

#ifdef _WIN32
#define COLONY_PLATFORM_WINDOWS_API_BITS 32
#endif

#ifdef _WIN64
#define COLONY_PLATFORM_WINDOWS_API_BITS 64
#endif

#ifndef COLONY_PLATFORM_STRING
#define COLONY_PLATFORM_STRING "unknown"
#endif
