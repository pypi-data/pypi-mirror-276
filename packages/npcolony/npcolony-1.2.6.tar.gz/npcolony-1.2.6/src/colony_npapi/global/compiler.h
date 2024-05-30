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

/* compiler structure */

#ifdef _MSC_VER
#define COLONY_PLATFORM_MSC true
#define COLONY_COMPILER "msvc"
#define COLONY_COMPILER_VERSION _MSC_VER
#define COLONY_COMPILER_VERSION_STRING "1.0.0"
#endif

#ifdef __GNUC__
#define COLONY_PLATFORM_GCC true
#define COLONY_COMPILER "gcc"
#define COLONY_COMPILER_VERSION (__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__)
#define COLONY_COMPILER_VERSION_STRING __VERSION__
#endif
