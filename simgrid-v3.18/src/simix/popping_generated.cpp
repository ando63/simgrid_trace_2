/**********************************************************************/
/* File generated by src/simix/simcalls.py from src/simix/simcalls.in */
/*                                                                    */
/*                    DO NOT EVER CHANGE THIS FILE                    */
/*                                                                    */
/* change simcalls specification in src/simix/simcalls.in             */
/* Copyright (c) 2014-2017. The SimGrid Team. All rights reserved.    */
/**********************************************************************/

/*
 * Note that the name comes from http://en.wikipedia.org/wiki/Popping
 * Indeed, the control flow is doing a strange dance in there.
 *
 * That's not about http://en.wikipedia.org/wiki/Poop, despite the odor :)
 */

#include "smx_private.hpp"
#include <xbt/base.h>
#if SIMGRID_HAVE_MC
#include "src/mc/mc_forward.hpp"
#endif

XBT_LOG_EXTERNAL_DEFAULT_CATEGORY(simix_popping);

/** @brief Simcalls' names (generated from src/simix/simcalls.in) */
const char* simcall_names[] = {
    "SIMCALL_NONE",
    "SIMCALL_PROCESS_KILLALL",
    "SIMCALL_PROCESS_CLEANUP",
    "SIMCALL_PROCESS_SUSPEND",
    "SIMCALL_PROCESS_JOIN",
    "SIMCALL_PROCESS_SLEEP",
    "SIMCALL_EXECUTION_START",
    "SIMCALL_EXECUTION_PARALLEL_START",
    "SIMCALL_EXECUTION_WAIT",
    "SIMCALL_EXECUTION_TEST",
    "SIMCALL_PROCESS_ON_EXIT",
    "SIMCALL_COMM_IPROBE",
    "SIMCALL_COMM_SEND",
    "SIMCALL_COMM_ISEND",
    "SIMCALL_COMM_RECV",
    "SIMCALL_COMM_IRECV",
    "SIMCALL_COMM_WAITANY",
    "SIMCALL_COMM_WAIT",
    "SIMCALL_COMM_TEST",
    "SIMCALL_COMM_TESTANY",
    "SIMCALL_MUTEX_LOCK",
    "SIMCALL_MUTEX_TRYLOCK",
    "SIMCALL_MUTEX_UNLOCK",
    "SIMCALL_COND_INIT",
    "SIMCALL_COND_SIGNAL",
    "SIMCALL_COND_WAIT",
    "SIMCALL_COND_WAIT_TIMEOUT",
    "SIMCALL_COND_BROADCAST",
    "SIMCALL_SEM_ACQUIRE",
    "SIMCALL_SEM_ACQUIRE_TIMEOUT",
    "SIMCALL_STORAGE_READ",
    "SIMCALL_STORAGE_WRITE",
    "SIMCALL_MC_RANDOM",
    "SIMCALL_SET_CATEGORY",
    "SIMCALL_RUN_KERNEL",
    "SIMCALL_RUN_BLOCKING",
};

/** @private
 * @brief (in kernel mode) unpack the simcall and activate the handler
 *
 * This function is generated from src/simix/simcalls.in
 */
void SIMIX_simcall_handle(smx_simcall_t simcall, int value) {
  XBT_DEBUG("Handling simcall %p: %s", simcall, SIMIX_simcall_name(simcall->call));
  SIMCALL_SET_MC_VALUE(simcall, value);
  if (simcall->issuer->context->iwannadie && simcall->call != SIMCALL_PROCESS_CLEANUP)
    return;
  switch (simcall->call) {
case SIMCALL_PROCESS_KILLALL:
  simcall_HANDLER_process_killall(simcall, simgrid::simix::unmarshal<int>(simcall->args[0]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_PROCESS_CLEANUP:
  SIMIX_process_cleanup(simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_PROCESS_SUSPEND:
  simcall_HANDLER_process_suspend(simcall, simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]));
  break;

case SIMCALL_PROCESS_JOIN:
  simcall_HANDLER_process_join(simcall, simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]), simgrid::simix::unmarshal<double>(simcall->args[1]));
  break;

case SIMCALL_PROCESS_SLEEP:
  simcall_HANDLER_process_sleep(simcall, simgrid::simix::unmarshal<double>(simcall->args[0]));
  break;

case SIMCALL_EXECUTION_START:
  simgrid::simix::marshal<boost::intrusive_ptr<simgrid::kernel::activity::ExecImpl>>(
      simcall->result, SIMIX_execution_start(simgrid::simix::unmarshal<const char*>(simcall->args[0]),
                                             simgrid::simix::unmarshal<double>(simcall->args[1]),
                                             simgrid::simix::unmarshal<double>(simcall->args[2]),
                                             simgrid::simix::unmarshal<double>(simcall->args[3]),
                                             simgrid::simix::unmarshal<sg_host_t>(simcall->args[4])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_EXECUTION_PARALLEL_START:
  simgrid::simix::marshal<boost::intrusive_ptr<simgrid::kernel::activity::ExecImpl>>(simcall->result, SIMIX_execution_parallel_start(simgrid::simix::unmarshal<const char*>(simcall->args[0]), simgrid::simix::unmarshal<int>(simcall->args[1]), simgrid::simix::unmarshal<sg_host_t*>(simcall->args[2]), simgrid::simix::unmarshal<double*>(simcall->args[3]), simgrid::simix::unmarshal<double*>(simcall->args[4]), simgrid::simix::unmarshal<double>(simcall->args[5]), simgrid::simix::unmarshal<double>(simcall->args[6])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_EXECUTION_WAIT:
  simcall_HANDLER_execution_wait(simcall, simgrid::simix::unmarshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->args[0]));
  break;

case SIMCALL_EXECUTION_TEST:
  simcall_HANDLER_execution_test(
      simcall,
      simgrid::simix::unmarshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->args[0]));
  break;

case SIMCALL_PROCESS_ON_EXIT:
  SIMIX_process_on_exit(simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]), simgrid::simix::unmarshal<int_f_pvoid_pvoid_t>(simcall->args[1]), simgrid::simix::unmarshal<void*>(simcall->args[2]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COMM_IPROBE:
  simgrid::simix::marshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->result, simcall_HANDLER_comm_iprobe(simcall, simgrid::simix::unmarshal<smx_mailbox_t>(simcall->args[0]), simgrid::simix::unmarshal<int>(simcall->args[1]), simgrid::simix::unmarshal<simix_match_func_t>(simcall->args[2]), simgrid::simix::unmarshal<void*>(simcall->args[3])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COMM_SEND:
  simcall_HANDLER_comm_send(simcall, simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]), simgrid::simix::unmarshal<smx_mailbox_t>(simcall->args[1]), simgrid::simix::unmarshal<double>(simcall->args[2]), simgrid::simix::unmarshal<double>(simcall->args[3]), simgrid::simix::unmarshal<void*>(simcall->args[4]), simgrid::simix::unmarshal<size_t>(simcall->args[5]), simgrid::simix::unmarshal<simix_match_func_t>(simcall->args[6]), simgrid::simix::unmarshal<simix_copy_data_func_t>(simcall->args[7]), simgrid::simix::unmarshal<void*>(simcall->args[8]), simgrid::simix::unmarshal<double>(simcall->args[9]));
  break;

case SIMCALL_COMM_ISEND:
  simgrid::simix::marshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->result, simcall_HANDLER_comm_isend(simcall, simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]), simgrid::simix::unmarshal<smx_mailbox_t>(simcall->args[1]), simgrid::simix::unmarshal<double>(simcall->args[2]), simgrid::simix::unmarshal<double>(simcall->args[3]), simgrid::simix::unmarshal<void*>(simcall->args[4]), simgrid::simix::unmarshal<size_t>(simcall->args[5]), simgrid::simix::unmarshal<simix_match_func_t>(simcall->args[6]), simgrid::simix::unmarshal<simix_clean_func_t>(simcall->args[7]), simgrid::simix::unmarshal<simix_copy_data_func_t>(simcall->args[8]), simgrid::simix::unmarshal<void*>(simcall->args[9]), simgrid::simix::unmarshal<int>(simcall->args[10])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COMM_RECV:
  simcall_HANDLER_comm_recv(simcall, simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]), simgrid::simix::unmarshal<smx_mailbox_t>(simcall->args[1]), simgrid::simix::unmarshal<void*>(simcall->args[2]), simgrid::simix::unmarshal<size_t*>(simcall->args[3]), simgrid::simix::unmarshal<simix_match_func_t>(simcall->args[4]), simgrid::simix::unmarshal<simix_copy_data_func_t>(simcall->args[5]), simgrid::simix::unmarshal<void*>(simcall->args[6]), simgrid::simix::unmarshal<double>(simcall->args[7]), simgrid::simix::unmarshal<double>(simcall->args[8]));
  break;

case SIMCALL_COMM_IRECV:
  simgrid::simix::marshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->result, simcall_HANDLER_comm_irecv(simcall, simgrid::simix::unmarshal<smx_actor_t>(simcall->args[0]), simgrid::simix::unmarshal<smx_mailbox_t>(simcall->args[1]), simgrid::simix::unmarshal<void*>(simcall->args[2]), simgrid::simix::unmarshal<size_t*>(simcall->args[3]), simgrid::simix::unmarshal<simix_match_func_t>(simcall->args[4]), simgrid::simix::unmarshal<simix_copy_data_func_t>(simcall->args[5]), simgrid::simix::unmarshal<void*>(simcall->args[6]), simgrid::simix::unmarshal<double>(simcall->args[7])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COMM_WAITANY:
  simcall_HANDLER_comm_waitany(simcall, simgrid::simix::unmarshal<xbt_dynar_t>(simcall->args[0]), simgrid::simix::unmarshal<double>(simcall->args[1]));
  break;

case SIMCALL_COMM_WAIT:
  simcall_HANDLER_comm_wait(simcall, simgrid::simix::unmarshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->args[0]), simgrid::simix::unmarshal<double>(simcall->args[1]));
  break;

case SIMCALL_COMM_TEST:
  simcall_HANDLER_comm_test(simcall, simgrid::simix::unmarshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->args[0]));
  break;

case SIMCALL_COMM_TESTANY:
  simcall_HANDLER_comm_testany(simcall, simgrid::simix::unmarshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>*>(simcall->args[0]), simgrid::simix::unmarshal<size_t>(simcall->args[1]));
  break;

case SIMCALL_MUTEX_LOCK:
  simcall_HANDLER_mutex_lock(simcall, simgrid::simix::unmarshal<smx_mutex_t>(simcall->args[0]));
  break;

case SIMCALL_MUTEX_TRYLOCK:
  simgrid::simix::marshal<int>(simcall->result, simcall_HANDLER_mutex_trylock(simcall, simgrid::simix::unmarshal<smx_mutex_t>(simcall->args[0])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_MUTEX_UNLOCK:
  simcall_HANDLER_mutex_unlock(simcall, simgrid::simix::unmarshal<smx_mutex_t>(simcall->args[0]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COND_INIT:
  simgrid::simix::marshal<smx_cond_t>(simcall->result, SIMIX_cond_init());
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COND_SIGNAL:
  SIMIX_cond_signal(simgrid::simix::unmarshal<smx_cond_t>(simcall->args[0]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_COND_WAIT:
  simcall_HANDLER_cond_wait(simcall, simgrid::simix::unmarshal<smx_cond_t>(simcall->args[0]), simgrid::simix::unmarshal<smx_mutex_t>(simcall->args[1]));
  break;

case SIMCALL_COND_WAIT_TIMEOUT:
  simcall_HANDLER_cond_wait_timeout(simcall, simgrid::simix::unmarshal<smx_cond_t>(simcall->args[0]), simgrid::simix::unmarshal<smx_mutex_t>(simcall->args[1]), simgrid::simix::unmarshal<double>(simcall->args[2]));
  break;

case SIMCALL_COND_BROADCAST:
  SIMIX_cond_broadcast(simgrid::simix::unmarshal<smx_cond_t>(simcall->args[0]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_SEM_ACQUIRE:
  simcall_HANDLER_sem_acquire(simcall, simgrid::simix::unmarshal<smx_sem_t>(simcall->args[0]));
  break;

case SIMCALL_SEM_ACQUIRE_TIMEOUT:
  simcall_HANDLER_sem_acquire_timeout(simcall, simgrid::simix::unmarshal<smx_sem_t>(simcall->args[0]), simgrid::simix::unmarshal<double>(simcall->args[1]));
  break;

case SIMCALL_STORAGE_READ:
  simcall_HANDLER_storage_read(simcall, simgrid::simix::unmarshal<surf_storage_t>(simcall->args[0]),
                               simgrid::simix::unmarshal<sg_size_t>(simcall->args[1]));
  break;

case SIMCALL_STORAGE_WRITE:
  simcall_HANDLER_storage_write(simcall, simgrid::simix::unmarshal<surf_storage_t>(simcall->args[0]),
                                simgrid::simix::unmarshal<sg_size_t>(simcall->args[1]));
  break;

case SIMCALL_MC_RANDOM:
  simgrid::simix::marshal<int>(simcall->result, simcall_HANDLER_mc_random(simcall, simgrid::simix::unmarshal<int>(simcall->args[0]), simgrid::simix::unmarshal<int>(simcall->args[1])));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_SET_CATEGORY:
  SIMIX_set_category(simgrid::simix::unmarshal<boost::intrusive_ptr<simgrid::kernel::activity::ActivityImpl>>(simcall->args[0]), simgrid::simix::unmarshal<const char*>(simcall->args[1]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_RUN_KERNEL:
  SIMIX_run_kernel(simgrid::simix::unmarshal<std::function<void()> const*>(simcall->args[0]));
  SIMIX_simcall_answer(simcall);
  break;

case SIMCALL_RUN_BLOCKING:
  SIMIX_run_blocking(simgrid::simix::unmarshal<std::function<void()> const*>(simcall->args[0]));
  break;
    case NUM_SIMCALLS:
      break;
    case SIMCALL_NONE:
      THROWF(arg_error,0,"Asked to do the noop syscall on %s@%s",
          simcall->issuer->name.c_str(),
          sg_host_get_name(simcall->issuer->host)
          );
      break;
    default:
      THROW_IMPOSSIBLE;
  }
}
