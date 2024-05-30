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

#include "../print/print.h"
#include "../system/system.h"
#include "../encoding/encoding.h"
#include "util.h"

/**
 * The number of methods (smbols) to be exposed
 * by the gateway to the javascript interface.
 */
#define METHODS_COUNT 8

COLONY_EXPORT_PREFIX bool invoke_default(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke_status(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke_version(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke_callback(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke_alert(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke_pformat(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke_print(NPObject *obj, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool invoke(NPObject* obj, NPIdentifier method_name, const NPVariant *args, uint32_t arg_count, NPVariant *result);
COLONY_EXPORT_PREFIX bool has_method(NPObject* obj, NPIdentifier method_name);
COLONY_EXPORT_PREFIX bool has_property(NPObject *obj, NPIdentifier property_name);
COLONY_EXPORT_PREFIX bool get_property(NPObject *obj, NPIdentifier property_name, NPVariant *result);

NPError nevv(NPMIMEType plugin_type, NPP instance, uint16_t mode, int16_t argc, char *argn[], char *argv[], NPSavedData *saved);
NPError destroy(NPP instance, NPSavedData **save);
NPError get_value(NPP instance, NPPVariable variable, void *value);
NPError set_value(NPP instance, NPNVariable variable, void *value);
NPError handle_event(NPP instance, void *ev);
NPError set_window(NPP instance, NPWindow *window);
NPError new_stream(NPP instance, NPMIMEType type, NPStream *stream, NPBool seekable, uint16_t *stype);
NPError destroy_stream(NPP instance, NPStream *stream, NPReason reason);
int32_t write_ready(NPP instance, NPStream *stream);
int32_t nwrite(NPP instance, NPStream *stream, int32_t offset, int32_t len, void *buffer);
void as_file(NPP instance, NPStream *stream, const char *fname);
void nprint(NPP instance, NPPrint *platform_print);
void nurl_notify(NPP instance, const char *url, NPReason reason, void *notify_data);

static NPClass ref_object = {
    NP_CLASS_STRUCT_VERSION,
    NULL,
    NULL,
    NULL,
    has_method,
    invoke,
    invoke_default,
    has_property,
    get_property,
    NULL,
    NULL,
};

static char *methods[METHODS_COUNT] = {
    "status",
    "version",
    "foo",
    "callback",
    "alert",
    "pformat",
    "pdevices",
    "print"
};
