/* Copyright (c) 2013-2016. The SimGrid Team.
 * All rights reserved.                                                     */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_HOST_H_
#define SIMGRID_HOST_H_

#include <stddef.h>

#include <xbt/dict.h>
#include <xbt/dynar.h>

#include <simgrid/forward.h>

SG_BEGIN_DECL()

XBT_PUBLIC(void) sg_host_exit();

XBT_PUBLIC(size_t) sg_host_count();
XBT_PUBLIC(sg_host_t *) sg_host_list();

XBT_PUBLIC(size_t) sg_host_extension_create(void(*deleter)(void*));
XBT_PUBLIC(void*) sg_host_extension_get(sg_host_t host, size_t rank);
XBT_PUBLIC(sg_host_t) sg_host_by_name(const char *name);
XBT_PUBLIC(const char*) sg_host_get_name(sg_host_t host);
XBT_PUBLIC(xbt_dynar_t) sg_hosts_as_dynar();

// ========== User Data ==============
XBT_PUBLIC(void*) sg_host_user(sg_host_t host);
XBT_PUBLIC(void) sg_host_user_set(sg_host_t host, void* userdata);
XBT_PUBLIC(void) sg_host_user_destroy(sg_host_t host);

// ========= storage related functions ============
XBT_PUBLIC(xbt_dict_t) sg_host_get_mounted_storage_list(sg_host_t host);
XBT_PUBLIC(xbt_dynar_t) sg_host_get_attached_storage_list(sg_host_t host);
// =========== user-level functions ===============
XBT_PUBLIC(double) sg_host_speed(sg_host_t host);
XBT_PUBLIC(double) sg_host_get_available_speed(sg_host_t host);

XBT_PUBLIC(sg_host_t) sg_host_self();
XBT_PUBLIC(const char*) sg_host_self_get_name();
XBT_PUBLIC(int) sg_host_get_nb_pstates(sg_host_t host);
XBT_PUBLIC(int) sg_host_get_pstate(sg_host_t host);
XBT_PUBLIC(void) sg_host_set_pstate(sg_host_t host,int pstate);
XBT_PUBLIC(xbt_dict_t) sg_host_get_properties(sg_host_t host);
XBT_PUBLIC(const char*) sg_host_get_property_value(sg_host_t host, const char* name);
XBT_PUBLIC(void) sg_host_set_property_value(sg_host_t host, const char* name, const char* value);
XBT_PUBLIC(void) sg_host_route(sg_host_t from, sg_host_t to, xbt_dynar_t links);
XBT_PUBLIC(double) sg_host_route_latency(sg_host_t from, sg_host_t to);
XBT_PUBLIC(double) sg_host_route_bandwidth(sg_host_t from, sg_host_t to);
XBT_PUBLIC(void) sg_host_dump(sg_host_t ws);
SG_END_DECL()

#endif /* SIMGRID_HOST_H_ */
