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

#ifdef COLONY_PLATFORM_UNIX

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Structure that describes a (printing) job
 * to be processed in the NPAPI context.
 */
typedef struct job_t {
    char *output_path;
    size_t urgency;
} job;

/**
 * Structure that defines and identifies a
 * printing device in a neutral manner.
 *
 * Should contain information that can
 * promote the re-usage of a device for its
 * internal/external operations.
 */
typedef struct device_t {
    char name[256];
    size_t name_s;
    char is_default;
    char media[256];
    size_t media_s;
    float width;
    float length;
} device;

/**
 * Retrieves the format of the data file (buffer) to be used in
 * the printing operation for the current operative system.
 *
 * This format should be used in conformance with the previously
 * defined specification.
 *
 * @return The format of the data file to be used in the printing
 * for the current operative system infra-structure.
 */
COLONY_EXPORT_PREFIX const char *pformat();

/**
 * Retrieves the complete set of printing devices currently
 * available in the system loaded in the appropriate structures.
 *
 * The number of devices available is also returned, so that's
 * it's possible to iterate over the sequence.
 *
 * @param devices_p The pointer to the buffer of device structures
 * to be set with the various elements.
 * @param devices_c The number of devices loaded into the devices
 * pointer (loaded devices).
 */
COLONY_EXPORT_PREFIX void pdevices(struct device_t **devices_p, size_t *devices_c);

/**
 * Prints a document using the default printer or in case the show
 * dialog option is set using the printer selected in the printing
 * dialog.
 *
 * The provided data buffer must be encoded using the pdf binary
 * file specification that specifies a series of basic printing
 * primitive routines.
 *
 * @param show_dialog If the printing dialog should be displayed for
 * printer selection.
 * @param config The job configuration for the print operation.
 * @param data The data buffer encoded in pdf format describing
 * the document to be printed.
 * @param size The size of the buffer of encoded data that was
 * passed as an argument.
 * @return The result of the printing process, if successful, a value
 * greater than zero should be returned.
 */
COLONY_EXPORT_PREFIX int print(
    bool show_dialog,
    struct job_t *config,
    char *data,
    size_t size
);

/**
 * Prints a document using the provided printer or in case the show
 * dialog option is set using the printer selected in the printing
 * dialog.
 *
 * The provided data buffer must be encoded using the pdf binary
 * file specification that specifies a series of basic printing
 * primitive routines.
 *
 * @param show_dialog If the printing dialog should be displayed for
 * printer selection.
 * @param printer The printer's name is to be used in the print
 * operation (only used in case the show dialog is not set).
 * @param config The job configuration for the print operation.
 * @param data The data buffer encoded in pdf format describing
 * the document to be printed.
 * @param size The size of the buffer of encoded data that was
 * passed as an argument.
 * @return The result of the printing process, if successful, a value
 * greater than zero should be returned.
 */
COLONY_EXPORT_PREFIX int print_printer(
    bool show_dialog,
    char *printer,
    struct job_t *config,
    char *data,
    size_t size
);

#ifdef __cplusplus
}
#endif

#endif
