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

#include "cpu.h"
#include "types.h"
#include "platforms.h"
#include "compiler.h"
#include "compilation.h"

/**
 * The name of the environment variable used to build
 * the COLONY path.
 */
#define HIVE_COLONY_ENVIRONMENT_PATH "COLONY_PATH"

/**
 * The root path being used.
 */
#define HIVE_COLONY_ROOT_PATH "."

#ifdef COLONY_PLATFORM_WIN32
#define COLONY_ENVIRONMENT_SEPARATOR ";"
#endif
#ifdef COLONY_PLATFORM_UNIX
#define COLONY_ENVIRONMENT_SEPARATOR ":"
#endif

#ifdef COLONY_PLATFORM_WIN32
#define COLONY_SHARED_OBJECT_EXTENSION ".dll"
#endif
#ifdef COLONY_PLATFORM_UNIX
#define COLONY_SHARED_OBJECT_EXTENSION ".so"
#endif

#ifdef COLONY_PLATFORM_WIN32
#define COLONY_SYSTEM_BASE_PATH "/"
#endif
#ifdef COLONY_PLATFORM_IPHONE
#define COLONY_SYSTEM_BASE_PATH getBundleDirectory()
#endif
#ifdef COLONY_PLATFORM_UNIX
#define COLONY_SYSTEM_BASE_PATH "/"
#endif

#ifdef COLONY_PLATFORM_WIN32
#define COLONY_MAX_PATH_SIZE 1024
#endif
#ifdef COLONY_PLATFORM_UNIX
#define COLONY_MAX_PATH_SIZE 1024
#endif
