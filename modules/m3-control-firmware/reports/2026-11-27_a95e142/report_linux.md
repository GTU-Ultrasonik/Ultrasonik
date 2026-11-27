# M3 test report — 2026-11-27_16-59-43

- Commit: a95e142
- System: Linux 5.15.167.4-microsoft-standard-WSL2 · Python 3.12.3
- Level: S (software and virtual board). B and R tests are not part of this run.
- Firmware build (esp32, esp32_simball): PASS
- Native C tests: PASS · Python tests: PASS

| Req | Level | Requirement | Tests | Result |
|---|---|---|---|---|
| R3.1 | S | PID computes exactly as designed | 11 | PASS |
| R3.2 | S | States and reset sequence as in the table | 13 | PASS |
| R3.3 | S | Every height used within 5 ms with Wi-Fi active (HIL) | 0 | not run (needs the board, HIL) |
| R3.4 | S | fan_cmd at least every 10 ms, new sequence number | 1 | PASS |
| R3.5 | S | Fault within 200 ms without a new real measurement | 7 | PASS |
| R3.6 | S | Raw fallback without jump; at most 5 bridged | 3 | PASS |
| R3.7 | S | Targets played on time despite network delay | 12 | PASS |
| R3.8 | S | Holds and moves the simulated ball | 3 | PASS |
| R3.9 | S | Gains robust to +-30 % model error and bad data | 2 | PASS |
| R3.10 | S | Commands checked; safety limits locked; game only in game mode | 21 | PASS |
| R3.11 | S | M1 fault / fan_state lost / E-stop -> fault; stuck-ball warning | 19 | PASS |
| R3.12 | R | Holds the real ball | 0 | not run (rig, integration) |
| R3.13 | S | Runs alone on Windows and Linux | 4 | PASS |

## HIL simulator, virtual board

| Scenario | Board state | Mean error mm | Peak-to-peak mm | Overshoot mm | Settled s | Target vs sent max mm | Fault after ms | Cause | Fault until Reset | Acks | Status msgs | Bad JSON | CRC errors |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hold_bad_data | Run | 2.24 | 12.6 | - | - | - | - | - | - | 2 | 1061 | 0 | 0 |
| start_and_status | Run | 0.92 | 1.11 | - | - | - | - | - | - | 2 | 182 | 0 | 0 |
| targets | Run | 50.82 | 244.23 | - | - | 2.09 | - | - | - | 2 | 1213 | 0 | 0 |
| commands | Run | 0.33 | 0.79 | - | - | - | - | - | - | 6 | 546 | 0 | 0 |
| camera_loss | Run | - | - | - | - | - | 184.0 | no_height | True | 4 | 485 | 0 | 0 |
| bridged_only | Run | - | - | - | - | - | 184.0 | no_height | True | 4 | 485 | 0 | 0 |
| m1_fault | Run | - | - | - | - | - | 0.0 | m1_fault | True | 4 | 485 | 0 | 0 |
| estop | Run | - | - | - | - | - | 0.0 | estop | True | 4 | 485 | 0 | 0 |
| fan_state_lost | Run | - | - | - | - | - | 90.0 | fan_state_lost | True | 4 | 485 | 0 | 0 |
| step | Run | 2.13 | 15.04 | 39.6 | 3.45 | - | - | - | - | 4 | 910 | 0 | 0 |

Mean error in the targets scenario is the ball's tracking error without feed-forward (M4's job, R4.7); T3.7 is the target column.

## Measured against the limits (HIL, virtual board)

| Req | Scenario | Measured | Limit | Result |
|---|---|---|---|---|
| R3.5 | camera_loss | 184.0 ms to Fault, no new real height | <= 200 | PASS |
| R3.6 | bridged_only | 184.0 ms to Fault, bridged heights only | <= 200 | PASS |
| R3.7 | targets | 2.09 mm, board target vs sent, delay <= 150 ms | <= 5 | PASS |
| R3.8 | step | 39.6 mm overshoot, 30 -> 50 cm step | < 50 | PASS |
| R3.8 | step | 3.45 s settled within +-2 cm | <= 4 | PASS |
| R3.8 | step | 2.13 mm mean error after the step | <= 20 | PASS |
| R3.8 | step | 15.04 mm oscillation after the step | <= 30 | PASS |
| R3.9 | hold_bad_data | 2.24 mm mean error, 5 mm noise, 5 % drops | <= 30 | PASS |
| R3.9 | hold_bad_data | 12.6 mm oscillation, 5 mm noise, 5 % drops | <= 50 | PASS |
| R3.11 | m1_fault | 0.0 ms to Fault after an M1 fault | <= 100 | PASS |
| R3.11 | estop | 0.0 ms to Fault after the E-stop | <= 100 | PASS |
| R3.11 | fan_state_lost | 90.0 ms to Fault, fan_state lost (100 ms + one frame) | <= 110 | PASS |

## Plots

The measurements are identical to the Windows run, so the Windows plots are linked.

- hold_bad_data: plots/hold_bad_data_windows.png
- start_and_status: plots/start_and_status_windows.png
- targets: plots/targets_windows.png
- commands: plots/commands_windows.png
- camera_loss: plots/camera_loss_windows.png
- bridged_only: plots/bridged_only_windows.png
- m1_fault: plots/m1_fault_windows.png
- estop: plots/estop_windows.png
- fan_state_lost: plots/fan_state_lost_windows.png
- step: plots/step_windows.png

## All test cases

| Suite | Test | Result | Message |
|---|---|---|---|
| native | test_R3_2_power_up_is_fault | PASS |  |
| native | test_R3_2_fault_refuses_start | PASS |  |
| native | test_R3_2_reset_sequence_waits_for_armed | PASS |  |
| native | test_R3_2_reset_refused_while_cause_present | PASS |  |
| native | test_R3_2_rearm_times_out | PASS |  |
| native | test_R3_2_start_refused_with_reason_when_condition_missing | PASS |  |
| native | test_R3_2_launch_to_run_above_30mm | PASS |  |
| native | test_R3_2_launch_without_lift_faults_after_1500ms | PASS |  |
| native | test_R3_2_stop_from_run_goes_idle | PASS |  |
| native | test_R3_2_game_hit_only_in_game_mode | PASS |  |
| native | test_R3_2_run_faults | PASS |  |
| native | test_R3_2_network_lost_keeps_run | PASS |  |
| native | test_R3_2_fault_not_left_by_returning_data_or_start_or_stop | PASS |  |
| native | test_R3_10_valid_change_applied_and_acked | PASS |  |
| native | test_R3_10_out_of_range_refused_with_reason_nothing_changes | PASS |  |
| native | test_R3_10_not_a_number_refused | PASS |  |
| native | test_R3_10_safety_limits_cannot_be_changed | PASS |  |
| native | test_R3_10_unknown_parameter_or_command_refused | PASS |  |
| native | test_R3_10_inconsistent_limits_refused | PASS |  |
| native | test_R3_10_target_outside_usable_range_refused | PASS |  |
| native | test_R3_10_twenty_bad_commands_change_nothing | PASS |  |
| native | test_R3_10_refused_start_has_reason | PASS |  |
| native | test_R3_10_mode_change_refused_while_flying | PASS |  |
| native | test_R3_10_game_out_outside_game_mode_ignored | PASS |  |
| native | test_R3_10_game_out_in_game_mode_sets_target_and_hit_stops | PASS |  |
| native | test_R3_1_proportional | PASS |  |
| native | test_R3_1_integral_uneven_dt | PASS |  |
| native | test_R3_1_invalid_dt_no_integral_no_derivative | PASS |  |
| native | test_R3_1_derivative_on_measurement_no_target_kick | PASS |  |
| native | test_R3_1_derivative_restart | PASS |  |
| native | test_R3_1_integral_limit | PASS |  |
| native | test_R3_1_anti_windup_at_output_limit | PASS |  |
| native | test_R3_1_output_limits | PASS |  |
| native | test_R3_1_rate_limit | PASS |  |
| native | test_R3_1_feed_forward_added | PASS |  |
| native | test_R3_1_gain_change_without_jump | PASS |  |
| native | test_R3_10_net_set_parsed_applied_and_acked | PASS |  |
| native | test_R3_10_net_refusals_carry_reason | PASS |  |
| native | test_R3_10_net_mode_command_changes_mode | PASS |  |
| native | test_R3_10_net_repeated_request_answered_not_applied_twice | PASS |  |
| native | test_R3_10_net_command_without_request_id_dropped | PASS |  |
| native | test_R3_10_net_malformed_datagrams_never_trusted | PASS |  |
| native | test_R3_10_net_every_truncation_and_random_bytes_rejected_safely | PASS |  |
| native | test_R3_7_net_target_points_reach_the_buffer | PASS |  |
| native | test_R3_7_net_target_points_ignored_in_game_mode_and_too_many_refused | PASS |  |
| native | test_R3_11_net_status_carries_state_fault_and_stuck_warning | PASS |  |
| native | test_R3_10_net_ack_escapes_echoed_text | PASS |  |
| native | test_R3_5_timer_starts_timed_out | PASS |  |
| native | test_R3_5_real_height_refreshes_timer_until_200ms | PASS |  |
| native | test_R3_5b_bridged_heights_never_refresh_timer | PASS |  |
| native | test_R3_5c_repeated_frame_number_ignored | PASS |  |
| native | test_R3_5d_new_session_accepts_numbers_from_zero | PASS |  |
| native | test_R3_6_filtered_preferred_raw_fallback_with_switch_flag | PASS |  |
| native | test_R3_6_only_five_bridged_in_a_row_used | PASS |  |
| native | test_dt_from_capture_times | PASS |  |
| native | test_R3_7_offset_is_smallest_delay_in_window | PASS |  |
| native | test_R3_7_points_interpolated_linearly | PASS |  |
| native | test_R3_7_wave_on_time_with_random_delay_up_to_150ms | PASS |  |
| native | test_R3_7_targets_stop_last_target_held | PASS |  |
| native | test_R3_7_new_session_holds_then_moves_smoothly | PASS |  |
| native | test_R3_7_resume_after_stop_blends_without_jump | PASS |  |
| native | test_R3_7_old_or_repeated_message_ignored | PASS |  |
| native | test_R3_7_points_out_of_order_refused | PASS |  |
| native | test_R3_7_game_mode_ignores_m4_targets | PASS |  |
| native | test_crc_check_value | PASS |  |
| native | test_vector_height | PASS |  |
| native | test_vector_fan_cmd | PASS |  |
| native | test_vector_fan_state | PASS |  |
| native | test_decoder_roundtrip_with_garbage_and_resync | PASS |  |
| native | test_corrupted_frames_rejected_and_counted | PASS |  |
| native | test_sequence_tracking | PASS |  |
| native | test_R3_4_fan_cmd_every_10ms_with_new_sequence | PASS |  |
| native | test_R3_5_heights_stop_fault_within_200ms | PASS |  |
| native | test_R3_5b_only_bridged_heights_fault_within_200ms | PASS |  |
| native | test_R3_8_holds_simulated_ball | PASS |  |
| native | test_R3_8_three_heights_and_step | PASS |  |
| native | test_R3_6_filtered_height_lost_during_hold_control_continues | PASS |  |
| native | test_R3_9_gains_robust_to_30pct_model_error_noise_and_drops | PASS |  |
| native | test_R3_9_dropped_frames_really_dropped | PASS |  |
| native | test_R3_11_m1_fault_10_times_fault_within_100ms | PASS |  |
| native | test_R3_11_estop_10_times_fault_within_100ms | PASS |  |
| native | test_R3_11_fan_state_lost_10_times_fault_within_100ms | PASS |  |
| native | test_R3_11_stuck_ball_warning_within_3500ms_no_fault | PASS |  |
| native | test_R3_11_steady_hold_near_top_no_warning | PASS |  |
| native | test_R3_11_stuck_warning_after_3s_when_all_conditions_hold | PASS |  |
| native | test_R3_11_no_warning_if_target_less_than_50mm_above | PASS |  |
| native | test_R3_11_no_warning_if_speed_below_90_percent | PASS |  |
| native | test_R3_11_no_warning_if_ball_rises_10mm_in_3s | PASS |  |
| native | test_R3_11_no_warning_outside_run | PASS |  |
| native | test_R3_11_holding_near_top_no_warning | PASS |  |
| native | test_R3_11_warning_clears_when_condition_goes | PASS |  |
| native | test_R3_11_short_interruption_restarts_window | PASS |  |
| tests.python.test_contract_py | test_crc_check_value | PASS |  |
| tests.python.test_contract_py | test_vectors_encode_and_decode | PASS |  |
| tests.python.test_contract_py | test_corrupted_frames_rejected | PASS |  |
| tests.python.test_contract_py | test_seq_tracker | PASS |  |
| tests.python.test_contract_py | test_plant_hover_and_rest | PASS |  |
| tests.python.test_hil_virtual | test_R3_13_hil_sim_holds_ball_with_virtual_board | PASS |  |
| tests.python.test_hil_virtual | test_R3_13_hil_sim_starts_board_with_json_commands_and_reads_status | PASS |  |
| tests.python.test_hil_virtual | test_R3_7_hil_targets_played_on_time_despite_network_delay | PASS |  |
| tests.python.test_hil_virtual | test_R3_10_hil_live_commands_checked_while_flying | PASS |  |
| tests.python.test_hil_virtual | test_R3_11_hil_failure_puts_board_in_fault_and_reset_recovers[camera_loss-200.0-no_height] | PASS |  |
| tests.python.test_hil_virtual | test_R3_11_hil_failure_puts_board_in_fault_and_reset_recovers[bridged_only-200.0-no_height] | PASS |  |
| tests.python.test_hil_virtual | test_R3_11_hil_failure_puts_board_in_fault_and_reset_recovers[m1_fault-20.0-m1_fault] | PASS |  |
| tests.python.test_hil_virtual | test_R3_11_hil_failure_puts_board_in_fault_and_reset_recovers[estop-20.0-estop] | PASS |  |
| tests.python.test_hil_virtual | test_R3_11_hil_failure_puts_board_in_fault_and_reset_recovers[fan_state_lost-110.0-fan_state_lost] | PASS |  |
| tests.python.test_hil_virtual | test_R3_8_hil_step_30_to_50_cm | PASS |  |
| tests.python.test_m2_standin | test_R3_13_m2_standin_smooths_less_than_m2_must | PASS |  |
| tests.python.test_m2_standin | test_R3_13_m2_standin_tracks_worse_than_m2_must_and_lag_is_in_spec | PASS |  |
